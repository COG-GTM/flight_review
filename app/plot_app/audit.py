"""
Structured audit records for security-relevant events (upload accepted or
rejected, log deleted, edit token failure, download of a private log, ...).

One JSON object per line via the standard logging module; no external sink.
"""
import datetime
import json
import logging
import sys
import uuid

AUDIT_LOGGER_NAME = 'flight_review.audit'
ERROR_LOGGER_NAME = 'flight_review.error'


_CONFIGURED_LOGGERS = set()


def _get_logger(name):
    """ logger that always has a stream handler, independent of how the
    hosting process (bokeh server) configured the root logger """
    logger = logging.getLogger(name)
    if name not in _CONFIGURED_LOGGERS:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False
        _CONFIGURED_LOGGERS.add(name)
    return logger


def build_audit_record(event, outcome, **fields):
    """ build the audit record dict: timestamp, event, outcome + fields.
    Values are stringified if not JSON-serializable. """
    record = {
        'timestamp': datetime.datetime.now(datetime.timezone.utc)
                     .isoformat(timespec='milliseconds'),
        'event': str(event),
        'outcome': str(outcome),
    }
    for key, value in fields.items():
        if value is None:
            continue
        record[key] = value
    return record


def audit_log(event, outcome, **fields):
    """ emit one JSON line for a security-relevant event
    :param event: e.g. 'upload', 'log_delete', 'log_download'
    :param outcome: 'success' or 'failure'
    :param fields: additional context (log_id, client_ip, reason, ...);
                   never pass secrets (tokens, keys) here
    """
    record = build_audit_record(event, outcome, **fields)
    _get_logger(AUDIT_LOGGER_NAME).info(json.dumps(record, sort_keys=True, default=str))


def new_correlation_id():
    """ short opaque id that ties a user-facing error to a server-side log entry """
    return uuid.uuid4().hex[:12]


def log_server_error(correlation_id, message, exc_info=None):
    """ record exception detail server-side only """
    _get_logger(ERROR_LOGGER_NAME).error(
        '[%s] %s', correlation_id, message, exc_info=exc_info)
