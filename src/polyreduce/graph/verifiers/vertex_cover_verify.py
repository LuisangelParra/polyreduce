from __future__ import annotations

from polyreduce.graph.vertex_cover_instance import VertexCoverInstance


def verify_vertex_cover_solution(
    instance: VertexCoverInstance,
    candidate: list[int],
) -> bool:
    return instance.verify(candidate)