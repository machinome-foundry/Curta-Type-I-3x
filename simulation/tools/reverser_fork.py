"""Locate the sixth counter input/fork contact before choosing any fit."""

import json
import logging
from simulation.reverser_seat_trial import ReverserSeatTrial
from simulation.standard.parts import ReversingActuator
from simulation.reverser_fits import FORK_ORIGIN
from simulation.tools.interference import world_solids


def bounds(shape):
    if not shape.Vertices():
        return None
    box = shape.BoundingBox()
    return [box.xmin, box.ymin, box.zmin, box.xmax, box.ymax, box.zmax]


def main():
    logging.disable(logging.INFO)
    bench = ReverserSeatTrial()
    bench.set_state(knob_height=-4.9425, gear_height=-4.85,
                    crank_angle=101.25, subtract=0, reversed_counter=1)
    bench.assemble()
    bench.build_stls()
    paths = {'Curta.lever.reversing_lever_knob_1.reversing_actuator',
             'Curta.digit_6.p_10230_410008_1_419237'}
    shapes = world_solids(bench, selected=paths)
    fork = shapes['Curta.lever.reversing_lever_knob_1.reversing_actuator']
    gear = shapes['Curta.digit_6.p_10230_410008_1_419237']
    # Reproduce the original interference after adopting the candidate too.
    # This is the source actuator's recorded placement, plus the trial height;
    # its unmodified solid is independent of the bounded fit's two cutters.
    original = ReversingActuator().shape().rotate((0, 0, 0), (0, 0, 1), -20)
    original = original.translate((*FORK_ORIGIN, -44.0075-4.9425))
    for label, placed in (('source', original), ('fitted', fork)):
        common = placed.intersect(gear)
        assert common.isValid()
        print(json.dumps({'variant': label, 'contact_mm3': common.Volume(),
                          'contact_bounds': bounds(common), 'fork_bounds': bounds(placed),
                          'gear_bounds': bounds(gear)}), flush=True)
    for label, shape in (('source fork', original), ('fitted fork', fork), ('gear', gear)):
        circles = set()
        for edge in shape.Edges():
            if edge.geomType() == 'CIRCLE':
                center = edge.arcCenter()
                circles.add(tuple(round(v, 7) for v in
                                  (center.x, center.y, center.z, edge.radius())))
        print(json.dumps({'part': label, 'circle_centres_and_radii': sorted(circles)}), flush=True)
    for crank in range(0, 361, 15):
        bench.set_state(crank_angle=crank)
        shapes = world_solids(bench, selected=paths)
        fork = shapes['Curta.lever.reversing_lever_knob_1.reversing_actuator']
        gear = shapes['Curta.digit_6.p_10230_410008_1_419237']
        for label, placed in (('source', original), ('fitted', fork)):
            common = placed.intersect(gear)
            assert common.isValid()
            if common.Volume() > 0:
                print(json.dumps({'variant': label, 'crank': crank,
                                  'contact_mm3': common.Volume(),
                                  'contact_bounds': bounds(common)}), flush=True)


if __name__ == '__main__':
    main()
