import pytest

from polyreduce.sat.sat_instance import SATInstance
from polyreduce.sat.three_sat import ThreeSATInstance
from polyreduce.sat.sat_to_3sat import convert_to_3sat
from polyreduce.sat.solvers.dummy_solver import DummySatSolver


def test_sat_instance_basic():
    sat = SATInstance(
        name="test",
        num_vars=3,
        clauses=[[1, -2], [2, 3]]
    )

    assert sat.num_vars == 3
    assert sat.clauses == [[1, -2], [2, 3]]
    assert "clauses" in sat.data
    assert "num_vars" in sat.data


def test_three_sat_instance_enforces_3_literals():
    # Valid 3-SAT clause
    sat3 = ThreeSATInstance(
        name="3sat",
        num_vars=3,
        clauses=[[1, -2, 3], [2, 3, -1]]
    )

    assert isinstance(sat3, ThreeSATInstance)
    assert all(len(c) == 3 for c in sat3.clauses)

    # Invalid clause (must be size 3)
    with pytest.raises(ValueError):
        ThreeSATInstance(
            name="bad3sat",
            num_vars=3,
            clauses=[[1, 2]]  # only 2 literals
        )


def test_convert_to_3sat():
    sat = SATInstance(
        name="orig",
        num_vars=4,
        clauses=[
            [1],        # 1 literal
            [1, -2],    # 2 literals
            [1, 2, 3],  # already 3-literal
            [1, 2, 3, 4]  # 4 literals: must be split
        ]
    )

    sat3 = convert_to_3sat(sat)

    assert isinstance(sat3, ThreeSATInstance)
    assert all(len(c) == 3 for c in sat3.clauses)
    assert sat3.num_vars >= sat.num_vars  # auxiliary vars added


def test_is_satisfiable_with_dummy_solver():
    sat = SATInstance(
        name="dummytest",
        num_vars=2,
        clauses=[[1], [-1, 2]]
    )

    solver = DummySatSolver()
    result = sat.is_satisfiable(solver)

    # Dummy solver: returns True for any non-empty CNF
    assert result is True


def test_real_solver_if_available():
    """
    Optional test: runs only if PySAT is installed.
    """

    try:
        from polyreduce.sat.solvers.pysat_solver import PySatSolver
    except Exception:
        pytest.skip("PySAT not installed")

    sat = SATInstance(
        name="real",
        num_vars=2,
        clauses=[[1], [-1, 2]]
    )

    solver = PySatSolver()
    result = solver.solve(sat.clauses)

    assert isinstance(result, bool)
