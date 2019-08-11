# -*- coding: utf-8 -*-
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import os
import sys
import shlex
import logging
import tempfile
import requests
import subprocess

log = logging.getLogger(__name__)


class DiscodocCommand:

    def __init__(self, options):
        self.options = options

    def run(self):

        if self.options.path is None:
            self.options.path = os.getcwd()

        if not os.path.isdir(self.options.path):
            raise KeyError('Output directory "{}" does not exist'.format(self.options.path))

        # Unique identifier generators
        #if self.options.format == 'pdf':
        discourse_to_document(self.options.url, format=self.options.format, output_path=self.options.path)

        #else:
        #    raise KeyError('Output format "{}" not implemented'.format(self.options.format))


def discourse_to_document(url, format=None, output_path=None):

    format = format or 'pdf'

    # Acquire posts from topic.
    url = url + '.json'
    response = requests.get(url)

    # Extract information.
    data = response.json()
    title = data['title']
    sections = []
    for post in data['post_stream']['posts']:
        sections.append(post['cooked'])

    # Debugging.
    #print(title); print(sections)

    log.info('Writing standalone file "{title}.{format}"'.format(**locals()))

    # By default, pandoc produces a document fragment. To produce a
    # standalone  document (e.g.  a valid HTML file including <head>
    # and <body>), use the --standalone flag.
    formatter = format
    if format == 'pdf':
        formatter = 'latex'

    output_file = '{title}.{format}'.format(**locals())
    if output_path is not None:
        output_file = os.path.join(output_path, output_file)

    command = 'pandoc --standalone --metadata title="{title}" --table-of-contents ' \
              '--from html --to {formatter} --output "{output_file}"'.format(**locals())
    log.info('Invoking command: %s', command)

    # Write sections to files.
    files = []
    filenames = []
    for section in sections:
        if not section:
            continue
        #f = tempfile.NamedTemporaryFile(suffix='.html', delete=False)
        f = tempfile.NamedTemporaryFile()
        f.write(section.encode('utf-8'))
        f.flush()
        files.append(f)
        filenames.append(f.name)

    # Run command.
    pargs = shlex.split(command)
    pargs.extend(filenames)

    try:
        outcome = subprocess.run(pargs, capture_output=True, timeout=60.0, check=True, encoding='utf-8')

    except Exception as ex:
        log.exception('Running pandoc failed, output was\nSTDOUT:\n{}\nSTDERR:\n{}\n'.format(ex.stdout, ex.stderr))


def main():
    url = sys.argv[1]
    try:
        format = sys.argv[2]
    except:
        format = None

    discourse_to_document(url, format=format)


if __name__ == '__main__':
    main()
