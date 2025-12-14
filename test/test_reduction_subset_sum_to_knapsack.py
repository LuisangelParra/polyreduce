from polyreduce.number.subset_sum_instance import SubsetSumInstance
from polyreduce.number.reductions.subset_sum_to_knapsack import SubsetSumToKnapsack
from polyreduce.sat.solvers.pysat_solver import PySatSolver


def test_subset_sum_to_knapsack_preserves_sat():
    solver = PySatSolver()
    reduce = SubsetSumToKnapsack()

    # ---------- TRUE ----------
    ss_true = SubsetSumInstance(
        name="ss_true",
        numbers=[7, 11, 13, 17],
        target=24,  # 11 + 13
    )

    ks_true = reduce.reduce(ss_true)

    print("SOURCE TRUE:", ss_true)
    print("TARGET TRUE:", ks_true)

    assert ss_true.to_sat().is_satisfiable(solver) is True
    assert ks_true.to_sat().is_satisfiable(solver) is True

    # ---------- FALSE ----------
    ss_false = SubsetSumInstance(
        name="ss_false",
        numbers=[7, 11, 13],
        target=5,
    )

    ks_false = reduce.reduce(ss_false)

    print("SOURCE FALSE:", ss_false)
    print("TARGET FALSE:", ks_false)

    assert ss_false.to_sat().is_satisfiable(solver) is False
    assert ks_false.to_sat().is_satisfiable(solver) is False
