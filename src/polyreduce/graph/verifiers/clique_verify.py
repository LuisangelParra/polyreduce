from __future__ import annotations

from polyreduce.graph.clique_instance import CliqueInstance


def verify_clique_solution(instance: CliqueInstance, candidate: list[int]) -> bool:
    return instance.verify(candidate)
