"""Test the housing window as a retaining stop, not the pocket centre alone."""

import json
import logging
from simulation.reverser_assembly import ReverserAssemblyBench
from simulation.running_parts import RunningEnclosure
from simulation.tools.interference import world_solids
from simulation.tools.reverser_knob_seat import bounds
from simulation.cover_fits import mesh_solid


class EnclosedReverserBench(ReverserAssemblyBench):
    enclosure = RunningEnclosure()


def probe():
    logging.disable(logging.INFO)
    bench = EnclosedReverserBench()
    bench.set_state(knob_height=0, gear_height=0, crank_angle=0,
                    subtract=0, reversed_counter=0)
    bench.assemble()
    bench.build_stls()
    key = 'Curta.lever.reversing_lever_knob_1.reversing_lever_knob'
    selected = {key, 'Curta.enclosure.lower_housing_1.bottom_housing',
                'Curta.enclosure.upper_outer_sleeve'}
    shapes = world_solids(bench, selected=selected)
    knob = shapes.pop(key)
    meshes = {
        'Curta.enclosure.lower_housing_1.bottom_housing': mesh_solid(
            bench.enclosure.lower_housing_1.bottom_housing.mesh),
        'Curta.enclosure.upper_outer_sleeve': mesh_solid(bench.enclosure.upper_outer_sleeve.mesh)}
    mesh_knob = mesh_solid(bench.lever.reversing_lever_knob_1.reversing_lever_knob.mesh)
    for height in (-7.6427, -6.8425, -6, -5.5, -5, -4.5, -4, 0, 3, 3.9075, 4.5):
        for name, shape in shapes.items():
            common = knob.translate((0, 0, height)).intersect(shape)
            faceted = mesh_knob.translate((0, 0, height)) ^ meshes[name]
            print(json.dumps({'knob_height': height, 'neighbour': name,
                              'native_valid': common.isValid(),
                              'native_overlap': common.Volume(), 'bounds': bounds(common),
                              'faceted_status': str(faceted.status()),
                              'faceted_overlap': faceted.volume()}), flush=True)


if __name__ == '__main__':
    probe()
