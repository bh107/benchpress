# -*- coding: utf-8 -*-
from __future__ import absolute_import
import argparse

_parser = argparse.ArgumentParser(description='Runs a benchmark suite and stores the results in a JSON-file.')
_parser.add_argument(
    '--output',
    type=str,
    metavar='RESULT_FILE',
    help='Path to the JSON file where the benchmark results will be written. '
         'If the file exist, the benchmark will resume.'
)

# This module maintains the state to '_args'
_args = None


def args():
    """Return the argparse object"""
    global _args
    if _args is None:
        _args = _parser.parse_args()
    return _args


def add_argument(*args, **kwargs):
    """
    add_argument(dest, ..., name=value, ...)
    add_argument(option_string, option_string, ..., name=value, ...)
    """
    return _parser.add_argument(*args, **kwargs)


def error(msg):
    """Raise an argparse error"""
    return _parser.error(msg)
