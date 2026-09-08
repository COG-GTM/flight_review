""" tests for the pure security helpers (plot_app/security.py) """
import json
import os
import uuid

import pytest

import security
from security import (is_valid_log_id, resolve_under, InvalidLogIdError,
                      is_ulog_header, is_ulge_header, generate_token,
                      is_valid_token_format, tokens_match,
                      json_for_script, sanitize_header_value)


# --- log id allow-list ------------------------------------------------------

@pytest.mark.parametrize('log_id', [
    str(uuid.uuid4()),
    '6d8f5f9e-4b4e-4d4b-9a5e-3d2b1c0a9f8e',
    '6D8F5F9E-4B4E-4D4B-9A5E-3D2B1C0A9F8E',
])
def test_valid_log_ids(log_id):
    assert is_valid_log_id(log_id)


@pytest.mark.parametrize('log_id', [
    '', None, 42,
    '../../etc/passwd',
    '..',
    '6d8f5f9e-4b4e-4d4b-9a5e-3d2b1c0a9f8e/../x',
    '6d8f5f9e-4b4e-4d4b-9a5e-3d2b1c0a9f8e.ulg',
    '6d8f5f9e4b4e4d4b9a5e3d2b1c0a9f8e',        # no dashes
    '6d8f5f9e-4b4e-4d4b-9a5e-3d2b1c0a9f8',     # too short
    '6d8f5f9e-4b4e-4d4b-9a5e-3d2b1c0a9f8e\n',  # trailing newline
    'g d8f5f9e-4b4e-4d4b-9a5e-3d2b1c0a9f8e',
    'some_log-name',                           # allowed by the old pattern
])
def test_invalid_log_ids(log_id):
    assert not is_valid_log_id(log_id)


# --- path containment -------------------------------------------------------

def test_resolve_under_returns_canonical_path_inside_base(tmp_path):
    base = tmp_path / 'log_files'
    base.mkdir()
    log_id = str(uuid.uuid4())
    result = resolve_under(str(base), log_id + '.ulg')
    assert result == os.path.join(os.path.realpath(str(base)), log_id + '.ulg')


def test_resolve_under_resolves_symlinked_base(tmp_path):
    real = tmp_path / 'real'
    real.mkdir()
    link = tmp_path / 'link'
    link.symlink_to(real, target_is_directory=True)
    result = resolve_under(str(link), 'a.ulg')
    assert result == os.path.join(os.path.realpath(str(real)), 'a.ulg')


@pytest.mark.parametrize('part', [
    '..', '../x.ulg', 'sub/x.ulg', '/etc/passwd', '', 'x/../../y', None,
])
def test_resolve_under_rejects_escaping_components(tmp_path, part):
    with pytest.raises(InvalidLogIdError):
        resolve_under(str(tmp_path), part)


def test_resolve_under_rejects_symlink_escape(tmp_path):
    base = tmp_path / 'base'
    base.mkdir()
    outside = tmp_path / 'outside.ulg'
    outside.write_bytes(b'x')
    (base / 'evil.ulg').symlink_to(outside)
    with pytest.raises(InvalidLogIdError):
        resolve_under(str(base), 'evil.ulg')


def test_invalid_log_id_error_is_value_error():
    assert issubclass(InvalidLogIdError, ValueError)


# --- ULog magic -------------------------------------------------------------

def test_ulog_magic_matches_pyulog_header():
    pyulog = pytest.importorskip('pyulog')
    assert pyulog.ULog.HEADER_BYTES == security.ULOG_MAGIC
    assert is_ulog_header(pyulog.ULog.HEADER_BYTES + b'\x00' * 9)


@pytest.mark.parametrize('data', [
    b'', None, 'ULog\x01\x125', b'ULog', b'ULog\x01\x12\x36', b'PK\x03\x04' + b'\x00' * 12,
    b'<html>' + b' ' * 10, b'ULogEnc' + b'\x00' * 9,
])
def test_is_ulog_header_rejects_non_ulog(data):
    assert not is_ulog_header(data)


def test_is_ulog_header_accepts_bytearray():
    assert is_ulog_header(bytearray(security.ULOG_MAGIC + b'\x00' * 20))


def test_is_ulge_header():
    assert is_ulge_header(b'ULogEnc\x01' + b'\x00' * 14)
    assert not is_ulge_header(security.ULOG_MAGIC + b'\x00' * 9)
    assert not is_ulge_header(b'')


# --- tokens -----------------------------------------------------------------

def test_generate_token_shape_and_uniqueness():
    tokens = {generate_token() for _ in range(100)}
    assert len(tokens) == 100
    for token in tokens:
        assert is_valid_token_format(token)
        assert len(token) == 2 * security.TOKEN_NUM_BYTES


@pytest.mark.parametrize('token', [
    '', None, 'abc', 'A' * 32, 'g' * 32, 'a' * 31, 'a' * 33, 'a' * 32 + '\n',
    "' OR 1=1 --", '<script>',
])
def test_is_valid_token_format_rejects(token):
    assert not is_valid_token_format(token)


def test_tokens_match():
    token = generate_token()
    assert tokens_match(token, token)
    assert not tokens_match(token, generate_token())
    assert not tokens_match(token[:-1], token)
    assert not tokens_match(token + 'a', token)
    assert not tokens_match('', token)
    assert not tokens_match(token, '')
    assert not tokens_match(None, token)
    assert not tokens_match(token, None)
    assert not tokens_match(token, token.encode('utf-8'))


def test_tokens_match_uses_constant_time_compare(monkeypatch):
    calls = []

    def fake_compare(a, b):
        calls.append((a, b))
        return True
    monkeypatch.setattr(security.hmac, 'compare_digest', fake_compare)
    assert tokens_match('ab', 'ab')
    assert calls == [(b'ab', b'ab')]


# --- JSON inside <script> ---------------------------------------------------

def test_json_for_script_neutralizes_script_breakout():
    encoded = json_for_script('</script><script>alert(1)</script>')
    assert '<' not in encoded and '>' not in encoded
    assert json.loads(encoded) == '</script><script>alert(1)</script>'


@pytest.mark.parametrize('value', [
    'plain', 'a&b', 'line\u2028sep', 'quote"inside', {'k': ['<', 1, None]}, 42,
])
def test_json_for_script_round_trips(value):
    encoded = json_for_script(value)
    for forbidden in ('<', '>', '&', '\u2028', '\u2029'):
        assert forbidden not in encoded
    assert json.loads(encoded) == value


# --- mail header sanitization -----------------------------------------------

@pytest.mark.parametrize('value, expected', [
    ('plain subject', 'plain subject'),
    ('a\r\nBcc: victim@example.com', 'aBcc: victim@example.com'),
    ('a\nb\rc', 'abc'),
    ('tab\tkept', 'tab\tkept'),
    ('nul\x00byte', 'nulbyte'),
    ('del\x7fchar', 'delchar'),
    ('', ''),
    (None, ''),
    (123, ''),
])
def test_sanitize_header_value(value, expected):
    assert sanitize_header_value(value) == expected


def test_sanitize_header_value_truncates():
    assert len(sanitize_header_value('x' * 500)) == 78
    assert sanitize_header_value('x' * 500, max_length=10) == 'x' * 10
