import json

from polyreduce.sat.sat_instance import SATInstance
from polyreduce.sat.three_sat import ThreeSATInstance
from polyreduce.graph.clique_instance import CliqueInstance
from polyreduce.graph.independent_set_instance import IndependentSetInstance
from polyreduce.graph.vertex_cover_instance import VertexCoverInstance
from polyreduce.graph.hamiltonian_cycle_instance import HamiltonianCycleInstance
from polyreduce.graph.three_color_instance import ThreeColorInstance
from polyreduce.number.subset_sum_instance import SubsetSumInstance
from polyreduce.number.knapsack_instance import KnapsackInstance
from polyreduce.set.set_cover_instance import SetCoverInstance


def load_instance_from_file(path: str):
    with open(path, "r") as f:
        data = json.load(f)

    t = data["type"].upper()
    name = data.get("name", "loaded_instance")

    if t == "SAT":
        return SATInstance(name, data["num_vars"], data["clauses"])

    if t == "3SAT":
        return ThreeSATInstance(name, data["num_vars"], data["clauses"])

    if t == "CLIQUE":
        return CliqueInstance(
            name,
            data["num_vertices"],
            [tuple(e) for e in data["edges"]],
            data["k"],
        )

    if t == "INDEPENDENT_SET":
        return IndependentSetInstance(
            name,
            data["num_vertices"],
            [tuple(e) for e in data["edges"]],
            data["k"],
        )

    if t == "VERTEX_COVER":
        return VertexCoverInstance(
            name,
            data["num_vertices"],
            [tuple(e) for e in data["edges"]],
            data["k"],
        )

    if t == "HAM_CYCLE":
        return HamiltonianCycleInstance(
            name,
            data["num_vertices"],
            [tuple(e) for e in data["edges"]],
        )

    if t == "3COLOR":
        return ThreeColorInstance(
            name,
            data["nodes"],
            [tuple(e) for e in data["edges"]],
        )

    if t == "SUBSET_SUM":
        return SubsetSumInstance(
            name,
            data["numbers"],
            data["target"],
        )

    if t == "KNAPSACK":
        return KnapsackInstance(
            name,
            [tuple(x) for x in data["items"]],
            data["capacity"],
            data["min_value"],
        )

    if t == "SET_COVER":
        return SetCoverInstance(
            name,
            set(data["universe"]),
            [set(s) for s in data["subsets"]],
            data["k"],
        )

    raise ValueError(f"Unknown instance type: {t}")
