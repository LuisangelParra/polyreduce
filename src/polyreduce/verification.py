from typing import TypeVar,Tuple

from .problems import ProblemInstance
from .reductions import Reduction
from .sat_solver import SatSolver


P_in = TypeVar("P_in", bound=ProblemInstance, contravariant=True)
P_out = TypeVar("P_out", bound=ProblemInstance, covariant=True)

def verify_reduction_with_sat(
    reduction: Reduction[P_in, P_out],
    original_instance: P_in,
    sat_instance: P_out,
    solver: SatSolver,
) -> Tuple[bool, bool]:
    """
    Verify that the reduction and the SAT instance are consistent.

    Returns:
      (is_valid_reduction, sat_result)

    In this first version we cannot formally "prove" the correctness
    of the reduction, but we can:
    - Reapply the reduction and check whether it matches the expected SAT instance.
    - Solve the SAT instance to obtain a satisfiability result.
    """
    recomputed = reduction.reduce(original_instance)

    structurally_equal = recomputed.data == sat_instance.data
    cnf = sat_instance.data.get("cnf", [])
    sat_result = solver.solve(cnf)

    return structurally_equal, sat_result
