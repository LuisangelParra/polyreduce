from abc import ABC, abstractmethod
from typing import List, Sequence


class SatSolver(ABC):
    """
    Abstract interface for SAT solvers.

    The default representation: CNF as a list of clauses,
    each clause is a list of integers (standard DIMACS).
    """

    @abstractmethod
    def solve(self, cnf: Sequence[Sequence[int]]) -> bool:
        """
        Returns True if the formula is satisfiable, False otherwise.
        """
        raise NotImplementedError


class DummySatSolver(SatSolver):
    """
    Toy implementation only for initial tests.

    Later you will replace it with a real wrapper around a solver.
    """

    def solve(self, cnf: Sequence[Sequence[int]]) -> bool:
        # For now, we assume every non-empty instance is "satisfiable"
        # Just to test the flow.
        return len(cnf) > 0