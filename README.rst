gr1py
=====

**gr1py** is an enumerative (or concrete) reactive synthesis tool for the GR(1)
fragment of LTL. It is pure Python.


Installation
------------

[![Build Status](https://travis-ci.org/slivingston/gr1py.svg?branch=master)](https://travis-ci.org/slivingston/gr1py)

Releases are available from the `Python Package Index
<https://pypi.python.org/pypi>`_ at https://pypi.python.org/pypi/gr1py
To get it from there and check the version, try ::

  pip install gr1py
  gr1py -V

[pip](https://pip.pypa.io) should get dependencies for you if you do not have
them. They are

* PLY (http://www.dabeaz.com/ply/)
* NetworkX (http://networkx.lanl.gov)

If you want to hack on gr1py, clone the repository from
https://github.com/slivingston/gr1py.git


Input formats
-------------

The default input format is that of gr1c (http://scottman.net/2012/gr1c).


Output formats
--------------

These are selected from the command-line using the ``-t`` switch. Each
corresponds to a function in ``gr1py.output``.

* ``json`` : `gr1c JSON <http://slivingston.github.io/gr1c/md_formats.html#gr1cjson>`_
* ``dot`` : `Graphviz dot <http://www.graphviz.org>`_


Feedback and contributing
-------------------------

Bug reports, feature requests, and comments can be submitted via the `project
issue tracker <https://github.com/slivingston/gr1py/issues>`_ or via email to
the authors.


Authors
-------

Scott C. Livingston  <slivingston@cds.caltech.edu>


License
-------

This is free software released under the terms of `the BSD 3-Clause License
<http://opensource.org/licenses/BSD-3-Clause>`_.  There is no warranty; not even
for merchantability or fitness for a particular purpose.  Consult LICENSE for
copying conditions.
