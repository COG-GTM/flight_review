""" tests for the structured audit record helper (plot_app/audit.py) """
import json
import logging
import sys

import pytest

import audit
from audit import build_audit_record, audit_log, new_correlation_id, log_server_error


class _ListHandler(logging.Handler):
    """ collects emitted records """
    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record):
        self.records.append(record)


@pytest.fixture(name='capture')
def capture_fixture():
    """ attach a capturing handler to the audit and error loggers """
    handler = _ListHandler()
    loggers = [logging.getLogger(audit.AUDIT_LOGGER_NAME),
               logging.getLogger(audit.ERROR_LOGGER_NAME)]
    for logger in loggers:
        logger.addHandler(handler)
    yield handler
    for logger in loggers:
        logger.removeHandler(handler)


def test_build_audit_record_shape():
    record = build_audit_record('upload', 'success', log_id='abc', size=12, none_field=None)
    assert set(record) == {'timestamp', 'event', 'outcome', 'log_id', 'size'}
    assert record['event'] == 'upload'
    assert record['outcome'] == 'success'
    assert record['log_id'] == 'abc'
    assert record['size'] == 12
    # ISO-8601 UTC timestamp
    assert record['timestamp'].endswith('+00:00')
    assert 'T' in record['timestamp']


def test_audit_log_emits_one_json_line(capture):
    audit_log('log_delete', 'failure', log_id='x', reason='token mismatch',
              client_ip='127.0.0.1')
    records = [r for r in capture.records if r.name == audit.AUDIT_LOGGER_NAME]
    assert len(records) == 1
    assert records[0].levelno == logging.INFO
    line = records[0].getMessage()
    assert '\n' not in line
    parsed = json.loads(line)
    assert parsed['event'] == 'log_delete'
    assert parsed['outcome'] == 'failure'
    assert parsed['log_id'] == 'x'
    assert parsed['reason'] == 'token mismatch'
    assert parsed['client_ip'] == '127.0.0.1'
    assert list(parsed) == sorted(parsed)


def test_audit_log_serializes_non_json_values(capture):
    audit_log('upload', 'failure', reason=ValueError('bad\nvalue'))
    records = [r for r in capture.records if r.name == audit.AUDIT_LOGGER_NAME]
    parsed = json.loads(records[0].getMessage())
    assert parsed['reason'] == 'bad\nvalue'
    assert '\n' not in records[0].getMessage()


def test_audit_logger_has_stream_handler_and_info_level():
    audit_log('probe', 'success')
    logger = logging.getLogger(audit.AUDIT_LOGGER_NAME)
    assert any(isinstance(h, logging.StreamHandler) for h in logger.handlers)
    assert logger.getEffectiveLevel() <= logging.INFO


def test_new_correlation_id():
    ids = {new_correlation_id() for _ in range(50)}
    assert len(ids) == 50
    for cid in ids:
        assert len(cid) == 12
        int(cid, 16)


def test_log_server_error_includes_correlation_id_and_traceback(capture):
    cid = new_correlation_id()
    try:
        raise RuntimeError('secret detail')
    except RuntimeError:
        log_server_error(cid, 'HTTP 500 for POST /upload', exc_info=sys.exc_info())
    records = [r for r in capture.records if r.name == audit.ERROR_LOGGER_NAME]
    assert len(records) == 1
    assert records[0].levelno == logging.ERROR
    assert cid in records[0].getMessage()
    assert records[0].exc_info is not None
    assert 'secret detail' in logging.Formatter().format(records[0])
