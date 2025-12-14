from __future__ import annotations

from typing import List, Sequence, Set, Hashable

from polyreduce.core.problems import ProblemInstance
from polyreduce.sat.sat_instance import SATInstance


class SetCoverInstance(ProblemInstance):
    def __init__(
        self,
        name: str,
        universe: Set[Hashable],
        subsets: Sequence[Set[Hashable]],
        k: int,
    ):
        super().__init__(name)

        if k < 0 or k > len(subsets):
            raise ValueError("k must satisfy 0 ≤ k ≤ number of subsets.")

        self.universe = set(universe)
        self.subsets = list(subsets)
        self.k = k

        self.data = {
            "universe": self.universe,
            "subsets": self.subsets,
            "k": k,
        }

    def __repr__(self) -> str:
        return (
            f"SetCoverInstance("
            f"name={self.name!r}, "
            f"|U|={len(self.universe)}, "
            f"|T|={len(self.subsets)}, "
            f"k={self.k})"
        )

    def verify(self, certificate: Sequence[int]) -> bool:
        if len(certificate) != self.k:
            return False

        if len(set(certificate)) != self.k:
            return False

        if any(i < 0 or i >= len(self.subsets) for i in certificate):
            return False

        covered: Set[Hashable] = set()

        for i in certificate:
            covered |= self.subsets[i]

        return covered == self.universe
    
    def to_sat(self) -> SATInstance:
        U = list(self.universe)
        subsets = self.subsets
        k = self.k

        m = len(U)
        n = len(subsets)

        clauses: List[List[int]] = []

        def var(p: int, i: int) -> int:
            return p * n + i + 1

        num_vars = k * n

        # --- R1: each position selects exactly one subset ---
        for p in range(k):
            clauses.append([var(p, i) for i in range(n)])

            for i in range(n):
                for j in range(i + 1, n):
                    clauses.append([-var(p, i), -var(p, j)])

        # --- R2: no subset appears in two positions ---
        for i in range(n):
            for p in range(k):
                for q in range(p + 1, k):
                    clauses.append([-var(p, i), -var(q, i)])

        # --- R3: coverage of universe ---
        for u in U:
            covering_literals = []
            for p in range(k):
                for i in range(n):
                    if u in subsets[i]:
                        covering_literals.append(var(p, i))

            if not covering_literals:
                clauses.append([])
            else:
                clauses.append(covering_literals)

        return SATInstance(
            name=f"{self.name}_to_SAT",
            num_vars=num_vars,
            clauses=clauses,
        )