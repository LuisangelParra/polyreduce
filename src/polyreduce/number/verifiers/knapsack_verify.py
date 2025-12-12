from __future__ import annotations

from typing import Sequence

from polyreduce.number.knapsack_instance import KnapsackInstance


def verify_knapsack(
    instance: KnapsackInstance,
    certificate: Sequence[bool],
) -> bool:
    return instance.verify(certificate)
