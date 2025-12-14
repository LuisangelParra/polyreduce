from polyreduce.graph.independent_set_instance import IndependentSetInstance
from polyreduce.graph.reductions.is_to_vertex_cover import IndependentSetToVertexCover
from polyreduce.sat.solvers.pysat_solver import PySatSolver


def test_independent_set_to_vertex_cover_preserves_sat():
    solver = PySatSolver()
    reduce = IndependentSetToVertexCover()

    # ---------- TRUE ----------
    is_true = IndependentSetInstance(
        name="is_true",
        num_vertices=6,
        edges=[
            (1,2),(2,3),(3,4),(4,5),(5,6),(6,1)
        ],
        k=3,
    )

    vc_true = reduce.reduce(is_true)

    print("SOURCE TRUE:", is_true)
    print("TARGET TRUE:", vc_true)

    assert is_true.to_sat().is_satisfiable(solver) is True
    assert vc_true.to_sat().is_satisfiable(solver) is True

    # ---------- FALSE ----------
    is_false = IndependentSetInstance(
        name="is_false",
        num_vertices=6,
        edges=[
            (1,2),(2,3),(3,4),(4,5),(5,6),(6,1)
        ],
        k=4,
    )

    vc_false = reduce.reduce(is_false)

    print("SOURCE FALSE:", is_false)
    print("TARGET FALSE:", vc_false)

    assert is_false.to_sat().is_satisfiable(solver) is False
    assert vc_false.to_sat().is_satisfiable(solver) is False
