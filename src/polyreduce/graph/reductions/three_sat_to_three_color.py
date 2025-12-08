from polyreduce.core.reduction import Reduction
from polyreduce.sat import ThreeSATInstance
from polyreduce.graph.three_color_instance import ThreeColorInstance


class ThreeSatToThreeColor(Reduction[ThreeSATInstance, ThreeColorInstance]):
    """
    3SAT → 3COL reduction using raw literal nodes (1, -1, 2, -2, ...)
    and two nested OR-gates per clause, wired as in the lecture gadget.
    """

    def __init__(self):
        super().__init__("3SAT", "3COL")

    def _add_edge(self, edges, u, v):
        if u != v:
            edges.append((u, v))

    def reduce(self, instance: ThreeSATInstance) -> ThreeColorInstance:
        nodes: list[object] = []
        edges: list[tuple[object, object]] = []

        # ------------------------------------------------------
        # Base triangle H, T, F
        # ------------------------------------------------------
        base = ["H", "T", "F"]
        nodes.extend(base)

        for u in base:
            for v in base:
                if u != v:
                    self._add_edge(edges, u, v)

        # ------------------------------------------------------
        # Variable gadgets (raw literals)
        # ------------------------------------------------------
        vars_set = set(abs(lit) for clause in instance.clauses for lit in clause)

        for x in sorted(vars_set):
            pos = x
            neg = -x

            if pos not in nodes:
                nodes.append(pos)
            if neg not in nodes:
                nodes.append(neg)

            # x connected to ¬x
            self._add_edge(edges, pos, neg)

            # both connected to H
            self._add_edge(edges, pos, "H")
            self._add_edge(edges, neg, "H")

        # ------------------------------------------------------
        # Clause gadgets: two nested OR gates per clause
        # ------------------------------------------------------
        gate_id = 1

        for (L1, L2, L3) in instance.clauses:
            # Aseguramos que los literales aparezcan como nodos
            for lit in (L1, L2, L3):
                if lit not in nodes:
                    nodes.append(lit)

            # ===============================
            # OR Gate 1 for (L1, L2)
            # inputs: L1, L2
            # internal: g1a, g1b
            # output:  O1
            # ===============================
            g1a = f"g_{gate_id}_a"
            g1b = f"g_{gate_id}_b"
            O1  = f"O_{gate_id}"
            gate_id += 1

            nodes.extend([g1a, g1b, O1])

            # Cada literal a UN nodo interno distinto (2 edges, no 4)
            self._add_edge(edges, L1, g1a)
            self._add_edge(edges, L2, g1b)

            # Triángulo interno
            self._add_edge(edges, g1a, g1b)
            self._add_edge(edges, g1a, O1)
            self._add_edge(edges, g1b, O1)

            # ===============================
            # OR Gate 2 for (O1, L3)
            # inputs: O1, L3
            # internal: g2a, g2b
            # output:  O2
            # ===============================
            g2a = f"g_{gate_id}_a"
            g2b = f"g_{gate_id}_b"
            O2  = f"O_{gate_id}"
            gate_id += 1

            nodes.extend([g2a, g2b, O2])

            # De nuevo: cada input a un nodo interno distinto
            self._add_edge(edges, O1, g2a)
            self._add_edge(edges, L3, g2b)

            # Triángulo interno
            self._add_edge(edges, g2a, g2b)
            self._add_edge(edges, g2a, O2)
            self._add_edge(edges, g2b, O2)

            # Salida final conectada a H y F (según el slide)
            self._add_edge(edges, O2, "H")
            self._add_edge(edges, O2, "F")

        return ThreeColorInstance(
            nodes=nodes,
            edges=edges,
        )
