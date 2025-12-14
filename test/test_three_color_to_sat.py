from polyreduce.graph.three_color_instance import ThreeColorInstance
from polyreduce.sat.solvers.pysat_solver import PySatSolver


def test_three_color_sat_instance():
    # C5 es 3-colorable (no trivial)
    nodes = [1, 2, 3, 4, 5]
    edges = [
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (5, 1),
    ]

    inst = ThreeColorInstance(
        name="3col_true",
        nodes=nodes,
        edges=edges,
    )

    # Coloreo válido: colores {1,2,3}
    # 1-2-3-1-2
    certificate = {
        1: 1,
        2: 2,
        3: 3,
        4: 1,
        5: 2,
    }

    print(inst)
    assert inst.verify(certificate) is True
    assert inst.to_sat().is_satisfiable(PySatSolver()) is True


def test_three_color_unsat_instance():
    # K4 NO es 3-colorable
    nodes = [1, 2, 3, 4]
    edges = [
        (1, 2),
        (1, 3),
        (1, 4),
        (2, 3),
        (2, 4),
        (3, 4),
    ]

    inst = ThreeColorInstance(
        name="3col_false",
        nodes=nodes,
        edges=edges,
    )

    print(inst)
    assert inst.to_sat().is_satisfiable(PySatSolver()) is False
