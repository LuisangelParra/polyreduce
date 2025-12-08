from polyreduce.graph.clique_instance import CliqueInstance
from polyreduce.reductions.clique_to_is import CliqueToIndependentSet

def test_clique_to_independent_set_reduction():
    # Graph with a triangle clique: 1-2-3
    clique = CliqueInstance(
        name="triangle",
        num_vertices=3,
        edges=[(1,2), (2,3), (1,3)],
        k=3
    )

    reducer = CliqueToIndependentSet()
    ind = reducer.reduce(clique)

    # In complement graph, edges are missing where clique was complete
    assert not ind.has_edge(1,2)
    assert not ind.has_edge(2,3)
    assert not ind.has_edge(1,3)
