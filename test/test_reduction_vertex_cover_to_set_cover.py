from polyreduce.graph.vertex_cover_instance import VertexCoverInstance
from polyreduce.set.reductions.vertex_cover_to_set_cover import VertexCoverToSetCover
from polyreduce.sat.solvers.pysat_solver import PySatSolver


def test_vertex_cover_to_set_cover_preserves_sat():
    solver = PySatSolver()
    reduce = VertexCoverToSetCover()

    # ---------- TRUE ----------
    vc_true = VertexCoverInstance(
        name="vc_true",
        num_vertices=6,
        edges=[
            (1,2),(2,3),(3,4),(4,5),(5,6),(6,1)
        ],
        k=3,
    )

    sc_true = reduce.reduce(vc_true)

    print("SOURCE TRUE:", vc_true)
    print("TARGET TRUE:", sc_true)

    assert vc_true.to_sat().is_satisfiable(solver) is True
    assert sc_true.to_sat().is_satisfiable(solver) is True

    # ---------- FALSE ----------
    vc_false = VertexCoverInstance(
        name="vc_false",
        num_vertices=6,
        edges=[
            (1,2),(2,3),(3,4),(4,5),(5,6),(6,1)
        ],
        k=2,
    )

    sc_false = reduce.reduce(vc_false)

    print("SOURCE FALSE:", vc_false)
    print("TARGET FALSE:", sc_false)

    assert vc_false.to_sat().is_satisfiable(solver) is False
    assert sc_false.to_sat().is_satisfiable(solver) is False
