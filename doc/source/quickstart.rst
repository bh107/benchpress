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

Go ahead and run the `numpy_only` suite, executing each benchmark in the suite twice::

  bp-run --no-perf --no-time --runs 2 --output my_run.json suites/numpy_only.py

The above will store results from the run in the file `my_run.json`. You can inspect the elapsed wall-clock by executing::

  bp-times my_run.json

