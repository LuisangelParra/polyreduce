from polyreduce.reduction import Reduction
from polyreduce.graph.independent_set_instance import IndependentSetInstance
from polyreduce.graph.vertex_cover_instance import VertexCoverInstance


class IndependentSetToVertexCover(Reduction[IndependentSetInstance, VertexCoverInstance]):
    """
    Reduction: INDEPENDENT SET ≤p VERTEX COVER.

    Given:
        (G = (V, E), k)

    Output:
        (G, |V| - k)

    Because:
        C is an independent set of size k
        <=> V\\C is a vertex cover of size |V| - k
    """

    def __init__(self):
        super().__init__("INDEPENDENT-SET", "VERTEX-COVER")

    def reduce(self, instance: IndependentSetInstance) -> VertexCoverInstance:
        V = instance.num_vertices
        new_k = V - instance.k

        return VertexCoverInstance(
            name=f"{instance.name}-to-vertex-cover",
            num_vertices=V,
            edges=instance.edges,
            k=new_k
        )
