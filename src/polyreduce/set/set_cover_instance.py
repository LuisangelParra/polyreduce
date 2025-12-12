from __future__ import annotations

from typing import Sequence, Set, Hashable

from polyreduce.core.problems import ProblemInstance


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
