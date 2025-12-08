from polyreduce.reduction import Reduction
from polyreduce.graph.clique_instance import CliqueInstance
from polyreduce.graph.independent_set_instance import IndependentSetInstance


class CliqueToIndependentSet(Reduction[CliqueInstance, IndependentSetInstance]):
    """
    Reduction CLIQUE ≤p INDEPENDENT SET.

    Construction:
        - Given G = (V,E), compute complement graph Gc = (V, E_complement)
        - A clique of size k in G <=> an independent set of size k in Gc.
    """

    def __init__(self):
        super().__init__("CLIQUE", "INDEPENDENT-SET")

    def reduce(self, instance: CliqueInstance) -> IndependentSetInstance:
        V = instance.num_vertices
        original_edges = set()

        # Normalize (u < v) edges
        for u, v in instance.edges:
            if u < v:
                original_edges.add((u, v))
            else:
                original_edges.add((v, u))

        # Compute complement edges
        complement_edges = []
        for u in range(1, V + 1):
            for v in range(u + 1, V + 1):
                if (u, v) not in original_edges:
                    complement_edges.append((u, v))

        return IndependentSetInstance(
            name=f"{instance.name}-complement",
            num_vertices=V,
            edges=complement_edges,
            k=instance.k
        )
