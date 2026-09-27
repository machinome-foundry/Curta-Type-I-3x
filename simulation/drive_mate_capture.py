"""Existing installed-part contracts exercised on the production frame adapters."""

from simulation.drive_frames import FramedRetainedAntiReversal, FramedRunningReverser
from simulation.running_pawl import RetainedPawlBench
from simulation.reverser_following import ReverserFollowerTrial


class PawlMateCaptureBench(RetainedPawlBench):
    pawl = FramedRetainedAntiReversal()


class ReverserMateCaptureBench(ReverserFollowerTrial):
    lever = FramedRunningReverser(seat_rise=ReverserFollowerTrial.seat_rise)
