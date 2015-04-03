#!/usr/bin/env python
import pprint
import glob
import os
from distutils.core import setup
from benchpress.version import APP_NAME, APP_VERSION, get_paths

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

paths = get_paths() # Grab the paths

setup(              # Set it up
    name        = APP_NAME,
    version     = APP_VERSION,
    description = 'Collection of benchmarks and tools for running them.',
    url         = 'http://benchpress.rtfd.org',
    author      = 'Simon A. F. Lund',
    author_email='safl@safl.dk',
    data_files = make_dfiles('share/benchpress', paths['benchmarks']) +\
                 make_dfiles('share/benchpress', paths['suites']),
    packages = ['benchpress'],
    scripts = [
        os.sep.join([paths["commands"], "bp-info"]),
        os.sep.join([paths["commands"], "bp-run"]),
        os.sep.join([paths["commands"], "bp-times"]),
        os.sep.join([paths["commands"], "bp-grapher"]),
        os.sep.join([paths["commands"], "bp-compile"]),
        os.sep.join([paths["hooks"], "proxy-VEM-pre-hook.sh"])
    ]
)
