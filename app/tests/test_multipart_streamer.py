"""Tests for MultiPartStreamer header parsing limits and complexity."""
import os
import sys
import time

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# pylint: disable=wrong-import-position
from tornado_handlers.multipart_streamer import MultiPartStreamer, ParseError  # noqa: E402


class MemoryPart:
    """Collects part data in memory."""
    def __init__(self, headers):
        self.headers = headers
        self.data = b""
        self._size = 0

    def feed(self, data):
        """append data"""
        self.data += data

    def finalize(self):
        """nothing to do"""

    def release(self):
        """nothing to do"""

    def get_payload(self):
        """return data"""
        return self.data


class MemoryStreamer(MultiPartStreamer):
    """Streamer that keeps parts in memory."""
    def create_part(self, headers):
        return MemoryPart(headers)

    def _begin_part(self, headers):
        if len(self.parts) >= self.MAX_PARTS:
            raise ParseError("Too many multipart parts")
        self.part = self.create_part(headers)
        self.parts.append(self.part)


BOUNDARY = b"----WebKitFormBoundaryabc123"


def build_body(parts):
    """parts: list of (headers_bytes_list, data)"""
    body = b""
    for headers, data in parts:
        body += b"--" + BOUNDARY + b"\r\n"
        for hdr in headers:
            body += hdr + b"\r\n"
        body += b"\r\n" + data + b"\r\n"
    body += b"--" + BOUNDARY + b"--\r\n"
    return body


def feed(body, chunk_size=None):
    """feed body into a MemoryStreamer and return it"""
    streamer = MemoryStreamer(len(body))
    if chunk_size is None:
        streamer.data_received(body)
    else:
        for i in range(0, len(body), chunk_size):
            streamer.data_received(body[i:i + chunk_size])
    streamer.data_complete()
    return streamer


@pytest.mark.parametrize("chunk_size", [None, 1, 7, 64])
def test_parses_browser_style_form(chunk_size):
    """normal browser upload parses correctly regardless of chunking"""
    body = build_body([
        ([b'Content-Disposition: form-data; name="description"'], b"hello world"),
        ([b'Content-Disposition: form-data; name="filelog"; filename="log.ulg"',
          b'Content-Type: application/octet-stream'], b"\x00\x01\x02ULog\r\ndata\r\n--not-a-boundary"),
    ])
    streamer = feed(body, chunk_size)
    assert len(streamer.parts) == 2
    desc, log = streamer.parts
    assert desc.headers[0]["name"] == "Content-Disposition"
    assert desc.headers[0]["value"] == "form-data"
    assert desc.headers[0]["params"] == {"name": "description"}
    assert desc.get_payload() == b"hello world"
    assert log.headers[0]["params"] == {"name": "filelog", "filename": "log.ulg"}
    assert log.headers[1]["name"] == "Content-Type"
    assert log.headers[1]["value"] == "application/octet-stream"
    assert log.get_payload() == b"\x00\x01\x02ULog\r\ndata\r\n--not-a-boundary"


def test_parse_header_params():
    """parameter parsing keeps all params and stops at first non-matching tail"""
    streamer = MemoryStreamer(0)
    hdr = streamer._parse_header(  # pylint: disable=protected-access
        b'Content-Disposition: form-data; name="a"; filename="b c.txt"; x="" garbage')
    assert hdr["params"] == {"name": "a", "filename": "b c.txt", "x": ""}
    assert streamer._parse_header(b'no colon here') == {"value": "no colon here"}  # pylint: disable=protected-access


def test_header_line_too_long_rejected():
    """a header line over the cap raises ParseError before parsing it"""
    long_hdr = b'Content-Disposition: form-data' + b'; a=""' * 20000
    body = build_body([([long_hdr], b"x")])
    with pytest.raises(ParseError):
        feed(body, 1024)


def test_header_line_without_crlf_rejected_early():
    """an unterminated header line is rejected once it exceeds the cap"""
    streamer = MemoryStreamer(0)
    streamer.data_received(b"--" + BOUNDARY + b"\r\n")
    with pytest.raises(ParseError):
        for _ in range(100):
            streamer.data_received(b"a" * 1024)


def test_too_many_headers_rejected():
    """more than MAX_HEADERS_PER_PART header lines raises ParseError"""
    headers = [b"X-H%d: v" % i for i in range(MultiPartStreamer.MAX_HEADERS_PER_PART + 1)]
    body = build_body([(headers, b"x")])
    with pytest.raises(ParseError):
        feed(body)


def test_max_headers_allowed():
    """exactly MAX_HEADERS_PER_PART header lines is accepted"""
    headers = [b"X-H%d: v" % i for i in range(MultiPartStreamer.MAX_HEADERS_PER_PART)]
    streamer = feed(build_body([(headers, b"x")]))
    assert len(streamer.parts[0].headers) == MultiPartStreamer.MAX_HEADERS_PER_PART


def test_too_many_parts_rejected():
    """more than MAX_PARTS parts raises ParseError"""
    parts = [([b'Content-Disposition: form-data; name="f%d"' % i], b"v")
             for i in range(MultiPartStreamer.MAX_PARTS + 1)]
    with pytest.raises(ParseError):
        feed(build_body(parts))


def test_parse_header_is_linear():
    """doubling header size should not quadruple parse time"""
    streamer = MemoryStreamer(0)
    streamer.MAX_HEADER_LINE_LENGTH = 10 ** 9  # measure the parser alone
    timings = []
    for size in (200_000, 400_000, 800_000):
        hdr = b'a: b' + b'; a=""' * (size // 6)
        start = time.perf_counter()
        streamer._parse_header(hdr)  # pylint: disable=protected-access
        timings.append(time.perf_counter() - start)
    # quadratic would give ~16x between first and last; allow generous slack
    assert timings[2] < timings[0] * 10


def test_param_regex_no_catastrophic_backtracking():
    """'; ' followed by many spaces and no '=' must be rejected quickly"""
    streamer = MemoryStreamer(0)
    streamer.MAX_HEADER_LINE_LENGTH = 10 ** 9
    hdr = b'a: b;' + b' ' * 200_000
    start = time.perf_counter()
    streamer._parse_header(hdr)  # pylint: disable=protected-access
    assert time.perf_counter() - start < 1.0


@pytest.mark.parametrize("hdr_len", [MultiPartStreamer.MAX_HEADER_LINE_LENGTH - 1,
                                     MultiPartStreamer.MAX_HEADER_LINE_LENGTH])
def test_max_length_header_accepted_with_split_crlf(hdr_len):
    """a header at the cap is accepted even when CRLF is split across chunks"""
    hdr = b'X-H: ' + b'v' * (hdr_len - 5)
    assert len(hdr) == hdr_len
    body = build_body([([hdr], b"x")])
    # split right between \r and \n of the header's terminator
    split = body.index(hdr) + len(hdr) + 1
    streamer = MemoryStreamer(len(body))
    streamer.data_received(body[:split])
    streamer.data_received(body[split:])
    streamer.data_complete()
    assert len(streamer.parts[0].headers[0]["value"]) == hdr_len - 5


def test_header_one_over_cap_rejected():
    """one byte over the cap is rejected"""
    hdr = b'X-H: ' + b'v' * (MultiPartStreamer.MAX_HEADER_LINE_LENGTH - 4)
    with pytest.raises(ParseError):
        feed(build_body([([hdr], b"x")]), 1)


def test_temporary_part_release_is_idempotent(tmp_path):
    """release() may be called twice (data_received failure + on_connection_close)"""
    from tornado_handlers.multipart_streamer import TemporaryFileStreamedPart  # pylint: disable=import-outside-toplevel
    part = TemporaryFileStreamedPart(None, [], tmp_dir=str(tmp_path))
    part.feed(b"data")
    part.finalize()
    assert os.path.exists(part.f_out.name)
    part.release()
    assert not os.path.exists(part.f_out.name)
    part.release()
