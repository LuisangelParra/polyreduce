from polyreduce.graph import GraphInstance


class VertexCoverInstance(GraphInstance):
    """
    Represents an instance of the VERTEX COVER problem.

    Given a graph G = (V, E) and integer k,
    the question is whether G has a vertex cover of size k.

    A vertex cover C ⊆ V satisfies:
        For every edge (u,v) ∈ E, at least one of u or v is in C.
    """

    def __init__(self, name: str, num_vertices: int, edges: list[tuple[int, int]], k: int):
        super().__init__(name, num_vertices, edges)

        if not (1 <= k <= num_vertices):
            raise ValueError("k must be between 1 and |V|.")

        self.k = k
        self.data["k"] = k

    def __repr__(self):
        return f"VertexCoverInstance(name={self.name!r}, |V|={self.num_vertices}, k={self.k})"
