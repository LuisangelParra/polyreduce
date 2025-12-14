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
    
    def to_sat(self) -> SATInstance:
        n = self.num_vertices
        edges = set(self.edges)
        clauses: List[List[int]] = []

        def var(v: int, p: int) -> int:
            return (v - 1) * n + p

        num_vars = n * n

        # --- R1: Each position has exactly one vertex ---
        for p in range(1, n + 1):
            clauses.append([var(v, p) for v in range(1, n + 1)])

            for u in range(1, n + 1):
                for v in range(u + 1, n + 1):
                    clauses.append([-var(u, p), -var(v, p)])

        # --- R2: Each vertex appears exactly once ---
        for v in range(1, n + 1):
            clauses.append([var(v, p) for p in range(1, n + 1)])

            for p in range(1, n + 1):
                for q in range(p + 1, n + 1):
                    clauses.append([-var(v, p), -var(v, q)])

        # --- R3: Only existing edges can be consecutive ---
        for u in range(1, n + 1):
            for v in range(1, n + 1):
                if u == v:
                    continue
                if (u, v) not in edges and (v, u) not in edges:
                    for p in range(1, n):
                        clauses.append([-var(u, p), -var(v, p + 1)])
                    clauses.append([-var(u, n), -var(v, 1)])

        return SATInstance(
            name=f"{self.name}_to_SAT",
            num_vars=num_vars,
            clauses=clauses,
        )   
