def verify_independent_set(instance, candidate: list[int]) -> bool:
    """
    Verifies whether a candidate vertex set is a valid independent set of size k.
    Runs in polynomial time, as required for NP verification.

    Conditions:
        - Candidate must contain exactly k vertices.
        - All vertices must be distinct.
        - No edge may exist between any two vertices in the candidate.
    """

    if len(candidate) != instance.k:
        return False

    if len(candidate) != len(set(candidate)):
        return False  # duplicates

    for i in range(len(candidate)):
        for j in range(i + 1, len(candidate)):
            u, v = candidate[i], candidate[j]
            if instance.has_edge(u, v):
                return False

    return True
