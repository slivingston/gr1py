# Copyright (c) 2015 by California Institute of Technology
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:

# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.

# 3. Neither the name of the California Institute of Technology nor
#    the names of its contributors may be used to endorse or promote
#    products derived from this software without specific prior
#    written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL CALTECH OR THE
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""Minimalistic dictionary-based graph and digraph objects

The primary design goal is to be an API-compatible, drop-in replacement
for basic yet crucial parts of NetworkX. While a few basic algorithms
may eventually be added, there is no intent to achieve the full
capabilities of NetworkX for random graph generation, isomorphism
checking, export/import routines, etc.

At least compatible with Python versions 2.6 and 2.7.


SCL; 22 Oct 2015
"""


class DiGraph(object):
    def __init__(self):
        self.node = dict()
        self.edge = dict()

    def number_of_nodes(self):
        return len(self.node)

    def add_node(self, x, attr=None):
        if attr is None:
            self.node[x] = dict()
        else:
            self.node[x] = attr

    def add_nodes_from(self, nbunch):
        for nodetuple in nbunch:
            if isinstance(nodetuple, tuple):
                self.add_node(*nodetuple)
            else:
                self.add_node(nodetuple)

    def add_edge(self, x, y, attr=None):
        if x not in self.node:
            self.add_node(x)
        if y not in self.node:
            self.add_node(y)
        if x not in self.edge:
            self.edge[x] = {y: dict()}
        if y not in self.edge[x]:
            if attr is None:
                self.edge[x][y] = dict()
            else:
                self.edge[x][y] = attr
        else:
            if attr is not None:
                self.node[x][y].update(attr)

    def add_edges_from(self, ebunch):
        for edgetuple in ebunch:
            self.add_edge(*edgetuple)

    def has_edge(self, x, y):
        if x in self.edge and y in self.edge[x]:
            return True
        else:
            return False

    def nodes(self, data=False):
        if data:
            return self.node.items()
        else:
            return self.node.keys()

    def nodes_iter(self, data=False):
        if data:
            return self.node.iteritems()
        else:
            return self.node.iterkeys()

    def edges_iter(self, data=False):
        for x, yd in self.edge.iteritems():
            for y in yd.iterkeys():
                if data:
                    yield x, y, yd[y]
                else:
                    yield x, y

    def successors(self, x):
        return self.edge[x].keys()

    def successors_iter(self, x):
        return self.edge[x].iterkeys()

    def predecessors(self, x):
        return [u for u in self.predecessors_iter(x)]

    def predecessors_iter(self, x):
        for u, yd in self.edge.iteritems():
            if x in yd.iterkeys():
                yield u

    def in_edges_iter(self, x):
        for u in self.predecessors_iter(x):
            yield (u, x)

    def in_edges(self, x):
        return [e for e in self.in_edges_iter(x)]

    def remove_node(self, x):
        if x in self.node:
            del self.node[x]
        if x in self.edge:
            del self.edge[x]
        for y in self.edge.iterkeys():
            if x in self.edge[y]:
                del self.edge[y][x]

    def remove_edge(self, u, v):
        if u in self.edge and v in self.edge[u]:
            del self.edge[u][v]

    def remove_edges_from(self, ebunch):
        for edgetuple in ebunch:
            self.remove_edge(*edgetuple)
