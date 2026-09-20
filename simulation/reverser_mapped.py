"""Trial of source-height-derived engagement, not a forced binary lever mode."""

from machinome.parameters import Flag
from simulation.reverser_following import ReverserFollowerTrial


class MappedReverserTrial(ReverserFollowerTrial):
    contact_mapped = Flag(True)
