"""Finite, geometry-checked pawl return for incremental operation.

The pose bench's instantaneous spring return is a jump, which a running
law correctly subtracts. Here that return traverses the already-probed
0.005-degree release interval. This prescribes travel, not spring dynamics.
"""

from machinome.math import clamp01, floor, piecewise
from simulation.arithmetic import modulo
from simulation.pawl import AntiReversal, PawlBench, RAMP, TOOTH_PITCH, RELEASE, CLOSING_RELEASE

RETURN_SPAN = .005


def continuous_pawl_angle(source, target):
    def angle(turn):
        crank = modulo(-turn, 360)
        closing = (TOOTH_PITCH - 3) * clamp01(floor(crank / CLOSING_RELEASE))
        position = modulo(crank + closing - RELEASE, TOOTH_PITCH)
        ramp = piecewise(position, RAMP)
        # The one shortened tooth reaches the ramp at 3 degrees, not at a
        # full regular pitch. Its following return starts at that height.
        peak = (RAMP[-1][1] + (piecewise(3, RAMP) - RAMP[-1][1])
                * (crank >= CLOSING_RELEASE) * (crank < CLOSING_RELEASE + TOOTH_PITCH))
        return ramp + (peak - ramp) * clamp01(1 - position / RETURN_SPAN)
    return angle


class RunningAntiReversal(AntiReversal):
    pawl_drive = AntiReversal.turn.drives(
        AntiReversal.reverse_rotation_prevention_pawl.turn, law=continuous_pawl_angle)


class ContinuousPawlBench(PawlBench):
    pawl = RunningAntiReversal()
