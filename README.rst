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
`discodoc` - create documents from Discourse content easily.

It aims to make documentation generation effortless.

There might still be dragons.



*******
Install
*******

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

Setup
=====
::

    pip install discodoc


********
Synopsis
********
::

    # Generate PDF document from all posts of given topic
    discodoc https://community.hiveeyes.org/t/anleitung-aufbau-und-installation-des-sensor-kits-grune-platine/2443 --format=pdf


********
Features
********
All output formats are provided by pandoc fame. These have been tested:
- pdf, docx, odt, pptx, epub2, epub3, fb2, latex, texinfo, html, html5


*******
Credits
*******
- `Donald Knuth`_ and the `LaTeX Team`_ for conceiving and maintaining TeX and LaTeX
- `John MacFarlane`_ and all contributors for creating and curating pandoc_
- The amazing `Discourse Team`_ and all contributors for creating Discourse and its spirit

Thanks!

.. _Donald Knuth: https://www-cs-faculty.stanford.edu/~knuth/
.. _LaTeX Team: https://www.latex-project.org/about/team/
.. _pandoc: https://pandoc.org/
.. _John MacFarlane: https://johnmacfarlane.net/
.. _Discourse Team: https://blog.discourse.org/2013/02/the-discourse-team/
