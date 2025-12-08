from polyreduce.sat import ThreeSATInstance
from polyreduce.graph.three_color_instance import ThreeColorInstance
from polyreduce.reductions.sat3_to_3col import ThreeSatToThreeColor


def is_3colorable(instance: ThreeColorInstance) -> bool:
    """
    Backtracking 3-coloring solver with the REQUIRED constraints:

        H = 0
        T = 1
        F = 2
    """

    nodes = list(instance.nodes)
    edges = instance.edges
    palette = (0, 1, 2)
    color = {}

    # Forced colors (theoretical gadget requirement)
    fixed = {"H": 0, "T": 1, "F": 2}

    # adjacency list
    adj = {v: set() for v in nodes}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)

    def backtrack(i: int) -> bool:
        if i == len(nodes):
            return all(color[u] != color[v] for u, v in edges)

        v = nodes[i]

        # If v has a fixed color, enforce it
        if isinstance(v, str) and v in fixed:
            color[v] = fixed[v]
            result = backtrack(i + 1)
            del color[v]
            return result

        # Otherwise, try all colors
        for c in palette:
            if any(nb in color and color[nb] == c for nb in adj[v]):
                continue

            color[v] = c
            if backtrack(i + 1):
                return True
            del color[v]

        return False

    return backtrack(0)

def test_3sat_to_3col_satisfiable_instance():
    """
    If a 3SAT formula is satisfiable, then the graph produced by the
    3SAT → 3COL reduction must be 3-colorable.
    """

    # Satisfiable 3SAT instance (small and simple)
    instance = ThreeSATInstance(
        name="sat-3sat",
        num_vars=3,
        clauses=[
            [1, 2, 3],
            [1, -2, 3],
        ],
    )

    reduction = ThreeSatToThreeColor()
    graph = reduction.reduce(instance)

    assert isinstance(graph, ThreeColorInstance)
    assert is_3colorable(graph) is True


def test_3sat_to_3col_unsatisfiable_instance():
    """
    If a 3SAT formula is UNSAT, then the graph produced by the
    3SAT → 3COL reduction must NOT be 3-colorable.

    Use an unsatisfiable 3CNF:
        (x ∨ x ∨ x) ∧ (¬x ∨ ¬x ∨ ¬x)
    """

    instance = ThreeSATInstance(
        name="unsat-3sat",
        num_vars=1,
        clauses=[
            [1, 1, 1],     # x ∨ x ∨ x
            [-1, -1, -1],  # ¬x ∨ ¬x ∨ ¬x
        ],
    )

    reduction = ThreeSatToThreeColor()
    graph = reduction.reduce(instance)

    assert isinstance(graph, ThreeColorInstance)
    assert is_3colorable(graph) is False
