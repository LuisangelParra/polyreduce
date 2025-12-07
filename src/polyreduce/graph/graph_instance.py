from polyreduce import ProblemInstance


class GraphInstance(ProblemInstance):
    """
    Represents an undirected graph G = (V, E).

    Vertices are numbered from 1 to n. Edges are unordered pairs (u, v).
    Internally, adjacency lists are used for efficient operations.
    """

    def __init__(self, name: str, num_vertices: int, edges: list[tuple[int, int]]):
        super().__init__(name)

        self.num_vertices = num_vertices
        self.edges = edges

        # Build adjacency list
        self.adj = {v: set() for v in range(1, num_vertices + 1)}

        for (u, v) in edges:
            if not (1 <= u <= num_vertices) or not (1 <= v <= num_vertices):
                raise ValueError(f"Invalid edge ({u}, {v}): vertex index out of range.")

            if u == v:
                raise ValueError(f"Self-loop detected: ({u}, {v})")

            # undirected graph
            self.adj[u].add(v)
            self.adj[v].add(u)

        # internal data for reductions
        self.data = {
            "num_vertices": num_vertices,
            "edges": edges,
            "adjacency": self.adj,
        }

    # ------------------------------
    # Graph utilities
    # ------------------------------

    def neighbors(self, v: int) -> set[int]:
        """Returns the set of neighbors of vertex v."""
        return self.adj[v]

    def has_edge(self, u: int, v: int) -> bool:
        """Returns True if (u, v) is an edge."""
        return v in self.adj[u]

    def degree(self, v: int) -> int:
        """Returns degree of vertex v."""
        return len(self.adj[v])

    def to_adjacency_matrix(self) -> list[list[int]]:
        """(Optional) Returns adjacency matrix A where A[u][v] = 1 if edge exists."""
        matrix = [[0] * self.num_vertices for _ in range(self.num_vertices)]
        for u in range(1, self.num_vertices + 1):
            for v in self.adj[u]:
                matrix[u - 1][v - 1] = 1
                matrix[v - 1][u - 1] = 1
        return matrix

    def __repr__(self):
        return f"GraphInstance(name={self.name!r}, |V|={self.num_vertices}, |E|={len(self.edges)})"
