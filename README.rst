.. image:: https://img.shields.io/badge/Python-3-green.svg
    :target: https://github.com/hiveeyes/discodoc

.. image:: https://img.shields.io/pypi/v/discodoc.svg
    :target: https://pypi.org/project/discodoc/

.. image:: https://img.shields.io/github/tag/hiveeyes/discodoc.svg
    :target: https://github.com/hiveeyes/discodoc

|

.. discodoc-readme:

########
discodoc
########


*****
About
*****
`discodoc` - create `hard copy`_-like documents from Discourse content easily.

It aims to make documentation generation effortless.

There might still be dragons.

.. _hard copy: https://en.wikipedia.org/wiki/Hard_copy


********
Synopsis
********
::

    # Generate PDF document from all posts of given topic.
    discodoc https://community.hiveeyes.org/t/anleitung-aufbau-und-installation-des-sensor-kits-grune-platine/2443 --format=pdf

For more information and further examples, please invoke ``discodoc --help``.


********
Features
********
All output formats are provided by pandoc fame. These have been tested:
pdf, docx, odt, pptx, epub2, epub3, fb2, latex, texinfo, txt, text, html, html5, json, plain, rtf, revealjs, s5.


************
Installation
************

Prerequisites
=============
::

    # Debian
    apt install texlive-latex-base pandoc

    # macOS / Homebrew
    brew install pandoc python3-requests
    brew cask install basictex

Optional::

    brew cask install wkhtmltopdf

For HTML slideshow rendering::

    yarn install


    wget https://meyerweb.com/eric/tools/s5/v/1.1/s5-11.zip
    cp -r ~/Downloads/s5-11/ui node_modules/s5

Setup
=====
::

    pip install discodoc


*******
Caveats
*******
If you are hitting one of the `global rate limits and throttling in Discourse`_ indicated like::

    {"errors":["You’ve performed this action too many times, please try again later."]}

You might want to authenticate using an appropriate API key like::

    export DISCOURSE_API_KEY=5c58bf5e4027622543f5179938182099c8b97188d00a9dc9f184cd3ca66db5ea

.. _global rate limits and throttling in Discourse: https://meta.discourse.org/t/global-rate-limits-and-throttling-in-discourse/78612

*******
Credits
*******
- `Donald Knuth`_ and the `LaTeX Team`_ for conceiving and maintaining TeX and LaTeX.
- `John MacFarlane`_ and all contributors for creating and curating pandoc_.
- The amazing `Discourse Team`_ and all contributors for creating Discourse and its spirit.

You know how you are. Thanks!


**************
Other programs
**************
- https://github.com/pfaffman/discourse-downloader
  - via: https://meta.discourse.org/t/struggling-with-pagination-within-search-query-json/59558/3


.. _Donald Knuth: https://www-cs-faculty.stanford.edu/~knuth/
.. _LaTeX Team: https://www.latex-project.org/about/team/
.. _pandoc: https://pandoc.org/
.. _John MacFarlane: https://johnmacfarlane.net/
.. _Discourse Team: https://blog.discourse.org/2013/02/the-discourse-team/
