
==========
Benchmarks
==========

+---------------------------+-------+---------------------+--------------------------------------------------------+
|                           | py    | c                   | cpp                                                    |
+---------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
|                           | Numpy | Omp | Omp Mpi | Seq | Armadillo | Blitz | Boost | Bxx | Eigen | Omp | Opencl |
+---------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`black_scholes`      | +     |     |         |     | +         | +     |       | +   | +     |     |        |
+---------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`gameoflife`         | +     |     |         |     |           |       |       |     |       |     |        |
+---------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`gauss`              | +     |     |         |     |           |       |       |     |       |     |        |
+---------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`heat_equation`      | +     | +   | +       | +   |           |       |       |     |       | +   | +      |
+---------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`knn_naive`          | +     |     |         |     |           |       |       |     |       |     |        |
+---------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`lbm_3d`             | +     |     |         |     |           |       |       |     |       |     |        |
+---------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`lu`                 | +     |     |         |     |           |       |       |     |       |     |        |
+---------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`mcpi`               | +     | +   |         |     |           | +     |       | +   |       |     |        |
+---------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`mxmul`              | +     |     |         |     |           |       |       |     |       |     |        |
+---------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`nbody`              | +     |     |         |     |           |       |       |     |       |     |        |
+---------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`nbody_nice`         | +     |     |         |     |           |       |       |     |       |     |        |
+---------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`ndstencil`          | +     |     |         |     |           |       |       |     |       |     |        |
+---------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`point27`            | +     |     |         |     |           |       |       |     |       |     |        |
+---------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`pricing`            | +     |     |         |     |           |       |       |     |       |     |        |
+---------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`shallow_water`      | +     |     |         | +   |           |       | +     |     |       |     |        |
+---------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`snakes_and_ladders` | +     |     |         |     |           |       |       |     |       |     |        |
+---------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`sor`                | +     |     |         |     |           |       |       |     |       |     |        |
+---------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`synth`              | +     |     |         |     |           |       |       |     |       |     |        |
+---------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`synth_inplace`      | +     |     |         |     |           |       |       |     |       |     |        |
+---------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`synth_stream`       | +     |     |         |     |           |       |       |     |       |     |        |
+---------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+



.. _black_scholes:

Black Scholes
=============


.. _black_scholes_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/black_scholes/python_numpy/black_scholes.py
   :language: py


.. _black_scholes_cpp11_armadillo:

Cpp11 Armadillo
---------------


.. literalinclude:: ../../benchmarks/black_scholes/cpp11_armadillo/src/black_scholes.cpp
   :language: cpp


.. _black_scholes_cpp11_blitz:

Cpp11 Blitz
-----------


.. literalinclude:: ../../benchmarks/black_scholes/cpp11_blitz/src/black_scholes.cpp
   :language: cpp


.. _black_scholes_cpp11_bxx:

Cpp11 Bxx
---------


.. literalinclude:: ../../benchmarks/black_scholes/cpp11_bxx/src/black_scholes.cpp
   :language: cpp


.. _black_scholes_cpp11_eigen:

Cpp11 Eigen
-----------


.. literalinclude:: ../../benchmarks/black_scholes/cpp11_eigen/src/black_scholes.cpp
   :language: cpp


.. _gameoflife:

Gameoflife
==========


.. _gameoflife_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/gameoflife/python_numpy/gameoflife.py
   :language: py


.. _gauss:

Gauss
=====


.. _gauss_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/gauss/python_numpy/gauss.py
   :language: py


.. _heat_equation:

Heat Equation
=============


.. _heat_equation_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/heat_equation/python_numpy/heat_equation.py
   :language: py


.. _heat_equation_c99_omp:

C99 Omp
-------


.. literalinclude:: ../../benchmarks/heat_equation/c99_omp/src/heat_equation.c
   :language: c


.. _heat_equation_c99_omp_mpi:

C99 Omp Mpi
-----------


.. literalinclude:: ../../benchmarks/heat_equation/c99_omp_mpi/src/heat_equation.c
   :language: c


.. _heat_equation_c99_seq:

C99 Seq
-------


.. literalinclude:: ../../benchmarks/heat_equation/c99_seq/src/heat_equation.c
   :language: c


.. _heat_equation_cpp11_omp:

Cpp11 Omp
---------


.. literalinclude:: ../../benchmarks/heat_equation/cpp11_omp/src/heat_equation.cpp
   :language: cpp


.. _heat_equation_cpp11_opencl:

Cpp11 Opencl
------------


.. literalinclude:: ../../benchmarks/heat_equation/cpp11_opencl/src/heat_equation.cpp
   :language: cpp


.. _knn_naive:

Knn Naive
=========


.. _knn_naive_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/knn_naive/python_numpy/knn_naive.py
   :language: py


.. _lbm_3d:

Lbm 3D
======


.. _lbm_3d_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/lbm_3d/python_numpy/lbm_3d.py
   :language: py


.. _lu:

Lu
==


.. _lu_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/lu/python_numpy/lu.py
   :language: py


.. _mcpi:

Mcpi
====


.. _mcpi_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/mcpi/python_numpy/mcpi.py
   :language: py


.. _mcpi_c99_omp:

C99 Omp
-------


.. literalinclude:: ../../benchmarks/mcpi/c99_omp/src/mcpi.c
   :language: c


.. _mcpi_cpp11_blitz:

Cpp11 Blitz
-----------


.. literalinclude:: ../../benchmarks/mcpi/cpp11_blitz/src/mcpi.cpp
   :language: cpp


.. _mcpi_cpp11_bxx:

Cpp11 Bxx
---------


.. literalinclude:: ../../benchmarks/mcpi/cpp11_bxx/mcpi.cpp
   :language: cpp


.. _mxmul:

Mxmul
=====


.. _mxmul_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/mxmul/python_numpy/mxmul.py
   :language: py


.. _nbody:

Nbody
=====


.. _nbody_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/nbody/python_numpy/nbody.py
   :language: py


.. _nbody_nice:

Nbody Nice
==========


.. _nbody_nice_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/nbody_nice/python_numpy/nbody_nice.py
   :language: py


.. _ndstencil:

Ndstencil
=========


.. _ndstencil_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/ndstencil/python_numpy/ndstencil.py
   :language: py


.. _point27:

Point27
=======


.. _point27_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/point27/python_numpy/point27.py
   :language: py


.. _pricing:

Pricing
=======


.. _pricing_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/pricing/python_numpy/pricing.py
   :language: py


.. _shallow_water:

Shallow Water
=============


.. _shallow_water_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/shallow_water/python_numpy/shallow_water.py
   :language: py


.. _shallow_water_c99_seq:

C99 Seq
-------


.. literalinclude:: ../../benchmarks/shallow_water/c99_seq/src/shallow_water.c
   :language: c


.. _shallow_water_cpp11_boost:

Cpp11 Boost
-----------


.. literalinclude:: ../../benchmarks/shallow_water/cpp11_boost/src/shallow_water.cpp
   :language: cpp


.. _snakes_and_ladders:

Snakes And Ladders
==================


.. _snakes_and_ladders_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/snakes_and_ladders/python_numpy/snakes_and_ladders.py
   :language: py


.. _sor:

Sor
===


.. _sor_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/sor/python_numpy/sor.py
   :language: py


.. _synth:

Synth
=====


.. _synth_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/synth/python_numpy/synth.py
   :language: py


.. _synth_inplace:

Synth Inplace
=============


.. _synth_inplace_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/synth_inplace/python_numpy/synth_inplace.py
   :language: py


.. _synth_stream:

Synth Stream
============


.. _synth_stream_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/synth_stream/python_numpy/synth_stream.py
   :language: py

