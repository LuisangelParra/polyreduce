from __future__ import annotations

from typing import List, Sequence, Dict

from polyreduce.core.problems import ProblemInstance
from polyreduce.sat.sat_instance import SATInstance


class SubsetSumInstance(ProblemInstance):
    def __init__(
        self,
        name: str,
        numbers: Sequence[int],
        target: int,
    ):
        super().__init__(name)

        if target < 0:
            raise ValueError("target must be non-negative.")

        self.numbers = list(numbers)
        self.target = target

        self.data = {
            "numbers": self.numbers,
            "target": self.target,
        }

    def __repr__(self) -> str:
        return (
            f"SubsetSumInstance("
            f"name={self.name!r}, "
            f"|U|={len(self.numbers)}, "
            f"target={self.target})"
        )

    def verify(self, certificate: Sequence[bool]) -> bool:
        if len(certificate) != len(self.numbers):
            return False

        total = 0

        for selected, value in zip(certificate, self.numbers):
            if selected:
                total += value

        return total == self.target

    def to_sat(self) -> SATInstance:
        nums = self.numbers
        T = self.target
        n = len(nums)

        clauses: List[List[int]] = []
        var_counter = 0

        def new_var() -> int:
            nonlocal var_counter
            var_counter += 1
            return var_counter

        # --- CNF helpers (Tseitin) ---
        # Ref: https://www.researchgate.net/figure/CNF-signatures-and-graphs-of-some-logic-gates_fig3_363830817
        def add_and(z: int, a: int, b: int) -> None:
            # z <-> (a & b)
            clauses.append([-z, a])
            clauses.append([-z, b])
            clauses.append([z, -a, -b])

        def add_or(z: int, a: int, b: int) -> None:
            # z <-> (a | b)
            clauses.append([z, -a])
            clauses.append([z, -b])
            clauses.append([-z, a, b])

        def add_xor(z: int, a: int, b: int) -> None:
            # z <-> (a xor b)
            clauses.append([-a, -b, -z])
            clauses.append([a, b, -z])
            clauses.append([a, -b, z])
            clauses.append([-a, b, z])

        def add_full_adder(a: int, b: int, cin: int) -> tuple[int, int]:
            """
            Returns (s, cout) where:
            s = a xor b xor cin
            cout = majority(a,b,cin) = (a&b) | (a&cin) | (b&cin)
            """
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

            o1 = new_var()
            add_or(o1, c1, c2)

            cout = new_var()
            add_or(cout, o1, c3)

            return s, cout

        # --- SAT constants ---
        TRUE = new_var()
        FALSE = new_var()
        clauses.append([TRUE])      # TRUE = 1
        clauses.append([-FALSE])    # FALSE = 0

        # --- Selection vars x_i ---
        x_vars = [new_var() for _ in range(n)]

        # --- bit-width ---
        max_sum = sum(nums)
        B = max_sum.bit_length()

        # --- build selected-number bits: b_i[j] = x_i AND bit(nums[i],j) ---
        sel_bits: List[List[int]] = []
        for i, val in enumerate(nums):
            row: List[int] = []
            for j in range(B):
                if ((val >> j) & 1) == 0:
                    row.append(FALSE)
                else:
                    z = new_var()
                    add_and(z, x_vars[i], TRUE)  # z <-> x_i
                    row.append(z)
            sel_bits.append(row)

        # --- sequential ripple addition: acc = sum(sel_bits[i]) ---
        acc = [FALSE] * B

        for i in range(n):
            carry = FALSE
            new_acc: List[int] = []
            for j in range(B):
                s, carry = add_full_adder(acc[j], sel_bits[i][j], carry)
                new_acc.append(s)
            acc = new_acc

        # --- enforce acc == T ---
        for j in range(B):
            if ((T >> j) & 1) == 1:
                clauses.append([acc[j]])
            else:
                clauses.append([-acc[j]])

        return SATInstance(
            name=f"{self.name}_to_SAT",
            num_vars=var_counter,
            clauses=clauses,
        )
