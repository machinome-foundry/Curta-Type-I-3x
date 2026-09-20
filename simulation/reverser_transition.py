"""Installed reverser travel, including the actual lower housing opening."""

from simulation.reverser_following import ReverserFollowerTrial
from simulation.running_parts import RunningEnclosure


class EnclosedReverserTrial(ReverserFollowerTrial):
    enclosure = RunningEnclosure()
