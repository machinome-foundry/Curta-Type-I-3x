"""Independent collar/pin seat at the operating carriage's measured datums.

The source collar has two R1.8 blind bores at local (0, +/-21), Z39..42.
The recentered carrier's unchanged pins stand at world (+/-21, 0), ending
at Z49.5. No source material or insertion depth is changed by this bench.
"""

from machinome.node import AssemblyNode
from machinome.parameters import Angle
from simulation.print_parts import CrankCollar
from simulation.standard.parts import CounterBodyPin, CrankCollarNut
from simulation.collar_seat_trial import TrialShoulderCollar
from simulation.operating_collar_parts import SeatedCollar


class CollarPinSeat(AssemblyNode):
    # Local +/-Y bore centres must face the carrier's world +/-X pins.
    collar_angle = Angle(-90)
    # At the retained Z12.3 seat, a 5-degree phase survey clears the thread
    # over approximately 16..66 degrees. Choose its interior and prove
    # axial free play and capture; thread material and height are unchanged.
    nut_angle = Angle(40)
    collar = CrankCollar()
    pin_left = CounterBodyPin()
    pin_right = CounterBodyPin()
    nut = CrankCollarNut()

    def render(self):
        self.collar.rotate(self.collar_angle, (0, 0, 1)).translate((0, 0, 7.8))
        self.nut.rotate(self.nut_angle, (0, 0, 1)).translate((0, 0, 12.3))
        self.pin_left.rotate(180, (0, 1, 0)).translate((-21, 0, 49.5))
        self.pin_right.rotate(180, (0, 1, 0)).translate((21, 0, 49.5))


class SourceCollarPinSeat(CollarPinSeat):
    """The source assembly's clocking, retained as the colliding witness."""
    collar_angle = Angle(-144.282220532)
    nut_angle = Angle(-54.282220532)


class FittedCollarPinSeat(CollarPinSeat):
    """Combine the measured clocking with the independently proven shoulder fit."""
    collar = TrialShoulderCollar()


class SeatedCollarPinSeat(CollarPinSeat):
    """Same measured datums, with the separately bounded lower-seat facing."""
    collar = SeatedCollar()
