============
Installation
============

Benchpress is distributed via PyPi and Github. Which means that you can install it as a Python package (from PyPi) or use it directly from an unpacked tarball or git-clone from Github.com.
The installation method of choice is based on what you want to do with Benchpress. Recommendations are as follows.

 * Install Benchpress as a Python packages from PyPi if your sole intent is to `run` benchmarks.
 * Use Benchpress directly from clone/tarball if you intend to modify it. Such as adding benchmarks, changing commands or benchmark suites.

.. note:: Benchpress is designed to work, with minimal friction, in an environment where the user has limited system permissions. Such as shared computing environments, clusters and supercomputers. A system-wide installation of Benchpress is therefore untested. However, it should work if write permission is assigned to Benchpress users for the ``benchmarks`` folder.


From pypi.python.org
--------------------

The following shows how to do a user-mode / local installation::

  pip install benchpress --user

Extend your ``$PATH``, such that the commands (`bp_info`, `bp_run`, `bp_times`, `bp_compile`, `and bp_grapher`) are readily available::

  export PATH=$PATH:$HOME/.local/bin

When you are done using Benchpress, purging it from your system is as easy as::

  pip uninstall benchpress

From clone or tarball
---------------------

Clone the repos::

  git clone git@bitbucket.org:bohrium/benchpress.git
  cd benchpress

or download and unpack a tarball::

  wget https://bitbucket.org/bohrium/benchpress/get/master.tar.gz
  tar xzvf master.tar.gz
  cd bohrium-benchpress-*

For Benchpress to operate correctly you `must` extend the two ``PATH`` and ``PYTHONPATH``. Extend ``PATH`` to include the subfolder ``bin`` and extend ``PYTHONPATH`` to include the subfolder ``module``. You can do this in whatever way your system requires, you will most likely be able to do the following::

  source util/setbpenv.bash

Make sure you persists the changes.
