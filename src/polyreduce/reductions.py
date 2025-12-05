from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .problems import ProblemInstance

P_in = TypeVar("P_in", bound=ProblemInstance)
P_out = TypeVar("P_out", bound=ProblemInstance)


class Reduction(ABC, Generic[P_in, P_out]):
    """
    Base class for polynomial-time reductions between decision problems.

    The idea is that you inherit from this class to implement things like:
    - CLIQUE <=p SAT
    - VERTEX-COVER <=p SAT
    - 3-SAT <=p SAT
    etc.
    """

    source_name: str
    target_name: str

    def __init__(self, source_name: str, target_name: str) -> None:
        self.source_name = source_name
        self.target_name = target_name

    @abstractmethod
    def reduce(self, instance: P_in) -> P_out:
        """
        Apply the polynomial-time reduction.

        Must:
        - Receive an instance of the source problem.
        - Return an instance of the target problem.
        """
        raise NotImplementedError
