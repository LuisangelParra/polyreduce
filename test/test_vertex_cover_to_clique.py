from polyreduce.graph.vertex_cover_instance import VertexCoverInstance
from polyreduce.graph.clique_instance import CliqueInstance
from polyreduce.graph.reductions.vertex_cover_to_clique import VertexCoverToClique


def test_vertex_cover_to_clique_basic():
    # Graph: path 1-2-3-4
    num_vertices = 4
    edges = [(1, 2), (2, 3), (3, 4)]
    k = 2  # {2,3} is a vertex cover

    vc_instance = VertexCoverInstance(
        name="path-vc",
        num_vertices=num_vertices,
        edges=edges,
        k=k,
    )

    reduction = VertexCoverToClique()
    clique_instance = reduction.reduce(vc_instance)

    assert isinstance(clique_instance, CliqueInstance)
    assert clique_instance.num_vertices == num_vertices
    # clique size must be |V| - k
    assert clique_instance.k == num_vertices - k

    # Check complement construction: no original edges appear in the complement
    original = set(tuple(sorted(e)) for e in edges)
    for (u, v) in clique_instance.edges:
        assert (min(u, v), max(u, v)) not in original
