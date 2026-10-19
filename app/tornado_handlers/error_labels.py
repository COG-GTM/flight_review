"""
Tornado handler for updating the error label information in the database
"""
from __future__ import print_function

import sys
import os
import tornado.web

# this is needed for the following imports
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'plot_app'))
from config import get_db_connection
from db_entry import *
from helper import validate_log_id, validate_error_ids

class UpdateErrorLabelHandler(tornado.web.RequestHandler):
    """ Update the error label of a flight log."""

    def post(self, *args, **kwargs):
        """ POST request """

        try:
            data = tornado.escape.json_decode(self.request.body)
            log_id = data['log']
            error_ids = data['labels']
        except (ValueError, TypeError, KeyError) as error:
            raise tornado.web.HTTPError(400, 'Invalid Parameter') from error

        if not validate_log_id(log_id):
            raise tornado.web.HTTPError(400, 'Invalid Parameter')

        if not validate_error_ids(error_ids):
            raise tornado.web.HTTPError(400, 'Invalid Parameter')

        error_id_str = ",".join(str(int(error_id)) for error_id in error_ids)

        con = get_db_connection()
        cur = con.cursor()

        cur.execute(
            'UPDATE Logs SET ErrorLabels = ? WHERE Id = ?',
            (error_id_str, log_id))

        con.commit()
        cur.close()
        con.close()

        self.write('OK')

    def data_received(self, chunk):
        """ called whenever new data is received """
        pass
