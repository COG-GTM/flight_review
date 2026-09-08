"""
Tornado handler for post-flight test cards:
  POST /test_card?log=<log_id>  upload a test card CSV (multipart, field 'testcard')
  GET  /test_card?log=<log_id>  results as JSON, or HTML for browsers
"""
import html
import json
import os
import sys
import tempfile

import tornado.web
from tornado.httputil import parse_body_arguments

# this is needed for the following imports
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../plot_app'))
from config import get_db_connection, get_log_filepath
from helper import get_log_filename, load_ulog_file
# plot_app/test_card.py (the pure data reduction module), not this handler
from test_card import (TestCardError, TEST_CARD_COLUMNS, is_valid_log_uuid, #pylint: disable=import-self
                       load_test_card_file, parse_test_card_csv,
                       reduce_test_card, test_card_filename)

#pylint: disable=relative-beyond-top-level
from .common import CustomHTTPError, TornadoRequestHandlerBase, get_jinja_env

#pylint: disable=abstract-method, attribute-defined-outside-init

MAX_CSV_SIZE = 256 * 1024
# the CSV part is limited to MAX_CSV_SIZE; the whole request body (multipart
# framing, file name, any extra form fields) is limited to MAX_BODY_SIZE
MAX_MULTIPART_OVERHEAD = 64 * 1024
MAX_BODY_SIZE = MAX_CSV_SIZE + MAX_MULTIPART_OVERHEAD
UPLOAD_FIELD = 'testcard'
ALLOWED_CONTENT_TYPES = ('text/csv',)


@tornado.web.stream_request_body
class TestCardHandler(TornadoRequestHandlerBase):
    """ upload a test card for a log and show the reduced results """

    def prepare(self):
        """ called before the body is streamed in """
        self._body = bytearray()
        self._body_too_large = False
        if self.request.method == 'POST':
            content_length = self.request.headers.get('Content-Length', '')
            if content_length.isdigit() and int(content_length) > MAX_BODY_SIZE:
                self._body_too_large = True

    def data_received(self, chunk):
        """ accumulate the request body, bounded by MAX_BODY_SIZE """
        if self._body_too_large:
            return
        if len(self._body) + len(chunk) > MAX_BODY_SIZE:
            self._body_too_large = True
            self._body = bytearray()
            return
        self._body.extend(chunk)

    def set_default_headers(self):
        """ security headers for all responses of this handler """
        self.set_header('X-Content-Type-Options', 'nosniff')
        self.set_header('X-Frame-Options', 'DENY')
        self.set_header('Cache-Control', 'no-store')

    def write_error(self, status_code, **kwargs):
        """ render errors as escaped HTML or JSON, depending on the client """
        error_message = ''
        if 'exc_info' in kwargs:
            exc = kwargs['exc_info'][1]
            if isinstance(exc, CustomHTTPError) and exc.error_message:
                error_message = exc.error_message
        if self._wants_html():
            self.set_header('Content-Type', 'text/html; charset=UTF-8')
            self.write('<html><title>Error {0}</title><body>HTTP Error {0}{1}</body></html>'
                       .format(status_code, html.escape(': ' + error_message)
                               if error_message else ''))
        else:
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps({'error': error_message or 'An error occurred',
                                   'status': status_code}))

    def _wants_html(self):
        if self.get_query_argument('format', default=None) == 'json':
            return False
        accept = self.request.headers.get('Accept', '')
        if 'application/json' in accept and 'text/html' not in accept:
            return False
        return True

    def _get_log_id(self):
        """
        Validate the log id against the UUID allow-list and make sure the log
        exists in the DB and on disk (404 otherwise).
        """
        log_id = self.get_query_argument('log', default=None)
        if log_id is None or not is_valid_log_uuid(log_id):
            raise CustomHTTPError(400, 'Invalid log id')

        con = get_db_connection()
        try:
            cur = con.cursor()
            cur.execute('select Id from Logs where Id = ?', [log_id])
            db_row = cur.fetchone()
        finally:
            con.close()
        if db_row is None or not os.path.exists(get_log_filename(log_id)):
            raise CustomHTTPError(404, 'Log not found')
        return log_id

    @staticmethod
    def _test_card_path(log_id):
        return test_card_filename(get_log_filepath(), log_id)

    def _load_results(self, log_id):
        """ reduce the stored test card for the log, or None if there is none """
        card_path = self._test_card_path(log_id)
        if not os.path.isfile(card_path):
            return None
        try:
            test_card = load_test_card_file(card_path)
        except TestCardError as exc:
            raise CustomHTTPError(500, 'Stored test card is invalid') from exc
        ulog = load_ulog_file(get_log_filename(log_id))
        return reduce_test_card(ulog, test_card)

    def _render_page(self, log_id, error_message=None):
        template = get_jinja_env().get_template('test_card.html')
        self.set_header('Content-Type', 'text/html; charset=UTF-8')
        self.write(template.render(
            log_id=log_id, results=self._load_results(log_id),
            csv_header=','.join(TEST_CARD_COLUMNS),
            max_csv_size_kb=MAX_CSV_SIZE // 1024,
            error_message=error_message))

    def get(self, *args, **kwargs):
        """ GET request: results page (HTML) or results as JSON """
        log_id = self._get_log_id()
        if self._wants_html():
            self._render_page(log_id)
            return
        results = self._load_results(log_id)
        if results is None:
            raise CustomHTTPError(404, 'No test card attached to this log')
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps({'log_id': log_id, **results}))

    def post(self, *args, **kwargs):
        """ POST request: validate and store an uploaded test card CSV """
        log_id = self._get_log_id()
        try:
            csv_data = self._validated_upload()
        except CustomHTTPError as exc:
            if not self._wants_html():
                raise
            # show the validation error on the page itself for browser uploads
            self.set_status(exc.status_code)
            self._render_page(log_id, error_message=exc.error_message)
            return

        self._write_atomically(self._test_card_path(log_id), csv_data)

        if self._wants_html():
            self.redirect('/test_card?log=' + log_id, status=303)
            return
        self.set_status(201)
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps({'log_id': log_id, 'stored': True}))

    def _validated_upload(self):
        """ parse the multipart body and return the validated CSV bytes """
        if self._body_too_large:
            raise CustomHTTPError(413, 'Test card exceeds {} KB'.format(MAX_CSV_SIZE // 1024))

        content_type = self.request.headers.get('Content-Type', '')
        if not content_type.startswith('multipart/form-data'):
            raise CustomHTTPError(400, 'Expected a multipart/form-data upload')
        arguments = {}
        files = {}
        parse_body_arguments(content_type, bytes(self._body), arguments, files,
                             self.request.headers)
        if UPLOAD_FIELD not in files or len(files[UPLOAD_FIELD]) != 1:
            raise CustomHTTPError(400, 'Expected exactly one file field "{}"'.format(
                UPLOAD_FIELD))
        upload = files[UPLOAD_FIELD][0]
        file_content_type = upload.content_type.split(';')[0].strip().lower()
        if file_content_type not in ALLOWED_CONTENT_TYPES:
            raise CustomHTTPError(415, 'Test card must be uploaded as text/csv')
        if len(upload.body) > MAX_CSV_SIZE:
            raise CustomHTTPError(413, 'Test card exceeds {} KB'.format(MAX_CSV_SIZE // 1024))

        try:
            parse_test_card_csv(upload.body)
        except TestCardError as exc:
            raise CustomHTTPError(400, 'Invalid test card: ' + str(exc)) from exc
        return upload.body

    @staticmethod
    def _write_atomically(path, data):
        directory = os.path.dirname(path)
        handle, tmp_path = tempfile.mkstemp(prefix='.testcard-', suffix='.tmp', dir=directory)
        try:
            with os.fdopen(handle, 'wb') as tmp_file:
                tmp_file.write(data)
            os.replace(tmp_path, path)
        except OSError:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            raise
