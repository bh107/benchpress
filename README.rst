Read the full  

.. image:: https://readthedocs.org/projects/benchpress/badge/?version=latest
   :target: http://benchpress.readthedocs.org
   :alt: Documentation Status

on Benchpress or see below for a quick start.

Quick Start
===========

Fire up your terminal, and::

  # Clone the repos
  git clone git@github.com:bh107/benchpress.git

  # Enter the root
  cd benchpress

  # Source environment vars
  source util/setbpenv.bash

You now have the Benchpress commands, ``bp_run``, ``bp_times``, ``bp_info``, ``bp_compile``, and ``bp_grapher`` ready at your finger-tips along with all the benchmarks and suites.

Go ahead and run the `numpy_only` suite, executing each benchmark in the suite twice::

  bp_run --no-perf --no-time --runs 2 --output my_run.json suites/numpy_only.py

The above will store results from the run in the file `my_run.json`. You can inspect the elapsed wall-clock by executing::

  bp_times my_run.json

