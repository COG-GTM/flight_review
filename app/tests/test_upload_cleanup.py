""" tests for removal of stored log files whose upload did not complete """
import logging
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
#pylint: disable=wrong-import-position
from tornado_handlers.upload import UploadHandler
from audit import ERROR_LOGGER_NAME


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
