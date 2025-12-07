from polyreduce.graph import GraphInstance

def test_graph_instance_basic():
    G = GraphInstance(
        name="g1",
        num_vertices=4,
        edges=[(1,2), (2,3), (3,4)]
    )

    assert G.degree(2) == 2
    assert G.has_edge(1,2)
    assert not G.has_edge(1,3)
    assert G.neighbors(3) == {2,4}
