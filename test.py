from polyreduce.sat.three_sat import ThreeSATInstance
from polyreduce.graph.reductions.three_sat_to_hamiltonian_cycle import ThreeSATToHamiltonianCycle
from polyreduce.sat.solvers.pysat_solver import PySatSolver

solver = PySatSolver()
reduce = ThreeSATToHamiltonianCycle()

sat_false = ThreeSATInstance(
    name="3sat_false_short",
    num_vars=3,
    clauses=[
        [ 1,  2,  3],
        [ 1,  2, -3],
        [-1, -2,  3],
        [-1, -2, -3],
    ],
)


hc_false = reduce.reduce(sat_false)

print("SOURCE FALSE:", sat_false)
print("TARGET FALSE:", hc_false)

print("Is SOURCE satisfiable?", sat_false.to_sat().is_satisfiable(solver))
print("Is TARGET satisfiable?", hc_false.to_sat().is_satisfiable(solver))
