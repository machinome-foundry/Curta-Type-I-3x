"""Historical inner-flank-only fixture, without the compiled axial restraint.

The retained reversed-counter path intersects the nine-tooth drum at crank
82.432377 degrees with the existing .36 mm fit. A native pair survey still
finds contact at .41 mm but none at .415 mm over 80--88 degrees at .1 degree
spacing. That sampling does not establish whole-stroke clearance or capture.
Uniform .415 relief loses axial fork capture at crank 75. That capture uses
the outer tips at radii 6.1657--6.2262, whereas the crank-83 drum collision
is at radii 4.5083--4.6195. Retain the existing .36 profile outside R6.
Inner .415 relief passes native clearance/capture but leaves only .00035 mm
at the closest measured passage. The .43 candidate adds a named .01 mm
minimum flank gap to accommodate both .005 mm outward contact covers,
without changing the preserved tips, fork or tooth phase.
The production parts share this proved fit. This fixture preserves the earlier
radial-ball root and tests the teeth separately from the compiled restraint.
"""

from machinome.motion.joints import Prismatic
from simulation.reverser_inputs import ReversingOnes
from simulation.reverser_mapped import MappedReverserTrial
from simulation.reverser_operating_parts import (
    ProtectedOnesPinion as TrialOnesPinion,
    ProtectedOnesInput as TrialOnesInput,
    ReverserContactOnes as TrialRetainedOnes,
    ReverserContactTurns as TrialTurns,
    ReverserContactTransmission as TrialTransmission,
)
from simulation.running import RadialBallOperatingCurta


class TrialOnes(ReversingOnes):
    p_10218_1 = TrialOnesInput(travel=Prismatic(axis=(0, 0, -1)))


class TrialSeat(MappedReverserTrial):
    ones = TrialOnes()


class TrialOperatingCurta(RadialBallOperatingCurta):
    transmission = TrialTransmission()
