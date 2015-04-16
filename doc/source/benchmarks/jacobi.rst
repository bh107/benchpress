

.. _jacobi:

Jacobi
======

.. include:: ../../../benchmarks/jacobi/readme.rst


.. _jacobi_python_numpy:

Python Numpy
------------


.. note:: There is Bohrium-specific code this implementation, this means Bohrium is required to run it.

    Uses Bohrium features from ``bohrium.stdviews`` specifically ``no_border``, ``grid``, and ``diagonals``.


.. literalinclude:: ../../../benchmarks/jacobi/python_numpy/jacobi.py
   :language: python


.. _jacobi_csharp_numcil:

Csharp Numcil
-------------


.. literalinclude:: ../../../benchmarks/jacobi/csharp_numcil/src/jacobi.cs
   :language: csharp
