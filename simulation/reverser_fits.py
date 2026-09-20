"""Measured local fork relief; source prints and other fork seats stay intact."""

from math import cos, sin, radians
import cadquery as cq
from machinome.parameters import Length
from simulation.standard.parts import ReversingActuator

# Source sixth input axis and source actuator placement, in the shared frame.
SIXTH_AXIS = (35.074028853, 20.25)
FORK_ORIGIN = (-1.88117949, .647742044)
_angle = radians(20)  # inverse of the source actuator's -20 degree placement
_x, _y = (SIXTH_AXIS[i] - FORK_ORIGIN[i] for i in range(2))
SIXTH_LOCAL = (_x*cos(_angle) - _y*sin(_angle), _x*sin(_angle) + _y*cos(_angle))


class FittedReversingActuator(ReversingActuator):
    """Open only the sixth sleeve seat for its fitted R3.85 plus .05 mm play.

    The source R5 seat is 1.333 mm eccentric to this input axis. The bounded
    cutter removes its contacting edge, not the tooth slot's axial faces or
    the knob mounting shoulder. Shared by the trial and operating candidate.
    """
    sleeve_radius = Length(3.85)
    radial_gap = Length(.05)
    tooth_radius = Length(6.28)
    # Preserve the small bore clearance when curved faces become STL chords.
    linear_deflection = .01
    angular_deflection = .1

    def adjust(self, shape):
        cutter = cq.Solid.makeCylinder(self.sleeve_radius + self.radial_gap,
                                        4.5, cq.Vector(*SIXTH_LOCAL, -2.25))
        # A rotating fitted tooth reaches R6.22621; the source slot's far
        # wall catches it at crank 195/240 degrees. Extend only that slot,
        # retaining both original axial faces and their .185 mm total play.
        slot = cq.Solid.makeCylinder(self.tooth_radius, 1.685,
                                     cq.Vector(*SIXTH_LOCAL, -.8425))
        return shape.cut(cutter).cut(slot).clean()
