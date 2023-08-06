#!/usr/bin/env python
import os
from setuptools import setup, find_packages

#
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

import os.path

def readver(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in readver(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")




setup(
    name="pyql700",
    description="Automatically created environment for python package",
    url="https://gitlab.com/jaromrax/pyql700",
    author=" me ",
    author_email="me@example.com",
    licence="GPL2",
    version=get_version("Pyql700/version.py"),
    packages=['Pyql700'],
    package_data={'pyql700': ['data/*']},
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    scripts = ['bin/pyql700'],
    install_requires = ['numpy',"ansicolors","qrcode","termcolor"],
)
