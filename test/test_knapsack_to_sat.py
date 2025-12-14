from polyreduce.number.knapsack_instance import KnapsackInstance
from polyreduce.sat.solvers.pysat_solver import PySatSolver


def test_knapsack_sat_instance():
    inst = KnapsackInstance(
        name="ks_true",
        items=[(4, 6), (5, 7), (6, 10), (3, 4)],
        capacity=14,
        min_value=21,
    )

    certificate = [False, True, True, True]  # weight=14, value=21
    
    print(inst)
    assert inst.verify(certificate) is True
    assert inst.to_sat().is_satisfiable(PySatSolver()) is True


def test_knapsack_unsat_instance():
    inst = KnapsackInstance(
        name="ks_false",
        items=[(4, 6), (5, 7), (6, 10), (3, 4)],
        capacity=9,
        min_value=18,
    )

    print(inst)
    assert inst.to_sat().is_satisfiable(PySatSolver()) is False
