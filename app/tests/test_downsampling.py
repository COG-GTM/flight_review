""" tests for the envelope / peak-preserving downsampling helpers """
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'plot_app'))

# pylint: disable=wrong-import-position
from downsampling import (minmax_downsample, peak_downsample, # noqa: E402
                          peak_downsample_columns, DownsampleIndicator)


def _series(num_samples=100000):
    timestamp = np.arange(num_samples, dtype=np.uint64) * 1000
    values = np.sin(timestamp / 1e6).astype(np.float32)
    return timestamp, values


def test_minmax_keeps_single_sample_spike_and_nan_gap():
    timestamp, values = _series()
    values[50000] = 50.0
    values[20000:20005] = np.nan
    flag = np.zeros(len(values), dtype=np.uint8)
    flag[70000] = 1

    reduced, step = minmax_downsample(
        {'timestamp': timestamp, 'y': values, 'flag': flag}, 'timestamp', 840 * 3)

    assert step > 1
    assert len(reduced['y']) < len(values) / 10
    assert 50.0 in reduced['y']
    assert np.isnan(reduced['y']).any()
    assert reduced['flag'].max() == 1
    assert reduced['timestamp'][0] == timestamp[0]
    assert reduced['timestamp'][-1] == timestamp[-1]
    assert reduced['flag'].dtype == np.uint8
    assert np.all(np.diff(reduced['timestamp'].astype(np.int64)) > 0)


def test_minmax_no_reduction_below_budget():
    timestamp, values = _series(100)
    reduced, step = minmax_downsample({'timestamp': timestamp, 'y': values},
                                      'timestamp', 1000)
    assert step == 1
    assert len(reduced['y']) == 100


def test_minmax_all_nan_series():
    timestamp, _ = _series(1000)
    reduced, step = minmax_downsample(
        {'timestamp': timestamp, 'y': np.full(1000, np.nan)}, 'timestamp', 20)
    assert step == 100
    assert np.isnan(reduced['y']).all()
    assert len(reduced['y']) >= 10


def test_peak_downsample_keeps_narrow_fft_peak():
    freqs = np.linspace(0, 1000, 100001)
    amplitude = np.ones(100001)
    amplitude[55555] = 100.0
    freqs_plot, values_plot, step = peak_downsample(freqs, amplitude, 840 * 3)
    assert step > 1
    assert len(values_plot) <= len(amplitude) // step + 1
    assert values_plot.max() == 100.0
    assert freqs_plot[np.argmax(values_plot)] == pytest.approx(freqs[55555])


def test_peak_downsample_columns_keeps_short_burst():
    image = np.zeros((129, 10000))
    image[5, 7777] = 9.0
    time = np.arange(10000)
    time_plot, image_plot, step = peak_downsample_columns(time, image, 1680)
    assert step == 6
    assert image_plot.shape == (129, 1667)
    assert image_plot.max() == 9.0
    assert len(time_plot) == 1667


def test_indicator_text_and_visibility():
    class _Plot: # pylint: disable=too-few-public-methods
        def add_layout(self, _label, _place=None):
            pass
    indicator = DownsampleIndicator(_Plot())
    assert not indicator.label.visible
    indicator.update('a', 7)
    assert indicator.label.visible
    assert indicator.label.text.startswith('downsampled 1:7 (min/max envelope)')
    indicator.update('b', 3)
    assert 'downsampled 1:3-1:7' in indicator.label.text
    indicator.update('a', 1)
    indicator.update('b', 1)
    assert not indicator.label.visible


def test_peak_downsample_keeps_partial_last_block():
    """ the remainder bins/columns must not be dropped """
    values = np.zeros(6001)
    values[6000] = 7.0
    x_values = np.arange(6001.)
    x_plot, y_plot, step = peak_downsample(x_values, values, 3000)
    assert step == 3
    assert len(y_plot) == 2001
    assert y_plot[-1] == 7.0 and x_plot[-1] == 6000
    image = np.zeros((4, 6001))
    image[2, 6000] = 7.0
    x_plot, image_plot, step = peak_downsample_columns(x_values, image, 3000)
    assert step == 3
    assert image_plot.shape == (4, 2001)
    assert image_plot[2, -1] == 7.0 and x_plot[-1] == 6000


def test_bucket_size_respects_budget():
    """ ceil division: the result must never exceed the budget """
    x_values = np.arange(4000.)
    _, y_plot, step = peak_downsample(x_values, x_values, 2520)
    assert step == 2 and len(y_plot) == 2000


def test_minmax_unchanged_data_is_not_reported_as_downsampled():
    """ two series whose per-bucket extrema together cover every sample """
    timestamp = np.arange(3000)
    pos = timestamp % 3  # bucket size is 3 for this budget
    y1 = np.where(pos == 0, 1.0, 0.0)  # max at 0, (first) min at 1
    y2 = np.where(pos == 2, 1.0, 0.0)  # max at 2, (first) min at 0
    reduced, step = minmax_downsample(
        {'timestamp': timestamp, 'y1': y1, 'y2': y2}, 'timestamp', 2520)
    assert step == 1
    assert len(reduced['timestamp']) == 3000
