from polyreduce.graph.independent_set_instance import IndependentSetInstance
from polyreduce.graph.reductions.is_to_vertex_cover import IndependentSetToVertexCover

def test_independent_set_to_vertex_cover():
    # Graph: triangle
    edges = [(1,2), (2,3), (1,3)]

    inst = IndependentSetInstance(
        name="triangle",
        num_vertices=3,
        edges=edges,
        k=1   # only single-vertex IS possible
    )

    reducer = IndependentSetToVertexCover()
    vc = reducer.reduce(inst)

    assert vc.k == 3 - 1    # |V| - k = 2
    assert vc.has_edge(1,2)
    assert vc.has_edge(1,3)
