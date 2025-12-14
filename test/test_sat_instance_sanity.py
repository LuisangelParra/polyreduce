from polyreduce.sat.sat_instance import SATInstance
from polyreduce.sat.solvers.pysat_solver import PySatSolver

def test_sat_instance_sat():
    inst = SATInstance(
        name="sat_true",
        num_vars=2,
        clauses=[
            [1, 2],
            [-1, 2],
        ],
    )
    cert = {1: False, 2: True}

    print(inst)
    assert inst.verify(cert) is True
    assert inst.is_satisfiable(PySatSolver()) is True

def test_sat_instance_unsat():
    inst = SATInstance(
        name="sat_false",
        num_vars=1,
        clauses=[
            [1],
            [-1],
        ],
    )

    print(inst)
    assert inst.is_satisfiable(PySatSolver()) is False
