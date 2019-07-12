from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from io import open
from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='hhc',
    version='3.0.2',
    description='The best way to express a number in a URL.',
    author='Alexander Ljungberg',
    author_email='aljungberg@slevenbits.com',
    url='https://github.com/aljungberg/hhc',
    packages=['hhc'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    keywords=["base64", "hexahexacontadecimal", "hhc", "base66", "url"],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
)
