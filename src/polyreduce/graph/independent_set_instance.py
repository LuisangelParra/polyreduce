from polyreduce.graph import GraphInstance


class IndependentSetInstance(GraphInstance):
    """
    Represents an instance of the INDEPENDENT SET problem.

    Input:
        - A graph G = (V, E)
        - A target size k

    Question:
        Does G contain an independent set of size k?
    """

    def __init__(self, name: str, num_vertices: int, edges: list[tuple[int, int]], k: int):
        super().__init__(name, num_vertices, edges)

        if not (1 <= k <= num_vertices):
            raise ValueError("k must be between 1 and number of vertices.")

        self.k = k
        self.data["k"] = k

    def __repr__(self):
        return f"IndependentSetInstance(name={self.name!r}, |V|={self.num_vertices}, k={self.k})"
