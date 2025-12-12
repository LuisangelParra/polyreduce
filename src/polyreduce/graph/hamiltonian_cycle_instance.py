from __future__ import annotations

from typing import Sequence, List

from polyreduce.graph.graph_instance import GraphInstance
from polyreduce.sat.sat_instance import SATInstance


class HamiltonianCycleInstance(GraphInstance):
    def __init__(
        self,
        name: str,
        num_vertices: int,
        edges: list[tuple[int, int]],
    ):
        super().__init__(name, num_vertices, edges)

    def __repr__(self) -> str:
        return (
            f"HamiltonianCycleInstance("
            f"name={self.name!r}, |V|={self.num_vertices})"
        )

    def verify(self, certificate: Sequence[int]) -> bool:
        if len(certificate) != self.num_vertices + 1:
            return False

        if certificate[0] != certificate[-1]:
            return False

        visited = certificate[:-1]

        if len(set(visited)) != self.num_vertices:
            return False

        if set(visited) != set(range(1, self.num_vertices + 1)):
            return False

        for i in range(self.num_vertices):
            u = certificate[i]
            v = certificate[i + 1]
            if not self.has_edge(u, v):
                return False

        return True