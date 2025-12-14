from polyreduce.graph.vertex_cover_instance import VertexCoverInstance
from polyreduce.graph.reductions.vertex_cover_to_clique import VertexCoverToClique
from polyreduce.sat.solvers.pysat_solver import PySatSolver


def test_vertex_cover_to_clique_preserves_sat():
    solver = PySatSolver()
    reduce = VertexCoverToClique()

    # ---------- TRUE ----------
    vc_true = VertexCoverInstance(
        name="vc_true",
        num_vertices=6,
        edges=[
            (1,2),(2,3),(3,4),(4,5),(5,6),(6,1)
        ],
        k=3,
    )

    clique_true = reduce.reduce(vc_true)

    print("SOURCE TRUE:", vc_true)
    print("TARGET TRUE:", clique_true)

    assert vc_true.to_sat().is_satisfiable(solver) is True
    assert clique_true.to_sat().is_satisfiable(solver) is True

    # ---------- FALSE ----------
    vc_false = VertexCoverInstance(
        name="vc_false",
        num_vertices=6,
        edges=[
            (1,2),(2,3),(3,4),(4,5),(5,6),(6,1)
        ],
        k=2,
    )

    clique_false = reduce.reduce(vc_false)

    print("SOURCE FALSE:", vc_false)
    print("TARGET FALSE:", clique_false)

    assert vc_false.to_sat().is_satisfiable(solver) is False
    assert clique_false.to_sat().is_satisfiable(solver) is False
