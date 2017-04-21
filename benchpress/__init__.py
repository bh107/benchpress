# -*- coding: utf-8 -*-

from pkg_resources import get_distribution, DistributionNotFound
import util
import visualizer
import suite_util
from .benchpress import *

# Set the package version
try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass
