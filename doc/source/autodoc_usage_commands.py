# This script runs all the BP binaries with the --help flag and writes the output in the `autodoc_usage_commands` dir

import sys
import os
from os.path import join
from subprocess import call


def _script_path():
    """Returns the path to the dir this script is in"""
    return os.path.dirname(os.path.realpath(__file__))


def main():
    out_dir = join(_script_path(), "autodoc_usage_commands")
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    bp_root = join(_script_path(), '..', '..', 'benchpress')
    command_list = [\
        ('bp-run.txt', join(bp_root, 'run.py')),
        ('bp-cli.txt', join(bp_root, 'visualizer', 'cli.py')),
        ('bp-cli-series.txt', join(bp_root, 'visualizer', 'cli_series.py')),
        ('bp-raw.txt', join(bp_root, 'visualizer', 'raw.py')),
        ('bp-chart.txt', join(bp_root, 'visualizer', 'bar_per_cmd.py')),
        ('bp-chart-series.txt', join(bp_root, 'visualizer', 'series_per_cmd.py')),
    ]

    for name, path in command_list:
        call("%s %s --help > %s" % (sys.executable, path, join(out_dir, name)), shell=True)
