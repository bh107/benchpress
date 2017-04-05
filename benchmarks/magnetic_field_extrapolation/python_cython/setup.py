from distutils.core import setup
from Cython.Build import cythonize
import os

os.environ['CFLAGS'] = "-O3 -Wall -std=c99"
setup(ext_modules = cythonize("magnetic_field_extrapolation.pyx"))
