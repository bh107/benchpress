============
Installation
============

Benchpress is distributed via PyPi and Github, which means that you can install it from a Python package (from PyPi) or directly from an unpacked tarball or git-clone from Github.com.

.. note:: Benchpress is designed to work, with minimal friction, in an environment where the user has limited system permissions. Such as shared computing environments, clusters and supercomputers. A system-wide installation of Benchpress is therefore untested. However, it should work if write permission is assigned to Benchpress users for the ``benchmarks`` folder.


From pypi.python.org
--------------------

The following shows how to do a user-mode / local installation::

  pip install benchpress --user

Extend your ``$PATH``, such that the binaries (`bp-run`, `bp-run`, `bp-cli`, `bp-chart`) are readily available::

  export PATH=$PATH:$HOME/.local/bin

When you are done using Benchpress, purging it from your system is as easy as::

  pip uninstall benchpress

From clone or tarball
---------------------

Clone the repos::

  git clone https://github.com/bh107/benchpress.git
  cd benchpress

or download and unpack a tarball::

  wget https://github.com/bh107/benchpress/archive/master.zip
  unzip master.zip
  cd bohrium-benchpress

And install it::

  pip install . --user


When developing Benchpress use PyPi's developer installation:

  pip install . --user -e

