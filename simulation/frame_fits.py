"""Fixed, local carry passages in the source upper frame; no moving-part fit.

Only stations one and two are selected. The first station is the measurement
frame; station two is its source rotation of -20 degrees about world Z.
"""

from functools import lru_cache
import cadquery as cq
from machinome.parameters import Length
from simulation.standard.parts import MainBody, TensSliderForResults
from simulation.carry_fits import in_first_result_station


def box(low, high):
    return cq.Solid.makeBox(*(b-a for a, b in zip(low, high)), cq.Vector(*low))


@lru_cache(maxsize=1)
def raised_shoulder():
    """The original slider's measured shoulder face, not a fitted-frame copy."""
    slider = in_first_result_station(TensSliderForResults().shape())
    faces = [face for face in slider.Faces() if face.geomType() == 'PLANE'
             and abs(face.Center().z + 21.6) < 1e-6
             and abs(face.normalAt().z) > .999999]
    if len(faces) != 1:
        raise ValueError('Source raised shoulder no longer matches its measured datum')
    return faces[0]


def first_station_passages(gap):
    # Only the shoulder beside the frame's X=52.8 registration edge is filed.
    # The curved joins are an actual planar offset of the source outline.
    wires = raised_shoulder().outerWire().offset2D(gap)
    if len(wires) != 1:
        raise ValueError('Raised-shoulder offset must remain one outline')
    shoulder = cq.Solid.extrudeLinear(wires[0].translate((0, 0, gap)), [],
                                     (0, 0, -.6-2*gap))
    shoulder = shoulder.intersect(box((47, -10, -23), (52.8+gap, -6, -21)))
    yield 'raised-shoulder', shoulder
    yield 'lowered-edge', box((52.725-gap, -7.89-gap, -16.8-gap),
                              (52.8+gap, -6.42+gap, -15.9+gap))
    # Separate lower-leg windows: never remove the bridge between the legs.
    # Outward-rounded native contact limits; full-path enclosure is checked
    # independently, not inferred from these four selected-pose measurements.
    for name, xmin, xmax in (('spring-left', 53.501, 54.197),
                             ('spring-right', 60.408, 61.104)):
        yield name, box((xmin-gap, -11.322-gap, -19.466-gap),
                        (xmax+gap, -11.01+gap, -15.9+gap))


def passages(gap, stations=(0, -20), omitted=()):
    for angle in stations:
        for family, tool in first_station_passages(gap):
            if family not in omitted:
                yield angle, family, tool.rotate((0, 0, 0), (0, 0, 1), angle)


class CarryPassageFrame(MainBody):
    # Only this measured dimensional trial range fits inside the independently
    # protected .08 mm envelope. This is not a manufacturing tolerance.
    running_gap = Length(.05, min=.04, max=.06)
    stations = (0, -20)

    def adjust(self, shape):
        for _, _, tool in passages(self.running_gap, self.stations):
            shape = shape.cut(tool)
        return shape
