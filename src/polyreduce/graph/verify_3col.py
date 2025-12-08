def verify_3col(instance, candidate):
    nodes = instance.nodes
    edges = instance.edges

    # We accept string or integer nodes
    for v in nodes:
        if v not in candidate:
            return False
        if candidate[v] not in (1, 2, 3):
            return False

    for (u, v) in edges:
        if candidate[u] == candidate[v]:
            return False

    return True


