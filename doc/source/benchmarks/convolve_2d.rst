

.. _convolve_2d:

Convolve 2D
===========


.. _convolve_2d_python_numpy:

Python Numpy
------------


.. error:: There are issues with the implementation.

    Fails when running with Bohrium::

    

      python -m bohrium convolve_2d.py --size=25 --bohrium=True

    

    Produces the following error::

    

      ~/.local/lib/python2.7/site-packages/bohrium/__main__.py:20: RuntimeWarning: Encounter ing an operation not supported by Bohrium. It will be handled by the original NumPy. execfile(sys.argv[0])

      Segmentation fault (core dumped)

    


.. note:: There is Bohrium-specific code this implementation, this means Bohrium is required to run it.

    The view generator ``bohrium.stdviews`` module is used.

    

    Specifically the ``cartesian`` generator.


.. literalinclude:: ../../../benchmarks/convolve_2d/python_numpy/convolve_2d.py
   :language: python
