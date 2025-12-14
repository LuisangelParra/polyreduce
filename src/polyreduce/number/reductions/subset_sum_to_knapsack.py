from __future__ import annotations

from typing import List, Tuple

from polyreduce.core.reduction import Reduction
from polyreduce.number.subset_sum_instance import SubsetSumInstance
from polyreduce.number.knapsack_instance import KnapsackInstance


class SubsetSumToKnapsack(Reduction[SubsetSumInstance, KnapsackInstance]):
    def __init__(self):
        super().__init__("SUBSET-SUM", "KNAPSACK")

    def reduce(self, instance: SubsetSumInstance) -> KnapsackInstance:
        items: List[Tuple[int, int]] = []

        for u in instance.numbers:
            items.append((u, u))

        return KnapsackInstance(
            name=f"Knapsack from {instance.name}",
            items=items,
            capacity=instance.target,
            min_value=instance.target,
        )
