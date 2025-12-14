from polyreduce.graph.clique_instance import CliqueInstance
from polyreduce.sat.solvers.pysat_solver import PySatSolver

def test_clique_sat_instance():
    inst = CliqueInstance(
        name="clique_true",
        num_vertices=6,
        edges=[
            # clique {1,2,3,4}
            (1,2),(1,3),(1,4),
            (2,3),(2,4),
            (3,4),
            # ruido
            (4,5),(5,6)
        ],
        k=4,
    )
    cert = [1,2,3,4]

    print(inst)
    assert inst.verify(cert) is True
    assert inst.to_sat().is_satisfiable(PySatSolver()) is True

def test_clique_unsat_instance():
    inst = CliqueInstance(
        name="clique_false",
        num_vertices=6,
        edges=[
            (1,2),(1,3),(1,4),
            (2,3),(2,4),
            (3,4),
            (4,5),(5,6)
        ],
        k=5,
    )

    print(inst)
    assert inst.to_sat().is_satisfiable(PySatSolver()) is False
