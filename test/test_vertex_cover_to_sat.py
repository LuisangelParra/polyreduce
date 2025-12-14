from polyreduce.graph.vertex_cover_instance import VertexCoverInstance
from polyreduce.sat.solvers.pysat_solver import PySatSolver

def test_vertex_cover_sat_instance():
    inst = VertexCoverInstance(
        name="vc_true",
        num_vertices=6,
        edges=[(1,2),(2,3),(3,4),(4,5),(5,6),(6,1)],
        k=3,
    )
    cert = [2,4,6]  # cubre todas las aristas del ciclo

    print(inst)
    assert inst.verify(cert) is True
    assert inst.to_sat().is_satisfiable(PySatSolver()) is True

def test_vertex_cover_unsat_instance():
    inst = VertexCoverInstance(
        name="vc_false",
        num_vertices=6,
        edges=[(1,2),(2,3),(3,4),(4,5),(5,6),(6,1)],
        k=2,
    )

    print(inst)
    assert inst.to_sat().is_satisfiable(PySatSolver()) is False
