"""Audit the unchanged reversing shaft's fastening seats before repositioning."""

import json
import logging
from math import hypot
from OCP.BRepAdaptor import BRepAdaptor_Surface
from simulation.reverser_assembly import ReverserAssemblyBench
from simulation.standard.layers import FrameFasteners
from simulation.tools.interference import world_solids
from simulation.tools.reverser_knob_seat import bounds


class ShaftSeatBench(ReverserAssemblyBench):
    fasteners = FrameFasteners()


def probe():
    logging.disable(logging.INFO)
    bench = ShaftSeatBench()
    bench.set_state(knob_height=0, gear_height=0, crank_angle=0,
                    subtract=0, reversed_counter=0)
    bench.assemble()
    selected = {'Curta.lever.reversing_shaft', 'Curta.upper_frame',
                'Curta.lower_frame', 'Curta.fasteners.m4_nut_2'}
    shapes = world_solids(bench, selected=selected)
    for path, shape in shapes.items():
        print(json.dumps({'part': path, 'bounds': bounds(shape),
                          'volume': shape.Volume(), 'valid': shape.isValid()}), flush=True)
        for face in shape.Faces():
            if path.endswith('reversing_shaft') and face.geomType() == 'PLANE':
                print(json.dumps({'shaft_plane': face.Center().toTuple(),
                                  'normal': face.normalAt().toTuple(),
                                  'area': face.Area(), 'bounds': bounds(face)}), flush=True)
            if face.geomType() == 'CYLINDER':
                cylinder = BRepAdaptor_Surface(face.wrapped).Cylinder()
                x, y, z = cylinder.Location().Coord()
                if hypot(x - 17.613968679, y - 54.210221429) < .01:
                    print(json.dumps({'coaxial_cylinder_part': path,
                                      'radius': cylinder.Radius(),
                                      'axis': cylinder.Axis().Direction().Coord(),
                                      'bounds': bounds(face)}), flush=True)
    shaft = shapes.pop('Curta.lever.reversing_shaft')
    for rise in (-.6, -.1, 0, .05, .25, .5, .6, 1):
        for name, shape in shapes.items():
            common = shaft.translate((0, 0, rise)).intersect(shape)
            print(json.dumps({'shaft_rise': rise, 'neighbour': name,
                              'valid': common.isValid(), 'overlap': common.Volume(),
                              'bounds': bounds(common)}), flush=True)


if __name__ == '__main__':
    probe()
