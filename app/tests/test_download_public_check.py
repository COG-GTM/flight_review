""" tests for the best-effort public/private classification of downloads """
import os
import sqlite3
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
#pylint: disable=wrong-import-position
from tornado_handlers import download


class _Con:
    """ minimal sqlite-like connection returning one row """
    def __init__(self, row, fail=False):
        self.row = row
        self.fail = fail
        self.closed = False

    def cursor(self):
        return self

    def execute(self, _sql, _params):
        if self.fail:
            raise sqlite3.OperationalError('database is locked')

    def fetchone(self):
        return self.row

    def close(self):
        self.closed = True


def test_public_log(monkeypatch):
    con = _Con((1,))
    monkeypatch.setattr(download, 'get_db_connection', lambda: con)
    assert download.DownloadHandler.is_public_log('x') is True
    assert con.closed


def test_private_and_unknown_logs(monkeypatch):
    for row in ((0,), None):
        con = _Con(row)
        monkeypatch.setattr(download, 'get_db_connection', lambda con=con: con)
        assert download.DownloadHandler.is_public_log('x') is False
        assert con.closed


def test_query_failure_counts_as_private(monkeypatch):
    con = _Con((1,), fail=True)
    monkeypatch.setattr(download, 'get_db_connection', lambda: con)
    assert download.DownloadHandler.is_public_log('x') is False
    assert con.closed


def test_connect_failure_counts_as_private(monkeypatch):
    def _connect():
        raise sqlite3.OperationalError('unable to open database file')
    monkeypatch.setattr(download, 'get_db_connection', _connect)
    assert download.DownloadHandler.is_public_log('x') is False
