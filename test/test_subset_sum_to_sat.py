from polyreduce.number.subset_sum_instance import SubsetSumInstance
from polyreduce.sat.solvers.pysat_solver import PySatSolver


def test_subset_sum_sat_instance():
    inst = SubsetSumInstance(
        name="ss_true",
        numbers=[7, 11, 13, 17, 19, 23],
        target=41,  # 11 + 13 + 17
    )

    certificate = [False, True, True, True, False, False]

    print(inst)
    assert inst.verify(certificate) is True
    assert inst.to_sat().is_satisfiable(PySatSolver()) is True


def test_subset_sum_unsat_instance():
    inst = SubsetSumInstance(
        name="ss_false",
        numbers=[7, 11, 13, 17, 19],
        target=10,
    )

    print(inst)
    assert inst.to_sat().is_satisfiable(PySatSolver()) is False
