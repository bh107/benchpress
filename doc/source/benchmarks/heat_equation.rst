

.. _heat_equation:

Heat Equation
=============

.. include:: ../../../benchmarks/heat_equation/readme.rst


.. _heat_equation_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../../benchmarks/heat_equation/python_numpy/heat_equation.py
   :language: python


.. _heat_equation_c99_omp:

C99 Omp
-------


.. literalinclude:: ../../../benchmarks/heat_equation/c99_omp/src/heat_equation.c
   :language: c


.. _heat_equation_c99_omp_mpi:

C99 Omp Mpi
-----------


.. literalinclude:: ../../../benchmarks/heat_equation/c99_omp_mpi/src/heat_equation.c
   :language: c


.. _heat_equation_c99_seq:

C99 Seq
-------


.. literalinclude:: ../../../benchmarks/heat_equation/c99_seq/src/heat_equation.c
   :language: c


.. _heat_equation_cpp11_omp:

Cpp11 Omp
---------


.. literalinclude:: ../../../benchmarks/heat_equation/cpp11_omp/src/heat_equation.cpp
   :language: cpp


.. _heat_equation_cpp11_opencl:

Cpp11 Opencl
------------


.. error:: There are issues with the implementation.

    Two known issues::

    

     * Implementation compiles (with warning) but execution is untested.

     * Implementation does not use ``bp-util`` for argparsing and timing, getting it to run in a suite might be cumbersome...

    


.. literalinclude:: ../../../benchmarks/heat_equation/cpp11_opencl/src/heat_equation.cpp
   :language: cpp


.. _heat_equation_csharp_numcil:

Csharp Numcil
-------------


.. literalinclude:: ../../../benchmarks/heat_equation/csharp_numcil/src/heat_equation.cs
   :language: csharp
