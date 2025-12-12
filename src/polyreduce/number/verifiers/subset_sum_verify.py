from __future__ import annotations

from typing import Sequence

from polyreduce.number.subset_sum_instance import SubsetSumInstance


def verify_subset_sum(
    instance: SubsetSumInstance,
    certificate: Sequence[bool],
) -> bool:
    return instance.verify(certificate)
