from polyreduce.sat.sat_instance import SATInstance
from polyreduce.sat.reductions.sat_to_3sat import SatToThreeSat
from polyreduce.sat.solvers.pysat_solver import PySatSolver


def test_sat_to_3sat_preserves_sat():
    solver = PySatSolver()
    reduce = SatToThreeSat()

    # ---------- TRUE ----------
    sat_true = SATInstance(
        name="sat_true",
        num_vars=3,
        clauses=[
            [1, 2],
            [-1, 3],
        ],
    )

    ts_true = reduce.reduce(sat_true)

    print("SOURCE TRUE:", sat_true)
    print("TARGET TRUE:", ts_true)

    assert sat_true.is_satisfiable(solver) is True
    assert ts_true.is_satisfiable(solver) is True

    # ---------- FALSE ----------
    sat_false = SATInstance(
        name="sat_false",
        num_vars=1,
        clauses=[
            [1],
            [-1],
        ],
    )

    ts_false = reduce.reduce(sat_false)

    print("SOURCE FALSE:", sat_false)
    print("TARGET FALSE:", ts_false)

    assert sat_false.is_satisfiable(solver) is False
    assert ts_false.is_satisfiable(solver) is False
