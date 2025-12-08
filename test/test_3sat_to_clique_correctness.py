from polyreduce.sat.sat_instance import SATInstance
from polyreduce.sat.three_sat import ThreeSATInstance
from polyreduce.sat.reductions.sat_to_3sat import convert_to_3sat
from polyreduce.graph.reductions.three_sat_to_clique import ThreeSATToClique
from polyreduce.graph.verifiers.clique_verify import verify_clique_solution
from polyreduce.sat.solvers.pysat_solver import PySatSolver


def test_3sat_to_clique_reduction_validity():
    solver = PySatSolver()

    # SAT instance (satisfiable)
    sat = ThreeSATInstance(
        name="φ1",
        num_vars=3,
        clauses=[
            [1, -2, 3],
            [-1, 2, 3],
        ]
    )

    # Check SAT satisfiability
    assert solver.solve(sat.clauses) is True

    # Reduce to CLIQUE
    reducer = ThreeSATToClique()
    clique_inst = reducer.reduce(sat)

    # We KNOW there exists a clique of size 2
    # From a satisfying assignment, we manually propose:
    # Clause1: pick literal "1"  → node_id (1,0)
    # Clause2: pick literal "3"  → node_id (2,2)
    candidate = [1, 6]  # Example IDs depending on construction

    assert verify_clique_solution(clique_inst, candidate) is True


def test_3sat_to_clique_unsat_does_not_force_search():
    solver = PySatSolver()

    # UNSAT instance
    unsat = ThreeSATInstance(
        name="φ2",
        num_vars=1,
        clauses=[
            [1, 1, 1],
            [-1, -1, -1],
        ]
    )

    # Check UNSAT
    assert solver.solve(unsat.clauses) is False

    # Reduce to CLIQUE
    reducer = ThreeSATToClique()
    clique_inst = reducer.reduce(unsat)

    # We NEVER try to "search" a clique.
    # Just verify that proposing a random incorrect candidate returns False.
    assert verify_clique_solution(clique_inst, [1]) is False
