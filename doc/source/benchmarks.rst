==========
Benchmarks
==========

+-------------------------------+------------------+---------------------+------------------------------------------------------------------------+--------+
| 39 Benchmarks                 | Python           | C                   | C++                                                                    | C#     |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
|                               | Numpy            | Omp | Omp Mpi | Seq | Armadillo | Blitz | Boost | Bxx      | Eigen    | Omp | Opencl   | Seq | Numcil |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`black_scholes`          | +                |     |         |     | +         | +     |       | +        | + [ISU]_ |     |          | +   | +      |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`convolve`               | + [ISU]_ [BH]_   |     |         |     |           |       |       |          |          |     |          |     |        |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`convolve_2d`            | + [ISU]_ [BH]_   |     |         |     |           |       |       |          |          |     |          |     |        |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`convolve_3d`            | + [ISU]_ [BH]_   |     |         |     |           |       |       |          |          |     |          |     |        |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`convolve_separate_std`  | + [ISU]_         |     |         |     |           |       |       |          |          |     |          |     |        |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`gameoflife`             | +                |     |         |     |           |       |       |          |          |     |          |     |        |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`gauss`                  | +                |     |         |     |           |       |       |          |          |     |          |     |        |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`heat_equation`          | +                | +   | +       | +   |           |       |       |          |          | +   | + [ISU]_ |     |        |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`idl_init_bh`            | + [ISU]_ [IBNP]_ |     |         |     |           |       |       |          |          |     |          |     |        |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`idl_init_fast`          | + [ISU]_ [IBNP]_ |     |         |     |           |       |       |          |          |     |          |     |        |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`idl_init_orig`          | + [ISU]_ [IBNP]_ |     |         |     |           |       |       |          |          |     |          |     |        |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`jacobi`                 | + [BH]_          |     |         |     |           |       |       |          |          |     |          |     | +      |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`jacobi_fixed`           | + [BH]_          |     |         |     |           |       |       |          |          |     |          |     | +      |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`jacobi_solve`           | +                |     |         |     |           |       |       |          |          |     |          |     | +      |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`jacobi_stencil`         | +                |     |         |     |           |       |       |          |          |     |          |     | +      |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`k_nearest_neighbor`     | + [ISU]_ [IBNP]_ |     |         |     |           |       |       |          |          |     |          |     |        |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`knn_naive1`             | +                |     |         |     |           |       |       |          |          |     |          |     |        |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`lattice_boltzmann_D2Q9` | + [ISU]_ [IBNP]_ |     |         |     |           |       |       |          |          |     |          |     |        |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`lbm_2d`                 | + [ISU]_ [IBNP]_ |     |         |     |           |       |       |          |          |     |          |     |        |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`lbm_3d`                 | +                |     |         |     |           |       |       |          |          |     |          |     |        |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`leibnitz_pi`            | +                |     |         | +   |           |       |       | +        |          | +   |          | +   |        |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`lmm_swaption_vec`       | + [ISU]_ [IBNP]_ |     |         |     |           |       |       |          |          |     |          |     |        |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`lu`                     | +                |     |         |     |           |       |       |          |          |     |          |     |        |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`mc`                     | +                |     |         |     |           |       |       |          |          |     |          |     |        |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`mxmul`                  | +                |     |         |     |           |       |       |          |          |     |          |     |        |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`nbody`                  | +                |     |         |     |           |       |       |          |          |     |          |     | +      |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`nbody_nice`             | + [ISU]_         |     |         |     |           |       |       |          |          |     |          |     | +      |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`ndstencil`              | +                |     |         |     |           |       |       |          |          |     |          |     |        |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`point27`                | + [BH]_          |     |         |     |           |       |       |          |          |     |          |     |        |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`pricing`                | + [ISU]_         |     |         |     |           |       |       |          |          |     |          |     |        |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`reactiondiffusion`      |                  |     |         |     |           |       |       |          |          |     |          |     | +      |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`rosenbrock`             | +                |     |         | +   |           |       |       | + [ISU]_ |          | +   |          | +   |        |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`shallow_water`          | +                |     |         | +   |           |       | +     |          |          |     |          |     | +      |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`snakes_and_ladders`     | + [ISU]_         |     |         |     |           |       |       |          |          |     |          |     |        |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`sor`                    | +                |     |         |     |           |       |       |          |          |     |          |     |        |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`synth`                  | +                |     |         |     |           |       |       |          |          |     |          |     |        |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`synth_inplace`          | +                |     |         |     |           |       |       |          |          |     |          |     |        |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`synth_stream`           | +                |     |         |     |           |       |       |          |          |     |          |     |        |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+
| :ref:`wireworld`              | + [ISU]_         |     |         |     |           |       |       |          |          |     |          |     |        |
+-------------------------------+------------------+-----+---------+-----+-----------+-------+-------+----------+----------+-----+----------+-----+--------+

.. [ISU] The implementation has issues... such as not using of Benchpress, segfaults, or does not run with Bohrium.
.. [BH] The implementation makes use of Bohrium specific features, which means that Bohrum is required to run it.
.. [IBNP] The implementation does `import bohrium as np`, which breaks the Bohrium dogma "High-Performance NumPy without changing a single line of code.
    



.. _black_scholes:

Black Scholes
=============

.. include:: ../../benchmarks/black_scholes/readme.rst


.. _black_scholes_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/black_scholes/python_numpy/black_scholes.py
   :language: python


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


.. error:: There are issues with the implementation.


.. include:: ../../benchmarks/black_scholes/cpp11_eigen/issues.rst

The above warning is concerned with the implementation below.


.. literalinclude:: ../../benchmarks/black_scholes/cpp11_eigen/src/black_scholes.cpp
   :language: cpp


.. _black_scholes_cpp11_seq:

Cpp11 Seq
---------


.. literalinclude:: ../../benchmarks/black_scholes/cpp11_seq/src/black_scholes.cpp
   :language: cpp


.. _black_scholes_csharp_numcil:

Csharp Numcil
-------------


.. literalinclude:: ../../benchmarks/black_scholes/csharp_numcil/src/black_scholes.cs
   :language: csharp


.. _convolve:

Convolve
========


.. _convolve_python_numpy:

Python Numpy
------------


.. error:: There are issues with the implementation.


.. include:: ../../benchmarks/convolve/python_numpy/issues.rst

The above warning is concerned with the implementation below.


.. note:: There is Bohrium-specific code this implementation, this means Bohrium is required to run it.


.. include:: ../../benchmarks/convolve/python_numpy/bohrium.rst

The above note is concerned with the implementation below.


.. literalinclude:: ../../benchmarks/convolve/python_numpy/convolve.py
   :language: python


.. _convolve_2d:

Convolve 2D
===========


.. _convolve_2d_python_numpy:

Python Numpy
------------


.. error:: There are issues with the implementation.


.. include:: ../../benchmarks/convolve_2d/python_numpy/issues.rst

The above warning is concerned with the implementation below.


.. note:: There is Bohrium-specific code this implementation, this means Bohrium is required to run it.


.. include:: ../../benchmarks/convolve_2d/python_numpy/bohrium.rst

The above note is concerned with the implementation below.


.. literalinclude:: ../../benchmarks/convolve_2d/python_numpy/convolve_2d.py
   :language: python


.. _convolve_3d:

Convolve 3D
===========


.. _convolve_3d_python_numpy:

Python Numpy
------------


.. error:: There are issues with the implementation.


.. include:: ../../benchmarks/convolve_3d/python_numpy/issues.rst

The above warning is concerned with the implementation below.


.. note:: There is Bohrium-specific code this implementation, this means Bohrium is required to run it.


.. include:: ../../benchmarks/convolve_3d/python_numpy/bohrium.rst

The above note is concerned with the implementation below.


.. literalinclude:: ../../benchmarks/convolve_3d/python_numpy/convolve_3d.py
   :language: python


.. _convolve_separate_std:

Convolve Separate Std
=====================


.. _convolve_separate_std_python_numpy:

Python Numpy
------------


.. error:: There are issues with the implementation.


.. include:: ../../benchmarks/convolve_separate_std/python_numpy/issues.rst

The above warning is concerned with the implementation below.


.. literalinclude:: ../../benchmarks/convolve_separate_std/python_numpy/convolve_separate_std.py
   :language: python


.. _gameoflife:

Gameoflife
==========


.. _gameoflife_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/gameoflife/python_numpy/gameoflife.py
   :language: python


.. _gauss:

Gauss
=====


.. _gauss_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/gauss/python_numpy/gauss.py
   :language: python


.. _heat_equation:

Heat Equation
=============

.. include:: ../../benchmarks/heat_equation/readme.rst


.. _heat_equation_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/heat_equation/python_numpy/heat_equation.py
   :language: python


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


.. error:: There are issues with the implementation.


.. include:: ../../benchmarks/heat_equation/cpp11_opencl/issues.rst

The above warning is concerned with the implementation below.


.. literalinclude:: ../../benchmarks/heat_equation/cpp11_opencl/src/heat_equation.cpp
   :language: cpp


.. _idl_init_bh:

Idl Init Bh
===========


.. _idl_init_bh_python_numpy:

Python Numpy
------------


.. error:: There are issues with the implementation.


.. include:: ../../benchmarks/idl_init_bh/python_numpy/issues.rst

The above warning is concerned with the implementation below.


.. literalinclude:: ../../benchmarks/idl_init_bh/python_numpy/idl_init_bh.py
   :language: python


.. _idl_init_fast:

Idl Init Fast
=============


.. _idl_init_fast_python_numpy:

Python Numpy
------------


.. error:: There are issues with the implementation.


.. include:: ../../benchmarks/idl_init_fast/python_numpy/issues.rst

The above warning is concerned with the implementation below.


.. literalinclude:: ../../benchmarks/idl_init_fast/python_numpy/idl_init_fast.py
   :language: python


.. _idl_init_orig:

Idl Init Orig
=============


.. _idl_init_orig_python_numpy:

Python Numpy
------------


.. error:: There are issues with the implementation.


.. include:: ../../benchmarks/idl_init_orig/python_numpy/issues.rst

The above warning is concerned with the implementation below.


.. literalinclude:: ../../benchmarks/idl_init_orig/python_numpy/idl_init_orig.py
   :language: python


.. _jacobi:

Jacobi
======

.. include:: ../../benchmarks/jacobi/readme.rst


.. _jacobi_python_numpy:

Python Numpy
------------


.. note:: There is Bohrium-specific code this implementation, this means Bohrium is required to run it.


.. include:: ../../benchmarks/jacobi/python_numpy/bohrium.rst

The above note is concerned with the implementation below.


.. literalinclude:: ../../benchmarks/jacobi/python_numpy/jacobi.py
   :language: python


.. _jacobi_csharp_numcil:

Csharp Numcil
-------------


.. literalinclude:: ../../benchmarks/jacobi/csharp_numcil/src/jacobi.cs
   :language: csharp


.. _jacobi_fixed:

Jacobi Fixed
============

.. include:: ../../benchmarks/jacobi_fixed/readme.rst


.. _jacobi_fixed_python_numpy:

Python Numpy
------------


.. note:: There is Bohrium-specific code this implementation, this means Bohrium is required to run it.


.. include:: ../../benchmarks/jacobi_fixed/python_numpy/bohrium.rst

The above note is concerned with the implementation below.


.. literalinclude:: ../../benchmarks/jacobi_fixed/python_numpy/jacobi_fixed.py
   :language: python


.. _jacobi_fixed_csharp_numcil:

Csharp Numcil
-------------


.. literalinclude:: ../../benchmarks/jacobi_fixed/csharp_numcil/src/jacobi_fixed.cs
   :language: csharp


.. _jacobi_solve:

Jacobi Solve
============

.. include:: ../../benchmarks/jacobi_solve/readme.rst


.. _jacobi_solve_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/jacobi_solve/python_numpy/jacobi_solve.py
   :language: python


.. _jacobi_solve_csharp_numcil:

Csharp Numcil
-------------


.. literalinclude:: ../../benchmarks/jacobi_solve/csharp_numcil/src/jacobi_solve.cs
   :language: csharp


.. _jacobi_stencil:

Jacobi Stencil
==============

.. include:: ../../benchmarks/jacobi_stencil/readme.rst


.. _jacobi_stencil_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/jacobi_stencil/python_numpy/jacobi_stencil.py
   :language: python


.. _jacobi_stencil_csharp_numcil:

Csharp Numcil
-------------


.. literalinclude:: ../../benchmarks/jacobi_stencil/csharp_numcil/src/jacobi_stencil.cs
   :language: csharp


.. _k_nearest_neighbor:

K Nearest Neighbor
==================

.. include:: ../../benchmarks/k_nearest_neighbor/readme.rst


.. _k_nearest_neighbor_python_numpy:

Python Numpy
------------


.. error:: There are issues with the implementation.


.. include:: ../../benchmarks/k_nearest_neighbor/python_numpy/issues.rst

The above warning is concerned with the implementation below.


.. literalinclude:: ../../benchmarks/k_nearest_neighbor/python_numpy/k_nearest_neighbor.py
   :language: python


.. _knn_naive1:

Knn Naive1
==========

.. include:: ../../benchmarks/knn_naive1/readme.rst


.. _knn_naive1_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/knn_naive1/python_numpy/knn_naive1.py
   :language: python


.. _lattice_boltzmann_D2Q9:

Lattice Boltzmann D2Q9
======================

.. include:: ../../benchmarks/lattice_boltzmann_D2Q9/readme.rst


.. _lattice_boltzmann_D2Q9_python_numpy:

Python Numpy
------------


.. error:: There are issues with the implementation.


.. include:: ../../benchmarks/lattice_boltzmann_D2Q9/python_numpy/issues.rst

The above warning is concerned with the implementation below.


.. literalinclude:: ../../benchmarks/lattice_boltzmann_D2Q9/python_numpy/lattice_boltzmann_D2Q9.py
   :language: python


.. _lbm_2d:

Lbm 2D
======

.. include:: ../../benchmarks/lbm_2d/readme.rst


.. _lbm_2d_python_numpy:

Python Numpy
------------


.. error:: There are issues with the implementation.


.. include:: ../../benchmarks/lbm_2d/python_numpy/issues.rst

The above warning is concerned with the implementation below.


.. literalinclude:: ../../benchmarks/lbm_2d/python_numpy/lbm_2d.py
   :language: python


.. _lbm_3d:

Lbm 3D
======

.. include:: ../../benchmarks/lbm_3d/readme.rst


.. _lbm_3d_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/lbm_3d/python_numpy/lbm_3d.py
   :language: python


.. _leibnitz_pi:

Leibnitz Pi
===========

.. include:: ../../benchmarks/leibnitz_pi/readme.rst


.. _leibnitz_pi_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/leibnitz_pi/python_numpy/leibnitz_pi.py
   :language: python


.. _leibnitz_pi_c99_seq:

C99 Seq
-------


.. literalinclude:: ../../benchmarks/leibnitz_pi/c99_seq/src/leibnitz_pi.c
   :language: c


.. _leibnitz_pi_cpp11_bxx:

Cpp11 Bxx
---------


.. literalinclude:: ../../benchmarks/leibnitz_pi/cpp11_bxx/src/leibnitz_pi.cpp
   :language: cpp


.. _leibnitz_pi_cpp11_omp:

Cpp11 Omp
---------


.. literalinclude:: ../../benchmarks/leibnitz_pi/cpp11_omp/src/leibnitz_pi.cpp
   :language: cpp


.. _leibnitz_pi_cpp11_seq:

Cpp11 Seq
---------


.. literalinclude:: ../../benchmarks/leibnitz_pi/cpp11_seq/src/leibnitz_pi.cpp
   :language: cpp


.. _lmm_swaption_vec:

Lmm Swaption Vec
================

.. include:: ../../benchmarks/lmm_swaption_vec/readme.rst


.. _lmm_swaption_vec_python_numpy:

Python Numpy
------------


.. error:: There are issues with the implementation.


.. include:: ../../benchmarks/lmm_swaption_vec/python_numpy/issues.rst

The above warning is concerned with the implementation below.


.. literalinclude:: ../../benchmarks/lmm_swaption_vec/python_numpy/lmm_swaption_vec.py
   :language: python


.. _lu:

Lu
==

.. include:: ../../benchmarks/lu/readme.rst


.. _lu_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/lu/python_numpy/lu.py
   :language: python


.. _mc:

Mc
==

.. include:: ../../benchmarks/mc/readme.rst


.. _mc_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/mc/python_numpy/mc.py
   :language: python


.. _mxmul:

Mxmul
=====

.. include:: ../../benchmarks/mxmul/readme.rst


.. _mxmul_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/mxmul/python_numpy/mxmul.py
   :language: python


.. _nbody:

Nbody
=====

.. include:: ../../benchmarks/nbody/readme.rst


.. _nbody_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/nbody/python_numpy/nbody.py
   :language: python


.. _nbody_csharp_numcil:

Csharp Numcil
-------------


.. literalinclude:: ../../benchmarks/nbody/csharp_numcil/src/nbody.cs
   :language: csharp


.. _nbody_nice:

Nbody Nice
==========

.. include:: ../../benchmarks/nbody_nice/readme.rst


.. _nbody_nice_python_numpy:

Python Numpy
------------


.. error:: There are issues with the implementation.


.. include:: ../../benchmarks/nbody_nice/python_numpy/issues.rst

The above warning is concerned with the implementation below.


.. literalinclude:: ../../benchmarks/nbody_nice/python_numpy/nbody_nice.py
   :language: python


.. _nbody_nice_csharp_numcil:

Csharp Numcil
-------------


.. literalinclude:: ../../benchmarks/nbody_nice/csharp_numcil/src/nbody_nice.cs
   :language: csharp


.. _ndstencil:

Ndstencil
=========

.. include:: ../../benchmarks/ndstencil/readme.rst


.. _ndstencil_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/ndstencil/python_numpy/ndstencil.py
   :language: python


.. _point27:

Point27
=======

.. include:: ../../benchmarks/point27/readme.rst


.. _point27_python_numpy:

Python Numpy
------------


.. note:: There is Bohrium-specific code this implementation, this means Bohrium is required to run it.


.. include:: ../../benchmarks/point27/python_numpy/bohrium.rst

The above note is concerned with the implementation below.


.. literalinclude:: ../../benchmarks/point27/python_numpy/point27.py
   :language: python


.. _pricing:

Pricing
=======

.. include:: ../../benchmarks/pricing/readme.rst


.. _pricing_python_numpy:

Python Numpy
------------


.. error:: There are issues with the implementation.


.. include:: ../../benchmarks/pricing/python_numpy/issues.rst

The above warning is concerned with the implementation below.


.. literalinclude:: ../../benchmarks/pricing/python_numpy/pricing.py
   :language: python


.. _reactiondiffusion:

Reactiondiffusion
=================


.. _reactiondiffusion_csharp_numcil:

Csharp Numcil
-------------


.. literalinclude:: ../../benchmarks/reactiondiffusion/csharp_numcil/src/reactiondiffusion.cs
   :language: csharp


.. _rosenbrock:

Rosenbrock
==========

.. include:: ../../benchmarks/rosenbrock/readme.rst


.. _rosenbrock_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/rosenbrock/python_numpy/rosenbrock.py
   :language: python


.. _rosenbrock_c99_seq:

C99 Seq
-------


.. literalinclude:: ../../benchmarks/rosenbrock/c99_seq/src/rosenbrock.c
   :language: c


.. _rosenbrock_cpp11_bxx:

Cpp11 Bxx
---------


.. error:: There are issues with the implementation.


.. include:: ../../benchmarks/rosenbrock/cpp11_bxx/issues.rst

The above warning is concerned with the implementation below.


.. literalinclude:: ../../benchmarks/rosenbrock/cpp11_bxx/src/rosenbrock.cpp
   :language: cpp


.. _rosenbrock_cpp11_omp:

Cpp11 Omp
---------


.. literalinclude:: ../../benchmarks/rosenbrock/cpp11_omp/src/rosenbrock.cpp
   :language: cpp


.. _rosenbrock_cpp11_seq:

Cpp11 Seq
---------


.. literalinclude:: ../../benchmarks/rosenbrock/cpp11_seq/src/rosenbrock.cpp
   :language: cpp


.. _shallow_water:

Shallow Water
=============

.. include:: ../../benchmarks/shallow_water/readme.rst


.. _shallow_water_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/shallow_water/python_numpy/shallow_water.py
   :language: python


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


.. _shallow_water_csharp_numcil:

Csharp Numcil
-------------


.. literalinclude:: ../../benchmarks/shallow_water/csharp_numcil/src/shallow_water.cs
   :language: csharp


.. _snakes_and_ladders:

Snakes And Ladders
==================

.. include:: ../../benchmarks/snakes_and_ladders/readme.rst


.. _snakes_and_ladders_python_numpy:

Python Numpy
------------


.. error:: There are issues with the implementation.


.. include:: ../../benchmarks/snakes_and_ladders/python_numpy/issues.rst

The above warning is concerned with the implementation below.


.. literalinclude:: ../../benchmarks/snakes_and_ladders/python_numpy/snakes_and_ladders.py
   :language: python


.. _sor:

Sor
===

.. include:: ../../benchmarks/sor/readme.rst


.. _sor_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/sor/python_numpy/sor.py
   :language: python


.. _synth:

Synth
=====

.. include:: ../../benchmarks/synth/readme.rst


.. _synth_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/synth/python_numpy/synth.py
   :language: python


.. _synth_inplace:

Synth Inplace
=============

.. include:: ../../benchmarks/synth_inplace/readme.rst


.. _synth_inplace_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/synth_inplace/python_numpy/synth_inplace.py
   :language: python


.. _synth_stream:

Synth Stream
============

.. include:: ../../benchmarks/synth_stream/readme.rst


.. _synth_stream_python_numpy:

Python Numpy
------------


.. literalinclude:: ../../benchmarks/synth_stream/python_numpy/synth_stream.py
   :language: python


.. _wireworld:

Wireworld
=========

.. include:: ../../benchmarks/wireworld/readme.rst


.. _wireworld_python_numpy:

Python Numpy
------------


.. error:: There are issues with the implementation.


.. include:: ../../benchmarks/wireworld/python_numpy/issues.rst

The above warning is concerned with the implementation below.


.. literalinclude:: ../../benchmarks/wireworld/python_numpy/wireworld.py
   :language: python

