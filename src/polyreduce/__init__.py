"""
polyreduce: Polynomial-time reductions between NP problems with SAT verification.
"""

from .problems import ProblemInstance
from .reductions import Reduction
from .verification import verify_reduction_with_sat

__all__ = [
    "ProblemInstance",
    "Reduction",
    "verify_reduction_with_sat",
]

__version__ = "0.1.0"
