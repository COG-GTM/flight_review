""" tests for removal of stored log files whose upload did not complete """
import json
import logging
import os
import sys
from types import SimpleNamespace

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
#pylint: disable=wrong-import-position
from tornado_handlers.upload import UploadHandler
from audit import AUDIT_LOGGER_NAME, ERROR_LOGGER_NAME


class _Stub: #pylint: disable=too-few-public-methods
    """ stand-in for the handler instance; _discard_stored_file does not
        touch request state """


def _discard(path):
    UploadHandler._discard_stored_file(_Stub(), path) #pylint: disable=protected-access


def test_discard_removes_stored_file(tmp_path):
    stored = tmp_path / 'incomplete.ulg'
    stored.write_bytes(b'ULog\x01\x12\x35' + b'\x00' * 9)
    _discard(str(stored))
    assert not stored.exists()


def test_discard_missing_file_is_noop(tmp_path):
    _discard(str(tmp_path / 'never-written.ulg'))


def test_discard_failure_is_logged_not_raised(tmp_path, caplog):
    # os.remove on a directory raises an OSError on every platform
    with caplog.at_level(logging.ERROR, logger=ERROR_LOGGER_NAME):
        _discard(str(tmp_path))
    assert tmp_path.exists()
    assert any('failed to remove incomplete upload' in rec.getMessage()
               for rec in caplog.records)


# --- one audit record per upload attempt -------------------------------------

class _Capture(logging.Handler):
    """ collects audit records """
    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record):
        self.records.append(json.loads(record.getMessage()))


@pytest.fixture(name='audit_records')
def audit_records_fixture():
    logger = logging.getLogger(AUDIT_LOGGER_NAME)
    handler = _Capture()
    logger.addHandler(handler)
    yield handler.records
    logger.removeHandler(handler)


def _handler(method='POST', status=200):
    """ an UploadHandler instance without a live Tornado request: only the
        attributes used by the audit/cleanup lifecycle methods are set """
    handler = UploadHandler.__new__(UploadHandler)
    handler.request = SimpleNamespace(method=method, remote_ip='127.0.0.1')
    handler._status_code = status #pylint: disable=protected-access
    handler.initialize()
    return handler


def test_reject_upload_emits_once(audit_records):
    handler = _handler()
    handler._reject_upload('first reason', size=5) #pylint: disable=protected-access
    handler._reject_upload('second reason') #pylint: disable=protected-access
    handler.on_finish()
    assert len(audit_records) == 1
    assert audit_records[0]['event'] == 'upload'
    assert audit_records[0]['outcome'] == 'failure'
    assert audit_records[0]['reason'] == 'first reason'
    assert audit_records[0]['size'] == 5


def test_failed_post_without_record_is_audited_on_finish(audit_records):
    handler = _handler(status=500)
    handler.on_finish()
    assert [(r['outcome'], r['reason'], r['status']) for r in audit_records] == \
        [('failure', 'request failed', 500)]


def test_successful_post_is_not_audited_as_failure(audit_records):
    handler = _handler(status=302)
    handler.upload_audited = True # set by post() together with the success record
    handler.on_finish()
    assert audit_records == []


def test_get_is_never_audited(audit_records):
    handler = _handler(method='GET', status=404)
    handler.on_finish()
    assert audit_records == []


def test_connection_close_audits_only_with_pending_stream(audit_records):
    handler = _handler()
    handler.on_connection_close()
    assert audit_records == []
    handler = _handler()
    handler.multipart_streamer = SimpleNamespace(release_parts=lambda: None)
    handler.on_connection_close()
    handler.on_finish()
    assert [r['reason'] for r in audit_records] == \
        ['connection closed before upload completed']
    assert handler.multipart_streamer is None
