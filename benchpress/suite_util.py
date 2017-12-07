# -*- coding: utf-8 -*-
"""
Utilities for Generating Commands 
---------------------------------
"""
from __future__ import absolute_import
import os
from os.path import join, realpath


def _script_path():
    """Returns the path to the dir this script is in"""
    return os.path.dirname(realpath(__file__))


# The path to the root of benchpress
BP_ROOT = realpath(join(_script_path()))


def benchmark_path(name, implementation, extension):
    """Returns the path to the executable of a benchmark implementation in the include suites.
    
    Parameters
    ----------
    name : str
        The name of the benchmark e.g. 'montecarlo_pi'
    implementation : str
        The name of the implementation e.g. 'python_numpy'
    extension : str
        The extension of the executable e.g. '.py'
    
    Returns
    -------
    path : str
        Absolute path to the executable
    """
    return realpath(join(_script_path(), "benchmarks", name, implementation, "%s%s" % (name, extension)))
