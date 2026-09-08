"""
Small, dependency-free helpers that sit at the untrusted-input boundaries:
identifier allow-listing, filesystem path containment, ULog header
validation, token generation/comparison and mail-header sanitization.

Everything in here is a pure function so it can be unit-tested without
Tornado, Bokeh or a database.
"""
import hmac
import json
import os
import re
import secrets

# log identifiers are generated with uuid.uuid4() at upload time
LOG_ID_RE = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
                       re.IGNORECASE)

# ULog file magic: 'ULog' 0x01 0x12 0x35 (first 7 of the 16 header bytes)
ULOG_MAGIC = b'\x55\x4c\x6f\x67\x01\x12\x35'
ULOG_HEADER_LEN = 16

# encrypted ULog container magic
ULGE_MAGIC = b'ULogEnc'

TOKEN_NUM_BYTES = 16


class InvalidLogIdError(ValueError):
    """ raised when a log identifier does not match the allow-list pattern
    or would resolve outside the configured storage directory """


def is_valid_log_id(log_id):
    """ allow-list check: the identifier must be a canonical UUID string """
    return isinstance(log_id, str) and LOG_ID_RE.fullmatch(log_id) is not None


def resolve_under(base_dir, *parts):
    """ join `parts` onto `base_dir` and return the canonical (realpath)
    result, raising InvalidLogIdError if the result is not strictly inside
    `base_dir` (guards against '..', absolute components and symlink escapes)
    """
    separators = [os.sep] + ([os.altsep] if os.altsep else [])
    for part in parts:
        if not isinstance(part, str) or part == '' or os.path.isabs(part):
            raise InvalidLogIdError('invalid path component')
        if any(sep in part for sep in separators):
            raise InvalidLogIdError('invalid path component')
    base = os.path.realpath(base_dir)
    candidate = os.path.realpath(os.path.join(base, *parts))
    if os.path.commonpath([base, candidate]) != base or candidate == base:
        raise InvalidLogIdError('path escapes storage directory')
    return candidate


def is_ulog_header(data):
    """ True if `data` starts with the ULog file magic """
    return isinstance(data, (bytes, bytearray)) and \
        bytes(data[:len(ULOG_MAGIC)]) == ULOG_MAGIC


def is_ulge_header(data):
    """ True if `data` starts with the encrypted ULog container magic """
    return isinstance(data, (bytes, bytearray)) and \
        bytes(data[:len(ULGE_MAGIC)]) == ULGE_MAGIC


def generate_token():
    """ url-safe secret token for the per-log edit/delete link """
    return secrets.token_hex(TOKEN_NUM_BYTES)


TOKEN_RE = re.compile(r'^[0-9a-f]{%d}$' % (2 * TOKEN_NUM_BYTES))

def is_valid_token_format(token):
    """ allow-list check for a client-supplied edit/delete token (hex string
    of the expected length); does not check whether it matches anything """
    return isinstance(token, str) and TOKEN_RE.fullmatch(token) is not None


def tokens_match(supplied, stored):
    """ constant-time comparison of a client-supplied token against the
    stored one. Returns False for missing/non-string/empty values. """
    if not isinstance(supplied, str) or not isinstance(stored, str):
        return False
    if len(supplied) == 0 or len(stored) == 0:
        return False
    return hmac.compare_digest(supplied.encode('utf-8'), stored.encode('utf-8'))


_SCRIPT_UNSAFE = {'<': '\\u003c', '>': '\\u003e', '&': '\\u0026',
                  '\u2028': '\\u2028', '\u2029': '\\u2029'}


def json_for_script(value):
    """ JSON-encode `value` so it can be embedded inside an HTML <script>
    block: the characters that could close the script element or break the
    JS parser are emitted as \\uXXXX escapes """
    encoded = json.dumps(value)
    for char, replacement in _SCRIPT_UNSAFE.items():
        encoded = encoded.replace(char, replacement)
    return encoded


_HEADER_CTRL_RE = re.compile(r'[\r\n\x00-\x08\x0b\x0c\x0e-\x1f\x7f]')

def sanitize_header_value(value, max_length=78):
    """ make a user-influenced string safe to place in a mail header:
    strip CR/LF and other control characters and truncate """
    if not isinstance(value, str):
        return ''
    value = _HEADER_CTRL_RE.sub('', value)
    return value[:max_length]
