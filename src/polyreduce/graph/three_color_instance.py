from dataclasses import dataclass
from typing import Any, Dict, List, Tuple
from polyreduce.problems import ProblemInstance


@dataclass
class ThreeColorInstance(ProblemInstance):
    """
    Represents an instance of the 3-COLOR problem.
    Nodes may be strings, integers, or any hashable objects.
    """

    nodes: List[object]
    edges: List[Tuple[object, object]]

    def __post_init__(self):
        self.data = {
            "nodes": self.nodes,
            "edges": self.edges,
        }

    def __repr__(self) -> str:
        return f"ThreeColorInstance(nodes={len(self.nodes)}, edges={len(self.edges)})"
