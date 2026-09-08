""" pytest configuration for the test-card tests """
import os
import sys

import pytest

_APP_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
for _path in (_APP_DIR, os.path.join(_APP_DIR, 'plot_app')):
    if _path not in sys.path:
        sys.path.insert(0, _path)

# pylint: disable=wrong-import-position
from pyulog import ULog
from ulog_gen import synthetic_flight


@pytest.fixture(scope='session')
def synthetic_log(tmp_path_factory):
    """ (file name, ground truth dict) of the default synthetic flight """
    filename = str(tmp_path_factory.mktemp('ulog') / 'synthetic.ulg')
    truth = synthetic_flight(filename)
    return filename, truth


@pytest.fixture(scope='session')
def synthetic_ulog(synthetic_log):
    """ parsed pyulog.ULog of the default synthetic flight """
    return ULog(synthetic_log[0])
