from polyreduce.reduction import Reduction
from polyreduce.sat.three_sat import ThreeSATInstance
from polyreduce.graph.clique_instance import CliqueInstance


class ThreeSATToClique(Reduction[ThreeSATInstance, CliqueInstance]):
    """
    Classical reduction 3SAT ≤p CLIQUE.

    Construction:
        - For each clause C_r (with 3 literals), create 3 nodes.
        - Add an edge between nodes (r,i) and (s,j) iff:
              r != s  AND  literal_i is NOT the negation of literal_j.
        - Target clique size k = number of clauses.

    A satisfying assignment exists iff graph contains
    a clique of size equal to number of clauses.
    """

    def __init__(self):
        super().__init__("3SAT", "CLIQUE")

    def reduce(self, instance: ThreeSATInstance) -> CliqueInstance:
        clauses = instance.clauses
        num_clauses = len(clauses)

        node_id = {}
        current = 1

        # --- Step 1: create nodes: 3 per clause ---
        for r, clause in enumerate(clauses, start=1):
            for i in range(3):
                node_id[(r, i)] = current
                current += 1

        edges = []

        # --- Step 2: connect nodes if compatible ---
        for r, clause_r in enumerate(clauses, start=1):
            for i, lit_i in enumerate(clause_r):
                for s, clause_s in enumerate(clauses, start=1):
                    if r >= s:
                        continue
                    for j, lit_j in enumerate(clause_s):
                        # Two literals contradict if lit_i == -lit_j
                        if lit_i != -lit_j:
                            u = node_id[(r, i)]
                            v = node_id[(s, j)]
                            edges.append((u, v))

        num_vertices = current - 1
        k = num_clauses

        return CliqueInstance(
            name="3SAT→CLIQUE",
            num_vertices=num_vertices,
            edges=edges,
            k=k
        )
