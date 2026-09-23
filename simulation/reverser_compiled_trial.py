"""Compatibility fixture for the combined restraint now in the default root."""

from simulation.running import OperatingCurta


class CompiledReverserTrial(OperatingCurta):
    # Do not attach another copy of the inherited contact bounds.
    pass
