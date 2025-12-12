from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from polyreduce.sat.sat_instance import SATInstance

class ProblemInstance(ABC):
    """
    Represents an instance of a decision problem.
    """

    def __init__(self, name: str):
        self.name = name
        self.data: Dict[str, Any] = {"name": name}

    def __repr__(self) -> str:
        return f"ProblemInstance(name={self.name!r}, keys={list(self.data.keys())})"

    @abstractmethod
    def verify(self, certificate: Any) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def to_sat(self) -> SATInstance:
        raise NotImplementedError