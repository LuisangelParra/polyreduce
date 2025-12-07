from typing import Sequence
from pysat.solvers import Glucose3
from polyreduce.sat_solver import SatSolver

class PySatSolver(SatSolver):
    """
    A SAT solver using the PySAT library (Glucose3 backend).
    Compatible with the SatSolver abstract interface.
    """

    def solve(self, cnf: Sequence[Sequence[int]]) -> bool:
        """
        Returns True if the CNF formula is satisfiable, False if unsatisfiable.
        If PySAT returns None (unknown), this method returns False.
        """
        with Glucose3() as solver:
            for clause in cnf:
                solver.add_clause(list(clause))

            result = solver.solve()
            
        return bool(result)
