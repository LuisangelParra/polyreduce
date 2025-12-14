from polyreduce.cli.defaults import default_instances
from polyreduce.cli.registry import REDUCTIONS
from polyreduce.cli.runners import run_instance, run_reduction
from polyreduce.cli.loaders import load_instance_from_file


def main():
    print("=== PolyReduce CLI ===\n")
    mode = input("Use default instance or load from file? [d/f]: ").strip().lower()

    if mode == "f":
        path = input("Path to instance file (.json): ").strip()
        instance = load_instance_from_file(path)
        problem_key = instance.__class__.__name__.replace("Instance", "").upper()
    else:
        instances = default_instances()

        print("=== PolyReduce CLI ===\n")
        print("Available problems:")
        for i, key in enumerate(instances.keys(), 1):
            print(f"{i}. {key}")

        choice = int(input("\nSelect problem: ")) - 1
        problem_key = list(instances.keys())[choice]
        instance = instances[problem_key]

    print("\n--- SOURCE INSTANCE ---")
    sat_source = run_instance(instance)

    reductions = REDUCTIONS.get(problem_key, [])
    if not reductions:
        print("\n(No reductions available)")
        return

    print("\nAvailable reductions:")
    for i, r in enumerate(reductions, 1):
        print(f"{i}. {r.source_name} → {r.target_name}")
        r_choice = int(input("\nSelect reduction: ")) - 1
        reduction = reductions[r_choice]

        run_reduction(instance, reduction)


if __name__ == "__main__":
    main()
