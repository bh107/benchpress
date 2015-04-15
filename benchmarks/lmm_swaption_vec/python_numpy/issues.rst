Error when running with Bohrium::

  Traceback (most recent call last):
    File "/usr/lib/python2.7/runpy.py", line 162, in _run_module_as_main
      "__main__", fname, loader, pkg_name)
    File "/usr/lib/python2.7/runpy.py", line 72, in _run_code
      exec code in run_globals
    File "/home/safl/.local/lib/python2.7/site-packages/bohrium/__main__.py", line 20, in <module>
      execfile(sys.argv[0])
    File "LMM_swaption_vec.py", line 108, in <module>
      main()
    File "LMM_swaption_vec.py", line 56, in main
      eps = np.concatenate((eps_tmp,-eps_tmp), axis = 1)
  AttributeError: 'module' object has no attribute 'concatenate'

