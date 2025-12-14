from polyreduce.sat.three_sat import ThreeSATInstance
from polyreduce.sat.solvers.pysat_solver import PySatSolver

def test_3sat_sat_instance():
    # (x1 ∨ x2 ∨ x3) ∧ (¬x1 ∨ x2 ∨ x3) ∧ (x1 ∨ ¬x2 ∨ x3)
    inst = ThreeSATInstance(
        name="3sat_true",
        num_vars=3,
        clauses=[
            [ 1, 2, 3],
            [-1, 2, 3],
            [ 1,-2, 3],
        ],
    )
    cert = {1: True, 2: True, 3: False}

    print(inst)
    assert inst.verify(cert) is True
    assert inst.to_sat().is_satisfiable(PySatSolver()) is True

def test_3sat_unsat_instance():
    # (x1) ∧ (¬x1) embed in 3-CNF
    inst = ThreeSATInstance(
        name="3sat_false",
        num_vars=1,
        clauses=[
            [ 1, 1, 1],
            [-1,-1,-1],
        ],
    )

    print(inst)
    assert inst.to_sat().is_satisfiable(PySatSolver()) is False
