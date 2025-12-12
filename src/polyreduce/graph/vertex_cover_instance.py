from __future__ import annotations

from polyreduce.graph.graph_instance import GraphInstance

from polyreduce.sat.sat_instance import SATInstance


class VertexCoverInstance(GraphInstance):
    """
    Represents an instance of the VERTEX COVER problem.

    Given a graph G = (V, E) and integer k,
    the question is whether G has a vertex cover of size k.

    A vertex cover C ⊆ V satisfies:
        For every edge (u,v) ∈ E, at least one of u or v is in C.
    """
    def __init__(
        self,
        name: str,
        num_vertices: int,
        edges: list[tuple[int, int]],
        k: int,
    ):
        super().__init__(name, num_vertices, edges)

        if not (0 <= k <= num_vertices):
            raise ValueError("k must be between 0 and number of vertices.")

        self.k = k
        self.data["k"] = k

    def __repr__(self) -> str:
        return (
            f"VertexCoverInstance(name={self.name!r}, "
            f"|V|={self.num_vertices}, k={self.k})"
        )

    def verify(self, certificate: list[int]) -> bool:
        if len(certificate) != self.k:
            return False

        if len(set(certificate)) != len(certificate):
            return False

        cover = set(certificate)
        for u, v in self.edges:
            if u not in cover and v not in cover:
                return False

        return True
    
    def to_sat(self) -> SATInstance:
        n = self.num_vertices
        k = self.k

        def var(v: int, i: int) -> int:
            return (v - 1) * k + i

        clauses = []

        # C1: every position in the vertex cover is occupied
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

        # C4: for each edge, at least one endpoint is in the vertex cover
        for (u, v) in self.edges:
            clause = []
            for i in range(1, k + 1):
                clause.append(var(u, i))
                clause.append(var(v, i))
            clauses.append(clause)

        num_vars = n * k

        return SATInstance(
            name=f"{self.name}-to-sat",
            num_vars=num_vars,
            clauses=clauses,
        )
