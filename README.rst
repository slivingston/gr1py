gr1py
=====

**gr1py** is an enumerative (or concrete) reactive synthesis tool for the GR(1)
fragment of LTL. It is pure Python.


Installation
------------

Releases are available from the `Python Package Index
<https://pypi.org/>`_ at https://pypi.org/project/gr1py/
To get it from there and check the version, try ::

  pip install gr1py
  gr1py -V

`pip <https://pip.pypa.io>`_ should get dependencies for you if you do not have
them. They are

* PLY (https://www.dabeaz.com/ply/)

If it is available, NetworkX (https://networkx.github.io/) will be used.
However, it is not required.  A simple built-in class for directed graphs will
be used if NetworkX is not found.

If you want to hack on gr1py, clone the repository from
https://github.com/slivingston/gr1py.git

Current `CI server report <https://github.com/slivingston/gr1py/actions/workflows/main.yml>`_:

.. image:: https://github.com/slivingston/gr1py/actions/workflows/main.yml/badge.svg
   :alt: build status from GitHub Actions


Examples
--------

Besides the Python package, a script named ``gr1py`` is installed that provides
access to several routines from the command-line. Consider the file named
examples/arbiter3.spc that is included in the source release. To check that the
specification defined by it can be realized, try ::

  gr1py -r examples/arbiter3.spc

To synthesize a winning strategy and dump it in the Graphviz DOT format, try ::

  gr1py -t dot examples/arbiter3.spc > arbiter3-fsm.dot
  dot -Tsvg -O arbiter3-fsm.dot

where the second command uses the program ``dot`` (part of Graphviz) to create
an SVG file, likely named arbiter3-fsm.dot.svg; e.g., the file can be displayed
using a Web browser or Inkscape.

A summary of command-line usage can be obtained by ``grpy -h``.


Input formats
-------------

The default input format is that of gr1c (http://scottman.net/2012/gr1c).


Output formats
--------------

These are selected from the command-line using the ``-t`` switch.  Each
corresponds to a function in ``gr1py.output``.

* ``json`` : `gr1c JSON <https://tulip-control.github.io/gr1c/md_formats.html#gr1cjson>`_
* ``dot`` : `Graphviz dot <http://www.graphviz.org>`_


Feedback and contributing
-------------------------

Bug reports, feature requests, and comments can be submitted via the `project
issue tracker <https://github.com/slivingston/gr1py/issues>`_ or via email to
the authors.

Code contributions are welcome. To avoid redundant effort, please check for an
existing issue or other indication of prior or intended work before starting.
When ready for review, send a `pull request <https://github.com/slivingston/gr1py/pulls>`_.


License
-------

This is free software released under the terms of `the BSD 3-Clause License
<https://opensource.org/licenses/BSD-3-Clause>`_.  There is no warranty; not
even for merchantability or fitness for a particular purpose.  Consult LICENSE
for copying conditions.
