from typing import Dict, Any
from polyreduce import ProblemInstance, verify_reduction_with_sat
from polyreduce.core.reduction import Reduction
from polyreduce.sat.solvers.dummy_solver import DummySatSolver


class SimpleProblem(ProblemInstance):
    """
    A simple problem instance used for testing reductions.
    Stores a CNF inside self.data["cnf"].
    """

    def __init__(self, name: str, cnf: list[list[int]]):
        super().__init__(name)
        self.cnf = cnf
        self.data = {"cnf": cnf}


class SimpleSatProblem(ProblemInstance):
    """
    Output problem for the identity reduction.
    """

    def __init__(self, name: str, cnf: list[list[int]]):
        super().__init__(name)
        self.cnf = cnf
        self.data = {"cnf": cnf}


class IdentityReduction(Reduction[SimpleProblem, SimpleSatProblem]):
    """
    Test reduction: copies the CNF field from input to output unchanged.
    """

    def __init__(self) -> None:
        super().__init__(source_name="SimpleProblem", target_name="SimpleSatProblem")

    def reduce(self, instance: SimpleProblem) -> SimpleSatProblem:
        cnf = instance.data.get("cnf", [])
        return SimpleSatProblem(
            name="SAT-instance",
            cnf=cnf,
        )


def test_identity_reduction_and_dummy_solver():
    original_cnf = [[1, -2], [2, 3]]
    original = SimpleProblem(name="simple", cnf=original_cnf)

    reduction = IdentityReduction()
    sat_instance = reduction.reduce(original)

    solver = DummySatSolver()
    is_valid, sat_result = verify_reduction_with_sat(
        reduction, original, sat_instance, solver
    )

    assert is_valid
    assert sat_result is True
