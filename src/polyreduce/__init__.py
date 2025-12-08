"""
polyreduce: A framework for polynomial-time reductions between NP problems.
"""

# Re-export core interfaces
from .core.problems import ProblemInstance
from .core.reduction import Reduction
from .core.verification import verify_reduction_with_sat
from .core.sat_solver import SatSolver

# Expose high-level modules
import polyreduce.sat
import polyreduce.graph
