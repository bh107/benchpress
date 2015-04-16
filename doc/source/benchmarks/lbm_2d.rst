

.. _lbm_2d:

Lbm 2D
======

.. include:: ../../../benchmarks/lbm_2d/readme.rst


.. _lbm_2d_python_numpy:

Python Numpy
------------


.. error:: There are issues with the implementation.

    Cannot run with Bohrium, fails with error::

    

      TypeError: Cannot determine the correct signature (sqrt:int64)

    

    Also, does not use benchpress util for argparsing and timing.


.. literalinclude:: ../../../benchmarks/lbm_2d/python_numpy/lbm_2d.py
   :language: python
