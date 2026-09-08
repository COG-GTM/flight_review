""" integration tests: test-card windows on the plot page for a log that only
has the modern topics the test-card reduction uses (no legacy airspeed, no GPS) """
import types
from unittest import mock

import pytest
from bokeh.models import BoxAnnotation, LabelSet
from pyulog import ULog
from pyulog.px4 import PX4ULog

import configured_plots
from db_entry import DBData
from ulog_gen import synthetic_flight

CARD = [
    {'test_point_id': 'TP-01', 'description': 'cruise', 'start_s': 10.0, 'end_s': 20.0,
     'nz_max_g': None, 'airspeed_max_mps': None, 'alt_min_m': None, 'alt_max_m': None},
    {'test_point_id': 'TP-02', 'description': 'pull-up', 'start_s': 48.0, 'end_s': 58.0,
     'nz_max_g': 2.0, 'airspeed_max_mps': None, 'alt_min_m': None, 'alt_max_m': None},
]


def _generate(ulog, test_card):
    px4_ulog = PX4ULog(ulog)
    px4_ulog.add_roll_pitch_yaw()
    # generate_plots reads the request from the bokeh document
    doc = types.SimpleNamespace(
        template_variables={},
        session_context=types.SimpleNamespace(request=types.SimpleNamespace(headers={})))
    with mock.patch.object(configured_plots, 'curdoc', return_value=doc):
        plots = configured_plots.generate_plots(
            ulog, px4_ulog, DBData(), None, '/3d', '/pid',
            '/test_card?log=x' if test_card else None, test_card)
    return {plot.title.text: plot for plot in plots
            if getattr(plot, 'title', None) is not None}


def _windows(plot):
    boxes = [r for r in plot.center if isinstance(r, BoxAnnotation)]
    labels = [r for r in plot.center if isinstance(r, LabelSet)]
    return boxes, labels


@pytest.fixture(scope='module')
def modern_ulog(tmp_path_factory):
    """ a log with only vehicle_acceleration, airspeed_validated,
    vehicle_local_position and vehicle_attitude """
    filename = str(tmp_path_factory.mktemp('ulog') / 'modern.ulg')
    synthetic_flight(filename)
    return ULog(filename)


def test_altitude_and_airspeed_plots_render_from_modern_topics(modern_ulog):
    plots = _generate(modern_ulog, None)
    assert 'Altitude Estimate' in plots
    assert 'Airspeed' in plots
    for title in ('Altitude Estimate', 'Airspeed'):
        boxes, labels = _windows(plots[title])
        assert boxes == [] and labels == []


def test_test_card_windows_are_drawn_on_altitude_and_airspeed_plots(modern_ulog):
    plots = _generate(modern_ulog, CARD)
    start = modern_ulog.start_timestamp
    for title in ('Altitude Estimate', 'Airspeed'):
        boxes, labels = _windows(plots[title])
        assert [(box.left, box.right) for box in boxes] == [
            (start + 10_000_000, start + 20_000_000),
            (start + 48_000_000, start + 58_000_000)]
        (label_set,) = labels
        assert list(label_set.source.data['text']) == ['TP-01', 'TP-02']
    # other plots are left alone
    boxes, labels = _windows(plots['Roll Angle'])
    assert boxes == [] and labels == []


def test_plots_without_local_position_still_work(tmp_path):
    filename = str(tmp_path / 'no_local_position.ulg')
    synthetic_flight(filename, include=('vehicle_acceleration', 'airspeed_validated',
                                        'vehicle_attitude'))
    plots = _generate(ULog(filename), CARD)
    assert 'Altitude Estimate' not in plots
    boxes, _ = _windows(plots['Airspeed'])
    assert len(boxes) == 2
