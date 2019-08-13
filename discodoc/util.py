# -*- coding: utf-8 -*-
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import sys
import logging
import tempfile
from datetime import datetime

from munch import munchify
from rfc3339 import rfc3339

log = logging.getLogger(__name__)


def setup_logging(level=logging.INFO):
    log_format = '%(asctime)-15s [%(name)-13s] %(levelname)-7s: %(message)s'
    logging.basicConfig(
        format=log_format,
        stream=sys.stderr,
        level=level)


def configure_http_logging(options):
    # Control debug logging of HTTP requests.

    if options.http_logging:
        log_level = log.getEffectiveLevel()
    else:
        log_level = logging.WARNING

    requests_log = logging.getLogger('requests')
    requests_log.setLevel(log_level)

    requests_log = logging.getLogger('urllib3.connectionpool')
    requests_log.setLevel(log_level)


def normalize_options(options):
    normalized = {}
    for key, value in options.items():

        # Add primary variant.
        key = key.strip('--<>')
        normalized[key] = value

        # Add secondary variant.
        key = key.replace('-', '_')
        normalized[key] = value

    return munchify(normalized)


def tempfile_items(items):
    # Write each fragment to a temporary file.
    tempfiles = []
    filenames = []
    for item in items:
        if not item:
            continue
        f = tempfile.NamedTemporaryFile(delete=True)
        f.write(item.encode('utf-8'))
        f.flush()
        tempfiles.append(f)
        filenames.append(f.name)

    return tempfiles


def now_rfc3339():
    return rfc3339(datetime.utcnow(), utc=True, use_system_timezone=False)
