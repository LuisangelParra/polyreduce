from __future__ import annotations

from polyreduce.sat.sat_instance import SATInstance


class ThreeSATInstance(SATInstance):
    """
    A restricted SAT instance where each clause contains *exactly*
    three literals. This corresponds to the classical 3-SAT problem.

    This subclass ensures:
    - CNF well-formedness (inherited from SATInstance)
    - Clause size equals 3
    """
    def __init__(self, name: str, num_vars: int, clauses: list[list[int]]):
        super().__init__(name, num_vars, clauses)

        for clause in clauses:
            if len(clause) != 3:
                raise ValueError("Each clause must contain exactly 3 literals.")
