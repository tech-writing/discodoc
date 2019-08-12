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
        self.headers = {}

        self.setup()

    def setup(self):
        """
        Run sanity checks and apply configuration defaults.
        """

        # Default output path.
        if self.options.path is None:
            self.options.path = os.getcwd()

        # Check output path.
        if not os.path.isdir(self.options.path):
            raise KeyError('Output directory "{}" does not exist'.format(self.options.path))

        # Discourse Api-Key for authentication.
        api_key = self.options.api_key or os.environ.get('DISCOURSE_API_KEY')
        if api_key:
            self.headers['Api-Key'] = api_key

        # Adjust renderer.
        if not self.options.renderer and self.options.format == 'pdf':
            self.options.renderer = 'latex'

    def run(self):

        # Acquire data and render using pandoc.
        self.discourse_to_document(self.options.url)

    def discourse_to_document(self, url, headers=None):
    
        self.options.format = self.options.format or 'pdf'
        headers = headers or {}
    
        # Acquire all posts from topic.
        # Remark: The ``print=true`` option will return up to 1000 posts in a topic.
        # API Documentation: https://docs.discourse.org/#tag/Topics%2Fpaths%2F~1t~1%7Bid%7D.json%2Fget
        url = url + '.json?print=true'
        response = requests.get(url, headers=self.headers)
    
        try:
            response.raise_for_status()
        except:
            log.exception('Failed requesting URL "{}". The response was:\n{}\n\n'.format(url, response.text))
            raise
    
        # Extract information.
        data = response.json()
        title = data['title']
        sections = []
        for post in data['post_stream']['posts']:
            sections.append(post['cooked'])
    
        # Debugging.
        #print(title); print(sections)

        # Compute output filename extension, honoring "--renderer" option.
        pandoc_to = ''
        extension = self.options.format
        renderer = self.options.renderer
        if renderer is not None:
            # Translate into pandoc's "--to" option.
            pandoc_to = '--to={}'.format(renderer)
            # Build extension.
            extension = '{}.{}'.format(renderer, extension)

        # Compute output file name.
        output_file = '{}.{}'.format(title, extension)
        log.info('Writing standalone file "{}"'.format(output_file))

        # Compute full output path.
        if self.options.path is not None:
            output_file = os.path.join(self.options.path, output_file)
    
        command = 'pandoc ' \
                  '--standalone --self-contained --table-of-contents ' \
                  '--from html {pandoc_to} --resource-path=./node_modules ' \
                  '--metadata title="{title}" --output "{output_file}"'.format(**locals())
        log.info('Invoking command: %s', command)
    
        # Write sections to temporary files.
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
    
        # Compute commandline arguments.
        pargs = shlex.split(command)
        pargs.extend(filenames)
    
        # Run pandoc command.
        try:
            outcome = subprocess.run(pargs, capture_output=True, timeout=60.0, check=True, encoding='utf-8')
    
        except Exception as ex:
            log.exception('Running pandoc failed, output was\nSTDOUT:\n{}\nSTDERR:\n{}\n'.format(ex.stdout, ex.stderr))
            raise
