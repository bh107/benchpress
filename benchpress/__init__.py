# -*- coding: utf-8 -*-
"""
===========================================
Benchpress: a benchmark tool and collection
===========================================

Benchpress is primarily a tool for running benchmarks and analyze/visualize the result.

The workflow:
    - Write a Python program that generates the commands to run and write the commands to a JSON file
    - Use `bp-run` to *run* the JSON file
    - Use a visualizer such as `bp-cli` or `bp-chart` to visualize the results within the JSON file

"""
from __future__ import absolute_import
from pkg_resources import get_distribution, DistributionNotFound
from . import visualizer
from . import suite_util
from . import argument_handling
from . import time_util
from . import benchmarks
from .benchpress import *

# Set the package version
try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass


# We expose the suite schema as the dict `suite_schema`
def _suite_schema():
    from os.path import join, realpath, dirname
    import json
    try:
        with open(join(dirname(realpath(__file__)), "suite_schema.json"), "r") as f:
            return json.load(f)
    except IOError:  # readthedocs cannot find "suite_schema.json"
        return None


suite_schema = _suite_schema()
