""" tests for the metric computation on a synthetic ULog """
import json

import numpy as np
import pytest
from pyulog import ULog

from test_card import (NOT_LOGGED, STATUS_COMPLETE, STATUS_EXCEEDANCE, STATUS_NO_DATA,
                       extract_series, reduce_test_card)
from ulog_gen import synthetic_flight


def _point(test_point_id, start_s, end_s, **limits):
    point = {'test_point_id': test_point_id, 'description': test_point_id,
             'start_s': float(start_s), 'end_s': float(end_s),
             'nz_max_g': None, 'airspeed_max_mps': None, 'alt_min_m': None, 'alt_max_m': None}
    point.update(limits)
    return point


def _reduce(ulog, *points):
    results = reduce_test_card(ulog, list(points))
    return results['test_points']


def test_synthetic_log_contains_expected_topics(synthetic_ulog):
    names = {d.name for d in synthetic_ulog.data_list}
    assert names == {'vehicle_acceleration', 'airspeed_validated',
                     'vehicle_local_position', 'vehicle_attitude'}
    assert synthetic_ulog.last_timestamp - synthetic_ulog.start_timestamp == 120_000_000


def test_level_flight_metrics(synthetic_ulog):
    (result,) = _reduce(synthetic_ulog, _point('TP', 10, 40, nz_max_g=2.0,
                                               airspeed_max_mps=30, alt_min_m=100, alt_max_m=400))
    metrics = result['metrics']
    assert result['status'] == STATUS_COMPLETE
    assert result['duration_flown_s'] == pytest.approx(30.0)
    assert result['not_logged'] == []
    assert result['exceedances'] == []
    assert metrics['nz_peak_g'] == pytest.approx(1.0, abs=1e-6)
    assert metrics['nz_mean_g'] == pytest.approx(1.0, abs=1e-6)
    # airspeed 15 -> 35 m/s over 120 s
    assert metrics['airspeed_min_mps'] == pytest.approx(15 + 20 * 10 / 120, abs=1e-4)
    assert metrics['airspeed_max_mps'] == pytest.approx(15 + 20 * 40 / 120, abs=1e-4)
    # altitude climbs 2 m/s from 100 m
    assert metrics['alt_min_m'] == pytest.approx(120.0, abs=1e-3)
    assert metrics['alt_max_m'] == pytest.approx(180.0, abs=1e-3)
    assert metrics['bank_max_deg'] == pytest.approx(0.0, abs=1e-6)
    # climbing: max sink rate is negative
    assert metrics['sink_rate_max_mps'] == pytest.approx(-2.0, abs=1e-3)


def test_nz_bust_is_detected(synthetic_ulog):
    (result,) = _reduce(synthetic_ulog, _point('PULL', 45, 60, nz_max_g=2.5))
    assert result['status'] == STATUS_EXCEEDANCE
    assert result['metrics']['nz_peak_g'] == pytest.approx(3.2, abs=1e-6)
    assert 1.0 < result['metrics']['nz_mean_g'] < 3.2
    assert len(result['exceedances']) == 1
    exceedance = result['exceedances'][0]
    assert exceedance['limit'] == 'nz_max_g'
    assert exceedance['limit_value'] == 2.5
    # the bust lasts 5 s (50 s <= t < 55 s)
    assert exceedance['seconds'] == pytest.approx(5.0, abs=0.06)


def test_exceedance_seconds_are_clipped_to_the_window(synthetic_ulog):
    # window covers only the first 2 s of the 5 s bust
    (result,) = _reduce(synthetic_ulog, _point('PART', 40, 52, nz_max_g=2.5))
    assert result['status'] == STATUS_EXCEEDANCE
    assert result['exceedances'][0]['seconds'] == pytest.approx(2.0, abs=0.06)

    # window entirely outside the bust: nothing is integrated
    (result,) = _reduce(synthetic_ulog, _point('OUT', 56, 70, nz_max_g=2.5))
    assert result['status'] == STATUS_COMPLETE
    assert result['exceedances'] == []
    assert result['unchecked_limits'] == []


def test_exceedance_window_starting_between_samples(synthetic_ulog):
    # samples every 50 ms; the sample at 50.00 s (3.2 g) is still in effect
    # at the window start 50.02 s and must be integrated from 50.02 s onwards
    (result,) = _reduce(synthetic_ulog, _point('MID', 50.02, 52.0, nz_max_g=2.5))
    assert result['status'] == STATUS_EXCEEDANCE
    assert result['exceedances'][0]['seconds'] == pytest.approx(1.98, abs=1e-6)
    # summary metrics stay sample based
    assert result['metrics']['nz_peak_g'] == pytest.approx(3.2, abs=1e-6)
    assert result['metrics']['nz_mean_g'] == pytest.approx(3.2, abs=1e-6)

    # the value before the window (1 g) must not leak in: window starts between
    # 49.95 s (1 g) and 50.00 s (3.2 g)
    (result,) = _reduce(synthetic_ulog, _point('EDGE', 49.98, 52.0, nz_max_g=2.5))
    assert result['exceedances'][0]['seconds'] == pytest.approx(2.0, abs=1e-6)

    # a window with no sample inside is NO DATA even though a held value exists
    (result,) = _reduce(synthetic_ulog, _point('GAP', 50.01, 50.04, nz_max_g=2.5))
    assert result['status'] == STATUS_NO_DATA
    assert result['exceedances'] == []
    assert result['unchecked_limits'] == ['nz_max_g']


def test_airspeed_and_altitude_limits(synthetic_ulog):
    # airspeed reaches 25 m/s at t = 60 s
    (result,) = _reduce(synthetic_ulog, _point('IAS', 55, 65, airspeed_max_mps=25.0))
    limits = {e['limit']: e for e in result['exceedances']}
    assert set(limits) == {'airspeed_max_mps'}
    assert limits['airspeed_max_mps']['seconds'] == pytest.approx(5.0, abs=0.06)

    # altitude is between 120 m and 180 m in [10, 40]; band 130..170 busts both sides for 5 s
    (result,) = _reduce(synthetic_ulog, _point('ALT', 10, 40, alt_min_m=130.0, alt_max_m=170.0))
    limits = {e['limit']: e for e in result['exceedances']}
    assert set(limits) == {'alt_min_m', 'alt_max_m'}
    assert limits['alt_min_m']['seconds'] == pytest.approx(5.0, abs=0.06)
    assert limits['alt_max_m']['seconds'] == pytest.approx(5.0, abs=0.06)
    assert result['status'] == STATUS_EXCEEDANCE


def test_bank_and_sink_rate(synthetic_ulog):
    (result,) = _reduce(synthetic_ulog, _point('TURN', 68, 82))
    assert result['metrics']['bank_max_deg'] == pytest.approx(45.0, abs=1e-3)
    # descending at 2 m/s after t = 60 s
    assert result['metrics']['sink_rate_max_mps'] == pytest.approx(2.0, abs=1e-3)
    assert result['status'] == STATUS_COMPLETE


def test_window_clipping_at_end_of_log(synthetic_ulog):
    (result,) = _reduce(synthetic_ulog, _point('LATE', 100, 130))
    assert result['start_s'] == 100.0 and result['end_s'] == 130.0
    assert result['duration_flown_s'] == pytest.approx(20.0)
    assert result['status'] == STATUS_COMPLETE
    # all samples belong to the log, none are extrapolated past 120 s
    assert result['metrics']['airspeed_max_mps'] == pytest.approx(35.0, abs=1e-4)


def test_no_data_beyond_end_of_log(synthetic_ulog):
    (result,) = _reduce(synthetic_ulog, _point('NONE', 130, 140, nz_max_g=1.0))
    assert result['status'] == STATUS_NO_DATA
    assert result['duration_flown_s'] == 0.0
    assert result['exceedances'] == []
    assert result['metrics']['nz_peak_g'] is None
    assert result['not_logged'] == []


def test_validity_flags_mask_altitude_samples(synthetic_ulog):
    # z / v_z are flagged invalid for 100 s <= t < 110 s
    (result,) = _reduce(synthetic_ulog, _point('INVALID', 100, 109.9, alt_min_m=0.0))
    assert result['metrics']['alt_min_m'] is None
    assert result['metrics']['alt_max_m'] is None
    assert result['metrics']['sink_rate_max_mps'] is None
    # other topics still have data -> not NO DATA
    assert result['status'] == STATUS_COMPLETE
    assert result['metrics']['airspeed_min_mps'] is not None

    # neighbouring valid samples are used, invalid ones are not
    (result,) = _reduce(synthetic_ulog, _point('EDGE', 95, 115))
    truth_alt = 220.0 - 2.0 * (np.array([95.0, 110.0, 115.0]) - 60.0)
    assert result['metrics']['alt_max_m'] == pytest.approx(truth_alt[0], abs=1e-3)
    assert result['metrics']['alt_min_m'] == pytest.approx(truth_alt[2], abs=1e-3)


def test_missing_topics_are_reported_as_not_logged(tmp_path):
    filename = str(tmp_path / 'no_accel.ulg')
    synthetic_flight(filename, include=('airspeed_validated',))
    ulog = ULog(filename)
    (result,) = _reduce(ulog, _point('TP', 10, 40, nz_max_g=1.5, alt_min_m=500.0))
    metrics = result['metrics']
    assert metrics['nz_peak_g'] == NOT_LOGGED
    assert metrics['nz_mean_g'] == NOT_LOGGED
    assert metrics['alt_min_m'] == NOT_LOGGED
    assert metrics['alt_max_m'] == NOT_LOGGED
    assert metrics['sink_rate_max_mps'] == NOT_LOGGED
    assert metrics['bank_max_deg'] == NOT_LOGGED
    assert metrics['airspeed_min_mps'] != NOT_LOGGED
    assert result['not_logged'] == ['alt_max_m', 'alt_min_m', 'bank_max_deg',
                                    'nz_mean_g', 'nz_peak_g', 'sink_rate_max_mps']
    # limits on metrics that are not logged cannot be exceeded, but are reported
    assert result['exceedances'] == []
    assert result['unchecked_limits'] == ['nz_max_g', 'alt_min_m']
    assert result['status'] == STATUS_COMPLETE


def test_no_topics_at_all_gives_no_data(tmp_path):
    filename = str(tmp_path / 'empty.ulg')
    synthetic_flight(filename, include=())
    ulog = ULog(filename)
    (result,) = _reduce(ulog, _point('TP', 0, 10))
    assert result['status'] == STATUS_NO_DATA
    assert len(result['not_logged']) == 8


def test_baro_altitude_fallback(tmp_path):
    filename = str(tmp_path / 'baro.ulg')
    synthetic_flight(filename, include=('vehicle_air_data',))
    ulog = ULog(filename)
    series = extract_series(ulog)
    assert series['sources']['alt_m'] == 'vehicle_air_data (baro_alt_meter)'
    assert series['sources']['sink_rate_mps'].startswith('vehicle_air_data')
    (result,) = _reduce(ulog, _point('DESC', 70, 80))
    assert result['metrics']['alt_max_m'] == pytest.approx(200.0, abs=1e-3)
    assert result['metrics']['alt_min_m'] == pytest.approx(180.0, abs=1e-3)
    assert result['metrics']['sink_rate_max_mps'] == pytest.approx(2.0, abs=1e-2)


def test_local_position_is_preferred_over_baro(tmp_path):
    filename = str(tmp_path / 'both.ulg')
    synthetic_flight(filename, include=('vehicle_local_position', 'vehicle_air_data'))
    series = extract_series(ULog(filename))
    assert series['sources']['alt_m'].startswith('vehicle_local_position')
    assert series['sources']['sink_rate_mps'] == 'vehicle_local_position (vz)'


def test_baro_sink_rate_fallback_without_local_vz(tmp_path):
    filename = str(tmp_path / 'no_vz.ulg')
    synthetic_flight(filename, include=('vehicle_local_position', 'vehicle_air_data'),
                     with_vz=False)
    ulog = ULog(filename)
    series = extract_series(ulog)
    assert series['sources']['alt_m'].startswith('vehicle_local_position')
    assert series['sources']['sink_rate_mps'] == 'vehicle_air_data (d/dt baro_alt_meter)'
    (result,) = _reduce(ulog, _point('DESC', 70, 80))
    assert result['metrics']['sink_rate_max_mps'] == pytest.approx(2.0, abs=1e-2)

    # without vehicle_air_data the vertical speed is simply not logged
    filename = str(tmp_path / 'no_vz_no_baro.ulg')
    synthetic_flight(filename, include=('vehicle_local_position',), with_vz=False)
    (result,) = _reduce(ULog(filename), _point('DESC', 70, 80))
    assert result['metrics']['sink_rate_max_mps'] == NOT_LOGGED
    assert result['metrics']['alt_min_m'] != NOT_LOGGED


def test_baro_fallback_when_every_local_sample_is_invalid(tmp_path):
    filename = str(tmp_path / 'all_invalid.ulg')
    synthetic_flight(filename, include=('vehicle_local_position', 'vehicle_air_data'),
                     invalid_z=(0.0, 1000.0))
    ulog = ULog(filename)
    series = extract_series(ulog)
    assert series['sources']['alt_m'] == 'vehicle_air_data (baro_alt_meter)'
    assert series['sources']['sink_rate_mps'] == 'vehicle_air_data (d/dt baro_alt_meter)'
    (result,) = _reduce(ulog, _point('DESC', 70, 80))
    assert result['metrics']['alt_max_m'] == pytest.approx(200.0, abs=1e-3)
    assert result['metrics']['sink_rate_max_mps'] == pytest.approx(2.0, abs=1e-2)


def test_results_are_json_serialisable(synthetic_ulog):
    results = reduce_test_card(synthetic_ulog, [_point('A', 0, 10), _point('B', 200, 300)])
    text = json.dumps(results)
    assert '"NO DATA"' in text and '"COMPLETE"' in text
