"""Actual-root regression: axial reversal must not cross an engaged drum tooth.

The first-contact height is a measured fixture, not a proposed universal
reverser limit. A production restraint must also consider retained shaft phase,
all six counter inputs, crank lift and travel in both directions.
"""

import unittest

from machinome.exact import intersect_shapes
from machinome.simulation import Sim
from simulation.cover_fits import mesh_solid
from simulation.running import OperatingCurta
from simulation.tools.higher_locking_envelope import faceted_common_volume
from simulation.tools.interference import rigid_leaves, world_solids


GEAR = 'Curta.transmission.turns.ones.p_10218_1'
DRUM = ('Curta.main_drive.stepped_drum.main_axle_step_drum_1.'
        'main_axle_step_drum_top_1')
FIRST_CONTACT = 1.0575


def prepare(model=OperatingCurta):
    sim = Sim(model(), dt=.1, meshes=True)
    command = sim.move('crank_rotation', to=90, duration=.5)
    sim.run(.5)
    assert command.status == 'completed'
    assert sim.state['crank_rotation'] == 90
    return sim


def commons(sim):
    native = world_solids(sim.node, selected={GEAR, DRUM})
    common = intersect_shapes(native[GEAR], native[DRUM], GEAR, DRUM)
    assert common.isValid()
    leaves = dict(rigid_leaves(sim.node))
    faceted = mesh_solid(leaves[GEAR].mesh) ^ mesh_solid(leaves[DRUM].mesh)
    return common.Volume(), faceted_common_volume(faceted)


class RunningReverserStrokeTest(unittest.TestCase):
    model = OperatingCurta

    def test_all_four_prepared_modes_complete_a_full_crank_stroke(self):
        for lever, lift in ((-4.9425, 0), (3.9075, 9), (3.9075, 0), (-4.9425, 9)):
            with self.subTest(lever=lever, lift=lift):
                sim = Sim(self.model(), dt=.1, meshes=False)
                self.assertEqual(sim.move('reverser_height', to=lever).status, 'completed')
                self.assertEqual(sim.move('crank_elevation', to=lift).status, 'completed')
                request = sim.move('crank_rotation', to=360, duration=2)
                sim.run(2)
                self.assertEqual(request.status, 'completed')
                self.assertEqual(sim.state['crank_rotation'], 360)


class RunningReverserWrongOrderTest(unittest.TestCase):
    model = OperatingCurta

    def test_long_request_cannot_cross_contact_into_a_later_clear_band(self):
        sim = prepare(self.model)
        saved = sim.snapshot()
        original = dict(sim.state)
        request = sim.move('reverser_height', to=-3)
        self.assertEqual(request.status, 'blocked')
        self.assertGreaterEqual(sim.state['reverser_height'], FIRST_CONTACT)
        self.assertLess(sim.state['reverser_height'], 3.9075)
        self.assertEqual(commons(sim), (0, 0))
        expected = sim.snapshot()
        request = sim.move('reverser_height', to=-3)
        self.assertEqual(request.status, 'blocked')
        self.assertEqual(sim.snapshot(), expected)
        sim.restore(saved)
        sim.move('reverser_height', to=-3)
        self.assertEqual(sim.snapshot(), expected)
        self.assertEqual(sim.state['crank_rotation'], original['crank_rotation'])
        self.assertEqual(sim.state['transmission.turns.ones.turn'],
                         original['transmission.turns.ones.turn'])
        # Relief is an explicit user request, not scheduled completion.
        self.assertEqual(sim.move('reverser_height', to=3.9075).status, 'completed')
        self.assertEqual(sim.snapshot(), saved)

    def test_actual_retained_request_cannot_enter_an_engaged_tooth(self):
        sim = prepare(self.model)
        before = dict(sim.state)
        command = sim.move('reverser_height', to=FIRST_CONTACT-.01)
        volumes = commons(sim)
        # Check geometry before the expected terminal state, so the baseline
        # fails on actual material penetration, not merely a guessed status.
        for kernel, volume in zip(('native', 'world64'), volumes):
            with self.subTest(kernel=kernel):
                self.assertEqual(volume, 0)
        self.assertEqual(command.status, 'blocked')
        self.assertGreaterEqual(sim.state['reverser_height'], FIRST_CONTACT)
        self.assertLess(sim.state['reverser_height'], 3.9075)
        for name in ('crank_rotation', 'crank_elevation', 'carriage_rotation',
                     'carriage_elevation', 'clearing_rotation'):
            self.assertEqual(sim.state[name], before[name], name)

    def test_precontact_play_is_admitted_without_preparing_another_control(self):
        sim = prepare(self.model)
        before = dict(sim.state)
        command = sim.move('reverser_height', to=FIRST_CONTACT+.01)
        self.assertEqual(command.status, 'completed')
        self.assertAlmostEqual(sim.state['reverser_height'], FIRST_CONTACT+.01)
        self.assertEqual(commons(sim), (0, 0))
        for name in ('crank_rotation', 'crank_elevation', 'carriage_rotation',
                     'carriage_elevation', 'clearing_rotation'):
            self.assertEqual(sim.state[name], before[name], name)

    def test_a_different_retained_phase_can_withdraw_from_the_same_crank_pose(self):
        sim = Sim(self.model(), dt=.1, meshes=True)
        self.assertEqual(sim.move('reverser_height', to=-4.9425).status, 'completed')
        command = sim.move('crank_rotation', to=90, duration=.5)
        sim.run(.5)
        self.assertEqual(command.status, 'completed')
        self.assertAlmostEqual(sim.state['transmission.turns.ones.turn'], 231.6)
        # Same crank angle as the red test, but a different physical history.
        # The ones pair must retain its available withdrawal path; a blanket
        # home-only lock or universal 1.0575 mm floor cannot represent both.
        for height in (-3, 0, 1.0675, 3.9075):
            with self.subTest(height=height):
                command = sim.move('reverser_height', to=height)
                self.assertEqual(command.status, 'completed')
                self.assertAlmostEqual(sim.state['reverser_height'], height)
                self.assertEqual(commons(sim), (0, 0))
                self.assertEqual(sim.state['crank_rotation'], 90)
                self.assertAlmostEqual(sim.state['transmission.turns.ones.turn'], 231.6)


if __name__ == '__main__':
    unittest.main()
