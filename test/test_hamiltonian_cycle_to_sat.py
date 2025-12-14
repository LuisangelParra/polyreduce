from polyreduce.graph.hamiltonian_cycle_instance import HamiltonianCycleInstance
from polyreduce.sat.solvers.pysat_solver import PySatSolver


def test_hamiltonian_cycle_sat_instance():
    inst = HamiltonianCycleInstance(
        name="hc_true",
        num_vertices=6,
        edges=[
            (1, 2), (2, 3), (3, 4),
            (4, 5), (5, 6), (6, 1),
            (1, 3), (2, 4), (3, 5),
        ],
    )

    print(inst)
    assert inst.to_sat().is_satisfiable(PySatSolver()) is True


def test_hamiltonian_cycle_unsat_instance():
    inst = HamiltonianCycleInstance(
        name="hc_false",
        num_vertices=6,
        edges=[
            (1, 2), (2, 3), (3, 1),
            (3, 4),
            (4, 5), (5, 6), (6, 4),
        ],
    )

    print(inst)
    assert inst.to_sat().is_satisfiable(PySatSolver()) is False
