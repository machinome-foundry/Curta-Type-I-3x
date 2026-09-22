"""Unadopted collar fit on the operating root, with all original motion laws.

The whole-neighbour and moving-seat contracts remain red. This trial must not
replace the default root until those contacts are resolved without exclusions.
"""

from simulation.running import OperatingCurta, RunningCarriage
from simulation.running_parts import RetainedCarriage, RetainedCarriageStructure
from simulation.collar_seat_trial import TrialShoulderCollar


class TrialCollarCarrier(RetainedCarriageStructure):
    crank_collar = TrialShoulderCollar()

    def render(self):
        super().render()
        # Local +/-Y bores face the unchanged, recentered +/-X carrier pins.
        self.crank_collar.rotate(54.282220532, (0, 0, 1))
        # Interior of the measured clear thread-phase interval, at source Z.
        self.crank_collar_nut.rotate(94.282220532, (0, 0, 1))


class TrialCollarRegisters(RetainedCarriage):
    carrier = TrialCollarCarrier()


class TrialCollarCarriage(RunningCarriage):
    registers = TrialCollarRegisters()


class OperatingCollarBench(OperatingCurta):
    carriage = TrialCollarCarriage()
