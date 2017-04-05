from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules = cythonize("magnetic_field_extrapolation.pyx"))
