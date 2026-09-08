""" keep the outcome totals in docs/security/asd-stig-nist-800-53-review.md
in sync with its findings table """
import os
import re

DOC_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    '../../docs/security/asd-stig-nist-800-53-review.md'
)
OUTCOMES = ('satisfied', 'not-satisfied', 'needs-input', 'not-applicable')
BOUNDARIES = {'B%d' % i for i in range(1, 14)}


def _read_doc():
    with open(DOC_PATH, encoding='utf-8') as doc_file:
        return doc_file.read()


def _findings_rows(text):
    """ (id, boundary, outcome) for every row of the findings table """
    rows = []
    for line in text.splitlines():
        match = re.match(r'^\| (F-\d\d) \| (B\d+(?:/B\d+)*) \|', line)
        if match is None:
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        outcome = cells[8].split(' ')[0]
        assert outcome in OUTCOMES, line
        rows.append((match.group(1), match.group(2), outcome))
    return rows


def _totals_rows(text):
    """ {outcome: (count, [ids])} from the outcome totals table """
    totals = {}
    for line in text.splitlines():
        match = re.match(r'^\| (%s) \| (\d+) \| (.*) \|$' % '|'.join(OUTCOMES), line)
        if match is None:
            continue
        ids = re.findall(r'F-\d\d', match.group(3).split('(')[0])
        totals[match.group(1)] = (int(match.group(2)), ids)
    return totals


def test_doc_exists():
    """ the assessment document is part of the repository """
    assert os.path.isfile(DOC_PATH)


def test_every_finding_has_one_outcome():
    """ each row carries exactly one of the four outcomes """
    rows = _findings_rows(_read_doc())
    assert len(rows) > 0
    ids = [row[0] for row in rows]
    assert len(ids) == len(set(ids))


def test_totals_match_findings_table():
    """ counts and id lists in the totals table equal the findings table """
    text = _read_doc()
    rows = _findings_rows(text)
    totals = _totals_rows(text)
    assert set(totals) == set(OUTCOMES)
    for outcome in OUTCOMES:
        expected_ids = sorted(fid for fid, _, out in rows if out == outcome)
        count, listed_ids = totals[outcome]
        assert count == len(expected_ids), outcome
        assert sorted(listed_ids) == expected_ids, outcome
    assert sum(count for count, _ in totals.values()) == len(rows)


def test_every_boundary_has_an_outcome():
    """ B1..B13 each appear in at least one findings row """
    rows = _findings_rows(_read_doc())
    assert len(rows) == 28
    covered = set()
    for _, boundary, _ in rows:
        covered.update(boundary.split('/'))
    assert BOUNDARIES <= covered, BOUNDARIES - covered
