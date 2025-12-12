from __future__ import annotations

from typing import Sequence

from polyreduce.core.problems import ProblemInstance


class SubsetSumInstance(ProblemInstance):
    def __init__(
        self,
        name: str,
        numbers: Sequence[int],
        target: int,
    ):
        super().__init__(name)

        if target < 0:
            raise ValueError("target must be non-negative.")

        self.numbers = list(numbers)
        self.target = target

        self.data = {
            "numbers": self.numbers,
            "target": self.target,
        }

    def __repr__(self) -> str:
        return (
            f"SubsetSumInstance("
            f"name={self.name!r}, "
            f"|U|={len(self.numbers)}, "
            f"target={self.target})"
        )

    def verify(self, certificate: Sequence[bool]) -> bool:
        if len(certificate) != len(self.numbers):
            return False

        total = 0

        for selected, value in zip(certificate, self.numbers):
            if selected:
                total += value

        return total == self.target
