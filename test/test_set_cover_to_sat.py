from polyreduce.set.set_cover_instance import SetCoverInstance
from polyreduce.sat.solvers.pysat_solver import PySatSolver


def test_set_cover_sat_instance():
    inst = SetCoverInstance(
        name="sc_true",
        universe={"a", "b", "c", "d", "e"},
        subsets=[
            {"a", "b"},
            {"c"},
            {"d", "e"},
            {"b", "c"},
            {"a", "d"},
        ],
        k=3,
    )

    certificate = [0, 1, 2]

    print(inst)
    assert inst.verify(certificate) is True
    assert inst.to_sat().is_satisfiable(PySatSolver()) is True


def test_set_cover_unsat_instance():
    inst = SetCoverInstance(
        name="sc_false",
        universe={"a", "b", "c", "d", "e"},
        subsets=[
            {"a", "b"},
            {"b", "c"},
            {"c", "d"},
            {"a"},
            {"e"},
        ],
        k=2,
    )

    print(inst)
    assert inst.to_sat().is_satisfiable(PySatSolver()) is False
