"""Measured stationary passages for the remaining thirteen carry stations.

The first-pair adapter remains intact. Counter shoulders come from the
counter's original native body, not the result slider or acceptance regions.
Moving parts, guide placements and the two spring-support bridges are intact.
"""

from functools import lru_cache

import cadquery as cq

from simulation.carry_fits import in_first_result_station
from simulation.frame_fits import CarryPassageFrame, box, passages
from simulation.standard.parts import TensSliderForTurnsCounter


@lru_cache(maxsize=2)
def counter_shoulder(lowered=False):
    source = in_first_result_station(TensSliderForTurnsCounter().shape(), counter=True)
    # That shared source-placement helper lowers the fork by 14.7 mm for
    # comparing its sleeve fit. Restore the actual frame-contact height.
    source = source.translate((0, 0, 14.7))
    z = -11.7 if lowered else -21.6
    faces = [face for face in source.Faces() if face.geomType() == 'PLANE'
             and abs(face.Center().z-z) < 1e-6
             and abs(face.normalAt().z) > .999999]
    if len(faces) != 1:
        raise ValueError('Counter source shoulder no longer matches its measured datum')
    return faces[0]


def counter_station_passages(gap):
    for lowered in (False, True):
        wires = counter_shoulder(lowered).outerWire().offset2D(gap)
        if len(wires) != 1:
            raise ValueError('Counter shoulder offset must remain one outline')
        offset = -4.2-gap if lowered else gap
        height = .6+2*gap if lowered else -.6-2*gap
        tool = cq.Solid.extrudeLinear(wires[0].translate((0, 0, offset)), [],
                                     (0, 0, height))
        tool = tool.intersect(box((47, -12, -23), (52.8+gap, -6, -15)))
        yield 'lowered-shoulder' if lowered else 'raised-shoulder', tool
    # Full counter detent extrema, outward-rounded to .001 mm. Its wider
    # spread differs from the result spring; each leg has its own window.
    for name, xmin, xmax in (('spring-left', 53.491, 54.203),
                             ('spring-right', 60.401, 61.114)):
        yield name, box((xmin-gap, -11.333-gap, -19.270-gap),
                        (xmax+gap, -11.01+gap, -15.9+gap))


def additional_passages(gap, *, omitted=(), rotation_error=0):
    for angle, family, tool in passages(gap, tuple(-20*i for i in range(2, 10))):
        if (angle, family) not in omitted:
            yield 'result', angle, family, tool.rotate((0, 0, 0), (0, 0, 1), rotation_error)
    for angle in (130, 110, 90, 70, 50):
        for family, tool in counter_station_passages(gap):
            if (angle, family) not in omitted:
                yield 'counter', angle, family, tool.rotate((0, 0, 0), (0, 0, 1),
                                                          angle+rotation_error)


class CarryBankPassageFrame(CarryPassageFrame):
    def adjust(self, shape):
        shape = super().adjust(shape)
        for _, _, _, tool in additional_passages(self.running_gap):
            shape = shape.cut(tool)
        return shape
