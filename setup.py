# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(name='discodoc',
      version='0.3.0',
      description='discodoc - create documents from Discourse content easily',
      long_description=README,
      license="AGPL 3, EUPL 1.2",
      classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "Topic :: Communications",
        "Topic :: Database",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Topic :: System :: Archiving",
        "Topic :: Text Processing",
        "Topic :: Utilities",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS"
        ],
      author='Andreas Motl',
      author_email='andreas@hiveeyes.org',
      url='https://github.com/hiveeyes/discodoc',
      keywords='discourse pandoc document hardcopy export pdf epub docx pptx odt html s5 reveal.js',
      packages=find_packages(),
      include_package_data=True,
      package_data={
      },
      zip_safe=False,
      install_requires=[
          'docopt>=0.6.2',
          'munch>=2.3.2',
          'requests',
          'rfc3339',
      ],
      extras_require={
      },
      entry_points={
          'console_scripts': [
              'discodoc = discodoc.cli:run',
          ],
      },
)
