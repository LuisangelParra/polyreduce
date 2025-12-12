from __future__ import annotations

from typing import Dict

from polyreduce.sat.sat_instance import SATInstance


def verify_sat_solution(
    instance: SATInstance,
    assignment: Dict[int, bool],
) -> bool:
    return instance.verify(assignment)
