"""
Post-flight test-card data reduction.

Pure module: parses a test card (CSV) and reduces a pyulog ULog into
per-test-point results. No Tornado or Bokeh dependencies so it can be
unit-tested and reused from the plot page and the HTTP handler.
"""
import csv
import io
import os
import re

import numpy as np

# CSV header, in this exact order (strict check)
TEST_CARD_COLUMNS = ('test_point_id', 'description', 'start_s', 'end_s',
                     'nz_max_g', 'airspeed_max_mps', 'alt_min_m', 'alt_max_m')
LIMIT_COLUMNS = ('nz_max_g', 'airspeed_max_mps', 'alt_min_m', 'alt_max_m')

TEST_CARD_FILE_SUFFIX = '.testcard.csv'
MAX_TEST_POINTS = 200
MAX_DESCRIPTION_LENGTH = 200

STATUS_COMPLETE = 'COMPLETE'
STATUS_EXCEEDANCE = 'COMPLETE WITH EXCEEDANCE'
STATUS_NO_DATA = 'NO DATA'
NOT_LOGGED = 'not logged'

STANDARD_GRAVITY = 9.80665

_LOG_UUID_RE = re.compile(
    r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
_TEST_POINT_ID_RE = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]{0,31}$')


class TestCardError(ValueError):
    """ raised for malformed test cards; the message is safe to show to the user """


def is_valid_log_uuid(log_id):
    """ allow-list check: log id must be a lower-case hex UUID """
    return isinstance(log_id, str) and _LOG_UUID_RE.match(log_id) is not None


def test_card_filename(log_dir, log_id):
    """
    Path of the stored test card for a log.
    :raises TestCardError: if log_id is not a UUID (checked before any path is built)
    """
    if not is_valid_log_uuid(log_id):
        raise TestCardError('Invalid log id')
    return os.path.join(log_dir, log_id + TEST_CARD_FILE_SUFFIX)


def _parse_float(value, column, line_no, required):
    value = value.strip()
    if value == '':
        if required:
            raise TestCardError('line {}: {} must not be empty'.format(line_no, column))
        return None
    try:
        result = float(value)
    except ValueError as exc:
        raise TestCardError('line {}: {} is not numeric ({!r})'.format(
            line_no, column, value)) from exc
    if not np.isfinite(result):
        raise TestCardError('line {}: {} must be finite'.format(line_no, column))
    return result


def parse_test_card_csv(text):
    """
    Parse test card CSV text into a list of dicts.

    :param text: str (or bytes, decoded as UTF-8)
    :return: list of dicts with keys TEST_CARD_COLUMNS; limits are float or None
    :raises TestCardError: on any malformed content
    """
    if isinstance(text, bytes):
        try:
            text = text.decode('utf-8-sig')
        except UnicodeDecodeError as exc:
            raise TestCardError('test card must be UTF-8 encoded') from exc
    text = text.lstrip('\ufeff')

    reader = csv.reader(io.StringIO(text))
    try:
        header = next(reader)
    except StopIteration as exc:
        raise TestCardError('test card is empty') from exc
    header = [column.strip() for column in header]
    if header != list(TEST_CARD_COLUMNS):
        raise TestCardError('invalid header: expected "{}"'.format(
            ','.join(TEST_CARD_COLUMNS)))

    points = []
    seen_ids = set()
    for row in reader:
        line_no = reader.line_num
        if len(row) == 0 or all(cell.strip() == '' for cell in row):
            continue
        if len(row) != len(TEST_CARD_COLUMNS):
            raise TestCardError('line {}: expected {} fields, got {}'.format(
                line_no, len(TEST_CARD_COLUMNS), len(row)))
        row = dict(zip(TEST_CARD_COLUMNS, row))

        test_point_id = row['test_point_id'].strip()
        if not _TEST_POINT_ID_RE.match(test_point_id):
            raise TestCardError(
                'line {}: test_point_id must be 1-32 characters '
                '[A-Za-z0-9._-]'.format(line_no))
        if test_point_id in seen_ids:
            raise TestCardError('line {}: duplicate test_point_id {!r}'.format(
                line_no, test_point_id))
        seen_ids.add(test_point_id)

        description = row['description'].strip()
        if len(description) > MAX_DESCRIPTION_LENGTH:
            raise TestCardError('line {}: description longer than {} characters'.format(
                line_no, MAX_DESCRIPTION_LENGTH))

        start_s = _parse_float(row['start_s'], 'start_s', line_no, required=True)
        end_s = _parse_float(row['end_s'], 'end_s', line_no, required=True)
        if start_s < 0:
            raise TestCardError('line {}: start_s must be >= 0'.format(line_no))
        if end_s <= start_s:
            raise TestCardError('line {}: end_s must be greater than start_s'.format(line_no))

        point = {
            'test_point_id': test_point_id,
            'description': description,
            'start_s': start_s,
            'end_s': end_s,
        }
        for column in LIMIT_COLUMNS:
            point[column] = _parse_float(row[column], column, line_no, required=False)
        if (point['alt_min_m'] is not None and point['alt_max_m'] is not None
                and point['alt_max_m'] <= point['alt_min_m']):
            raise TestCardError('line {}: alt_max_m must be greater than alt_min_m'.format(
                line_no))
        points.append(point)
        if len(points) > MAX_TEST_POINTS:
            raise TestCardError('too many test points (max {})'.format(MAX_TEST_POINTS))

    if len(points) == 0:
        raise TestCardError('test card has no test points')
    return points


def load_test_card_file(filename):
    """ read and parse a stored test card; raises TestCardError """
    with open(filename, 'rb') as csv_file:
        return parse_test_card_csv(csv_file.read())


class _Series:
    """ a time series (seconds from log start) with samples masked by validity """

    def __init__(self, time_s, values):
        values = np.asarray(values, dtype=np.float64)
        time_s = np.asarray(time_s, dtype=np.float64)
        mask = np.isfinite(values) & np.isfinite(time_s)
        self.time_s = time_s[mask]
        self.values = values[mask]

    def window(self, start_s, end_s):
        """ samples with start_s <= t <= end_s """
        mask = (self.time_s >= start_s) & (self.time_s <= end_s)
        return _Series(self.time_s[mask], self.values[mask])

    def hold_window(self, start_s, end_s):
        """
        Like window(), but also includes the last sample before start_s: under
        zero-order hold that sample is the value in effect at start_s.
        """
        mask = (self.time_s >= start_s) & (self.time_s <= end_s)
        before = np.flatnonzero(self.time_s < start_s)
        if len(before) > 0:
            mask[before[-1]] = True
        return _Series(self.time_s[mask], self.values[mask])

    def __len__(self):
        return len(self.values)

    def exceedance_seconds(self, start_s, end_s, predicate):
        """
        Time (s) the predicate holds, integrated over [start_s, end_s] only.
        Each sample holds its value until the next sample (zero-order hold);
        the last sample is held until end_s.
        """
        if len(self) == 0:
            return 0.0
        exceed = predicate(self.values)
        if not np.any(exceed):
            return 0.0
        next_time = np.append(self.time_s[1:], end_s)
        durations = np.clip(next_time, start_s, end_s) - np.clip(self.time_s, start_s, end_s)
        return float(np.sum(durations[exceed]))


def _dataset(ulog, name):
    try:
        return ulog.get_dataset(name)
    except (KeyError, IndexError, ValueError):
        return None


def _time_s(ulog, dataset):
    return (dataset.data['timestamp'].astype(np.float64)
            - float(ulog.start_timestamp)) / 1e6


def _valid_mask(dataset, flag_name):
    if flag_name in dataset.data:
        return dataset.data[flag_name].astype(bool)
    return np.ones(len(dataset.data['timestamp']), dtype=bool)


def _masked(values, mask):
    values = np.asarray(values, dtype=np.float64).copy()
    values[~mask] = np.nan
    return values


def extract_series(ulog):
    """
    Extract the time series needed by the test card from a ULog.

    :return: dict metric-group -> _Series or None (if not logged), plus
        'sources' dict describing where altitude/vertical speed came from
    """
    series = {'nz_g': None, 'airspeed_mps': None, 'alt_m': None,
              'sink_rate_mps': None, 'bank_deg': None}
    sources = {}

    accel = _dataset(ulog, 'vehicle_acceleration')
    if accel is not None and 'xyz[2]' in accel.data:
        # FRD body frame: specific force along z is -g in level flight
        series['nz_g'] = _Series(_time_s(ulog, accel),
                                 -accel.data['xyz[2]'] / STANDARD_GRAVITY)

    airspeed = _dataset(ulog, 'airspeed_validated')
    if airspeed is not None and 'calibrated_airspeed_m_s' in airspeed.data:
        # selected_airspeed_index < 0: no valid airspeed source selected
        airspeed_valid = np.ones(len(airspeed.data['timestamp']), dtype=bool)
        if 'selected_airspeed_index' in airspeed.data:
            airspeed_valid = airspeed.data['selected_airspeed_index'] >= 0
        series['airspeed_mps'] = _Series(
            _time_s(ulog, airspeed),
            _masked(airspeed.data['calibrated_airspeed_m_s'], airspeed_valid))

    local_pos = _dataset(ulog, 'vehicle_local_position')
    if local_pos is not None and 'z' in local_pos.data:
        time_s = _time_s(ulog, local_pos)
        z_valid = _valid_mask(local_pos, 'z_valid')
        alt = -local_pos.data['z'].astype(np.float64)
        alt_source = 'vehicle_local_position (-z)'
        if 'ref_alt' in local_pos.data:
            # keep the whole series in one frame: absolute (AMSL) if a
            # reference is ever available, masking samples without one
            ref_alt = local_pos.data['ref_alt'].astype(np.float64)
            ref_valid = np.isfinite(ref_alt)
            if np.any(ref_valid):
                alt = _masked(alt + ref_alt, ref_valid)
                alt_source = 'vehicle_local_position (ref_alt - z)'
        alt = _Series(time_s, _masked(alt, z_valid))
        if len(alt) > 0:
            series['alt_m'] = alt
            sources['alt_m'] = alt_source
        if 'vz' in local_pos.data:
            vz_valid = _valid_mask(local_pos, 'v_z_valid')
            sink_rate = _Series(time_s, _masked(local_pos.data['vz'], vz_valid))
            if len(sink_rate) > 0:
                series['sink_rate_mps'] = sink_rate
                sources['sink_rate_mps'] = 'vehicle_local_position (vz)'

    # barometric fallback, independently for altitude and vertical speed, if
    # the estimator topic is missing or has no valid sample at all
    if series['alt_m'] is None or series['sink_rate_mps'] is None:
        air_data = _dataset(ulog, 'vehicle_air_data')
        if air_data is not None and 'baro_alt_meter' in air_data.data:
            time_s = _time_s(ulog, air_data)
            baro_alt = air_data.data['baro_alt_meter'].astype(np.float64)
            if series['alt_m'] is None:
                series['alt_m'] = _Series(time_s, baro_alt)
                sources['alt_m'] = 'vehicle_air_data (baro_alt_meter)'
            if series['sink_rate_mps'] is None and len(time_s) > 1:
                series['sink_rate_mps'] = _Series(
                    time_s, -np.gradient(baro_alt, time_s))
                sources['sink_rate_mps'] = 'vehicle_air_data (d/dt baro_alt_meter)'

    attitude = _dataset(ulog, 'vehicle_attitude')
    if attitude is not None and all('q[{}]'.format(i) in attitude.data for i in range(4)):
        q_w, q_x, q_y, q_z = (attitude.data['q[{}]'.format(i)].astype(np.float64)
                              for i in range(4))
        roll = np.arctan2(2.0 * (q_w * q_x + q_y * q_z),
                          1.0 - 2.0 * (q_x * q_x + q_y * q_y))
        series['bank_deg'] = _Series(_time_s(ulog, attitude), np.degrees(np.abs(roll)))

    series['sources'] = sources
    return series


def _stat(window, func):
    if window is None:
        return NOT_LOGGED
    if len(window) == 0:
        return None
    return float(func(window.values))


def _above(limit):
    return lambda values: values > limit


def _below(limit):
    return lambda values: values < limit


# (limit column, series name, predicate factory)
_LIMIT_CHECKS = (
    ('nz_max_g', 'nz_g', _above),
    ('airspeed_max_mps', 'airspeed_mps', _above),
    ('alt_min_m', 'alt_m', _below),
    ('alt_max_m', 'alt_m', _above),
)


def _exceedances(series, windows, point, start_s, end_s):
    """
    :return: (list of exceedances, list of limits that could not be checked
        because the metric is not logged or has no sample in the window)
    """
    exceedances = []
    unchecked = []
    for limit_name, series_name, predicate_factory in _LIMIT_CHECKS:
        limit = point.get(limit_name)
        if limit is None:
            continue
        window = windows[series_name]
        if window is None or len(window) == 0:
            unchecked.append(limit_name)
            continue
        hold_window = series[series_name].hold_window(start_s, end_s)
        seconds = hold_window.exceedance_seconds(start_s, end_s, predicate_factory(limit))
        if seconds > 0.0:
            exceedances.append({'limit': limit_name, 'limit_value': limit,
                                'seconds': seconds})
    return exceedances, unchecked


def reduce_test_point(series, point, log_duration_s):
    """ compute the results of a single test point """
    start_s = point['start_s']
    end_s = point['end_s']
    clipped_start = max(start_s, 0.0)
    clipped_end = min(end_s, log_duration_s)
    duration_flown_s = max(0.0, clipped_end - clipped_start)

    windows = {}
    for name in ('nz_g', 'airspeed_mps', 'alt_m', 'sink_rate_mps', 'bank_deg'):
        windows[name] = None if series[name] is None else \
            series[name].window(clipped_start, clipped_end)

    metrics = {
        'nz_peak_g': _stat(windows['nz_g'], np.max),
        'nz_mean_g': _stat(windows['nz_g'], np.mean),
        'airspeed_min_mps': _stat(windows['airspeed_mps'], np.min),
        'airspeed_max_mps': _stat(windows['airspeed_mps'], np.max),
        'alt_min_m': _stat(windows['alt_m'], np.min),
        'alt_max_m': _stat(windows['alt_m'], np.max),
        'bank_max_deg': _stat(windows['bank_deg'], np.max),
        'sink_rate_max_mps': _stat(windows['sink_rate_mps'], np.max),
    }
    not_logged = sorted(name for name, value in metrics.items() if value == NOT_LOGGED)
    has_data = any(window is not None and len(window) > 0 for window in windows.values())

    exceedances = []
    unchecked_limits = [name for name in LIMIT_COLUMNS if point.get(name) is not None]
    if has_data and duration_flown_s > 0:
        exceedances, unchecked_limits = _exceedances(series, windows, point,
                                                     clipped_start, clipped_end)

    if not has_data or duration_flown_s <= 0:
        status = STATUS_NO_DATA
    elif exceedances:
        status = STATUS_EXCEEDANCE
    else:
        status = STATUS_COMPLETE

    return {
        'test_point_id': point['test_point_id'],
        'description': point['description'],
        'start_s': start_s,
        'end_s': end_s,
        'duration_flown_s': duration_flown_s,
        'clipped': duration_flown_s < end_s - start_s,
        'limits': {name: point.get(name) for name in LIMIT_COLUMNS},
        'metrics': metrics,
        'not_logged': not_logged,
        'exceedances': exceedances,
        'unchecked_limits': unchecked_limits,
        'status': status,
    }


def reduce_test_card(ulog, test_card):
    """
    Reduce a ULog against a parsed test card.

    :param ulog: pyulog.ULog
    :param test_card: list of dicts as returned by parse_test_card_csv
    :return: dict with 'log_duration_s', 'sources' and 'test_points' (list of results)
    """
    series = extract_series(ulog)
    log_duration_s = max(0.0, (float(ulog.last_timestamp) - float(ulog.start_timestamp)) / 1e6)
    results = [reduce_test_point(series, point, log_duration_s) for point in test_card]
    return {
        'log_duration_s': log_duration_s,
        'sources': series['sources'],
        'test_points': results,
    }
