

.. _lattice_boltzmann_D2Q9:

Lattice Boltzmann D2Q9
======================

.. include:: ../../../benchmarks/lattice_boltzmann_D2Q9/readme.rst


.. _lattice_boltzmann_D2Q9_python_numpy:

Python Numpy
------------


.. error:: There are issues with the implementation.

    Copies data back and forth between NumPy and Bohrium::

    

      .local/lib/python2.7/site-packages/bohrium/__main__.py:55: RuntimeWarning: Encountering an operation not supported by Bohrium. It will be handled by the original NumPy.

    


.. literalinclude:: ../../../benchmarks/lattice_boltzmann_D2Q9/python_numpy/lattice_boltzmann_D2Q9.py
   :language: python
