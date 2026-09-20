"""Inspection controls reproduce a finding, not a working reverser claim."""

import numpy as np
from machinome.simulation import Sim
from machinome.test import TestCase
from simulation.reverser_inspection import ReverserInspection
from simulation.reverser_assembly import ReverserAssemblyBench
from simulation.contracts import assert_connected_material


class ReverserInspectionTest(TestCase):
    node = ReverserInspection

    def setUp(self):
        self.node.set_state(lever_height=-6.8425, gear_offset=.185,
                            drum_angle=101.25, pinion_probe=0)

    def test_default_has_measured_axial_gap(self):
        gear = self.node.pinion.transmission_gear_0_5.mesh
        row = self.node.drum.nine_tooth_turns_step_drum_segment.mesh
        self.assertAlmostEqual(row.bounds[0, 2] - gear.bounds[1, 2], .3075, delta=.001)

    def test_lever_moves_fork_ball_and_pinion_but_not_shaft_or_drum(self):
        nodes = (self.node.fork, self.node.detent.p_5mm_ball,
                 self.node.pinion, self.node.detent.reversing_shaft, self.node.drum)
        before = [n.mesh.vertices.copy() for n in nodes]
        self.node.set_state(lever_height=-5.8425)
        for index, (n, vertices) in enumerate(zip(nodes, before)):
            expected = (0, 0, 1) if index < 3 else (0, 0, 0)
            np.testing.assert_allclose(n.mesh.vertices - vertices,
                                       np.tile(expected, (len(vertices), 1)), atol=1e-8)

    def test_offset_moves_only_pinion(self):
        fork = self.node.fork.mesh.vertices.copy()
        gear = self.node.pinion.mesh.vertices.copy()
        self.node.set_state(gear_offset=.685)
        np.testing.assert_allclose(self.node.fork.mesh.vertices, fork, atol=1e-8)
        np.testing.assert_allclose(self.node.pinion.mesh.vertices - gear,
                                   np.tile((0, 0, .5), (len(gear), 1)), atol=1e-8)

    def test_drum_does_not_fake_contact_driven_pinion_motion(self):
        pinion = self.node.pinion.mesh.vertices.copy()
        drum = self.node.drum.mesh.vertices.copy()
        self.node.set_state(drum_angle=110)
        np.testing.assert_allclose(self.node.pinion.mesh.vertices, pinion, atol=1e-8)
        self.assertGreater(np.max(np.abs(self.node.drum.mesh.vertices - drum)), 1)

    def test_presets_restore_measured_gap_and_experimental_alignment(self):
        sim = Sim(self.node, dt=.02)
        for button, gap in [('Lower centre', .4925), ('Best slot play', .3075),
                            ('Align teeth - unseated', -1.5), ('Best slot play', .3075)]:
            sim.trigger(button)
            sim.run(.2)
            gear = self.node.pinion.transmission_gear_0_5.mesh
            row = self.node.drum.nine_tooth_turns_step_drum_segment.mesh
            self.assertAlmostEqual(row.bounds[0, 2] - gear.bounds[1, 2], gap, delta=.001)

    def test_view_matches_complete_diagnostic_at_same_pose(self):
        other = ReverserAssemblyBench()
        other.set_state(knob_height=-6.8425, gear_height=-6.6575,
                        crank_angle=101.25, subtract=0, reversed_counter=1)
        other.assemble()
        other.build_stls()
        pairs = ((self.node.pinion, other.tens.p_10230_410008_1_419080),
                 (self.node.drum, other.drum.main_axle_step_drum_top_1),
                 (self.node.fork, other.lever.reversing_lever_knob_1.reversing_actuator),
                 (self.node.detent.reversing_shaft, other.lever.reversing_shaft),
                 (self.node.detent.p_5mm_ball, other.lever.p_5mm_ball))
        for shown, full in pairs:
            np.testing.assert_allclose(shown.mesh.vertices, full.mesh.vertices, atol=1e-7)

    def test_probe_turns_about_pinion_axis_not_main_axis(self):
        before = self.node.pinion.mesh.vertices.copy()
        self.node.set_state(pinion_probe=12)
        after = self.node.pinion.mesh.vertices
        center = np.array([-13.851815805, 38.057551142])
        np.testing.assert_allclose(np.linalg.norm(before[:, :2] - center, axis=1),
                                   np.linalg.norm(after[:, :2] - center, axis=1), atol=1e-8)
        self.assertGreater(np.max(np.abs(after - before)), .1)

    def test_solid_integrity(self):
        # This project's fused pinion has an enclosed negative-volume cavity
        # shell. Check material connectivity, not the number of surface shells.
        for part in (self.node.drum, self.node.pinion, self.node.fork,
                     self.node.detent.reversing_shaft, self.node.detent.p_5mm_ball):
            assert_connected_material(part.mesh)
            self.assertEqual(len(part.shape().Solids()), 1)
            self.assertTrue(part.shape().isValid())

    def test_probe_misses_below_row_but_contacts_when_raised(self):
        self.node.set_state(pinion_probe=-12)
        self.assertNotIntersecting(self.node.pinion, self.node.drum)
        self.node.set_state(lever_height=-5.035)
        self.assertIntersecting(self.node.pinion, self.node.drum)

    def test_assembly_integrity(self):
        self.assertNoSolidInterference(self.node)
