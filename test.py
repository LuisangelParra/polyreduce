from polyreduce.set.set_cover_instance import SetCoverInstance
from polyreduce.sat.solvers.pysat_solver import PySatSolver

inst_true = SetCoverInstance(
    name="sc_nontrivial_true",
    universe={"a", "b", "c", "d", "e"},
    subsets=[
        {"a", "b"},        # 0
        {"c"},             # 1
        {"d", "e"},        # 2
        {"b", "c"},        # 3
        {"a", "d"},        # 4
    ],
    k=3,
)

print(inst_true.to_sat().is_satisfiable(PySatSolver()))


inst_false = SetCoverInstance(
    name="sc_nontrivial_false",
    universe={"a", "b", "c", "d", "e"},
    subsets=[
        {"a", "b"},        # 0
        {"b", "c"},        # 1
        {"c", "d"},        # 2
        {"a"},             # 3
        {"e"},             # 4
    ],
    k=2,
)

print(inst_false.to_sat().is_satisfiable(PySatSolver()))
