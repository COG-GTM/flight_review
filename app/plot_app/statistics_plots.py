""" Class for statistics plots page """
from dateutil.relativedelta import relativedelta

import numpy as np

from bokeh.plotting import figure
from bokeh.palettes import viridis # alternatives: magma, inferno
from bokeh.models import (
    DatetimeTickFormatter,
    HoverTool, ColumnDataSource
    )

from plotting import TOOLS, ACTIVE_SCROLL_TOOLS
from config import get_db_connection, get_statistics_max_major_version
from helper import get_airframe_data, flight_modes_table


#pylint: disable=invalid-name,consider-using-dict-items


class _Log:
    """
    container class containing a DB entry for one log
    """

    def __init__(self, db_tuple):
        self.log_id = db_tuple[0]
        self.date = db_tuple[1]
        self.source = db_tuple[2]
        self.is_public = db_tuple[3]
        self.rating = db_tuple[4]

        self.duration = 0
        self.autostart_id = 0
        self.hardware = ""
        self.uuid = ""
        self.sw_version = ""
        self.flight_mode_durations = []

        self.is_release = False

    def set_generated(self, db_tuple):
        """ set from a LogsGenerated DB tuple """
        self.duration = db_tuple[1]
        self.autostart_id = db_tuple[4]
        self.hardware = db_tuple[5]
        self.uuid = db_tuple[11]
        # the version has typically the form 'v<i>.<j>.<k> <l>', where <l>
        # is the firmware release type enum (0=dev, 64=alpha, 128=beta, 192=rc, 255=release)
        version = db_tuple[10].split(' ')
        self.sw_version = version[0]
        release_type_suffix = {64: '-alpha', 128: '-beta', 192: '-rc', 255: ''}
        if len(version) > 1:
            try:
                rtype = int(version[1])
                suffix = release_type_suffix.get(rtype)
                if suffix is not None:
                    self.sw_version += suffix
                else:
                    # type 0 or unknown — untagged dev build, keep bare version
                    pass
                self.is_release = rtype == 255
            except ValueError:
                self.is_release = False
        else:
            self.is_release = False

        self.flight_mode_durations = \
            [tuple(map(int, x.split(':'))) for x in db_tuple[12].split(',') if len(x) > 0]


class StatisticsPlots:
    """
    Class to generate statistics plots from Database entries
    """

    # Selection rules for the public log statistics. Every log that is dropped
    # by one of them is counted in _exclusion_counts, so the page can disclose
    # the filtering (see public_logs_selection_html()).
    PUBLIC_LOGS_WINDOW_DAYS = 90
    MAX_LOG_DURATION_DAYS = 7
    MIN_MAJOR_VERSION = 1
    MAX_NUM_GROUPS = 20

    EXCLUSION_NO_GENERATED_DATA = 'no generated log data available'
    EXCLUSION_VERSION_UNSET = 'firmware version not set'
    EXCLUSION_VERSION_ZERO = 'firmware version v0.0.0'
    EXCLUSION_DURATION = 'flight duration above %i days (probably bogus timestamps)' % \
        MAX_LOG_DURATION_DAYS
    EXCLUSION_AUTOSTART = 'no airframe (SYS_AUTOSTART = 0)'
    EXCLUSION_VERSION_UNPARSABLE = 'firmware version not parsable'

    def __init__(self, plot_config, verbose_output=False):

        self._config = plot_config

        self._verbose_output = verbose_output

        self._num_logs_total = 0
        self._num_logs_ci = 0
        self._num_flight_hours_total = 0

        self._public_logs = []
        self._num_public_logs_candidates = 0
        self._max_major_version = get_statistics_max_major_version()
        if self._max_major_version > 0:
            exclusion_version_range = 'firmware major version outside %i..%i' % \
                (self.MIN_MAJOR_VERSION, self._max_major_version)
        else:
            exclusion_version_range = 'firmware major version below %i' % \
                self.MIN_MAJOR_VERSION
        self._exclusion_version_range = exclusion_version_range
        # ordered by the sequence the rules are applied
        self._exclusion_counts = {
            self.EXCLUSION_NO_GENERATED_DATA: 0,
            self.EXCLUSION_VERSION_ZERO: 0,
            self.EXCLUSION_DURATION: 0,
            self.EXCLUSION_VERSION_UNSET: 0,
            self.EXCLUSION_AUTOSTART: 0,
            exclusion_version_range: 0,
            self.EXCLUSION_VERSION_UNPARSABLE: 0,
            }

        # read from the DB
        con = get_db_connection()
        try:
            cur = con.cursor()

            cur.execute("select count(Id) from Logs")
            db_tuple = cur.fetchone()
            if db_tuple is not None:
                self._num_logs_total = db_tuple[0]

            cur.execute("select count(Id) from Logs where Source = 'CI'")
            db_tuple = cur.fetchone()
            if db_tuple is not None:
                self._num_logs_ci = db_tuple[0]

            # Get all log dates of specific types within 6 hour intervals
            cur.execute('''
select
    Date,
    count(*) cnt,
    datetime((strftime('%s', Date) / (6 * 60 * 60)) * 6 * 60 * 60, 'unixepoch') new_date
from Logs
where Public = 1
group by new_date
order by new_date
''')
            self._public_log_dates_intervals = cur.fetchall()
            cur.execute('''
select
    Date,
    count(*) cnt,
    datetime((strftime('%s', Date) / (6 * 60 * 60)) * 6 * 60 * 60, 'unixepoch') new_date
from Logs
where Public = 0
group by new_date
order by new_date
''')
            self._private_log_dates_intervals = cur.fetchall()

            # Get all public logs within the last few months
            cur.execute("select Id, Date, Source, Public, Rating from Logs where Public = 1 "
                        "and Source != 'CI' and "
                        "Date > date('now', ?) order by Date",
                        ['-%i day' % self.PUBLIC_LOGS_WINDOW_DAYS])
            db_tuples = cur.fetchall()
            self._num_public_logs_candidates = len(db_tuples)
            for db_tuple in db_tuples:
                log = _Log(db_tuple)

                cur.execute('select * from LogsGenerated where Id = ?', [log.log_id])
                db_tuple = cur.fetchone()

                if db_tuple is None:
                    self._exclude_log(log, self.EXCLUSION_NO_GENERATED_DATA)
                    continue

                log.set_generated(db_tuple)

                # filter bogus entries
                if log.sw_version == 'v0.0.0':
                    self._exclude_log(log, self.EXCLUSION_VERSION_ZERO)
                    continue
                if log.duration > self.MAX_LOG_DURATION_DAYS*24*3600:
                    self._exclude_log(log, self.EXCLUSION_DURATION,
                                      'duration=%i' % log.duration)
                    continue

                if log.sw_version == '':
                    # FIXME: does that still occur and if so why?
                    self._exclude_log(log, self.EXCLUSION_VERSION_UNSET)
                    continue

                if log.autostart_id == 0:
                    self._exclude_log(log, self.EXCLUSION_AUTOSTART)
                    continue

                try:
                    ver_major = int(log.sw_version[1:].split('.')[0])
                except ValueError:
                    self._exclude_log(log, self.EXCLUSION_VERSION_UNPARSABLE, log.sw_version)
                    continue
                if ver_major < self.MIN_MAJOR_VERSION or \
                        0 < self._max_major_version < ver_major:
                    self._exclude_log(log, self._exclusion_version_range, log.sw_version)
                    continue

                self._public_logs.append(log)
                self._num_flight_hours_total += log.duration

            self._num_flight_hours_total /= 3600
        finally:
            con.close()

    def _exclude_log(self, log, reason, details=''):
        """ record that a public log is excluded from the statistics """
        self._exclusion_counts[reason] += 1
        if self._verbose_output:
            print('Warning: excluding log %s from statistics: %s %s' %
                  (log.log_id, reason, details))

    def public_logs_window_days(self):
        """ get the time window (in days) of the public log statistics """
        return self.PUBLIC_LOGS_WINDOW_DAYS

    def num_public_logs_candidates(self):
        """ get the number of public, non-CI logs within the time window,
        before applying the selection rules """
        return self._num_public_logs_candidates

    def num_public_logs_included(self):
        """ get the number of public logs the statistics are computed from """
        return len(self._public_logs)

    def public_logs_exclusion_counts(self):
        """ get a dict of (exclusion rule description -> number of excluded logs),
        in the order the rules are applied """
        return dict(self._exclusion_counts)

    def public_logs_selection_html(self):
        """
        get an HTML description of how the logs for the public statistics were
        selected: time window, CI exclusion, each exclusion rule with the number
        of logs it removed, and the grouping into 'Others'
        """
        num_excluded = sum(self._exclusion_counts.values())
        html = ('<p>These statistics are computed from %i of the %i public, non-CI logs '
                'uploaded within the last %i days. %i logs were excluded by the following '
                'rules:</p>' % (self.num_public_logs_included(),
                                self._num_public_logs_candidates,
                                self.PUBLIC_LOGS_WINDOW_DAYS, num_excluded))
        html += '<ul>'
        for reason, count in self._exclusion_counts.items():
            html += '<li>%s: %i</li>' % (reason, count)
        html += '</ul>'
        html += ('<p>Logs uploaded as private or from Continuous Integration (CI) are not '
                 'included. Per-group plots show the %i largest groups; all remaining groups '
                 'are merged into &quot;Others&quot;.</p>' % self.MAX_NUM_GROUPS)
        return html


    def get_data_for_plotting(self, groups_value_getter, empty_value=0,
                              value_adder=lambda a, b: a+b):
        """
        Get some data in a form that it can be used for plotting
        :return: tuple of list(dates), dict(group, list(value)),
                 with len(list(dates)) == len(list(value))
        """
        if len(self._public_logs) == 0:
            return [], {}
        interval = relativedelta(days=1)
        cur_interval_date = self._public_logs[0].date
        dates = [cur_interval_date]
        groups = {} # map with list of values for each group
        for log in self._public_logs:
            if log.date > cur_interval_date + interval:
                dates.append(log.date)
                for group in groups:
                    groups[group].append(empty_value)
                cur_interval_date = log.date
            groups_and_values = groups_value_getter(log)
            for group, value in groups_and_values:
                if group not in groups:
                    groups[group] = [empty_value] * len(dates)
                groups[group][-1] = value_adder(groups[group][-1], value)
        return dates, groups



    def num_logs_total(self):
        """ get the total number of logs on the server """
        return self._num_logs_total

    def num_logs_ci(self):
        """ get the total number of CI logs on the server """
        return self._num_logs_ci

    def plot_log_upload_statistics(self, colors):
        """
        plot upload statistics for different upload types. Each type is a list of
        datetime of a single upload
        :param colors: list of 5 colors
        :return: bokeh plot
        """
        title = 'Number of Log Files on the Server'
        p = figure(title=title, x_axis_label=None,
                   y_axis_label=None, tools=TOOLS,
                   active_scroll=ACTIVE_SCROLL_TOOLS)

        def plot_dates(p, data_points, last_date, legend, color):
            """ plot a single line from a list of dates """

            # subsample
            dates_list_subsampled = []
            counts_subsampled = []
            count_total = 0
            for date, count, _ in data_points:
                dates_list_subsampled.append(date)
                count_total += count
                counts_subsampled.append(count_total)

            if len(counts_subsampled) > 0:
                if dates_list_subsampled[-1] < last_date:
                    # make sure the plot line extends to the last date
                    counts_subsampled.append(counts_subsampled[-1])
                    dates_list_subsampled.append(last_date)

                p.line(dates_list_subsampled, counts_subsampled,
                       legend_label=legend, line_width=2, line_color=color)

        if len(self._public_log_dates_intervals) > 0:
            last_date = self._public_log_dates_intervals[-1][0]
            plot_dates(p, self._private_log_dates_intervals, last_date, 'Private', colors[2])
            plot_dates(p, self._public_log_dates_intervals, last_date, 'Public', colors[4])

        self._setup_plot(p, 'large')

        return p

    def total_public_flight_duration(self):
        """ get total public flight hours """
        return self._num_flight_hours_total

    def plot_public_airframe_statistics(self):
        """
        plot airframe flight hour statistics, for public logs
        :return: bokeh plot
        """

        def label_callback(airframe_id):
            """ get the airframe label for the sys_autostart id """
            airframe_data = get_airframe_data(airframe_id)
            if airframe_data is None:
                airframe_label = airframe_id
            else:
                airframe_type = ''
                if 'type' in airframe_data:
                    airframe_type = ', '+airframe_data['type']
                airframe_label = airframe_data.get('name')+ \
                                   airframe_type+' ('+airframe_id+')'
            return airframe_label

        dates, groups = self.get_data_for_plotting(lambda log: [(str(log.autostart_id), 1)])
        # Cumulative
        for group in groups:
            groups[group] = np.cumsum(groups[group])

        return self.plot_groups_as_stack(dates, groups, "Number of Flights", "Airframe",
                                         label_callback)

    def plot_public_flight_mode_statistics(self):
        """
        plot flight mode statistics, for public logs
        :return: bokeh plot
        """

        def label_callback(flight_mode):
            """ get flight mode as string from an integer value """
            try:
                return flight_modes_table[int(flight_mode)][0]
            except:
                return f'Unknown ({flight_mode})'

        dates, groups = self.get_data_for_plotting(
            # Filter out invalid durations
            lambda log: [(str(mode), duration / 3600)
                         for mode, duration in log.flight_mode_durations
                         if duration < 7 * 24 * 3600])
        # Cumulative
        for group in groups:
            groups[group] = np.cumsum(groups[group])

        return self.plot_groups_as_stack(dates, groups, "Flight Hours", "Flight Mode",
                                         label_callback)

    def plot_public_board_flights_statistics(self):
        """
        plot per-board #logs statistics, for public logs
        :return: bokeh plot
        """

        dates, groups = self.get_data_for_plotting(lambda log: [(log.hardware, 1)])
        # Cumulative
        for group in groups:
            groups[group] = np.cumsum(groups[group])

        return self.plot_groups_as_stack(dates, groups, "Number of Flights", "Board")

    def plot_public_board_hours_statistics(self):
        """
        plot per-board flight hour statistics, for public logs
        :return: bokeh plot
        """

        dates, groups = self.get_data_for_plotting(
            lambda log: [(log.hardware, log.duration / 3600)])
        # Cumulative
        for group in groups:
            groups[group] = np.cumsum(groups[group])

        return self.plot_groups_as_stack(dates, groups, "Flight Hours", "Board")

    def plot_public_version_flights_statistics(self):
        """
        plot per-version #logs statistics, for public logs
        :return: bokeh plot
        """

        dates, groups = self.get_data_for_plotting(
            lambda log: [(log.sw_version, 1)])
        # Cumulative
        for group in groups:
            groups[group] = np.cumsum(groups[group])

        return self.plot_groups_as_stack(dates, groups, "Number of Flights", "Version")

    def plot_public_unique_boards_statistics(self):
        """
        plot per-board #unique-boards statistics, for public logs
        :return: bokeh plot
        """

        dates, groups = self.get_data_for_plotting(
            lambda log: [(log.hardware, log.uuid)], [], lambda a, b: a + [b])
        # Cumulative
        for group in groups:
            all_previous = set()
            for i, date_list in enumerate(groups[group]):
                all_previous.update(set(date_list))
                groups[group][i] = len(all_previous)

        return self.plot_groups_as_stack(dates, groups, "Number of Unique Boards", "Board Type")

    def plot_groups_as_stack(self, dates, groups, title_prefix, title_name,
                             label_callback=lambda label: label):
        """
        Plot a set of groups as a stack plot
        :param dates: list of dates
        :param groups: dict of groups, each is a list of values
        :param title_prefix: plot title prefix
        :param title_name: plot tile name
        :param label_callback: convert the group name to a label
        :return: bokeh plot
        """

        all_groups = sorted(groups.keys(), key=lambda group: groups[group][-1])

        # Limit number of groups
        max_num_groups = self.MAX_NUM_GROUPS
        num_others = 0
        if len(all_groups) > max_num_groups:
            num_others = len(all_groups)-max_num_groups+1
            others = np.array(groups[all_groups[0]])
            for i in range(1, num_others):
                others += groups[all_groups[i]]
            groups['__others__'] = others
            all_groups = ['__others__'] + all_groups[num_others:]

        colors = []
        palette = list(viridis(10))
        while len(colors) < len(all_groups):
            colors.extend(palette[:len(all_groups)-len(colors)])

        area = figure(title=title_prefix+" per "+title_name, tools=TOOLS,
                      active_scroll=ACTIVE_SCROLL_TOOLS,
                      x_axis_type='datetime',
                      y_axis_label='')

        others_label = 'Others (%i groups merged)' % num_others
        legend_labels = [others_label if l == '__others__' else label_callback(l)
                         for l in all_groups]

        # Directly use the displayed label as data keys. It's the easiest way to ensure the hover
        # tool shows the right label, with the slight risk of creating a collision if 2 labels are
        # equal
        displayed_groups = {}
        for i, legend_label in enumerate(legend_labels):
            displayed_groups[legend_label] = groups[all_groups[i]]

        displayed_groups['__dates__'] = dates
        source = ColumnDataSource(data=displayed_groups)
        area.varea_stack(legend_labels, x='__dates__', color=colors, source=source,
                         legend_label=legend_labels, alpha=0.8)

        tooltips = """
    <div>
        <div>
            <span style="font-size: 12px; color: #05ABFF;">$name:</span>
            <span style="font-size: 12px; color: #000;">@$name</span>
        </div>
    </div>
"""
        area.add_tools(HoverTool(tooltips=tooltips))

        if area.legend:
            area.legend[0].items.reverse()

            # decrease size a bit to fit all items
            area.legend.label_text_font_size = '8pt'
            area.legend.label_height = 8
            area.legend.glyph_height = 10

        self._setup_plot(area, 'large')
        return area

    def _setup_plot(self, p, plot_height='normal'):
        """ apply layout options to a bokeh plot """

        p.xaxis.formatter = DatetimeTickFormatter(
            hours="%d %b %Y %H:%M",
            days="%d %b %Y",
            months="%d %b %Y",
            years="%d %b %Y",
        )

        plots_width = self._config['plot_width']
        plots_height = self._config['plot_height'][plot_height]
        p.width = plots_width
        p.height = plots_height

        p.xgrid.grid_line_color = 'navy'
        p.xgrid.grid_line_alpha = 0.13
        p.ygrid.grid_line_color = 'navy'
        p.ygrid.grid_line_alpha = 0.13
        p.legend.location = "top_left"
        p.toolbar.logo = None

