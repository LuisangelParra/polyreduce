from polyreduce.sat.three_sat import ThreeSATInstance
from polyreduce.graph.reductions.three_sat_to_three_color import ThreeSatToThreeColor
from polyreduce.sat.solvers.pysat_solver import PySatSolver


def test_3sat_to_three_color_preserves_sat():
    solver = PySatSolver()
    reduce = ThreeSatToThreeColor()

    # ---------- TRUE ----------
    sat_true = ThreeSATInstance(
        name="3sat_true",
        num_vars=3,
        clauses=[
            [1, 2, 3],
            [-1, 2, 3],
            [1, -2, 3],
        ],
    )

    col_true = reduce.reduce(sat_true)

    print("SOURCE TRUE:", sat_true)
    print("TARGET TRUE:", col_true)

    assert sat_true.to_sat().is_satisfiable(solver) is True
    assert col_true.to_sat().is_satisfiable(solver) is True

    # ---------- FALSE ----------
    sat_false = ThreeSATInstance(
        name="3sat_false",
        num_vars=1,
        clauses=[
            [1, 1, 1],
            [-1, -1, -1],
        ],
    )

    col_false = reduce.reduce(sat_false)

    print("SOURCE FALSE:", sat_false)
    print("TARGET FALSE:", col_false)

    assert sat_false.to_sat().is_satisfiable(solver) is False
    assert col_false.to_sat().is_satisfiable(solver) is False
