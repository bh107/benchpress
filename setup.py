#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
import os
import re


def _script_path():
    """Returns the path to the dir this script is in"""
    return os.path.dirname(os.path.realpath(__file__))


def find_data_files(relative_to, directory, regex_exclude="\.pyc|{0}bin{0}|{0}obj{0}".format(os.sep)):
    ret = []
    for root, _, filenames in os.walk(os.path.join(relative_to, directory)):
        for filename in filenames:
            fullname = os.path.join(root, filename)
            if not re.search(regex_exclude, fullname):
                # NB: we remove the 'relative_to' part of the path
                ret.append(fullname[len(os.path.normpath(relative_to))+1:])
    return ret


# Get the long description from the README file
with open(os.path.join(_script_path(), 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='benchpress',

    setup_requires=['setuptools_scm'],
    use_scm_version={'version_scheme': 'post-release', 'local_scheme': lambda x: ''},

    description='Benchmark suite tool',
    long_description=long_description,

    # The project's main homepage.
    url='http://benchpress.readthedocs.io',

    # Author details
    author='The Benchpress Team',
    author_email='benchpress@bh107.org',
    maintainer='Mads R. B. Kristensen',
    maintainer_email='madsbk@gmail.com',
    platforms=['Linux', 'OSX'],

    # Choose your license
    license='GPL',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: End Users/Desktop',
        'Topic :: Multimedia',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License (GPL)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],

    # What does your project relate to?
    keywords='Benchmark, Bohrium, bh107',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['numpy', 'jsonschema'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
   # extras_require={
   #     'dev': ['check-manifest'],
   #     'test': ['coverage'],
   # },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        'benchpress': find_data_files("benchpress", "benchmarks") +
                      find_data_files("benchpress", "suites"),
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
   # data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'bp-run=benchpress.run:main',
            'bp-info=benchpress.info:main',
            'bp-cli=benchpress.visualizer.cli:main',
            'bp-raw=benchpress.visualizer.raw:main',
            'bp-cli-series=benchpress.visualizer.cli_series:main',
            'bp-chart=benchpress.visualizer.bar_per_cmd:main',
            'bp-chart-series=benchpress.visualizer.series_per_cmd:main',
            'bp-total=benchpress.visualizer.totaltime:main',
        ],
    },
)
