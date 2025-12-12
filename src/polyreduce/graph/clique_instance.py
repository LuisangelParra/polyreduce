from __future__ import annotations

from .graph_instance import GraphInstance

from polyreduce.sat.sat_instance import SATInstance


class CliqueInstance(GraphInstance):
    """
    Represents an instance of the CLIQUE problem.

    Given:
        - A graph G = (V, E)
        - A target size k

    Question:
        Does G contain a clique of size k?
    """
    def __init__(
        self,
        name: str,
        num_vertices: int,
        edges: list[tuple[int, int]],
        k: int,
    ):
        super().__init__(name, num_vertices, edges)

        if not (1 <= k <= num_vertices):
            raise ValueError("k must be between 1 and the number of vertices.")

        self.k = k
        self.data["k"] = k

    def __repr__(self) -> str:
        return f"CliqueInstance(name={self.name!r}, |V|={self.num_vertices}, k={self.k})"

    def verify(self, certificate: list[int]) -> bool:
        if len(certificate) != self.k:
            return False

        if len(set(certificate)) != len(certificate):
            return False

        for i in range(len(certificate)):
            for j in range(i + 1, len(certificate)):
                u = certificate[i]
                v = certificate[j]
                if not self.has_edge(u, v):
                    return False

        return True
    
    def to_sat(self) -> SATInstance:
        n = self.num_vertices
        k = self.k

        def var(v: int, i: int) -> int:
            return (v - 1) * k + i

        clauses = []

        # C1: every position in the clique is occupied
        for i in range(1, k + 1):
            clause = []
            for v in range(1, n + 1):
                clause.append(var(v, i))
            clauses.append(clause)

        # C2: a vertex cannot occupy two positions
        for v in range(1, n + 1):
            for i in range(1, k + 1):
                for j in range(i + 1, k + 1):
                    clauses.append([
                        -var(v, i),
                        -var(v, j)
                    ])

        # C3: two vertices cannot occupy the same position
        for i in range(1, k + 1):
            for u in range(1, n + 1):
                for v in range(u + 1, n + 1):
                    clauses.append([
                        -var(u, i),
                        -var(v, i)
                    ])

        # C4: if two vertices are not connected, they cannot both be in the clique
        for u in range(1, n + 1):
            for v in range(u + 1, n + 1):
                if not self.has_edge(u, v):
                    for i in range(1, k + 1):
                        for j in range(1, k + 1):
                            if i != j:
                                clauses.append([
                                    -var(u, i),
                                    -var(v, j)
                                ])
        num_vars = n * k

        return SATInstance(
            name=f"{self.name}-to-sat",
            num_vars=num_vars,
            clauses=clauses,
        )