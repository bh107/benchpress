

.. _rosenbrock:

Rosenbrock
==========

.. include:: ../../../benchmarks/rosenbrock/readme.rst


.. _rosenbrock_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../../benchmarks/rosenbrock/python_numpy/rosenbrock.py
   :language: python


.. _rosenbrock_c99_seq:

C99 Seq
-------


.. literalinclude:: ../../../benchmarks/rosenbrock/c99_seq/src/rosenbrock.c
   :language: c


.. _rosenbrock_cpp11_bxx:

Cpp11 Bxx
---------


.. error:: There are issues with the implementation.

    BXX, does not handle slices as arguments properly.


.. literalinclude:: ../../../benchmarks/rosenbrock/cpp11_bxx/src/rosenbrock.cpp
   :language: cpp


.. _rosenbrock_cpp11_omp:

Cpp11 Omp
---------


.. literalinclude:: ../../../benchmarks/rosenbrock/cpp11_omp/src/rosenbrock.cpp
   :language: cpp


.. _rosenbrock_cpp11_seq:

Cpp11 Seq
---------


.. literalinclude:: ../../../benchmarks/rosenbrock/cpp11_seq/src/rosenbrock.cpp
   :language: cpp
