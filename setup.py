#!/usr/bin/env python
from distutils.core import setup
from benchpress.version import APP_NAME, APP_VERSION

setup(
    name        = APP_NAME,
    version     = APP_VERSION,
    description = 'Collection of benchmarks and tools for running them.',
    url         = 'http://benchpress.rtfd.org',
    author      = 'Simon A. F. Lund',
    author_email='safl@safl.dk',

    packages = ['benchpress'],
    scripts = ["bp_run", "bp_times", "bp_grapher"]
)
