def verify_vertex_cover(instance, candidate: list[int]) -> bool:
    """
    Verifies whether a candidate vertex set is a valid vertex cover.

    Conditions:
        - |candidate| <= k
        - For every edge (u, v), at least one of them is in the set.

    Runs in polynomial time as required for NP verification.
    """
    if len(candidate) > instance.k:
        return False

    C = set(candidate)

    for (u, v) in instance.edges:
        if not (u in C or v in C):
            return False

    return True
