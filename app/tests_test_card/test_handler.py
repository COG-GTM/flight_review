""" handler-level tests for /test_card via Tornado's AsyncHTTPTestCase """
import csv
import json
import os
import shutil
import sqlite3
import tempfile
import unittest
import uuid

import tornado.web
from tornado.testing import AsyncHTTPTestCase

from tornado_handlers import test_card as handler_module
from tornado_handlers.test_card import MAX_BODY_SIZE, MAX_CSV_SIZE
from test_card import TEST_CARD_COLUMNS, TEST_CARD_FILE_SUFFIX
from ulog_gen import synthetic_flight

HEADER = ','.join(TEST_CARD_COLUMNS)
VALID_CARD = (HEADER + '\n'
              'TP-01,Climb,10,40,2.0,30,120,400\n'
              'TP-02,Pull-up,45,60,2.5,,,\n'
              'TP-05,Beyond end,130,140,,,,\n').encode()
BOUNDARY = 'testcardboundary'


def multipart(field, filename, content, content_type='text/csv', extra_fields=()):
    """ build a multipart/form-data body with a single file part (and optional
    plain form fields, as (name, value) pairs, in front of it) """
    body = ''
    for name, value in extra_fields:
        body += ('--{b}\r\nContent-Disposition: form-data; name="{n}"\r\n\r\n'
                 '{v}\r\n').format(b=BOUNDARY, n=name, v=value)
    body += ('--{b}\r\n'
             'Content-Disposition: form-data; name="{f}"; filename="{n}"\r\n'
             'Content-Type: {t}\r\n\r\n').format(b=BOUNDARY, f=field, n=filename, t=content_type)
    body = body.encode() + content + '\r\n--{}--\r\n'.format(BOUNDARY).encode()
    return body, 'multipart/form-data; boundary=' + BOUNDARY


def test_readme_documents_current_size_limit():
    """ the README states the upload limit; keep it in sync with the handler """
    readme = os.path.join(os.path.dirname(__file__), '..', '..', 'README.md')
    with open(readme, encoding='utf-8') as readme_file:
        assert 'max {} KB'.format(MAX_CSV_SIZE // 1024) in readme_file.read()


class TestCardHandlerTest(AsyncHTTPTestCase):
    """ exercises the handler against a temporary log directory and DB """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.log_dir = tempfile.mkdtemp(prefix='test_card_logs_')
        cls.db_file = os.path.join(cls.log_dir, 'logs.sqlite')
        cls.log_id = str(uuid.uuid4())
        cls.orphan_log_id = str(uuid.uuid4())  # in the DB, but no file on disk
        cls.unknown_log_id = str(uuid.uuid4())  # neither in the DB nor on disk
        synthetic_flight(os.path.join(cls.log_dir, cls.log_id + '.ulg'))
        con = sqlite3.connect(cls.db_file)
        with con:
            con.execute('create table Logs (Id TEXT PRIMARY KEY, Description TEXT)')
            con.execute('insert into Logs (Id, Description) values (?, ?)',
                        [cls.log_id, 'synthetic'])
            con.execute('insert into Logs (Id, Description) values (?, ?)',
                        [cls.orphan_log_id, 'orphan'])
        con.close()

        cls._originals = (handler_module.get_log_filepath, handler_module.get_log_filename,
                          handler_module.get_db_connection)
        handler_module.get_log_filepath = lambda: cls.log_dir
        handler_module.get_log_filename = lambda log_id: os.path.join(cls.log_dir,
                                                                      log_id + '.ulg')
        handler_module.get_db_connection = lambda: sqlite3.connect(cls.db_file)

    @classmethod
    def tearDownClass(cls):
        (handler_module.get_log_filepath, handler_module.get_log_filename,
         handler_module.get_db_connection) = cls._originals
        shutil.rmtree(cls.log_dir, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        super().setUp()
        card = os.path.join(self.log_dir, self.log_id + TEST_CARD_FILE_SUFFIX)
        if os.path.exists(card):
            os.remove(card)

    def get_app(self):
        return tornado.web.Application([(r'/test_card', handler_module.TestCardHandler)])

    def _post(self, log_id, body, content_type, accept='application/json'):
        return self.fetch('/test_card?log=' + log_id, method='POST', body=body,
                          headers={'Content-Type': content_type, 'Accept': accept})

    def _upload(self, log_id, content=VALID_CARD, **kwargs):
        body, content_type = multipart('testcard', 'card.csv', content, **kwargs)
        return self._post(log_id, body, content_type)

    def _card_path(self, log_id):
        return os.path.join(self.log_dir, log_id + TEST_CARD_FILE_SUFFIX)

    # --- 404 / invalid log id -------------------------------------------------

    def test_get_unknown_log_is_404(self):
        response = self.fetch('/test_card?log=' + self.unknown_log_id,
                              headers={'Accept': 'application/json'})
        self.assertEqual(response.code, 404)
        self.assertEqual(json.loads(response.body)['error'], 'Log not found')

    def test_get_log_in_db_without_file_is_404(self):
        response = self.fetch('/test_card?log=' + self.orphan_log_id,
                              headers={'Accept': 'application/json'})
        self.assertEqual(response.code, 404)

    def test_post_unknown_log_is_404_and_stores_nothing(self):
        response = self._upload(self.unknown_log_id)
        self.assertEqual(response.code, 404)
        self.assertFalse(os.path.exists(self._card_path(self.unknown_log_id)))

    def test_invalid_log_ids_are_rejected_before_any_path_is_built(self):
        for bad in ('..%2F..%2Fetc%2Fpasswd', 'not-a-uuid', self.log_id.upper(),
                    self.log_id.replace('-', ''), self.log_id + '.ulg', ''):
            response = self.fetch('/test_card?log=' + bad, headers={'Accept': 'application/json'})
            self.assertEqual(response.code, 400, bad)
            self.assertEqual(json.loads(response.body)['error'], 'Invalid log id')
            response = self._upload(bad)
            self.assertEqual(response.code, 400, bad)
        response = self.fetch('/test_card', headers={'Accept': 'application/json'})
        self.assertEqual(response.code, 400)
        self.assertEqual(os.listdir(self.log_dir).count('..'), 0)

    def test_html_error_is_escaped(self):
        response = self.fetch('/test_card?log=%3Cscript%3E', headers={'Accept': 'text/html'})
        self.assertEqual(response.code, 400)
        self.assertIn(b'Invalid log id', response.body)
        self.assertNotIn(b'<script>', response.body)

    # --- upload validation ----------------------------------------------------

    def test_oversized_csv_is_rejected(self):
        big = HEADER.encode() + b'\n' + b'TP-01,' + b'x' * MAX_CSV_SIZE + b',0,1,,,,\n'
        response = self._upload(self.log_id, big)
        self.assertEqual(response.code, 413)
        self.assertIn('256 KB', json.loads(response.body)['error'])
        self.assertFalse(os.path.exists(self._card_path(self.log_id)))

    def test_csv_just_over_the_limit_is_rejected(self):
        # a valid card padded with comment-free blank lines to MAX_CSV_SIZE + 1 bytes
        content = VALID_CARD + b'\n' * (MAX_CSV_SIZE + 1 - len(VALID_CARD))
        self.assertEqual(len(content), MAX_CSV_SIZE + 1)
        response = self._upload(self.log_id, content)
        self.assertEqual(response.code, 413)
        self.assertFalse(os.path.exists(self._card_path(self.log_id)))

    def test_csv_at_the_limit_is_accepted(self):
        content = VALID_CARD + b'\n' * (MAX_CSV_SIZE - len(VALID_CARD))
        self.assertEqual(len(content), MAX_CSV_SIZE)
        response = self._upload(self.log_id, content)
        self.assertEqual(response.code, 201)
        self.assertTrue(os.path.exists(self._card_path(self.log_id)))

    def test_csv_at_the_limit_with_large_multipart_framing_is_accepted(self):
        # the CSV limit applies to the CSV part only: a long file name and
        # extra form fields (> 4 KB of framing) must not cause a rejection
        content = VALID_CARD + b'\n' * (MAX_CSV_SIZE - len(VALID_CARD))
        body, content_type = multipart('testcard', 'x' * 2048 + '.csv', content,
                                       extra_fields=[('note', 'y' * 3000)])
        self.assertGreater(len(body), MAX_CSV_SIZE + 4 * 1024)
        response = self._post(self.log_id, body, content_type)
        self.assertEqual(response.code, 201)
        self.assertTrue(os.path.exists(self._card_path(self.log_id)))

    def test_whole_body_is_still_bounded(self):
        # a small CSV wrapped in an oversized multipart body is rejected
        body, content_type = multipart('testcard', 'card.csv', VALID_CARD,
                                       extra_fields=[('note', 'y' * MAX_BODY_SIZE)])
        response = self._post(self.log_id, body, content_type)
        self.assertEqual(response.code, 413)
        self.assertFalse(os.path.exists(self._card_path(self.log_id)))

    def test_wrong_content_type_is_rejected(self):
        response = self._upload(self.log_id, content_type='application/octet-stream')
        self.assertEqual(response.code, 415)
        self.assertFalse(os.path.exists(self._card_path(self.log_id)))

    def test_non_multipart_body_is_rejected(self):
        response = self._post(self.log_id, VALID_CARD, 'text/csv')
        self.assertEqual(response.code, 400)

    def test_wrong_field_name_is_rejected(self):
        body, content_type = multipart('file', 'card.csv', VALID_CARD)
        response = self._post(self.log_id, body, content_type)
        self.assertEqual(response.code, 400)
        self.assertIn('testcard', json.loads(response.body)['error'])

    def test_bad_header_is_rejected(self):
        response = self._upload(self.log_id, b'id,start,end\n1,0,1\n')
        self.assertEqual(response.code, 400)
        self.assertIn('invalid header', json.loads(response.body)['error'])
        self.assertFalse(os.path.exists(self._card_path(self.log_id)))

    def test_malformed_row_is_rejected_with_line_number(self):
        response = self._upload(self.log_id, HEADER.encode() + b'\nTP-01,x,10,5,,,,\n')
        self.assertEqual(response.code, 400)
        self.assertIn('line 2', json.loads(response.body)['error'])

    def test_field_above_csv_parser_limit_is_a_validation_error(self):
        # size-compliant body, but one field larger than csv.field_size_limit()
        content = HEADER.encode() + b'\nTP-01,' + b'x' * (csv.field_size_limit() + 1) + b',10,20,,,,\n'
        self.assertLess(len(content), MAX_CSV_SIZE)
        response = self._upload(self.log_id, content)
        self.assertEqual(response.code, 400)
        self.assertIn('malformed CSV', json.loads(response.body)['error'])
        self.assertFalse(os.path.exists(self._card_path(self.log_id)))

    def test_malformed_upload_does_not_replace_existing_card(self):
        self.assertEqual(self._upload(self.log_id).code, 201)
        self.assertEqual(self._upload(self.log_id, b'garbage').code, 400)
        with open(self._card_path(self.log_id), 'rb') as stored:
            self.assertEqual(stored.read(), VALID_CARD)

    def test_browser_upload_error_renders_page(self):
        body, content_type = multipart('testcard', 'card.csv', b'garbage')
        response = self._post(self.log_id, body, content_type, accept='text/html')
        self.assertEqual(response.code, 400)
        self.assertIn(b'invalid header', response.body)
        self.assertIn(b'<form', response.body)

    # --- happy path -----------------------------------------------------------

    def test_get_without_card(self):
        response = self.fetch('/test_card?log=' + self.log_id,
                              headers={'Accept': 'application/json'})
        self.assertEqual(response.code, 404)
        self.assertIn('No test card', json.loads(response.body)['error'])

        response = self.fetch('/test_card?log=' + self.log_id, headers={'Accept': 'text/html'})
        self.assertEqual(response.code, 200)
        self.assertIn(b'<form', response.body)
        self.assertIn(HEADER.encode(), response.body)

    def test_upload_then_get_json(self):
        response = self._upload(self.log_id)
        self.assertEqual(response.code, 201)
        self.assertEqual(json.loads(response.body), {'log_id': self.log_id, 'stored': True})
        with open(self._card_path(self.log_id), 'rb') as stored:
            self.assertEqual(stored.read(), VALID_CARD)

        response = self.fetch('/test_card?log=' + self.log_id,
                              headers={'Accept': 'application/json'})
        self.assertEqual(response.code, 200)
        self.assertTrue(response.headers['Content-Type'].startswith('application/json'))
        self.assertEqual(response.headers['X-Content-Type-Options'], 'nosniff')
        results = json.loads(response.body)
        self.assertEqual(results['log_id'], self.log_id)
        self.assertEqual(results['log_duration_s'], 120.0)
        points = {p['test_point_id']: p for p in results['test_points']}
        self.assertEqual(list(points), ['TP-01', 'TP-02', 'TP-05'])
        self.assertEqual(points['TP-01']['status'], 'COMPLETE')
        self.assertEqual(points['TP-02']['status'], 'COMPLETE WITH EXCEEDANCE')
        self.assertEqual(points['TP-02']['exceedances'][0]['limit'], 'nz_max_g')
        self.assertAlmostEqual(points['TP-02']['metrics']['nz_peak_g'], 3.2, places=5)
        self.assertEqual(points['TP-05']['status'], 'NO DATA')

    def test_format_json_query_overrides_accept(self):
        self._upload(self.log_id)
        response = self.fetch('/test_card?log={}&format=json'.format(self.log_id),
                              headers={'Accept': 'text/html'})
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body)['log_id'], self.log_id)

    def test_upload_then_get_html(self):
        self._upload(self.log_id)
        response = self.fetch('/test_card?log=' + self.log_id,
                              headers={'Accept': 'text/html,application/xhtml+xml'})
        self.assertEqual(response.code, 200)
        self.assertTrue(response.headers['Content-Type'].startswith('text/html'))
        self.assertEqual(response.headers['X-Frame-Options'], 'DENY')
        html = response.body.decode()
        for expected in ('TP-01', 'TP-02', 'TP-05', 'COMPLETE WITH EXCEEDANCE', 'NO DATA',
                         'plot_app?log=' + self.log_id, 'format=json'):
            self.assertIn(expected, html)

    def test_default_browser_navigation_returns_html(self):
        self._upload(self.log_id)
        response = self.fetch('/test_card?log=' + self.log_id)
        self.assertEqual(response.code, 200)
        self.assertTrue(response.headers['Content-Type'].startswith('text/html'))

    def test_browser_upload_redirects_to_results_page(self):
        body, content_type = multipart('testcard', 'card.csv', VALID_CARD)
        response = self._post(self.log_id, body, content_type, accept='text/html')
        self.assertEqual(response.code, 200)  # after following the 303 redirect
        self.assertIn(b'TP-02', response.body)

    def test_html_output_escapes_description(self):
        card = HEADER.encode() + b'\nTP-01,<b onclick="x">bold</b>,10,40,,,,\n'
        self.assertEqual(self._upload(self.log_id, card).code, 201)
        response = self.fetch('/test_card?log=' + self.log_id, headers={'Accept': 'text/html'})
        self.assertNotIn(b'<b onclick', response.body)
        self.assertIn(b'&lt;b onclick=', response.body)


if __name__ == '__main__':
    unittest.main()
