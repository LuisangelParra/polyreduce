from __future__ import annotations

from polyreduce.graph.independent_set_instance import IndependentSetInstance


def verify_independent_set_solution(
    instance: IndependentSetInstance,
    candidate: list[int],
) -> bool:
    return instance.verify(candidate)