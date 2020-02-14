from gr1py.minnx import DiGraph


class DiGraph_test(object):
    def setUp(self):
        self.G = DiGraph()

    def tearDown(self):
        self.G = None

    def test_add_remove_nodes(self):
        assert self.G.number_of_nodes() == 0
        self.G.add_node(0)
        assert self.G.number_of_nodes() == 1
        self.G.add_nodes_from(range(10))
        assert self.G.number_of_nodes() == 10
        self.G.remove_node(0)
        assert self.G.number_of_nodes() == 9

    def test_add_remove_edges(self):
        assert self.G.number_of_nodes() == 0
        self.G.add_edge(0,1)
        assert self.G.number_of_nodes() == 2
        self.G.add_edge(0,2)
        assert self.G.number_of_nodes() == 3
        self.G.remove_edge(0,1)
        assert self.G.number_of_nodes() == 3
        assert self.G.has_edge(0, 2) and not self.G.has_edge(0, 1)

    def test_add_remove_edges_from(self):
        assert self.G.number_of_nodes() == 0
        self.G.add_edges_from([(0,1), (0,2)])
        assert self.G.number_of_nodes() == 3
        self.G.add_edges_from([(0,1), (1,3)])
        assert self.G.number_of_nodes() == 4
        self.G.remove_edges_from([(0,2), (0,1)])
        assert self.G.number_of_nodes() == 4
        assert self.G.has_edge(1, 3)
        assert not self.G.has_edge(0, 2) and not self.G.has_edge(0, 1)
