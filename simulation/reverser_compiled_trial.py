"""Compatibility fixture for the combined restraint now in the default root."""

from simulation.mechanistic import MechanisticCurta


class CompiledReverserTrial(MechanisticCurta):
    # Do not attach another copy of the inherited contact bounds.
    pass
