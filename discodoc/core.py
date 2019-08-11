#!/usr/bin/env python
"""
========
Synopsis
========
::

    pandisco https://community.hiveeyes.org/t/anleitung-aufbau-und-installation-des-sensor-kits-grune-platine/2443


=====
Setup
=====
::

    brew install pandoc python3-requests
    brew cask install basictex

Alternative::

    pip install requests


=======
Backlog
=======
- Obtain output format from commandline
- Obtain PANDOC_OPTIONS from environment
- Select specific posts

"""
import os
import sys
import shlex
import tempfile
import requests
import subprocess


def discourse_to_pdf(url, format=None):

    format = format or 'pdf'

    # Acquire posts from topic.
    url = url + '.json'
    response = requests.get(url)
    #print(response.text)

    # Extract information.
    data = response.json()
    title = data['title']
    sections = []
    for post in data['post_stream']['posts']:
        sections.append(post['cooked'])

    # Debugging.
    #print(title)
    #print(sections)

    print(f'INFO: Writing standalone file "{title}.{format}"')

    # By default, pandoc produces a document fragment. To produce a
    # standalone  document (e.g.  a valid HTML file including <head>
    # and <body>), use the --standalone flag.
    command = f'pandoc --standalone --metadata title="{title}" --output "{title}.{format}" --from html'
    print('command:', command)

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
    print('command:', pargs)

    response = subprocess.run(pargs)
    print('response:', response)


def main():
    url = sys.argv[1]
    try:
        format = sys.argv[2]
    except:
        format = None

    discourse_to_pdf(url, format=format)


if __name__ == '__main__':
    main()
