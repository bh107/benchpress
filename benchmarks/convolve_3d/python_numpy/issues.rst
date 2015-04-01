Fails when running with Bohrium::

  python -m bohrium convolve_3d.py --size=25 --bohrium=True

Produces the following error::

  .local/lib/python2.7/site-packages/bohrium/__main__.py:21: RuntimeWarning: Encountering an operation not supported by Bohrium. It will be handled by the original NumPy.
    else:
  Segmentation fault (core dumped)

