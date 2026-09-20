"""Measure outside-profile relief at a full-bank failure, not just one gear."""

import json
import logging
from simulation.reverser_seat_trial import ReverserSeatTrial
from simulation.reverser_assembly import counter_passage
from simulation.fit import FittedCounterPinion
from simulation.tools.interference import world_solids


def main():
    logging.disable(logging.INFO)
    bench = ReverserSeatTrial()
    bench.set_state(knob_height=3.9075, gear_height=4, crank_angle=123,
                    subtract=1, reversed_counter=0)
    bench.assemble()
    path = 'Curta.drum.main_axle_step_drum_top_1'
    drum = world_solids(bench, selected={path})[path]
    angle = counter_passage(2)(None, None)(123, 1, 0)
    for relief in (.36, .37, .38, .39, .4, .42):
        gear = FittedCounterPinion(flank_relief=relief).shape()
        gear = gear.rotate((0, 0, 0), (0, 0, 1), angle).translate((0, 40.5, -40.85))
        common = gear.intersect(drum)
        assert common.isValid()
        print(json.dumps({'channel': 'hundreds', 'crank': 123, 'subtract': 1,
                          'gear_height': 4, 'relief': relief,
                          'overlap_mm3': common.Volume()}), flush=True)


if __name__ == '__main__':
    main()
