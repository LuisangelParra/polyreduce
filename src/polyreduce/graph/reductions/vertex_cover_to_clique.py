from polyreduce.core.reduction import Reduction
from polyreduce.graph.vertex_cover_instance import VertexCoverInstance
from polyreduce.graph.clique_instance import CliqueInstance


class VertexCoverToClique(Reduction[VertexCoverInstance, CliqueInstance]):
    """
    Reduction from Vertex Cover to Clique.

    Input:  VertexCoverInstance on a graph G = (V, E) with |V| = n and parameter k.
    Output: CliqueInstance on the complement graph G' = (V, E')
            with clique size k' = n - k.

    Construction:
      - V is {1, 2, ..., n} implicitly (as in GraphInstance).
      - E' contains all edges (u, v) with u < v such that (u, v) ∉ E.
    """

    def __init__(self) -> None:
        super().__init__(source_name="VertexCover", target_name="Clique")

    def reduce(self, instance: VertexCoverInstance) -> CliqueInstance:
        n = instance.num_vertices
        original_edges = set()

        # Normalize edges to (min, max) for easy lookup
        for (u, v) in instance.edges:
            if u == v:
                continue
            if u > v:
                u, v = v, u
            original_edges.add((u, v))

        complement_edges: list[tuple[int, int]] = []

        # Build complement graph on vertices {1, 2, ..., n}
        for u in range(1, n + 1):
            for v in range(u + 1, n + 1):
                if (u, v) not in original_edges:
                    complement_edges.append((u, v))

        # New clique size: |V| - k
        new_k = n - instance.k

        return CliqueInstance(
            name=f"{instance.name}-to-clique",
            num_vertices=n,
            edges=complement_edges,
            k=new_k,
        )
