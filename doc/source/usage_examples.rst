.. _usage_examples:

================
Usage - Examples
================

Make sure that you have set your ``PATH`` and ``PYTHONPATH`` correctly. Test it by invoking::

  bp-info --all

This should output something similar to::

  benchmarks: /home/safl/benchpress/benchmarks
  commands: /home/safl/benchpress/bin
  docsrc: /home/safl/benchpress/doc
  hooks: /home/safl/benchpress/hooks
  mod: /home/safl/benchpress/module/benchpress
  mod_parent: /home/safl/benchpress/module
  suites: /home/safl/benchpress/suites

Benchmarks can be run `manually` / `by hand` or via the `bp-run` tool. The ``bp-info`` command comes in handy when you want to find your way around. It can tell you where benchmarks and suites are located. This has multiple uses, such as::

  # Go to the benchmark directory
  cd `bp-info --benchmarks`

  # Go to the suites directory
  cd `bp-info --suites`

Or listing what is available::

  # Show me the benchmark suites
  ls `bp-info --suites`

The ``bp-info`` command is used by the benchmark suites themselves to locate the benchmark directory.

Running benchmarks via bp-run
=============================

The following will run the ``python_numpy`` benchmark suite::

  bp-run NOREPOS `bp-info --suites`/python_numpy.py --output /tmp/my_run.json

And store the results from the run in the file ``/tmp/my_run.json``.

Each benchmark in the suite is executed three times by default. You can change the number of executions with the ``--runs`` flag. The data collected in the output-file contains a bunch of information about the environment that the benchmark was executed in, such operating system version, hardware info, state of environment variables and other things.
You can inspect the data with your text-editor and write a parser for extracting the data your are interested in.

Benchpress has several helper functions available, in the Python benchpress module to aid such as task. Additionally the ``bp-times`` command provides a convenient overview of elapsed time.

Try invoking it on your output-file::

  bp-times ``/tmp/my_run.json``

This should provide output similar to::

  1D Stencil [NumPy, N/A, N/A]: [21.174466, 15.875864, 11.602997] 16.217776 (3.915008) 3
  2D Stencil [NumPy, N/A, N/A]: [29.273266, 29.554602, 29.318557] 29.382142 (0.123342) 3
  3D Stencil [NumPy, N/A, N/A]: N/A
  Black Scholes [NumPy, N/A, N/A]: [5.905177, 5.846048, 5.819017] 5.856747 (0.035979) 3
  Game of Life [NumPy, N/A, N/A]: [34.63458, 32.782089, 32.694652] 33.370440 (0.894594) 3
  Gauss Elimination [NumPy, N/A, N/A]: [0.182918, 0.181614, 0.18278] 0.182437 (0.000585) 3
  Heat Equation [NumPy, N/A, N/A]: [4.194531, 4.135326, 4.185207] 4.171688 (0.025992) 3
  Jacobi Solve [NumPy, N/A, N/A]: [4.155966, 4.185878, 4.180958] 4.174267 (0.013096) 3
  Jacobi Stencil [NumPy, N/A, N/A]: [3.060532, 3.006271, 3.023313] 3.030039 (0.022657) 3
  LU Factorization [NumPy, N/A, N/A]: [1.766148, 1.71995, 1.719055] 1.735051 (0.021992) 3
  Lattice Boltzmann 3D [NumPy, N/A, N/A]: [0.574888, 0.581474, 0.571298] 0.575887 (0.004214) 3
  Matrix Multiplication [NumPy, N/A, N/A]: [0.042147, 0.04208, 0.042872] 0.042366 (0.000359) 3
  Monte Carlo PI [NumPy, N/A, N/A]: [15.190297, 14.993777, 15.236259] 15.140111 (0.105161) 3
  SOR [NumPy, N/A, N/A]: N/A
  Shallow Water [NumPy, N/A, N/A]: N/A
  Synthetic [NumPy, N/A, N/A]: N/A
  Synthetic Inplace [NumPy, N/A, N/A]: N/A
  Synthetic Stream #0 Ones [NumPy, N/A, N/A]: N/A
  Synthetic Stream #1 Range [NumPy, N/A, N/A]: N/A
  Synthetic Stream #2 Random [NumPy, N/A, N/A]: N/A
  kNN Naive 1 [NumPy, N/A, N/A]: [1.364709, 1.3518, 1.352595] 1.356368 (0.005907) 3
  nbody [NumPy, N/A, N/A]: [9.603349, 9.665165, 9.727452] 9.665322 (0.050665) 3

.. note:: You do not have to wait for the benchmark run to finish, results at added to the output-file as they are available. Runs that have not yet finished show up as "N/A".

Running benchmarks "by hand"
============================

If you, for some reason, do not wish to run via ``bp-run``, then you can go to the just execute them manually::

  python `bp-info --benchmarks`/heat_equation/python_numpy/heat_equation.py --size=10000*10000*10

The above command executes the Python/NumPy implementation of :ref:`heat_equation`.
If you would like to execute the same benchmark but using Bohrium as backend then do the following::

  python -m bohrium `bp-info --benchmarks`/heat_equation/python_numpy/heat_equation.py --size=10000*10000*10 --bohrium=True

.. note:: Notice the ``-m bohrium`` right after the ``python`` command, and the ``--bohrium=True`` argument at the end. Both are needed.

The ``-m bohrium`` flag overloads the ``numpy`` module, which means you do not have to change the code to run using Bohrium.

The ``--bohrium=True`` tells the benchpress tool that it is running with Bohrium. Bohrium uses lazy evaluation so we must instruct the benchpress tool to flush computions in order to accurate measurements.

