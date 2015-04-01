Fails when running with Bohrium::

  python -m bohrium convolve_2d.py --size=25 --bohrium=True

Produces the following error::

  ~/.local/lib/python2.7/site-packages/bohrium/__main__.py:20: RuntimeWarning: Encounter ing an operation not supported by Bohrium. It will be handled by the original NumPy. execfile(sys.argv[0])
  Segmentation fault (core dumped)

