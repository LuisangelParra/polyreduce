from __future__ import annotations

from typing import Dict, List, Sequence

from polyreduce.core.problems import ProblemInstance
from polyreduce.core.sat_solver import SatSolver


class SATInstance(ProblemInstance):
    """
    Represents a propositional CNF formula for the SAT problem.

    - Variables are represented as positive integers: 1, 2, 3, ...
    - Negated literals are negative integers: -1 means ¬x1.
    - A clause is a list of literals representing an OR: [1, -3] → (x1 ∨ ¬x3).
    - A CNF formula is a list of clauses, representing an AND of clauses.

    This instance structure is fully compatible with:
    - DIMACS CNF format
    - PySAT library
    - Standard NP-completeness reductions to SAT
    """
    def __init__(self, name: str, num_vars: int, clauses: List[List[int]]):
        """
        Perform basic structural validation of the CNF formula.
        """
        super().__init__(name)

        if num_vars <= 0:
            raise ValueError("Number of variables must be positive.")

        for clause in clauses:
            if not clause:
                raise ValueError("Clause cannot be empty.")
            for lit in clause:
                if lit == 0 or abs(lit) > num_vars:
                    raise ValueError("Invalid literal.")

        self.num_vars = num_vars
        self.clauses = clauses

        self.data = {
            "num_vars": num_vars,
            "clauses": clauses,
        }

    def __repr__(self) -> str:
        return (
            f"SATInstance(name={self.name!r}, "
            f"num_vars={self.num_vars}, "
            f"num_clauses={len(self.clauses)})"
        )

    def verify(self, certificate: Dict[int, bool]) -> bool:
        if not certificate:
            return False

        for var in certificate:
            if var < 1 or var > self.num_vars:
                return False

        for clause in self.clauses:
            satisfied = False
            for lit in clause:
                var = abs(lit)
                value = certificate.get(var, False)
                if (lit > 0 and value) or (lit < 0 and not value):
                    satisfied = True
                    break
            if not satisfied:
                return False

        return True
    
    def to_sat(self) -> "SATInstance":
        return self

    def is_satisfiable(self, solver: SatSolver) -> bool:
        """
        Returns True if this SAT instance is satisfiable using the given solver.

        This method simply delegates the CNF clauses to the solver.
        """
        return solver.solve(self.clauses)