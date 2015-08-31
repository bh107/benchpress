Synthetic benchmark for illustrating performance pitfalls on ccNUMA architectures.

Invoke as::

  --size=100000000*10

And the environment variable:: ``SYNTH_INIT_MODE``. This value must be one of the following::

  0 = serial initialization and serial access
  1 = parallel initialization and serial access
  2 = serial initialization and parallel access
  3 = parallel initialization and parallel access

When compiled with gcc the following values are useful for demonstrating AFFINITY policies::

  # Scattered / numa-node affinity on a system with 32 cores on four numa nodes
  GOMP_CPU_AFFINITY="0 8 16 24 1 9 17 25 2 10 18 26 3 11 19 27 4 12 20 28 5 13 21 29 6 14 22 30 7 15 23 31"
  # Core locality
  GOMP_CPU_AFFINITY="0-31"
