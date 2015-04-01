=====
Tools
=====

Installation
============

Benchpress is distributed as a Python package via PyPi. It can also be used directly from an unpacked tar-ball or from a git-clone.

From pypi.python.org
--------------------

The following shows how to do a user-mode / local installation::

  pip install benchpress --user

Extend your ``$PATH``, such that the commands (`bp_run`, `bp_times`, `bp_compile`, `and bp_grapher`) are readily available::

  export PATH=$PATH:$HOME/.local/bin

The benchmark implementations are available in ``$HOME/.local/share/benchpress/benchmarks``.

The benchmark suites are avaiable in ``$HOME/.local/share/suites``.

When using this approach uninstall is equally simple::

  pip uninstall benchpress

You can do a system-wide installation by omitting the ``--user`` flag. If you do a system-wide installation then extending ``$PATH`` is not required.
Additionally, implementations and suites will be avaiable are operating systems ``share`` location instead of ``.local``.

From clone or tarball
---------------------

Clone the repos::

  git clone git@bitbucket.org:bohrium/benchpress.git
  cd benchpress

or download and unpack tarball::

  wget https://bitbucket.org/bohrium/benchpress/get/master.tar.gz
  tar xzvf master.tar.gz
  cd bohrium-benchpress-*

Then set your ``$PATH`` to the directory you have cloned or extracted to.
Set your ``$PYTHONPATH`` to the benchpress subdirectory.

If you do not want to set paths then your working directory must be the root of the clone/tarball.

Cli
===

bp_run
------

...

bp_times
--------

...

bp_grapher
----------

...

Implementations / Libraries / Modules
=====================================

Python
------

...

C / C++
-------

...

Protocol
========

...
