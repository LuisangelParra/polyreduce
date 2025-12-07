from typing import List
from .sat_instance import SATInstance
from .three_sat import ThreeSATInstance


def convert_to_3sat(instance: SATInstance) -> ThreeSATInstance:
    """
    Converts a general CNF SAT instance into an equivalent 3-SAT instance.
    Ensures every clause has *exactly* 3 literals.

    Uses auxiliary variables when clause size < 3 or > 3.
    """

    new_clauses: List[List[int]] = []
    next_var = instance.num_vars + 1

    for clause in instance.clauses:
        k = len(clause)

        # ---- Case 1: clause already size 3 ----
        if k == 3:
            new_clauses.append(clause)
            continue

        # ---- Case 2: clause size 1 ----
        # (a)  →  (a ∨ y1 ∨ y2)
        if k == 1:
            y1 = next_var; next_var += 1
            y2 = next_var; next_var += 1
            new_clauses.append([clause[0], y1, y2])
            continue

        # ---- Case 3: clause size 2 ----
        # (a ∨ b) → (a ∨ b ∨ y1)
        if k == 2:
            y = next_var; next_var += 1
            new_clauses.append([clause[0], clause[1], y])
            continue

        # ---- Case 4: clause size > 3 (split it) ----
        lits = clause[:]

        while len(lits) > 3:
            a, b = lits[0], lits[1]
            y = next_var
            next_var += 1

            # create a clause of 3 literals
            new_clauses.append([a, b, y])

            # reduce the clause
            lits = [-y] + lits[2:]

        # last clause now has size 3
        new_clauses.append(lits)

    return ThreeSATInstance(
        name="3SAT-normalized",
        num_vars=next_var - 1,
        clauses=new_clauses
    )
