"""Contract wrappers for the adopted seat and its unmodified negative control."""

from simulation.standard.parts import ReverseNosePlate
from simulation.pawl import PawlBearingPlate
from simulation.mechanism import Frame
from simulation.running import OperatingCurta


class UnseatedReverseNoseBearing(PawlBearingPlate):
    reverse_nose_plate = ReverseNosePlate()


class UnseatedReverseNoseFrame(Frame):
    lower_bearing_plate = UnseatedReverseNoseBearing()


class ReverseNoseSeatTrial(OperatingCurta):
    """Historical trial name retained for reproducing the acceptance instrument."""


class UnseatedReverseNoseReference(OperatingCurta):
    frame = UnseatedReverseNoseFrame()
