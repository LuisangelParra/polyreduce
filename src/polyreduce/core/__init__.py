"""
Core abstractions for all NP problem instances and reductions.
"""

from .problems import ProblemInstance
from .reduction import Reduction
from .verification import verify_reduction_with_sat
from .sat_solver import SatSolver
