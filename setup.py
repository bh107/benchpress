#!/usr/bin/env python
import pprint
import glob
import os
from distutils.core import setup
from benchpress.version import APP_NAME, APP_VERSION

def make_dfiles(prefix, directory):
    """
    Constructs a recursive directory listing compatible with
    setup.py such that an entire directory and its subdirectories
    can be added as data_files.
    """

    dfiles = []
    for root, dirnames, filenames in os.walk(directory):
        flist = []
        for fn in filenames:
            flist.append(os.sep.join([root,fn]))
        if flist:
            dfiles.append((os.sep.join([prefix, root]), flist))
    return dfiles

setup(
    name        = APP_NAME,
    version     = APP_VERSION,
    description = 'Collection of benchmarks and tools for running them.',
    url         = 'http://benchpress.rtfd.org',
    author      = 'Simon A. F. Lund',
    author_email='safl@safl.dk',
    data_files = make_dfiles('share/benchpress', 'benchmarks') +\
                 make_dfiles('share/benchpress', 'suites'),
    packages = ['benchpress'],
    scripts = ["bp_run", "bp_times", "bp_grapher", "hooks/proxy-VEM-pre-hook.sh"]
)
