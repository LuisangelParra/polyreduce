from polyreduce.graph.reductions.clique_to_independent_set import CliqueToIndependentSet
from polyreduce.graph.reductions.is_to_vertex_cover import IndependentSetToVertexCover
from polyreduce.graph.reductions.vertex_cover_to_clique import VertexCoverToClique
from polyreduce.set.reductions.vertex_cover_to_set_cover import VertexCoverToSetCover
from polyreduce.graph.reductions.three_sat_to_clique import ThreeSATToClique
from polyreduce.graph.reductions.three_sat_to_hamiltonian_cycle import ThreeSATToHamiltonianCycle
from polyreduce.graph.reductions.three_sat_to_three_color import ThreeSatToThreeColor
from polyreduce.number.reductions.three_sat_to_subset_sum import ThreeSATToSubsetSum
from polyreduce.number.reductions.subset_sum_to_knapsack import SubsetSumToKnapsack
from polyreduce.sat.reductions.sat_to_3sat import SatToThreeSat


REDUCTIONS = {
    "SAT": [SatToThreeSat()],
    "3SAT": [
        ThreeSATToClique(),
        ThreeSATToHamiltonianCycle(),
        ThreeSatToThreeColor(),
        ThreeSATToSubsetSum(),
    ],
    "CLIQUE": [CliqueToIndependentSet()],
    "INDEPENDENT_SET": [IndependentSetToVertexCover()],
    "VERTEX_COVER": [
        VertexCoverToClique(),
        VertexCoverToSetCover(),
    ],
    "SUBSET_SUM": [SubsetSumToKnapsack()],
}
