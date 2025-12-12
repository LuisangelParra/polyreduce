from __future__ import annotations

from typing import Dict, List, Tuple

from polyreduce.core.problems import ProblemInstance

from polyreduce.sat.sat_instance import SATInstance
from typing import Sequence, Tuple, Any


class ThreeColorInstance(ProblemInstance):
    def __init__(
        self,
        name: str,
        nodes: Sequence[Any],
        edges: Sequence[Tuple[Any, Any]]
    ):
        super().__init__(name)

        self.nodes = nodes
        self.edges = edges

        self.data = {
            "nodes": nodes,
            "edges": edges,
        }

    def __repr__(self) -> str:
        return (
            f"ThreeColorInstance(name={self.name!r}, "
            f"nodes={len(self.nodes)}, edges={len(self.edges)})"
        )

    def verify(self, certificate: Dict[Any, int]) -> bool:
        if not certificate:
            return False

        for node in self.nodes:
            if node not in certificate:
                return False
            color = certificate[node]
            if color not in {1, 2, 3}:
                return False

        for u, v in self.edges:
            if certificate[u] == certificate[v]:
                return False

        return True
    
    def to_sat(self) -> SATInstance:
        nodes = list(self.nodes)
        edges = self.edges

        node_index = {v: i for i, v in enumerate(nodes, start=1)}

        def var(v, c: int) -> int:
            return (node_index[v] - 1) * 3 + c

        clauses = []

        # C1: cada vértice tiene al menos un color
        for v in nodes:
            clauses.append([
                var(v, 1),
                var(v, 2),
                var(v, 3),
            ])

        # C2: cada vértice tiene a lo sumo un color
        for v in nodes:
            clauses.append([-var(v, 1), -var(v, 2)])
            clauses.append([-var(v, 1), -var(v, 3)])
            clauses.append([-var(v, 2), -var(v, 3)])

        # C3: vértices adyacentes no comparten color
        for (u, v) in edges:
            for c in (1, 2, 3):
                clauses.append([
                    -var(u, c),
                    -var(v, c),
                ])

        num_vars = 3 * len(nodes)

        return SATInstance(
            name=f"{self.name}-to-sat",
            num_vars=num_vars,
            clauses=clauses,
        )
