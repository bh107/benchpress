.. image:: https://readthedocs.org/projects/benchpress/badge/?version=latest
    :target: https://readthedocs.org/projects/benchpress/?badge=latest
    :alt: Documentation Status

.. image:: https://pypip.in/version/benchpress/badge.svg
    :target: https://pypi.python.org/pypi/benchpress/
    :alt: Latest Version

.. image:: https://pypip.in/py_versions/benchpress/badge.svg
    :target: https://pypi.python.org/pypi/benchpress/
    :alt: Supported Python versions

.. image:: https://pypip.in/implementation/benchpress/badge.svg
    :target: https://pypi.python.org/pypi/benchpress/
    :alt: Supported Python implementations

Quick Start
===========

Fire up your terminal, and::

  # Clone the repos
  git clone git@github.com:bh107/benchpress.git

  # Enter the root
  cd benchpress

  # Source environment vars
  source util/setbpenv.bash

You now have the Benchpress commands, ``bp-run``, ``bp-times``, ``bp-info``, ``bp-compile``, and ``bp-grapher`` ready at your finger-tips along with all the benchmarks and suites.

Go ahead and run the `python_numpy` suite, executing each benchmark in the suite twice::

  bp-run NOREPOS suites/python_numpy.py --runs 2 --output my_run.json

The above will store results from the run in the file `my_run.json`. You can inspect the elapsed wall-clock by executing::

  bp-times my_run.json

