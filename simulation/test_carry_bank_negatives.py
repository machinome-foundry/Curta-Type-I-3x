"""The carry-frame acceptance checks must reject omitted or misleading fits."""

import logging
import unittest

import cadquery as cq

from simulation.carry_bank_fits import CarryBankPassageFrame, additional_passages
from simulation.carry_bank_frame import FittedCarryBankFrameBench
from simulation.carry_bank_regions import forbidden_removal
from simulation.frame_fits import CarryPassageFrame
from simulation.standard.parts import MainBody
from simulation.tools.carry_bank_dense import require_frame, require_stroke
from simulation.tools.interference import world_solids


class CarryBankNegativeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = FittedCarryBankFrameBench()
        cls.model.set_state(drop_mm=0)
        cls.model.assemble()
        cls.model.build_stls()
        cls.original = MainBody().shape()
        cls.fitted = cls.model.frame.main_body.shape()

    def native_part(self, counter, spring, drop):
        self.model.set_state(drop_mm=drop)
        path = ('turns_carries.turns_tens_lever_assembly_1' if counter else
                'result_carries.results_tens_lever_assembly_3')
        suffix = 'carry_lever_spring.wire' if spring else (
            'tens_slider_for_turns_counter' if counter else 'tens_slider_for_results')
        key = 'Curta.'+path+'.'+suffix
        return world_solids(self.model, include_flexible=True, selected={key})[key]

    def test_each_distinct_omitted_passage_restores_a_real_obstruction(self):
        # Restore only native material removed by the chosen passage. All
        # other candidate relief remains. This is an omitted-cut negative,
        # not a collision against the cutter's empty-space bounding box.
        tools = {(angle, family): tool for _, angle, family, tool in additional_passages(.05)}
        for counter, angle in ((False, -40), (True, 130)):
            for family, drop, spring in (
                    ('raised-shoulder', 0, False),
                    ('lowered-shoulder' if counter else 'lowered-edge', 4.2, False),
                    ('spring-left', 2.562, True), ('spring-right', 2.562, True)):
                restored = self.original.intersect(tools[angle, family])
                part = self.native_part(counter, spring, drop)
                common = part.intersect(restored)
                with self.subTest(counter=counter, family=family):
                    self.assertTrue(restored.isValid() and common.isValid())
                    self.assertGreater(restored.Volume(), 0)
                    self.assertGreater(common.Volume(), 0)

    def test_misplaced_additional_passages_do_not_clear_the_slider(self):
        wrong = CarryPassageFrame().shape()
        for _, _, _, tool in additional_passages(.05, rotation_error=1):
            wrong = wrong.cut(tool)
        require_frame(wrong)
        for counter in (False, True):
            common = self.native_part(counter, False, 0).intersect(wrong)
            with self.subTest(counter=counter):
                self.assertTrue(common.isValid())
                self.assertGreater(common.Volume(), 0)

    def test_excessive_relief_fails_independent_material_bounds(self):
        # The unmodified central frame is deliberately drilled beyond every
        # named carry passage; a clearance-only test would miss this damage.
        tool = cq.Solid.makeCylinder(25, 100, cq.Vector(0, 0, -50))
        wrong = self.fitted.cut(tool)
        lost = forbidden_removal(self.original, wrong)
        self.assertTrue(lost.isValid())
        self.assertGreater(lost.Volume(), 0)

    def test_hidden_frame_is_rejected_before_clearance(self):
        empty = cq.Compound.makeCompound([])
        with self.assertRaisesRegex(ValueError, 'complete positive-volume frame'):
            require_frame(empty)

    def test_shortened_actual_stroke_cannot_pass_the_four_point_two_mm_guard(self):
        self.model.set_state(drop_mm=0)
        part = self.model.result_carries.results_tens_lever_assembly_3.tens_slider_for_results
        raised = part.mesh.vertices.copy()
        self.model.set_state(drop_mm=3.9)
        with self.assertRaises(AssertionError):
            require_stroke(raised, part.mesh.vertices, 4.2)
        self.model.set_state(drop_mm=4.2)
        require_stroke(raised, part.mesh.vertices, 4.2)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    unittest.main()
