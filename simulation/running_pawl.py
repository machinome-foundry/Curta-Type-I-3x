"""Finite, geometry-checked pawl return for incremental operation.

The pose bench's instantaneous spring return is a jump, which a running
law correctly subtracts. Here that return traverses the already-probed
0.005-degree release interval. This prescribes travel, not spring dynamics.
"""

from machinome.math import clamp, clamp01, floor, piecewise, max
from machinome.motion.joints import Bound, Revolute
from machinome.motion.ports import Time
from simulation.standard.parts import ZeroPositioningDisc
from simulation.arithmetic import modulo
from simulation.pawl import AntiReversal, PawlBench, RAMP, TOOTH_PITCH, RELEASE, CLOSING_RELEASE

RETURN_SPAN = .005

# Native contact brackets place the seated tip .20005--.20008 degrees
# before release. The rounded free-side stop is therefore release - .2.
BACKLASH = .2
RELEASES = tuple(RELEASE + i * TOOTH_PITCH for i in range(98)) + tuple(
    CLOSING_RELEASE + i * TOOTH_PITCH for i in range(19))


def reverse_stop(turn, pawl):
    """Upper bound in the physical crank's clockwise-negative coordinate.

    Compare and return the same represented stop, including the shortened
    closing tooth, so landing on a stop cannot lose it on the next tick.
    """
    forward = -turn
    base = 360 * floor(forward / 360)
    stop = base - 360 + RELEASES[-1] - BACKLASH
    # Two regular trains meet at the shortened interval. Check the estimated
    # neighbour as well as the estimate: division at an exact tooth can round
    # to the preceding index. Selection still compares the represented angles.
    for origin, last in ((RELEASE, 97), (CLOSING_RELEASE, 18)):
        index = floor((forward - base - origin + BACKLASH) / TOOTH_PITCH)
        for offset in (-1, 0, 1):
            release = origin + clamp(index + offset, 0, last) * TOOTH_PITCH
            candidate = base + (release - BACKLASH)
            captured = max(forward >= base + release,
                           (forward >= candidate) * (pawl <= RAMP[0][1]))
            stop = max(stop, candidate * captured + stop * (1 - captured))
    return -stop


def continuous_pawl_angle(source, target):
    def angle(turn):
        crank = modulo(-turn, 360)
        closing = (TOOTH_PITCH - 3) * clamp01(floor(crank / CLOSING_RELEASE))
        position = modulo(crank + closing - RELEASE, TOOTH_PITCH)
        ramp = piecewise(position, RAMP)
        # The one shortened tooth reaches the ramp at 3 degrees, not at a
        # full regular pitch. Its following return starts at that height.
        peak = (RAMP[-1][1] + (piecewise(3, RAMP) - RAMP[-1][1])
                * (crank >= CLOSING_RELEASE - 1) * (crank < CLOSING_RELEASE + 1))
        return ramp + (peak - ramp) * clamp01(1 - position / RETURN_SPAN)
    return angle


class RunningAntiReversal(AntiReversal):
    pawl_drive = AntiReversal.turn.drives(
        AntiReversal.reverse_rotation_prevention_pawl.turn, law=continuous_pawl_angle)


def retained_pawl_angle(sources, target):
    """The spring closes the pawl; reverse backlash cannot lift it again."""
    def angle(turn, own):
        crank = modulo(-turn, 360)
        closing = (TOOTH_PITCH - 3) * clamp01(floor(crank / CLOSING_RELEASE))
        position = modulo(crank + closing - RELEASE, TOOTH_PITCH)
        # The unused continuation below the seat makes seating a crossing,
        # rather than a tangential touch which an own-read switch cannot hold.
        # The gate stops the physical pawl at RAMP[0][1], never below it.
        ramp = piecewise(position, ((RETURN_SPAN, RAMP[0][1] - .001), *RAMP[1:]))
        # Select the shortened return's height while its return term is
        # identically zero. Switching it on the modulo cut itself creates
        # two nearly coincident floating-point surfaces and a spurious drop.
        peak = (RAMP[-1][1] + (piecewise(3, RAMP) - RAMP[-1][1])
                * (crank >= CLOSING_RELEASE - 1) * (crank < CLOSING_RELEASE + 1))
        raised = own > RAMP[0][1]
        shortened = (crank >= CLOSING_RELEASE - 3 + RETURN_SPAN) * (crank < CLOSING_RELEASE)
        free_end = TOOTH_PITCH - BACKLASH + (3 - TOOTH_PITCH) * shortened
        approaching = (position < free_end) * (ramp >= RAMP[0][1])
        return (ramp * max(raised, approaching)
                + (peak - ramp) * clamp01(1 - position / RETURN_SPAN) * raised)
    return angle


class RetainedAntiReversal(AntiReversal):
    pawl_drive = (AntiReversal.turn & AntiReversal.reverse_rotation_prevention_pawl.turn).drives(
        AntiReversal.reverse_rotation_prevention_pawl.turn, law=retained_pawl_angle)

    def simulate(self):
        if self.reverse_rotation_prevention_pawl.turn.value is None:
            self.reverse_rotation_prevention_pawl.turn = continuous_pawl_angle(None, None)(self.turn.value)


class ContinuousPawlBench(PawlBench):
    pawl = RunningAntiReversal()


class RetainedPawlBench(PawlBench):
    time = Time.running()
    pawl = RetainedAntiReversal()
    disc = ZeroPositioningDisc(turn=Revolute(axis=(0, 0, 1), range=(None,
        Bound(reverse_stop, reads=(pawl.reverse_rotation_prevention_pawl.turn,)))))
