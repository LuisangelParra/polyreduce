from typing import Tuple

from .problems import ProblemInstance
from .reductions import Reduction
from .sat_solver import SatSolver


def verify_reduction_with_sat(
    reduction: Reduction[ProblemInstance, ProblemInstance],
    original_instance: ProblemInstance,
    sat_instance: ProblemInstance,
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
