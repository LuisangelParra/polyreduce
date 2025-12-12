from __future__ import annotations

from typing import Dict

from polyreduce.graph.three_color_instance import ThreeColorInstance


def verify_three_color_solution(
    instance: ThreeColorInstance,
    candidate: Dict[object, int],
) -> bool:
    return instance.verify(candidate)
