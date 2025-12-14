from __future__ import annotations

from typing import Hashable, List, Set, Tuple

from polyreduce.core.reduction import Reduction
from polyreduce.set.set_cover_instance import SetCoverInstance
from polyreduce.graph.vertex_cover_instance import VertexCoverInstance

class VertexCoverToSetCover(Reduction[VertexCoverInstance, SetCoverInstance]):
    def __init__(self):
        super().__init__("VERTEX-COVER", "SET-COVER")
        
    def reduce(self, instance: VertexCoverInstance) -> SetCoverInstance:
        # Construc the universe U from the set of edges. Type of Universe is Set[Hashable]
        universe: Set[Hashable] = set()
        for edge in instance.edges:
            universe.add(edge)
        
        # Construct the set of subsets T from the respective incident edges of the nodes. Type of Subsets is List[Set[Hashable]]
        subsets: List[Set[Hashable]] = []
        for v in range(instance.num_vertices):
            incident_edges: Set[Hashable] = set()
            for edge in instance.edges:
                if edge[0] == v or edge[1] == v:
                    incident_edges.add(edge)
            subsets.append(incident_edges)
        
        return SetCoverInstance(
            name=f"Set-Cover from {instance.name}",
            universe=universe,
            subsets=subsets,
            k=instance.k,
        )
        