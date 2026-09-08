""" tests for the log-id -> filesystem path helpers in plot_app/helper.py
(needs the full app dependencies; skipped if they are not installed) """
import os
import uuid

import pytest

helper = pytest.importorskip('helper')
from security import InvalidLogIdError  # pylint: disable=wrong-import-position


def test_get_log_filename_is_inside_log_dir():
    log_id = str(uuid.uuid4())
    path = helper.get_log_filename(log_id)
    base = os.path.realpath(helper.get_log_filepath())
    assert path == os.path.join(base, log_id + '.ulg')


@pytest.mark.parametrize('log_id', ['../../etc/passwd', '..', 'x/y', 'abc', ''])
def test_get_log_filename_rejects_invalid_ids(log_id):
    with pytest.raises(InvalidLogIdError):
        helper.get_log_filename(log_id)


def test_validate_log_id_uses_allowlist():
    assert helper.validate_log_id(str(uuid.uuid4()))
    assert not helper.validate_log_id('some_log-name')
    assert not helper.validate_log_id('../x')


def test_get_log_derived_filename(tmp_path):
    log_id = str(uuid.uuid4())
    assert helper.get_log_derived_filename(str(tmp_path), log_id, '.kml') == \
        os.path.join(os.path.realpath(str(tmp_path)), log_id + '.kml')
    with pytest.raises(InvalidLogIdError):
        helper.get_log_derived_filename(str(tmp_path), '../' + log_id, '.kml')
