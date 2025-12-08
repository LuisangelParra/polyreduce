"""
polyreduce: Polynomial-time reductions between NP problems with SAT verification.
"""

from .problems import ProblemInstance
from .reduction import Reduction
from .verification import verify_reduction_with_sat
from .sat.sat_instance import SATInstance
from .graph.graph_instance import GraphInstance



__all__ = [
    "ProblemInstance",
    "Reduction",
    "verify_reduction_with_sat",
    "SATInstance",
    "GraphInstance",
]

__version__ = "0.1.0"
