from __future__ import annotations

from typing import Sequence

from polyreduce.graph.hamiltonian_cycle_instance import HamiltonianCycleInstance


def verify_hamiltonian_cycle(
    instance: HamiltonianCycleInstance,
    certificate: Sequence[int],
) -> bool:
    return instance.verify(certificate)
