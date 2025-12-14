from __future__ import annotations

from typing import Sequence, Tuple

from polyreduce.core.problems import ProblemInstance
from polyreduce.sat.sat_instance import SATInstance


class KnapsackInstance(ProblemInstance):
    def __init__(
        self,
        name: str,
        items: Sequence[Tuple[int, int]],
        capacity: int,
        min_value: int,
    ):
        super().__init__(name)

        if capacity < 0:
            raise ValueError("capacity must be non-negative.")

        if min_value < 0:
            raise ValueError("min_value must be non-negative.")

        self.items = list(items)
        self.capacity = capacity
        self.min_value = min_value

        self.data = {
            "items": self.items,
            "capacity": self.capacity,
            "min_value": self.min_value,
        }

    def __repr__(self) -> str:
        return (
            f"KnapsackInstance("
            f"name={self.name!r}, "
            f"|W|={len(self.items)}, "
            f"capacity={self.capacity}, "
            f"min_value={self.min_value})"
        )

    def verify(self, certificate: Sequence[bool]) -> bool:
        if len(certificate) != len(self.items):
            return False

        total_weight = 0
        total_value = 0

        for selected, (weight, value) in zip(certificate, self.items):
            if selected:
                total_weight += weight
                total_value += value

        if total_weight > self.capacity:
            return False

        if total_value < self.min_value:
            return False

        return True
    
    def to_sat(self) -> SATInstance:
        items = self.items
        C = self.capacity
        Vmin = self.min_value
        n = len(items)

        clauses: list[list[int]] = []
        var_counter = 0

        def new_var() -> int:
            nonlocal var_counter
            var_counter += 1
            return var_counter

        # ---------- Tseitin helpers ----------

        def add_and(z, a, b):
            clauses.append([-z, a])
            clauses.append([-z, b])
            clauses.append([z, -a, -b])

        def add_or(z, a, b):
            clauses.append([z, -a])
            clauses.append([z, -b])
            clauses.append([-z, a, b])

        def add_not(z, a):
            clauses.append([z, a])
            clauses.append([-z, -a])

        def add_xor(z, a, b):
            clauses.append([-a, -b, -z])
            clauses.append([a, b, -z])
            clauses.append([a, -b, z])
            clauses.append([-a, b, z])

        def full_adder(a, b, cin):
            t = new_var()
            add_xor(t, a, b)

            s = new_var()
            add_xor(s, t, cin)

            c1 = new_var()
            c2 = new_var()
            c3 = new_var()
            add_and(c1, a, b)
            add_and(c2, a, cin)
            add_and(c3, b, cin)

            o = new_var()
            add_or(o, c1, c2)

            cout = new_var()
            add_or(cout, o, c3)

            return s, cout

        # ---------- SAT constants ----------

        TRUE = new_var()
        FALSE = new_var()
        clauses.append([TRUE])
        clauses.append([-FALSE])

        # ---------- Selection variables ----------

        x_vars = [new_var() for _ in range(n)]

        # ---------- Bit widths ----------

        max_weight = sum(w for w, _ in items)
        max_value = sum(v for _, v in items)

        Bw = max_weight.bit_length()
        Bv = max_value.bit_length()

        # ---------- Build weighted bits ----------

        def build_weighted_bits(values, B):
            rows = []
            for i, val in enumerate(values):
                row = []
                for j in range(B):
                    if ((val >> j) & 1) == 0:
                        row.append(FALSE)
                    else:
                        z = new_var()
                        add_and(z, x_vars[i], TRUE)
                        row.append(z)
                rows.append(row)
            return rows


        weight_bits = build_weighted_bits([w for w, _ in items], Bw)
        value_bits  = build_weighted_bits([v for _, v in items], Bv)


        # ---------- Ripple-carry sum ----------

        def sum_bits(bit_rows, B):
            acc = [FALSE] * B
            for i in range(len(bit_rows)):
                carry = FALSE
                new_acc = []
                for j in range(B):
                    s, carry = full_adder(acc[j], bit_rows[i][j], carry)
                    new_acc.append(s)
                acc = new_acc
            return acc

        W = sum_bits(weight_bits, Bw)
        V = sum_bits(value_bits, Bv)

        # ---------- Comparator A < B ----------

        def less_than(A, B):
            assert len(A) == len(B)
            k = len(A)

            eq_prefix = TRUE
            lt_terms = []

            for i in reversed(range(k)):
                xor = new_var()
                add_xor(xor, A[i], B[i])

                eq = new_var()
                add_not(eq, xor)

                nota = new_var()
                add_not(nota, A[i])

                lt = new_var()
                add_and(lt, nota, B[i])

                cond = new_var()
                add_and(cond, eq_prefix, lt)
                lt_terms.append(cond)

                new_eq = new_var()
                add_and(new_eq, eq_prefix, eq)
                eq_prefix = new_eq

            cur = lt_terms[0]
            for t in lt_terms[1:]:
                nxt = new_var()
                add_or(nxt, cur, t)
                cur = nxt

            return cur


        # ---------- Enforce constraints ----------

        # W ≤ C  ⇔  NOT (W > C)
        C_bits = [(C >> j) & 1 for j in range(Bw)]
        C_vars = []
        for bit in C_bits:
            if bit == 1:
                C_vars.append(TRUE)
            else:
                C_vars.append(FALSE)

        w_gt_c = less_than(C_vars, W)
        clauses.append([-w_gt_c])

        # V ≥ Vmin  ⇔  NOT (V < Vmin)
        Vmin_bits = [(Vmin >> j) & 1 for j in range(Bv)]
        Vmin_vars = []
        for bit in Vmin_bits:
            if bit == 1:
                Vmin_vars.append(TRUE)
            else:
                Vmin_vars.append(FALSE)

        v_lt_vmin = less_than(V, Vmin_vars)
        clauses.append([-v_lt_vmin])

        return SATInstance(
            name=f"{self.name}_to_SAT",
            num_vars=var_counter,
            clauses=clauses,
        )

