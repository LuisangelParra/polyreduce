from polyreduce.sat.solvers.pysat_solver import PySatSolver


def run_instance(instance):
    solver = PySatSolver()
    print("INSTANCE:", instance)
    sat = instance.to_sat().is_satisfiable(solver)
    print("SAT:", sat)
    return sat


def run_reduction(instance, reduction):
    solver = PySatSolver()

    print("\n--- REDUCTION:", reduction.source_name, "→", reduction.target_name, "---")
    print("SOURCE:", instance)

    sat_source = instance.to_sat().is_satisfiable(solver)
    print("SAT(SOURCE):", sat_source)

    target = reduction.reduce(instance)
    print("TARGET:", target)

    sat_target = target.to_sat().is_satisfiable(solver)
    print("SAT(TARGET):", sat_target)

    print("PRESERVES SAT:", sat_source == sat_target)
