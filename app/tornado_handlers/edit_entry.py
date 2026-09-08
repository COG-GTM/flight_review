"""
Tornado handler to edit/delete a log upload entry
"""
from __future__ import print_function
import os
import sys
import tornado.web

# this is needed for the following imports
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../plot_app'))
from config import get_db_connection, get_kml_filepath, get_overview_img_filepath
from helper import clear_ulog_cache, get_log_filename, get_log_derived_filename, \
    validate_log_id
from security import tokens_match, is_valid_token_format
from audit import audit_log

#pylint: disable=relative-beyond-top-level
from .common import get_jinja_env, TornadoRequestHandlerBase

EDIT_TEMPLATE = 'edit.html'

#pylint: disable=abstract-method


class EditEntryHandler(TornadoRequestHandlerBase):
    """ Edit a log entry, with confirmation (currently only delete) """

    def get(self, *args, **kwargs):
        """ GET request """
        log_id = self.get_argument('log')
        action = self.get_argument('action')
        confirmed = self.get_argument('confirm', default='0')
        token = self.get_argument('token')
        if not validate_log_id(log_id):
            raise tornado.web.HTTPError(400, 'Invalid Parameter')
        if not is_valid_token_format(token):
            audit_log('log_edit', 'failure', log_id=log_id, reason='malformed token',
                      client_ip=self.request.remote_ip)
            raise tornado.web.HTTPError(400, 'Invalid Parameter')

        if action == 'delete':
            if confirmed == '1':
                if self.delete_log_entry(log_id, token):
                    audit_log('log_delete', 'success', log_id=log_id,
                              client_ip=self.request.remote_ip)
                    content = """
<h3>Log File deleted</h3>
<p>
Successfully deleted the log file.
</p>
"""
                else:
                    audit_log('log_delete', 'failure', log_id=log_id,
                              reason='unknown log or token mismatch',
                              client_ip=self.request.remote_ip)
                    content = """
<h3>Failed</h3>
<p>
Failed to delete the log file.
</p>
"""
            else: # request user to confirm
                # use the same url, just append 'confirm=1'
                delete_url = self.request.path+'?action=delete&log='+log_id+ \
                        '&token='+token+'&confirm=1'
                content = """
<h3>Delete Log File</h3>
<p>
Click <a href="{delete_url}">here</a> to confirm and delete the log {log_id}.
</p>
""".format(delete_url=delete_url, log_id=log_id)
        else:
            raise tornado.web.HTTPError(400, 'Invalid Parameter')

        template = get_jinja_env().get_template(EDIT_TEMPLATE)
        self.write(template.render(content=content))


    @staticmethod
    def delete_log_entry(log_id, token):
        """
        delete a log entry (DB & file), validate token first

        :return: True on success
        """
        con = get_db_connection()
        try:
            cur = con.cursor()
            cur.execute('select Token from Logs where Id = ?', (log_id,))
            db_tuple = cur.fetchone()
            if db_tuple is None:
                return False
            if not tokens_match(token, db_tuple[0]):
                return False

            # kml file
            kml_file_name = get_log_derived_filename(get_kml_filepath(), log_id, '.kml')
            if os.path.exists(kml_file_name):
                os.unlink(kml_file_name)

            #preview image
            preview_image_filename = get_log_derived_filename(
                get_overview_img_filepath(), log_id, '.png')
            if os.path.exists(preview_image_filename):
                os.unlink(preview_image_filename)

            log_file_name = get_log_filename(log_id)
            print('deleting log entry {} and file {}'.format(log_id, log_file_name))
            if os.path.exists(log_file_name):
                os.unlink(log_file_name)
            cur.execute("DELETE FROM LogsGenerated WHERE Id = ?", (log_id,))
            cur.execute("DELETE FROM Logs WHERE Id = ?", (log_id,))
            con.commit()
        finally:
            con.close()

        # need to clear the cache as well
        clear_ulog_cache()

        return True
