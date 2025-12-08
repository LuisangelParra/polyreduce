from polyreduce.core.sat_solver import SatSolver

class DummySatSolver(SatSolver):
    """
    A simple SAT solver mock used for testing pipelines.
    Always returns True if CNF is non-empty.
    This does NOT perform real SAT solving.
    """

    def solve(self, cnf):
        return len(cnf) > 0