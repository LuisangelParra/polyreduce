from __future__ import annotations

from typing import List

from polyreduce.core.reduction import Reduction
from polyreduce.sat.sat_instance import SATInstance
from polyreduce.sat.three_sat import ThreeSATInstance


class SatToThreeSat(Reduction[SATInstance, ThreeSATInstance]):
    """
    Converts a general CNF SAT instance into an equivalent 3-SAT instance.
    
    The transformation preserves satisfiability and unsatisfiability.

    Rules:
    - Clause of length 1:  (a)       → (a ∨ a ∨ a)
    - Clause of length 2:  (a ∨ b)   → (a ∨ b ∨ b)
    - Clause of length 3:  keep as is
    - Clause of length >3: apply standard splitting with new auxiliary variables.
    """
    def __init__(self):
        super().__init__("SAT", "3-SAT")

    def reduce(self, instance: SATInstance) -> ThreeSATInstance:
        new_clauses: List[List[int]] = []
        next_var = instance.num_vars + 1

        for clause in instance.clauses:
            k = len(clause)

            
            # -------------------------------------------
            # Case 1: Clause already has exactly 3 literals
            # -------------------------------------------
            if k == 3:
                new_clauses.append(clause)
                continue

            # -------------------------------------------
            # Case 2: Clause with 1 literal
            # (a) → (a ∨ a ∨ a)
            # This preserves satisfiability and unsatisfiability.
            # -------------------------------------------
            if k == 1:
                a = clause[0]
                new_clauses.append([a, a, a])
                continue
            
            # -------------------------------------------
            # Case 3: Clause with 2 literals
            # (a ∨ b) → (a ∨ b ∨ b)
            # This preserves satisfiability and unsatisfiability.
            # -------------------------------------------
            if k == 2:
                a, b = clause
                new_clauses.append([a, b, b])
                continue
            
            # -------------------------------------------
            # Case 4: Clause with more than 3 literals
            # Apply the standard splitting method:
            # (x1 ∨ x2 ∨ x3 ∨ ... ∨ xk) becomes:
            #   (x1 ∨ x2 ∨ y1)
            #   (¬y1 ∨ x3 ∨ y2)
            #   ...
            #   (¬y_{m-1} ∨ x_{k-1} ∨ x_k)
            # -------------------------------------------
            lits = clause[:]
            while len(lits) > 3:
                a, b = lits[0], lits[1]
                y = next_var
                next_var += 1
                new_clauses.append([a, b, y])
                lits = [-y] + lits[2:]

            new_clauses.append(lits)

        return ThreeSATInstance(
            name=f"{instance.name}-to-3sat",
            num_vars=next_var - 1,
            clauses=new_clauses,
        )
