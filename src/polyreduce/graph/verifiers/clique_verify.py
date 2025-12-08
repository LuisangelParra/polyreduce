from polyreduce.graph.clique_instance import CliqueInstance


def verify_clique_solution(instance: CliqueInstance, candidate: list[int]) -> bool:
    """
    Verifies whether a candidate list of vertices forms a valid clique
    of size k in the given CliqueInstance.

    Conditions:
        - candidate must contain exactly k vertices
        - candidate vertices must be distinct
        - every pair of vertices must have an edge between them
    """

    if len(candidate) != instance.k:
        return False

    if len(set(candidate)) != len(candidate):
        return False  # duplicate vertices

    # Check all pairs
    for i in range(len(candidate)):
        for j in range(i + 1, len(candidate)):
            u = candidate[i]
            v = candidate[j]
            if not instance.has_edge(u, v):
                return False

    return True
