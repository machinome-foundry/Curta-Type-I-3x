"""Source-backed carriage pin/frame contact bench; no operating limits inferred.

The fitted bench uses the operating carrier and its documented pin seating.
The source bench retains the original insertion for reproduction.
Independent pose inputs allow measuring contact before declaring a restraint.
"""

from machinome.node import AssemblyNode, StlNode
from machinome.motion.joints import Revolute, Prismatic
from machinome.simulation import Driver
from simulation.mechanism import CarriageStructure
from simulation.running_parts import RetainedCarriageStructure, RetainedAxleCarrier
from simulation.standard.parts import MainBody
from simulation.print_parts import PRINTS
from simulation.colors import ALUMINUM


class SourceCarriageStopBench(AssemblyNode):
    angle = Driver(default=0, unit='deg')
    elevation = Driver(default=0, unit='mm')
    frame = MainBody()
    carrier = CarriageStructure(turn=Revolute(axis=(0, 0, 1)),
                               lift=Prismatic(axis=(0, 0, 1)))
    angle.drives(carrier.turn)
    elevation.drives(carrier.lift)
    elevation.drives(carrier.upper_carriage_body_1.press, ratio=0)


class CarriageStopBench(SourceCarriageStopBench):
    carrier = RetainedCarriageStructure(turn=Revolute(axis=(0, 0, 1)),
                                       lift=Prismatic(axis=(0, 0, 1)))


class PinCarrierView(RetainedAxleCarrier):
    """Inspection-only visibility; the contact benches keep every part."""

    def render(self):
        super().render()
        for name in ('counter_body', 'counter_body_pin_1', 'counter_body_pin_2',
                     'clearing_pin', 'clearing_pin_spring', 'clearing_stop_pin_sleeve'):
            getattr(self, name).omit()
        for index in range(1, 18):
            getattr(self, f'digits_axle_{index}').omit()


class PinStructureView(RetainedCarriageStructure):
    upper_carriage_body_1 = PinCarrierView()

    def render(self):
        super().render()
        self.crank_collar.omit()
        self.crank_collar_nut.omit()
        self.crank_collar_washer.omit()


class CarriageStopView(CarriageStopBench):
    carrier = PinStructureView(turn=Revolute(axis=(0, 0, 1)),
                               lift=Prismatic(axis=(0, 0, 1)))


class PrintedMainBody(StlNode):
    """Unmodified author-supplied print, for comparison with the STEP body."""

    stl_source = str(PRINTS / '9 - Tens Bell & Main Body/main body.stl')
    color = ALUMINUM


class PrintedCarriageStopBench(CarriageStopBench):
    frame = PrintedMainBody()


class PrintedSourceCarriageStopBench(SourceCarriageStopBench):
    frame = PrintedMainBody()
