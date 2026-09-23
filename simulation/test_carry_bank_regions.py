"""Test the maximum allowed removal before building any production cutter."""

import json
import logging
import unittest

from simulation.carry_bank_frame import CarryBankFrameBench, stations
from simulation.carry_bank_regions import (maximally_relieved, seat_edge_regions,
                                           RESULT_ANGLES, COUNTER_ANGLES)
from simulation.standard.parts import MainBody
from simulation.test_frame_fits import registration_lands
from simulation.tools.interference import world_solids


class CarryBankRegionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = MainBody().shape()
        cls.maximum = maximally_relieved(cls.original)
        cls.bench = CarryBankFrameBench()
        cls.bench.set_state(drop_mm=0)
        cls.bench.assemble()

    def test_maximum_allowed_removal_keeps_one_solid_and_adds_nothing(self):
        self.assertTrue(self.maximum.isValid())
        self.assertEqual(len(self.maximum.Solids()), 1)
        self.assertEqual(self.maximum.cut(self.original).Volume(), 0)

    def test_all_guide_lands_are_preserved_outside_measured_edges(self):
        paths = {'Curta.'+path+'.tens_slide_bearing' for path, _, _ in stations(self.bench)}
        guides = world_solids(self.bench, selected=paths)
        for path, node, slider in stations(self.bench):
            counter = path.startswith('turns_carries')
            index = int(path.rsplit('_', 1)[-1])-1
            angle = (COUNTER_ANGLES if counter else RESULT_ANGLES)[index]
            lands = list(registration_lands(self.original, guides['Curta.'+path+'.tens_slide_bearing']))
            self.assertTrue(lands)
            total, retained = 0, 0
            for number, land in enumerate(lands):
                total += land.Area()
                retained += land.intersect(self.maximum).Area()
                protected = land
                for edge in seat_edge_regions(angle, counter=counter):
                    protected = protected.cut(edge)
                lost = protected.cut(self.maximum)
                with self.subTest(path=path, land=number):
                    self.assertTrue(lost.isValid())
                    self.assertEqual(lost.Area(), 0)
            print(json.dumps(dict(station=path, original_land_mm2=total,
                                  retained_land_mm2=retained,
                                  retained_fraction=retained/total)), flush=True)
            with self.subTest(path=path, criterion='retained-land'):
                self.assertGreaterEqual(retained, .98*total)

    def test_small_cylindrical_bores_keep_their_source_surfaces(self):
        checked = 0
        for index, face in enumerate(self.original.Faces()):
            if face.geomType() != 'CYLINDER':
                continue
            radii = [edge.radius() for edge in face.Edges() if edge.geomType() == 'CIRCLE']
            if not radii or max(radii) >= 20:
                continue
            checked += 1
            lost = face.cut(self.maximum)
            with self.subTest(face=index, radii=radii):
                self.assertTrue(lost.isValid())
                self.assertEqual(lost.Area(), 0)
        self.assertGreater(checked, 15)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    unittest.main()
