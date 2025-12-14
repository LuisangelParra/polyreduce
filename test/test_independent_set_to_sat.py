from polyreduce.graph.independent_set_instance import IndependentSetInstance
from polyreduce.sat.solvers.pysat_solver import PySatSolver

def test_independent_set_sat_instance():
    inst = IndependentSetInstance(
        name="is_true",
        num_vertices=6,
        edges=[
            (1,2),(2,3),(3,4),(4,5),(5,6),(1,6),
            (1,3),(3,5)  # ruido extra
        ],
        k=3,
    )
    cert = [2,4,6]

    print(inst)
    assert inst.verify(cert) is True
    assert inst.to_sat().is_satisfiable(PySatSolver()) is True

def test_independent_set_unsat_instance():
    inst = IndependentSetInstance(
        name="is_false",
        num_vertices=6,
        edges=[(1,2),(2,3),(3,4),(4,5),(5,6),(6,1)],
        k=4,
    )

    print(inst)
    assert inst.to_sat().is_satisfiable(PySatSolver()) is False
