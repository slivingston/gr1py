gr1py
=====

**gr1py** is an enumerative (or concrete) reactive synthesis tool for the GR(1)
fragment of LTL. It is pure Python.

Scott C. Livingston  <slivingston@cds.caltech.edu>

[![Build Status](https://travis-ci.org/slivingston/gr1py.svg?branch=master)](https://travis-ci.org/slivingston/gr1py)


Input formats
-------------

The default input format is that of [gr1c](http://scottman.net/2012/gr1c).


Output formats
--------------

These are selected from the command-line using the `-t` switch. Each corresponds
to a function in `gr1py.output`.

* `json` : [gr1c JSON](http://slivingston.github.io/gr1c/md_formats.html#gr1cjson)
* `dot` : [Graphviz dot](http://www.graphviz.org)


License
-------

This is free software released under the terms of [the BSD 3-Clause License]
(http://opensource.org/licenses/BSD-3-Clause).  There is no warranty; not even
for merchantability or fitness for a particular purpose.  Consult LICENSE for
copying conditions.
