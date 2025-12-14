from polyreduce.graph.clique_instance import CliqueInstance
from polyreduce.graph.reductions.clique_to_independent_set import CliqueToIndependentSet
from polyreduce.sat.solvers.pysat_solver import PySatSolver


def test_clique_to_independent_set_preserves_sat():
    solver = PySatSolver()
    reduce = CliqueToIndependentSet()

    # ---------- TRUE ----------
    clique_true = CliqueInstance(
        name="clique_true",
        num_vertices=5,
        edges=[
            (1,2),(1,3),(2,3),
            (3,4),(4,5)
        ],
        k=3,
    )

    is_true = reduce.reduce(clique_true)

    print("SOURCE TRUE:", clique_true)
    print("TARGET TRUE:", is_true)

    assert clique_true.to_sat().is_satisfiable(solver) is True
    assert is_true.to_sat().is_satisfiable(solver) is True

    # ---------- FALSE ----------
    clique_false = CliqueInstance(
        name="clique_false",
        num_vertices=5,
        edges=[
            (1,2),(1,3),(2,3),
            (3,4),(4,5)
        ],
        k=4,
    )

    is_false = reduce.reduce(clique_false)

    print("SOURCE FALSE:", clique_false)
    print("TARGET FALSE:", is_false)

    assert clique_false.to_sat().is_satisfiable(solver) is False
    assert is_false.to_sat().is_satisfiable(solver) is False
