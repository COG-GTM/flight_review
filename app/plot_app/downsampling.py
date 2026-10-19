""" Server-side data downsampling for bokeh plots, with on-plot disclosure """

from timeit import default_timer as timer
import numpy as np
from bokeh.models import ColumnDataSource, Title
from helper import print_timing


def bucket_size_for(num_samples, max_num_data_points):
    """ number of consecutive samples that get reduced into one bucket so that
        at most max_num_data_points buckets remain. 1 means no reduction """
    if num_samples <= max_num_data_points or max_num_data_points <= 0:
        return 1
    return max(1, int(np.ceil(num_samples / max_num_data_points)))


def _bucket_extrema_indices(values, bucket_size):
    """ per bucket of bucket_size consecutive samples, return the indices of
        the minimum, the maximum and (if any) the first NaN sample """
    num_samples = len(values)
    num_buckets = -(-num_samples // bucket_size)
    padded = np.full(num_buckets * bucket_size, np.nan)
    padded[:num_samples] = np.asarray(values, dtype=float)
    buckets = padded.reshape(num_buckets, bucket_size)
    offsets = np.arange(num_buckets) * bucket_size

    nan_mask = np.isnan(buckets)
    all_nan = np.all(nan_mask, axis=1)
    # nanargmin/nanargmax raise on all-NaN rows, so use a finite stand-in
    safe = np.where(all_nan[:, np.newaxis], 0.0, buckets)
    indices = [offsets + np.nanargmin(safe, axis=1),
               offsets + np.nanargmax(safe, axis=1)]
    has_nan = np.any(nan_mask, axis=1)
    if np.any(has_nan):
        first_nan = np.argmax(nan_mask[has_nan], axis=1)
        indices.append(offsets[has_nan] + first_nan)
    indices = np.concatenate(indices)
    return indices[indices < num_samples]


def minmax_downsample(data, x_key, max_num_data_points):
    """ envelope (min/max per bucket) downsampling of a dict of equally long
        numpy arrays sharing the x axis x_key.

        Each bucket of N consecutive samples keeps, for every y array, the
        sample with the minimum and the maximum value (plus the first NaN, so
        gaps stay visible); the first and last sample are always kept. Unlike
        every-N-th-sample decimation this preserves short spikes and dropouts.

        max_num_data_points is the budget of plotted samples for a single
        y series (2 per bucket), the total can be larger for several series.

        :return: (downsampled data dict, bucket size N; 1 means no reduction)
    """
    num_samples = len(data[x_key])
    bucket_size = bucket_size_for(num_samples, max_num_data_points / 2)
    if bucket_size <= 1:
        return data, 1
    keep = [np.array([0, num_samples - 1])]
    for key, values in data.items():
        if key == x_key:
            continue
        keep.append(_bucket_extrema_indices(values, bucket_size))
    keep = np.unique(np.concatenate(keep))
    if len(keep) == num_samples:
        return data, 1
    return {k: v[keep] for k, v in data.items()}, bucket_size


def peak_downsample(x_values, y_values, max_num_data_points):
    """ peak-preserving reduction for static (non time-series) line data such
        as an FFT: each block of N consecutive bins is replaced by its maximum
        y value, located at the x value where that maximum occurs.

        :return: (x, y, block size N; 1 means no reduction)
    """
    num_samples = len(y_values)
    step_size = bucket_size_for(num_samples, max_num_data_points)
    if step_size <= 1:
        return x_values, y_values, 1
    block_starts = np.arange(0, num_samples, step_size)
    # pad the last (partial) block with -inf so that it is kept as well
    padded = np.full(len(block_starts) * step_size, -np.inf)
    padded[:num_samples] = y_values
    peak_idx = block_starts + np.argmax(padded.reshape(len(block_starts), step_size), axis=1)
    return np.asarray(x_values)[peak_idx], np.asarray(y_values)[peak_idx], step_size


def peak_downsample_columns(x_values, image, max_num_data_points):
    """ peak-preserving reduction of the columns (axis 1) of a 2D image such as
        a spectrogram: each block of N consecutive columns is replaced by the
        per-row maximum, keeping the x value of the first column of the block.

        :return: (x, image, block size N; 1 means no reduction)
    """
    num_columns = image.shape[1]
    step_size = bucket_size_for(num_columns, max_num_data_points)
    if step_size <= 1:
        return x_values, image, 1
    block_starts = np.arange(0, num_columns, step_size)
    # reduceat includes the last (partial) block
    return (np.asarray(x_values)[block_starts],
            np.maximum.reduceat(image, block_starts, axis=1), step_size)


class DownsampleIndicator:
    """ on-plot disclosure of a reduction: a small note below the x axis of
        a bokeh plot (so it never covers data). Hidden while nothing is
        reduced. Several downsamplers of the same plot can share one indicator """

    def __init__(self, bokeh_plot, method='min/max envelope', dynamic=True):
        """
        :param method: short description of the reduction method
        :param dynamic: whether zooming in restores the full resolution
        """
        self._method = method
        self._dynamic = dynamic
        self._step_sizes = {}
        self.label = Title(text='', text_font_size='8pt', text_font_style='italic',
                           text_color='#555555', align='left', visible=False)
        bokeh_plot.add_layout(self.label, 'below')

    def update(self, source_id, step_size):
        """ report the current reduction factor of one data source """
        self._step_sizes[source_id] = step_size
        step_sizes = [s for s in self._step_sizes.values() if s > 1]
        if len(step_sizes) == 0:
            self.label.visible = False
            self.label.text = ''
            return
        min_step, max_step = min(step_sizes), max(step_sizes)
        ratio = '1:{}'.format(max_step) if min_step == max_step \
            else '1:{}-1:{}'.format(min_step, max_step)
        text = 'downsampled {} ({})'.format(ratio, self._method)
        if self._dynamic:
            text += ', zoom in for full resolution'
        self.label.text = text
        self.label.visible = True


class DynamicDownsample:
    """ server-side dynamic data downsampling of bokeh time series plots
        using numpy data sources.
        Initializes the plot with a fixed number of samples per pixel and then
        dynamically loads samples when zooming in or out based on density
        thresholds.
        Uses min/max envelope downsampling (see minmax_downsample) and reports
        the current reduction factor to a DownsampleIndicator.
    """
    def __init__(self, bokeh_plot, data, x_key, indicator=None):
        """ Initialize and setup callback

        Args:
            bokeh_plot (bokeh.plotting.figure) : plot for downsampling
            data (dict) : data source of the plots, contains all samples. Arrays
                          are expected to be numpy
            x_key (str): key for x axis in data
            indicator (DownsampleIndicator): shared on-plot indicator, created
                          if None
        """
        self.bokeh_plot = bokeh_plot
        self.x_key = x_key
        self.data = data
        self.last_step_size = 1
        self.indicator = indicator
        if self.indicator is None:
            self.indicator = DownsampleIndicator(bokeh_plot)

        # parameters
        # minimum number of samples/pixel. Below that, we load new data
        self.min_density = 2
        # density on startup: density used for initializing the plot. The
        # smaller this is, the less data needs to be loaded on page load (this
        # must still be >= min_density).
        self.startup_density = 3
        # when loading new data, number of samples/pixel is set to this value
        self.init_density = 5
        # when loading new data, add a percentage of data on both sides
        self.range_margin = 0.2
        # min/max downsampling keeps up to 2 samples per bucket and series
        self.max_samples_per_bucket = 2 * max(1, len(data) - 1)

        # create a copy of the initial data
        self.init_data = {}
        self.cur_data = {}
        for k in data:
            self.init_data[k] = data[k]
            self.cur_data[k] = data[k]

        # first downsampling
        self.downsample(self.cur_data, self.bokeh_plot.width *
                        self.startup_density)
        self.data_source = ColumnDataSource(data=self.cur_data)

        # register the callbacks
        bokeh_plot.x_range.on_change('start', self.x_range_change_cb)
        bokeh_plot.x_range.on_change('end', self.x_range_change_cb)


    def x_range_change_cb(self, attr, old, new):
        """ bokeh server-side callback when plot x-range changes (zooming) """
        cb_start_time = timer()

        new_range = [self.bokeh_plot.x_range.start, self.bokeh_plot.x_range.end]
        if None in new_range:
            return
        plot_width = self.bokeh_plot.width
        init_x = self.init_data[self.x_key]
        cur_x = self.cur_data[self.x_key]
        cur_range = [cur_x[0], cur_x[-1]]

        need_update = False
        if (new_range[0] < cur_range[0] and cur_range[0] > init_x[0]) or \
                (new_range[1] > cur_range[1] and cur_range[1] < init_x[-1]):
            need_update = True # zooming out / panning

        visible_points = ((new_range[0] < cur_x) & (cur_x < new_range[1])).sum()
        if visible_points / plot_width < self.min_density:
            visible_points_all_data = ((new_range[0] < init_x) & (init_x < new_range[1])).sum()
            if visible_points_all_data > visible_points:
                need_update = True
            # else: reached maximum zoom level

        if visible_points / plot_width > self.init_density * 3 * self.max_samples_per_bucket:
            # mostly a precaution, the panning case above catches most cases
            need_update = True

        if need_update:
            drange = new_range[1] - new_range[0]
            new_range[0] -= drange * self.range_margin
            new_range[1] += drange * self.range_margin
            num_data_points = plot_width * self.init_density * (1 + 2*self.range_margin)
            indices = np.logical_and(init_x > new_range[0], init_x < new_range[1])

            self.cur_data = {}
            for k,value in self.init_data.items():
                self.cur_data[k] = value[indices]

            # downsample
            self.downsample(self.cur_data, num_data_points)

            self.data_source.data = self.cur_data

            print_timing("Data update", cb_start_time)


    def downsample(self, data, max_num_data_points):
        """ min/max downsampling with a given maximum number of samples per
            series (in-place on data) """
        if len(data[self.x_key]) == 0:
            self.last_step_size = 1
        else:
            reduced, self.last_step_size = minmax_downsample(data, self.x_key,
                                                             max_num_data_points)
            data.update(reduced)
        self.indicator.update(id(self), self.last_step_size)
