""" tests for the test card CSV parser """
import csv
import os

import pytest

import test_card as reduction  # the pure module plot_app/test_card.py
from test_card import TEST_CARD_COLUMNS, is_valid_log_uuid, parse_test_card_csv

HEADER = ','.join(TEST_CARD_COLUMNS)


def _csv(*rows):
    return '\n'.join((HEADER,) + rows) + '\n'


def test_header_matches_documented_columns():
    assert HEADER == ('test_point_id,description,start_s,end_s,'
                      'nz_max_g,airspeed_max_mps,alt_min_m,alt_max_m')
    readme = os.path.join(os.path.dirname(__file__), '..', '..', 'README.md')
    with open(readme, encoding='utf-8') as readme_file:
        assert HEADER + '\n' in readme_file.read()


def test_parse_valid_card():
    points = parse_test_card_csv(_csv(
        'TP-01,Climb,10,40,2.0,30,120,400',
        'TP-02,"Pull-up, symmetric",45,60,,,,',
        '',
    ))
    assert [p['test_point_id'] for p in points] == ['TP-01', 'TP-02']
    assert points[0]['description'] == 'Climb'
    assert points[0]['start_s'] == 10.0 and points[0]['end_s'] == 40.0
    assert points[0]['nz_max_g'] == 2.0
    assert points[0]['airspeed_max_mps'] == 30.0
    assert points[0]['alt_min_m'] == 120.0 and points[0]['alt_max_m'] == 400.0
    assert points[1]['description'] == 'Pull-up, symmetric'
    for limit in ('nz_max_g', 'airspeed_max_mps', 'alt_min_m', 'alt_max_m'):
        assert points[1][limit] is None


def test_parse_accepts_bytes_with_bom_and_crlf():
    data = ('\ufeff' + HEADER + '\r\nTP-01,x,0,1,,,,\r\n').encode('utf-8')
    points = parse_test_card_csv(data)
    assert len(points) == 1


@pytest.mark.parametrize('header', [
    'test_point_id,description,start_s,end_s',
    'id,description,start_s,end_s,nz_max_g,airspeed_max_mps,alt_min_m,alt_max_m',
    'description,test_point_id,start_s,end_s,nz_max_g,airspeed_max_mps,alt_min_m,alt_max_m',
    HEADER + ',extra',
])
def test_strict_header(header):
    with pytest.raises(reduction.TestCardError, match='invalid header'):
        parse_test_card_csv(header + '\nTP-01,x,0,1,,,,\n')


def test_empty_file():
    with pytest.raises(reduction.TestCardError, match='empty'):
        parse_test_card_csv('')


def test_header_only():
    with pytest.raises(reduction.TestCardError, match='no test points'):
        parse_test_card_csv(HEADER + '\n')


@pytest.mark.parametrize('row', [
    'TP-01,x,0,1',
    'TP-01,x,0,1,,,',
    'TP-01,x,0,1,,,,,',
])
def test_wrong_field_count(row):
    with pytest.raises(reduction.TestCardError, match='line 2: expected 8 fields'):
        parse_test_card_csv(_csv(row))


@pytest.mark.parametrize('row, column', [
    ('TP-01,x,abc,1,,,,', 'start_s'),
    ('TP-01,x,0,1s,,,,', 'end_s'),
    ('TP-01,x,,1,,,,', 'start_s'),
    ('TP-01,x,0,,,,,', 'end_s'),
    ('TP-01,x,0,1,nan,,,', 'nz_max_g'),
    ('TP-01,x,0,1,,inf,,', 'airspeed_max_mps'),
    ('TP-01,x,0,1,,,low,', 'alt_min_m'),
])
def test_non_numeric_values(row, column):
    with pytest.raises(reduction.TestCardError, match='line 2: {}'.format(column)):
        parse_test_card_csv(_csv(row))


@pytest.mark.parametrize('row', [
    'TP-01,x,10,10,,,,',
    'TP-01,x,10,5,,,,',
])
def test_end_must_be_after_start(row):
    with pytest.raises(reduction.TestCardError, match='end_s must be greater than start_s'):
        parse_test_card_csv(_csv(row))


def test_negative_start():
    with pytest.raises(reduction.TestCardError, match='start_s must be >= 0'):
        parse_test_card_csv(_csv('TP-01,x,-1,5,,,,'))


def test_altitude_band_order():
    with pytest.raises(reduction.TestCardError, match='alt_max_m must be greater'):
        parse_test_card_csv(_csv('TP-01,x,0,5,,,200,100'))


def test_duplicate_test_point_id():
    with pytest.raises(reduction.TestCardError, match='duplicate test_point_id'):
        parse_test_card_csv(_csv('TP-01,x,0,5,,,,', 'TP-01,y,5,10,,,,'))


@pytest.mark.parametrize('test_point_id', ['', ' ', 'a b', '<script>', 'x' * 33, '-TP'])
def test_invalid_test_point_id(test_point_id):
    with pytest.raises(reduction.TestCardError, match='test_point_id'):
        parse_test_card_csv(_csv('{},x,0,5,,,,'.format(test_point_id)))


def test_error_reports_correct_line_number():
    with pytest.raises(reduction.TestCardError, match='line 4'):
        parse_test_card_csv(_csv('TP-01,x,0,5,,,,', 'TP-02,x,5,10,,,,', 'TP-03,x,10,bad,,,,'))


def test_invalid_utf8():
    with pytest.raises(reduction.TestCardError, match='UTF-8'):
        parse_test_card_csv(HEADER.encode() + b'\nTP-01,\xff\xfe,0,1,,,,\n')


def test_field_above_csv_parser_limit_is_a_test_card_error():
    huge = 'x' * (csv.field_size_limit() + 1)
    with pytest.raises(reduction.TestCardError, match='line 3: malformed CSV'):
        parse_test_card_csv(_csv('TP-01,x,0,5,,,,', 'TP-02,' + huge + ',5,10,,,,'))
    with pytest.raises(reduction.TestCardError, match='line 1: malformed CSV'):
        parse_test_card_csv(huge + ',' + HEADER + '\n')


@pytest.mark.parametrize('log_id, valid', [
    ('f2f80d26-de4e-45d1-97b4-7e750bdc42b2', True),
    ('F2F80D26-DE4E-45D1-97B4-7E750BDC42B2', False),
    ('f2f80d26de4e45d197b47e750bdc42b2', False),
    ('../f2f80d26-de4e-45d1-97b4-7e750bdc42b2', False),
    ('f2f80d26-de4e-45d1-97b4-7e750bdc42b2/../x', False),
    ('', False),
    (None, False),
])
def test_log_uuid_allow_list(log_id, valid):
    assert is_valid_log_uuid(log_id) is valid


def test_card_path_rejects_non_uuid():
    with pytest.raises(reduction.TestCardError):
        reduction.test_card_filename('/logs', '../etc/passwd')
    assert reduction.test_card_filename('/logs', 'f2f80d26-de4e-45d1-97b4-7e750bdc42b2') == \
        '/logs/f2f80d26-de4e-45d1-97b4-7e750bdc42b2.testcard.csv'
