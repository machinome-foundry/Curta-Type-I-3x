"""Unconstrained source-backed bench for measuring the clearing/carriage stop.

The cover follows its existing measured cam and the actual operating carrier
owns the pin. Independent pose inputs deliberately permit impossible seating;
this bench is evidence for a restraint, not a declaration that it exists.
"""

from machinome.node import AssemblyNode
from machinome.motion.joints import Revolute, Prismatic
from machinome.simulation import Driver
from simulation.running_parts import RetainedCarriageStructure, RetainedAxleCarrier, RunningClearingAssembly
from simulation.clearing_stop_motion import following
from simulation.standard.parts import MainBody, ClearingPin, CounterBody


class SourceClearingPinCarrier(RetainedAxleCarrier):
    clearing_pin = ClearingPin(slide=Prismatic(axis=(0, 0, -1)))
    counter_body = CounterBody()


class SourceClearingSeatStructure(RetainedCarriageStructure):
    upper_carriage_body_1 = SourceClearingPinCarrier()


class SourceClearingSeatCarriage(AssemblyNode):
    carrier = SourceClearingSeatStructure()
    ring = RunningClearingAssembly(turn=Revolute(axis=(0, 0, 1)))
    ring.turn.drives(carrier.upper_carriage_body_1.clearing_pin.slide, law=following)


class SourceClearingSeatBench(AssemblyNode):
    elevation = Driver(default=0, unit='mm')
    shift = Driver(default=0, unit='deg')
    sweep = Driver(default=0, unit='deg')
    frame = MainBody()
    carriage = SourceClearingSeatCarriage(lift=Prismatic(axis=(0, 0, 1)),
                                          turn=Revolute(axis=(0, 0, 1)))
    elevation.drives(carriage.lift)
    shift.drives(carriage.turn)
    sweep.drives(carriage.ring.turn, ratio=-1)


class ClearingSeatCarriage(SourceClearingSeatCarriage):
    carrier = RetainedCarriageStructure()


class ClearingSeatBench(SourceClearingSeatBench):
    carriage = ClearingSeatCarriage(lift=Prismatic(axis=(0, 0, 1)),
                                    turn=Revolute(axis=(0, 0, 1)))


class ClearingPinInspection(RetainedAxleCarrier):
    """Visibility only; the tests retain the omitted neighbours."""

    def render(self):
        super().render()
        for name in ('counter_body', 'counter_body_pin_1', 'counter_body_pin_2',
                     'counter_body_stop_pin', 'clearing_stop_pin_sleeve'):
            getattr(self, name).omit()
        for index in range(1, 18):
            getattr(self, f'digits_axle_{index}').omit()


class ClearingStructureInspection(RetainedCarriageStructure):
    upper_carriage_body_1 = ClearingPinInspection()

    def render(self):
        super().render()
        self.crank_collar.omit()
        self.crank_collar_nut.omit()
        self.crank_collar_washer.omit()


class ClearingCarriageInspection(ClearingSeatCarriage):
    carrier = ClearingStructureInspection()

    def render(self):
        self.ring.omit()


class ClearingSeatView(ClearingSeatBench):
    elevation = Driver(default=4.810085, unit='mm')
    sweep = Driver(default=90, unit='deg')
    carriage = ClearingCarriageInspection(lift=Prismatic(axis=(0, 0, 1)),
                                          turn=Revolute(axis=(0, 0, 1)))
