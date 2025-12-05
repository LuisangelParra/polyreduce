from dataclasses import dataclass
from typing import Dict, Any

from polyreduce import ProblemInstance, verify_reduction_with_sat
from polyreduce.reductions import Reduction
from polyreduce.sat_solver import DummySatSolver


@dataclass
class SimpleProblem(ProblemInstance):
    pass


@dataclass
class SimpleSatProblem(ProblemInstance):
    pass


class IdentityReduction(Reduction[SimpleProblem, SimpleSatProblem]):
    """
    Reducción de juguete: copia el campo 'cnf' del problema de entrada
    hacia el problema de salida sin cambios.
    """

    def __init__(self) -> None:
        super().__init__(source_name="SimpleProblem", target_name="SAT")

    def reduce(self, instance: SimpleProblem) -> SimpleSatProblem:
        cnf = instance.data.get("cnf", [])
        return SimpleSatProblem(
            name="SAT-instance",
            data={"cnf": cnf},
        )


def test_identity_reduction_and_dummy_solver():
    original_cnf = [[1, -2], [2, 3]]
    original = SimpleProblem(name="simple", data={"cnf": original_cnf})

    reduction = IdentityReduction()
    sat_instance = reduction.reduce(original)

    solver = DummySatSolver()
    is_valid, sat_result = verify_reduction_with_sat(
        reduction, original, sat_instance, solver
    )

    assert is_valid
    assert sat_result is True
