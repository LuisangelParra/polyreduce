from polyreduce.sat.three_sat import ThreeSATInstance
from polyreduce.graph.clique_instance import CliqueInstance
from polyreduce.graph.independent_set_instance import IndependentSetInstance
from polyreduce.graph.vertex_cover_instance import VertexCoverInstance
from polyreduce.graph.hamiltonian_cycle_instance import HamiltonianCycleInstance
from polyreduce.graph.three_color_instance import ThreeColorInstance
from polyreduce.number.subset_sum_instance import SubsetSumInstance
from polyreduce.number.knapsack_instance import KnapsackInstance
from polyreduce.set.set_cover_instance import SetCoverInstance
from polyreduce.sat.sat_instance import SATInstance


def default_instances():
    return {
        "SAT": SATInstance(
            name="sat_default",
            num_vars=2,
            clauses=[[1, 2], [-1, 2]],
        ),

        "3SAT": ThreeSATInstance(
            name="3sat_default",
            num_vars=3,
            clauses=[[1, 2, 3], [-1, 2, 3]],
        ),

        "CLIQUE": CliqueInstance(
            name="clique_default",
            num_vertices=4,
            edges=[(1,2),(1,3),(2,3),(3,4)],
            k=3,
        ),

        "INDEPENDENT_SET": IndependentSetInstance(
            name="is_default",
            num_vertices=4,
            edges=[(1,2),(2,3),(3,4)],
            k=2,
        ),

        "VERTEX_COVER": VertexCoverInstance(
            name="vc_default",
            num_vertices=4,
            edges=[(1,2),(2,3),(3,4)],
            k=2,
        ),

        "HAM_CYCLE": HamiltonianCycleInstance(
            name="hc_default",
            num_vertices=4,
            edges=[(1,2),(2,3),(3,4),(4,1)],
        ),

        "3COLOR": ThreeColorInstance(
            name="3col_default",
            nodes=[1,2,3],
            edges=[(1,2),(2,3)],
        ),

        "SUBSET_SUM": SubsetSumInstance(
            name="ss_default",
            numbers=[3, 7, 11],
            target=10,
        ),

        "KNAPSACK": KnapsackInstance(
            name="ks_default",
            items=[(2,3),(3,4),(4,5)],
            capacity=5,
            min_value=7,
        ),

        "SET_COVER": SetCoverInstance(
            name="sc_default",
            universe={1,2,3},
            subsets=[{1},{2},{3}],
            k=3,
        ),
    }
