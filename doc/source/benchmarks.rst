
==========
Benchmarks
==========

+-------------------------------+-------+---------------------+--------------------------------------------------------+
|                               | py    | c                   | cpp                                                    |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
|                               | Numpy | Omp | Omp Mpi | Seq | Armadillo | Blitz | Boost | Bxx | Eigen | Omp | Opencl |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`LMM_swaption_vec`       | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`black_scholes`          | +     |     |         |     | +         | +     |       | +   | +     |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`convolve`               | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`convolve_2d`            | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`convolve_3d`            | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`convolve_separate_std`  | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`gameoflife`             | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`gauss`                  | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`heat_equation`          | +     | +   | +       | +   |           |       |       |     |       | +   | +      |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`idl_init_bh`            | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`idl_init_fast`          | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`idl_init_orig`          | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`jacobi`                 | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`jacobi_fixed`           | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`jacobi_solve`           | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`jacobi_stencil`         | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`k_nearest_neighbor`     | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`knn_naive`              | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`knn_naive1`             | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`lattice_boltzmann_D2Q9` | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`lbm_2d`                 | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`lbm_3d`                 | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`lu`                     | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`mc`                     | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`mxmul`                  | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`nbody`                  | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`nbody_nice`             | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`ndstencil`              | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`point27`                | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`pricing`                | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`shallow_water`          | +     |     |         | +   |           |       | +     |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`snakes_and_ladders`     | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`sor`                    | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`synth`                  | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`synth_inplace`          | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`synth_stream`           | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`synth_strided`          | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+
| :ref:`wireworld`              | +     |     |         |     |           |       |       |     |       |     |        |
+-------------------------------+-------+-----+---------+-----+-----------+-------+-------+-----+-------+-----+--------+



.. _LMM_swaption_vec:

Lmm Swaption Vec
================


.. _LMM_swaption_vec_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/LMM_swaption_vec/python_numpy/LMM_swaption_vec.py
   :language: py


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


.. _convolve:

Convolve
========


.. _convolve_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/convolve/python_numpy/convolve.py
   :language: py


.. _convolve_2d:

Convolve 2D
===========


.. _convolve_2d_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/convolve_2d/python_numpy/convolve_2d.py
   :language: py


.. _convolve_3d:

Convolve 3D
===========


.. _convolve_3d_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/convolve_3d/python_numpy/convolve_3d.py
   :language: py


.. _convolve_separate_std:

Convolve Separate Std
=====================


.. _convolve_separate_std_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/convolve_separate_std/python_numpy/convolve_separate_std.py
   :language: py


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


.. _idl_init_bh:

Idl Init Bh
===========


.. _idl_init_bh_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/idl_init_bh/python_numpy/idl_init_bh.py
   :language: py


.. _idl_init_fast:

Idl Init Fast
=============


.. _idl_init_fast_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/idl_init_fast/python_numpy/idl_init_fast.py
   :language: py


.. _idl_init_orig:

Idl Init Orig
=============


.. _idl_init_orig_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/idl_init_orig/python_numpy/idl_init_orig.py
   :language: py


.. _jacobi:

Jacobi
======


.. _jacobi_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/jacobi/python_numpy/jacobi.py
   :language: py


.. _jacobi_fixed:

Jacobi Fixed
============


.. _jacobi_fixed_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/jacobi_fixed/python_numpy/jacobi_fixed.py
   :language: py


.. _jacobi_solve:

Jacobi Solve
============


.. _jacobi_solve_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/jacobi_solve/python_numpy/jacobi_solve.py
   :language: py


.. _jacobi_stencil:

Jacobi Stencil
==============


.. _jacobi_stencil_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/jacobi_stencil/python_numpy/jacobi_stencil.py
   :language: py


.. _k_nearest_neighbor:

K Nearest Neighbor
==================


.. _k_nearest_neighbor_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/k_nearest_neighbor/python_numpy/k_nearest_neighbor.py
   :language: py


.. _knn_naive:

Knn Naive
=========


.. _knn_naive_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/knn_naive/python_numpy/knn_naive.py
   :language: py


.. _knn_naive1:

Knn Naive1
==========


.. _knn_naive1_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/knn_naive1/python_numpy/knn_naive1.py
   :language: py


.. _lattice_boltzmann_D2Q9:

Lattice Boltzmann D2Q9
======================


.. _lattice_boltzmann_D2Q9_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/lattice_boltzmann_D2Q9/python_numpy/lattice_boltzmann_D2Q9.py
   :language: py


.. _lbm_2d:

Lbm 2D
======


.. _lbm_2d_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/lbm_2d/python_numpy/lbm_2d.py
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


.. _mc:

Mc
==


.. _mc_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/mc/python_numpy/mc.py
   :language: py


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


.. _synth_strided:

Synth Strided
=============


.. _synth_strided_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/synth_strided/python_numpy/synth_strided.py
   :language: py


.. _wireworld:

Wireworld
=========


.. _wireworld_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/wireworld/python_numpy/wireworld.py
   :language: py

