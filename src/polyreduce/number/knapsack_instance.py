from __future__ import annotations

from typing import Sequence, Tuple

from polyreduce.core.problems import ProblemInstance


class KnapsackInstance(ProblemInstance):
    def __init__(
        self,
        name: str,
        items: Sequence[Tuple[int, int]],
        capacity: int,
        min_value: int,
    ):
        super().__init__(name)

        if capacity < 0:
            raise ValueError("capacity must be non-negative.")

        if min_value < 0:
            raise ValueError("min_value must be non-negative.")

        self.items = list(items)
        self.capacity = capacity
        self.min_value = min_value

        self.data = {
            "items": self.items,
            "capacity": self.capacity,
            "min_value": self.min_value,
        }

    def __repr__(self) -> str:
        return (
            f"KnapsackInstance("
            f"name={self.name!r}, "
            f"|W|={len(self.items)}, "
            f"capacity={self.capacity}, "
            f"min_value={self.min_value})"
        )

    def verify(self, certificate: Sequence[bool]) -> bool:
        if len(certificate) != len(self.items):
            return False

        total_weight = 0
        total_value = 0

        for selected, (weight, value) in zip(certificate, self.items):
            if selected:
                total_weight += weight
                total_value += value

        if total_weight > self.capacity:
            return False

        if total_value < self.min_value:
            return False

        return True
