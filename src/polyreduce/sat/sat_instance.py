from dataclasses import dataclass
from typing import List
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

    num_vars: int
    clauses: List[List[int]]

    def __init__(self, name: str, num_vars: int, clauses: list[list[int]]):
        """
        Perform basic structural validation of the CNF formula.
        """
        super().__init__(name)
        self.num_vars = num_vars
        self.clauses = clauses

        # Build internal data representation
        self.data = {
            "num_vars": num_vars,
            "clauses": clauses,
        }

        if self.num_vars <= 0:
            raise ValueError("Number of variables must be positive.")

        for clause in self.clauses:
            if not clause:
                raise ValueError("Clause cannot be empty.")

            for lit in clause:
                if lit == 0:
                    raise ValueError("Literal 0 is not allowed in CNF.")
                if abs(lit) > self.num_vars:
                    raise ValueError(
                        f"Literal {lit} refers to a variable outside the valid range."
                    )
    
    def is_satisfiable(self, solver: SatSolver) -> bool:
        """
        Returns True if this SAT instance is satisfiable using the given solver.

        This method simply delegates the CNF clauses to the solver.
        """
        return solver.solve(self.clauses)