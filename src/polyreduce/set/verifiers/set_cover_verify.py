from __future__ import annotations

from typing import Sequence

from polyreduce.set.set_cover_instance import SetCoverInstance


def verify_set_cover(
    instance: SetCoverInstance,
    certificate: Sequence[int],
) -> bool:
    return instance.verify(certificate)
