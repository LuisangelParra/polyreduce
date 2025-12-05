from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ProblemInstance:
    """
    Represents an instance of a decision problem.

    In this first version we leave it generic. Later
    you will be able to specialize for SAT, 3-SAT, CLIQUE, VERTEX-COVER, etc.
    """
    name: str
    data: Dict[str, Any]

    def __repr__(self) -> str:
        return f"ProblemInstance(name={self.name!r}, keys={list(self.data.keys())})"
