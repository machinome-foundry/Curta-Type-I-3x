"""Full-root frame trial and visual inspection; neither is the default model."""

from simulation.carry_bank_frame import FittedUpperFrame, FirstPairUpperFrame
from simulation.mechanism import Frame
from simulation.running import OperatingCurta
from simulation.views import CarryFrameInspection


class FittedCarryFrame(Frame):
    upper_frame = FittedUpperFrame()


class FirstPairCarryFrame(Frame):
    upper_frame = FirstPairUpperFrame()


class FirstPairOperatingReference(OperatingCurta):
    """The prior frame geometry with otherwise current operating mechanisms."""
    frame = FirstPairCarryFrame()


class CarryBankOperatingTrial(OperatingCurta):
    frame = FittedCarryFrame()


class CarryBankInspection(CarryFrameInspection):
    """Only the enclosing shell is hidden, as in the prior first-pair view."""
    frame = FittedCarryFrame()
