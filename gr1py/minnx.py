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


class NodesView(object):
    def __init__(self):
        self.nodes = dict()

    def __len__(self):
        return len(self.nodes)

    def __contains__(self, k):
        return k in self.nodes

    def __getitem__(self, k):
        return self.nodes[k]

    def __setitem__(self, k, v):
        self.nodes[k] = v

    def __delitem__(self, k):
        del self.nodes[k]

    def __call__(self, data=False):
        if data:
            return self.nodes.items()
        else:
            return self.nodes.keys()


class EdgesView(object):
    def __init__(self):
        self.edges = dict()

    def __contains__(self, k):
        return k in self.edges

    def __getitem__(self, k):
        return self.edges[k]

    def __setitem__(self, k, v):
        self.edges[k] = v

    def __call__(self, data=False):
        for x, yd in self.edges.items():
            for y in yd.keys():
                if data:
                    yield x, y, yd[y]
                else:
                    yield x, y

    def items(self):
        for k, v in self.edges.items():
            yield k, v

    def keys(self):
        for k in self.edges:
            yield k


class DiGraph(object):
    def __init__(self):
        self.nodes = NodesView()
        self.edges = EdgesView()

    def number_of_nodes(self):
        return len(self.nodes)

    def add_node(self, x, **attr):
        if attr is None:
            attr = dict()
        if x not in self.nodes:
            self.nodes[x] = attr
        else:
            self.nodes[x].update(attr)

    def add_nodes_from(self, nbunch):
        for nodetuple in nbunch:
            if isinstance(nodetuple, tuple):
                node, attr = nodetuple
                self.add_node(node, **attr)
            else:
                self.add_node(nodetuple)

    def add_edge(self, x, y, **attr):
        if x not in self.nodes:
            self.add_node(x)
        if y not in self.nodes:
            self.add_node(y)
        if x not in self.edges:
            self.edges[x] = {y: dict()}
        if y not in self.edges[x]:
            self.edges[x][y] = attr
        else:
            self.edges[x][y].update(attr)

    def add_edges_from(self, ebunch):
        for edgetuple in ebunch:
            self.add_edge(*edgetuple)

    def has_edge(self, x, y):
        if x in self.edges and y in self.edges[x]:
            return True
        else:
            return False

    def nodes_list(self, data=False):
        if data:
            return self.nodes.items()
        else:
            return self.nodes.keys()

    def successors_list(self, x):
        return self.edges[x].keys()

    def successors(self, x):
        return self.edges[x].keys()

    def predecessors_list(self, x):
        return [u for u in self.predecessors(x)]

    def predecessors(self, x):
        for u, yd in self.edges.items():
            if x in yd.keys():
                yield u

    def in_edges(self, x):
        for u in self.predecessors(x):
            yield (u, x)

    def in_edges_list(self, x):
        return [e for e in self.in_edges(x)]

    def remove_node(self, x):
        if x in self.nodes:
            del self.nodes[x]
        if x in self.edges:
            del self.edges[x]
        for y in self.edges.keys():
            if x in self.edges[y]:
                del self.edges[y][x]

    def remove_edge(self, u, v):
        if u in self.edges and v in self.edges[u]:
            del self.edges[u][v]

    def remove_edges_from(self, ebunch):
        for edgetuple in ebunch:
            self.remove_edge(*edgetuple)
