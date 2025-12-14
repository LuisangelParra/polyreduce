from __future__ import annotations

from typing import List

from polyreduce.core.reduction import Reduction
from polyreduce.sat.three_sat import ThreeSATInstance
from polyreduce.number.subset_sum_instance import SubsetSumInstance


class ThreeSATToSubsetSum(Reduction[ThreeSATInstance, SubsetSumInstance]):
    def __init__(self):
        super().__init__("3-SAT", "SUBSET-SUM")

    def reduce(self, instance: ThreeSATInstance) -> SubsetSumInstance:
        clauses = instance.clauses

        vars: List[int] = []
        for clause in clauses:
            for lit in clause:
                v = abs(lit)
                if v not in vars:
                    vars.append(v)

        t = len(vars)
        m = len(clauses)

        def make_number(bits: List[int]) -> int:
            return int("".join(str(b) for b in bits))

        numbers: List[int] = []

        for i, var in enumerate(vars):
            pos_bits = [0] * (t + m)
            neg_bits = [0] * (t + m)

            pos_bits[i] = 1
            neg_bits[i] = 1

            for j, clause in enumerate(clauses):
                if var in clause:
                    pos_bits[t + j] = 1
                if -var in clause:
                    neg_bits[t + j] = 1

            numbers.append(make_number(pos_bits))
            numbers.append(make_number(neg_bits))

        for j in range(m):
            bits = [0] * (t + m)
            bits[t + j] = 1
            num = make_number(bits)
            numbers.append(num)
            numbers.append(num)

        target_bits = [1] * t + [3] * m
        target = make_number(target_bits)

        return SubsetSumInstance(
            name=f"Subset-Sum from {instance.name}",
            numbers=numbers,
            target=target,
        )
