""" tests for temporary-file cleanup of interrupted multipart uploads """
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                '../tornado_handlers'))
#pylint: disable=wrong-import-position
from multipart_streamer import MultiPartStreamer, TemporaryFileStreamedPart

BOUNDARY = b'----boundary'


def _part_header(name, filename=None):
    disposition = 'form-data; name="%s"' % name
    if filename is not None:
        disposition += '; filename="%s"' % filename
    return (b'--' + BOUNDARY + b'\r\n'
            b'Content-Disposition: ' + disposition.encode() + b'\r\n\r\n')


def _temp_files(streamer):
    return [part.f_out.name for part in streamer.parts
            if isinstance(part, TemporaryFileStreamedPart)]


def test_release_removes_files_of_interrupted_stream():
    """ a body that stops mid-part (client abort / size limit) must not leave
    temporary files behind once release_parts() runs """
    body = (_part_header('description') + b'hello\r\n' +
            _part_header('filearg', 'log.ulg') + b'ULog\x01\x12\x35' + b'x' * 1000)
    streamer = MultiPartStreamer(len(body) + 5000) # Content-Length overstates
    streamer.data_received(body[:len(body) // 2])
    streamer.data_received(body[len(body) // 2:])
    # no data_complete(): the stream was cut off
    files = _temp_files(streamer)
    assert len(files) == 2
    assert all(os.path.exists(f) for f in files)

    streamer.release_parts()
    assert not any(os.path.exists(f) for f in files)


def test_release_parts_is_idempotent():
    """ calling release twice (post() finally + on_finish/on_connection_close)
    must not raise """
    body = _part_header('filearg', 'log.ulg') + b'abc\r\n--' + BOUNDARY + b'--\r\n'
    streamer = MultiPartStreamer(len(body))
    streamer.data_received(body)
    streamer.data_complete()
    files = _temp_files(streamer)
    assert len(files) == 1

    streamer.release_parts()
    streamer.release_parts()
    assert not os.path.exists(files[0])
    assert streamer.parts[0].is_released


def test_release_keeps_moved_file(tmp_path):
    """ a part moved into log storage is not deleted by release """
    body = _part_header('filearg', 'log.ulg') + b'abc\r\n--' + BOUNDARY + b'--\r\n'
    streamer = MultiPartStreamer(len(body))
    streamer.data_received(body)
    streamer.data_complete()
    part = streamer.get_parts_by_name('filearg')[0]
    target = str(tmp_path / 'stored.ulg')
    part.move(target)

    streamer.release_parts()
    streamer.release_parts()
    assert os.path.exists(target)
    with open(target, 'rb') as stored:
        assert stored.read() == b'abc'


def test_release_retries_after_failed_unlink(monkeypatch):
    """ a transient unlink failure must not mark the part released: the next
    release() call deletes the file """
    body = _part_header('filearg', 'log.ulg') + b'abc\r\n--' + BOUNDARY + b'--\r\n'
    streamer = MultiPartStreamer(len(body))
    streamer.data_received(body)
    streamer.data_complete()
    part = streamer.parts[0]
    real_unlink = os.unlink
    calls = []

    def _flaky_unlink(path):
        calls.append(path)
        if len(calls) == 1:
            raise PermissionError('busy')
        real_unlink(path)
    monkeypatch.setattr(os, 'unlink', _flaky_unlink)

    with pytest.raises(OSError):
        streamer.release_parts()
    assert not part.is_released
    assert os.path.exists(part.f_out.name)

    streamer.release_parts()
    assert part.is_released
    assert not os.path.exists(part.f_out.name)
    assert len(calls) == 2


def test_release_treats_missing_file_as_released():
    """ a temporary file already removed by someone else is not an error """
    body = _part_header('filearg', 'log.ulg') + b'abc\r\n--' + BOUNDARY + b'--\r\n'
    streamer = MultiPartStreamer(len(body))
    streamer.data_received(body)
    streamer.data_complete()
    part = streamer.parts[0]
    part.f_out.close()
    os.unlink(part.f_out.name)

    streamer.release_parts()
    assert part.is_released


def test_release_parts_attempts_every_part(monkeypatch):
    """ one failing part does not stop the others from being released """
    body = (_part_header('description') + b'hello\r\n' +
            _part_header('filearg', 'log.ulg') + b'abc\r\n--' + BOUNDARY + b'--\r\n')
    streamer = MultiPartStreamer(len(body))
    streamer.data_received(body)
    streamer.data_complete()
    files = _temp_files(streamer)
    assert len(files) == 2
    real_unlink = os.unlink

    def _fail_first(path):
        if path == files[0]:
            raise PermissionError('busy')
        real_unlink(path)
    monkeypatch.setattr(os, 'unlink', _fail_first)

    with pytest.raises(OSError):
        streamer.release_parts()
    assert os.path.exists(files[0])
    assert not os.path.exists(files[1])
    monkeypatch.undo()
    streamer.release_parts()
    assert not os.path.exists(files[0])
