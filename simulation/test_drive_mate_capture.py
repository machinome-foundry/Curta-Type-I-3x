"""Unchanged geometric assertions, no new tolerances or omitted neighbours."""

from simulation.drive_mate_capture import PawlMateCaptureBench, ReverserMateCaptureBench
from simulation.test_running_pawl import RetainedPawlGeometryTest as _PawlContract
from simulation.test_reverser_following import ReverserFollowerTest as _ReverserContract


class PawlMateCaptureTest(_PawlContract):
    node = PawlMateCaptureBench


class ReverserMateCaptureTest(_ReverserContract):
    node = ReverserMateCaptureBench
