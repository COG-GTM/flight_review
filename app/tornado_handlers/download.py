"""
Tornado handler for the download page
"""

from __future__ import print_function
import os
from html import escape
import sqlite3
import sys
import uuid
import shutil
import tornado.web

from pyulog.ulog2kml import convert_ulog2kml

# this is needed for the following imports
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../plot_app'))
from helper import get_log_filename, get_log_derived_filename, validate_log_id, \
    flight_modes_table, load_ulog_file, get_default_parameters
from audit import audit_log
from security import sanitize_header_value

from config import get_db_connection, get_kml_filepath

#pylint: disable=relative-beyond-top-level
from .common import CustomHTTPError, TornadoRequestHandlerBase

#pylint: disable=abstract-method, unused-argument, attribute-defined-outside-init

class DownloadHandler(TornadoRequestHandlerBase):
    """ Download log file Tornado request handler """

    def initialize(self):
        """ initialize the instance """
        self._pending_audit = None

    def _emit_download_audit(self, outcome, **fields):
        """ write the audit record for a private-log download exactly once """
        if self._pending_audit is None:
            return
        record = self._pending_audit
        self._pending_audit = None
        audit_log('log_download', outcome, **record, **fields)

    def on_finish(self):
        """ response complete (normal or error): record the real outcome """
        status = self.get_status()
        if status < 400:
            self._emit_download_audit('success')
        else:
            self._emit_download_audit('failure', status=status)

    def on_connection_close(self):
        """ client went away before the response was complete """
        self._emit_download_audit('failure', reason='connection closed')

    def get(self, *args, **kwargs):
        """ GET request callback """
        log_id = self.get_argument('log')
        if not validate_log_id(log_id):
            raise tornado.web.HTTPError(400, 'Invalid Parameter')
        log_file_name = get_log_filename(log_id)
        download_type = self.get_argument('type', default='0')
        if not os.path.exists(log_file_name):
            raise tornado.web.HTTPError(404, 'Log not found')

        if not self.is_public_log(log_id):
            # emitted from on_finish / on_connection_close with the outcome
            self._pending_audit = {'log_id': log_id, 'download_type': download_type,
                                   'public': False, 'client_ip': self.request.remote_ip}

        def get_original_filename(default_value, new_file_suffix):
            """
            get the uploaded file name & exchange the file extension
            """
            con = None
            try:
                con = get_db_connection()
                cur = con.cursor()
                cur.execute('select OriginalFilename '
                            'from Logs where Id = ?', [log_id])
                db_tuple = cur.fetchone()
                if db_tuple is not None:
                    original_file_name = escape(db_tuple[0])
                    if original_file_name[-4:].lower() == '.ulg':
                        original_file_name = original_file_name[:-4]
                    # header value: no control chars, no quotes, no path parts
                    original_file_name = sanitize_header_value(
                        os.path.basename(original_file_name), max_length=120
                    ).replace('"', '')
                    if len(original_file_name) > 0:
                        return original_file_name + new_file_suffix
            except:
                print("DB access failed:", sys.exc_info()[0], sys.exc_info()[1])
            finally:
                if con is not None:
                    con.close()
            return default_value

        if download_type == '1': # download the parameters
            ulog = load_ulog_file(log_file_name)
            param_keys = sorted(ulog.initial_parameters.keys())

            self.set_header('Content-Type', 'application/octet-stream')
            self.set_header("Content-Description", "File Transfer")
            self.set_header('Content-Disposition', 'attachment; filename=vehicle.params')

            delimiter = '	'
            for param_key in param_keys:
                self.write("1") #sysid
                self.write(delimiter)
                self.write("1") #compid
                self.write(delimiter)
                self.write(param_key)
                self.write(delimiter)
                self.write(str(ulog.initial_parameters[param_key]))

                #if the value is an int write a 6, if not write a 9
                if isinstance(ulog.initial_parameters[param_key], int):
                    self.write(delimiter)
                    self.write("6")
                else:
                    self.write(delimiter)
                    self.write("9")

                self.write('\n')

        elif download_type == '2': # download the kml file
            kml_file_name = get_log_derived_filename(get_kml_filepath(), log_id, '.kml')

            # check if chached file exists
            if not os.path.exists(kml_file_name):
                print('need to create kml file', kml_file_name)

                def kml_colors(flight_mode):
                    """ flight mode colors for KML file """
                    if flight_mode not in flight_modes_table: flight_mode = 0

                    color_str = flight_modes_table[flight_mode][1][1:] # color in form 'ff00aa'

                    # increase brightness to match colors with template
                    rgb = [int(color_str[2*x:2*x+2], 16) for x in range(3)]
                    for i in range(3):
                        rgb[i] += 40
                        if rgb[i] > 255: rgb[i] = 255

                    color_str = "".join(map(lambda x: format(x, '02x'), rgb))

                    return 'ff'+color_str[4:6]+color_str[2:4]+color_str[0:2] # KML uses aabbggrr

                style = {'line_width': 2}
                # create in random temporary file, then move it (to avoid races)
                try:
                    temp_file_name = kml_file_name+'.'+str(uuid.uuid4())
                    convert_ulog2kml(log_file_name, temp_file_name,
                                     'vehicle_global_position', kml_colors,
                                     style=style,
                                     camera_trigger_topic_name='camera_capture')
                    shutil.move(temp_file_name, kml_file_name, copy_function=shutil.copyfile)
                except Exception as e:
                    print('Error creating KML file', sys.exc_info()[0], sys.exc_info()[1])
                    raise CustomHTTPError(400, 'No Position Data in log') from e


            kml_dl_file_name = get_original_filename('track.kml', '.kml')

            # send the whole KML file
            self.set_header("Content-Type", "application/vnd.google-earth.kml+xml")
            self.set_header('Content-Disposition',
                            'attachment; filename="{}"'.format(kml_dl_file_name))
            with open(kml_file_name, 'rb') as kml_file:
                while True:
                    data = kml_file.read(4096)
                    if not data:
                        break
                    self.write(data)
                self.finish()

        elif download_type == '3': # download the non-default parameters
            ulog = load_ulog_file(log_file_name)
            param_keys = sorted(ulog.initial_parameters.keys())

            self.set_header('Content-Type', 'application/octet-stream')
            self.set_header("Content-Description", "File Transfer")
            self.set_header('Content-Disposition', 'attachment; filename=non-default.params')
            delimiter = '	'

            # Use defaults from log if available
            if ulog.has_default_parameters:
                system_defaults = ulog.get_default_parameters(0)
                airframe_defaults = ulog.get_default_parameters(1)
                for param_key in param_keys:
                    try:
                        param_value = ulog.initial_parameters[param_key]
                        is_default = True
                        if param_key in airframe_defaults:
                            is_default = param_value == airframe_defaults[param_key]
                        elif param_key in system_defaults:
                            is_default = param_value == system_defaults[param_key]

                        if not is_default:
                            self.write("1") # sysid
                            self.write(delimiter)
                            self.write("1") # compid
                            self.write(delimiter)
                            self.write(param_key)
                            self.write(delimiter)
                            self.write(str(param_value))

                            #if the value is an int write a 6, if not write a 9
                            if isinstance(param_value, int):
                                self.write(delimiter)
                                self.write("6")
                            else:
                                self.write(delimiter)
                                self.write("9")

                            self.write('\n')
                    except:
                        pass

            else:
                default_params = get_default_parameters()

                for param_key in param_keys:
                    try:
                        param_value = str(ulog.initial_parameters[param_key])
                        is_default = False

                        if param_key in default_params:
                            default_param = default_params[param_key]
                            if default_param['type'] == 'FLOAT':
                                is_default = abs(float(default_param['default']) -
                                                 float(param_value)) < 0.00001
                            else:
                                is_default = int(default_param['default']) == int(param_value)

                        if not is_default:
                            self.write("1") # sysid
                            self.write(delimiter)
                            self.write("1") # compid
                            self.write(delimiter)
                            self.write(param_key)
                            self.write(delimiter)
                            self.write(param_value)

                            #if the value is an int write a 6, if not write a 9
                            if isinstance(param_value, int):
                                self.write(delimiter)
                                self.write("6")
                            else:
                                self.write(delimiter)
                                self.write("9")

                            self.write('\n')
                    except:
                        pass

        else: # download the log file
            self.set_header('Content-Type', 'application/octet-stream')
            self.set_header("Content-Description", "File Transfer")
            self.set_header('Content-Disposition', 'attachment; filename={}'.format(
                os.path.basename(log_file_name)))
            with open(log_file_name, 'rb') as log_file:
                while True:
                    data = log_file.read(4096)
                    if not data:
                        break
                    self.write(data)
                self.finish()

    @staticmethod
    def is_public_log(log_id):
        """ True if the log is flagged public in the DB (unknown logs count
        as private) """
        con = get_db_connection()
        try:
            cur = con.cursor()
            cur.execute('select Public from Logs where Id = ?', [log_id])
            db_tuple = cur.fetchone()
            return db_tuple is not None and db_tuple[0] == 1
        except sqlite3.Error:
            return False
        finally:
            con.close()

