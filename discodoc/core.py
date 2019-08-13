# -*- coding: utf-8 -*-
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import os
import shlex
import logging
import tempfile
from pprint import pprint

import requests
import subprocess
from munch import munchify

from discodoc.util import tempfile_items, now_rfc3339

log = logging.getLogger(__name__)


class DiscourseTopic:

    def __init__(self, url, headers=None):
        self.url = url
        self.headers = headers or {}
        self.data = None
        self.fragments = None

    def fetch(self):

        # Acquire all posts from topic.
        # Remark: The ``print=true`` option will return up to 1000 posts in a topic.
        # API Documentation: https://docs.discourse.org/#tag/Topics%2Fpaths%2F~1t~1%7Bid%7D.json%2Fget
        url = '{}.json?include_raw=true&print=true'.format(self.url)
        response = requests.get(url, headers=self.headers)

        try:
            response.raise_for_status()
        except:
            log.exception('Failed requesting URL "{}". The response was:\n{}\n\n'.format(url, response.text))
            raise

        # Extract information.
        data = response.json()
        log.info('Collecting posts from topic #{id} "{title}" created at {created_at}'.format(**data))

        posts = []

        # Debugging
        # pprint(data)

        for post in data['post_stream']['posts']:

            if post.get('post_type') == 4:
                log.info('Skipping whisper post number {post_number}'.format(**post))
                continue

            abstract = post['raw'][:50].replace('\n', ' ')
            log.info('Collecting post number {post_number} from topic {topic_id} '
                     'created at {created_at} "{abstract}..."'.format(**post, abstract=abstract))

            posts.append(post['cooked'])

        self.data = data
        self.fragments = posts

    def write_temporary_files(self):
        return tempfile_items(self.fragments)


class DiscodocCommand:

    def __init__(self, options):
        self.options = options
        self.headers = {}

    def setup(self):
        """
        Run sanity checks and apply configuration defaults.
        """

        # Default output path.
        if self.options.output_path is None:
            self.options.output_path = os.getcwd()

        # Check output path.
        if not os.path.isdir(self.options.output_path):
            raise KeyError('Output directory "{}" does not exist'.format(self.options.output_path))

        # --combine option needs --title
        if self.options.combine and self.options.title is None:
            raise KeyError('Combining documents requires title')

        # Discourse Api-Key for authentication.
        api_key = self.options.api_key or os.environ.get('DISCOURSE_API_KEY')
        if api_key:
            self.headers['Api-Key'] = api_key

        # Adjust default format.
        self.options.format = self.options.format or 'pdf'

        # Adjust renderer.
        if not self.options.renderer and self.options.format == 'pdf':
            self.options.renderer = 'latex'

    def run(self):
        if self.options.combine:
            self.run_combined()
        else:
            self.run_sequential()

    def run_sequential(self):

        # How many zeros to use when padding the filename through "--enumerate".
        enumeration_width = max(2, len(str(len(self.options.url))))

        # Acquire data and render using pandoc.
        for index, url in enumerate(self.options.url):

            # Optionally prefix filename with sequence number through "--enumerate".
            filename_prefix = None
            if self.options.enumerate:
                seqnumber = str(index + 1).rjust(enumeration_width, '0')
                filename_prefix = '{} - '.format(seqnumber)

            self.render_topic(url, filename_prefix=filename_prefix)

    def run_combined(self):
        temporary_files = []
        for url in self.options.url:
            topic = DiscourseTopic(url, headers=self.headers)
            topic.fetch()
            temporary_files += topic.write_temporary_files()

        filenames = [tempfile.name for tempfile in temporary_files]

        self.pandoc(self.options.title, filenames, metadata={'date': now_rfc3339()})

    def render_topic(self, url, filename_prefix=None):

        topic = DiscourseTopic(url, headers=self.headers)
        topic.fetch()
        temporary_files = topic.write_temporary_files()
        filenames = [tempfile.name for tempfile in temporary_files]

        return self.pandoc(topic.data['title'], filenames, filename_prefix=filename_prefix, metadata={'date': topic.data['created_at']})

    def pandoc(self, title, filenames, filename_prefix=None, metadata=None):

        filename_prefix = filename_prefix or ''
        metadata = metadata or {}

        # Debugging.
        # print(title); print(sections)

        # TODO: Add "author" by collecting all authors of all posts.
        # Looks like "created_at" is actually "updated_at".
        tplvars = {'title': title, 'pandoc_to': ''}
        tplvars.update(metadata)

        # Compute output filename extension, honoring "--renderer" option.
        extension = self.options.format
        renderer = self.options.renderer
        if renderer is not None:
            # Translate into pandoc's "--to" option.
            tplvars['pandoc_to'] = '--to={}'.format(renderer)
            # Build extension.
            extension = '{}.{}'.format(renderer, extension)

        # Compute output file name.
        output_file = '{}{}.{}'.format(filename_prefix, title, extension)
        log.info('Writing standalone file "{}"'.format(output_file))

        # Compute full output path.
        if self.options.output_path is not None:
            output_file = os.path.join(self.options.output_path, output_file)

        tplvars['output_file'] = output_file

        # https://stackoverflow.com/questions/13515893/set-margin-size-when-converting-from-markdown-to-pdf-with-pandoc
        command = 'pandoc ' \
                  '--standalone --self-contained --table-of-contents ' \
                  '--from=html {pandoc_to} --resource-path=./node_modules ' \
                  '--variable=geometry:margin=2cm ' \
                  '--metadata=title="{title}" --metadata=date="{date}" --output="{output_file}"'.format(**tplvars)

        # TODO: --metadata=author="{author}"

        log.info('Invoking command: %s', command)

        # Compute commandline arguments.
        pargs = shlex.split(command)
        pargs.extend(filenames)

        # Run pandoc command.
        try:
            outcome = subprocess.run(pargs, capture_output=True, timeout=60.0, check=True, encoding='utf-8')
    
        except Exception as ex:
            log.exception('Running pandoc failed, output was\nSTDOUT:\n{}\nSTDERR:\n{}\n'.format(ex.stdout, ex.stderr))
            raise
