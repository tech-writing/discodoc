# -*- coding: utf-8 -*-
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import json
import logging
from docopt import docopt, DocoptExit

from discodoc import __appname__, __version__
from discodoc.core import DiscodocCommand
from discodoc.util import normalize_options, setup_logging

log = logging.getLogger(__name__)


def run():
    """
    discodoc creates documents from Discourse content easily

    Usage:
      vasuki <url> [--format=<format>] [--path=<output-path>] [--debug]
      vasuki --version
      vasuki (-h | --help)

    Options:
      --format=<format>                 Output format.
                                        Use any format of pandoc, e.g. pdf, epub. [Default: pdf]
      --path=<path>                     Output directory. Defaults to the current working directory.
      --version                         Show version information
      --debug                           Enable debug messages
      -h --help                         Show this screen

    Examples::

        discodoc --format=pdf https://community.hiveeyes.org/t/anleitung-aufbau-und-installation-des-sensor-kits-grune-platine/2443

    """

    name = '{__appname__} {__version__}'.format(**globals())

    # Parse command line arguments
    options = normalize_options(docopt(run.__doc__, version=name))

    # Setup logging
    debug = options.get('debug')
    log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
    setup_logging(log_level)

    # Debugging
    log.debug('Options: {}'.format(json.dumps(options, indent=4)))

    # Run command, optionally multiple times.
    command = DiscodocCommand(options)
    results = command.run()
