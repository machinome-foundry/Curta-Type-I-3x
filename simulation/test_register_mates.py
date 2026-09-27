"""Compare frame-attached dial banks with the pre-migration declarations.

The independent witnesses keep the original site joints and source placement
code. They must not inherit from the refactored dial banks under test.
"""

import unittest

from machinome.node import AssemblyNode
from machinome.motion.joints import Revolute
from machinome.motion.mates import declared_mates
from machinome.motion.ports import Time
from machinome.simulation import Driver, Sim
from simulation import dial_fits as fitted
from simulation.standard import layers as source
from simulation.fit import CARRIAGE_CENTER, CARRIAGE_CLOCKING
from simulation.registers import ResultDials, TurnsDials
from simulation.running_parts import RESULT_DIALS, TURNS_DIALS
from simulation.test_mate_refactor import placed_basis


class LegacyResultDials(source.ResultRegister):
    p_10203_1 = fitted.Part10203_1(turn=Revolute(
        axis=(-0.9999539409, -0.0095977127, 2e-10), at=(72.008486542, 0.647810225, 33.9)))
    p_10203_2 = fitted.Part10203_2(turn=Revolute(
        axis=(-0.9429319505, 0.3329854904, 1e-10), at=(67.932893459, -23.838001321, 33.9)))
    p_10205_1 = fitted.Part10205_1(turn=Revolute(
        axis=(-0.7721784508, 0.6354057288, 0.0), at=(55.72844801, -45.453202839, 33.9)))
    p_10205_2 = fitted.Part10205_2(turn=Revolute(
        axis=(-0.5082888339, 0.8611866588, 0.0), at=(36.867186359, -61.590682021, 33.9)))
    p_10204_1 = fitted.Part10204_1(turn=Revolute(
        axis=(-0.183092082, 0.9830957682, 0.0), at=(13.624055025, -70.304020713, 33.9)))
    p_10204_2 = fitted.Part10204_2(turn=Revolute(
        axis=(0.164188277, 0.9864290191, 0.0), at=(-11.197481322, -70.542261674, 33.9)))
    p_10204_3 = fitted.Part10204_3(turn=Revolute(
        axis=(0.491665107, 0.870784372, 0.0), at=(-34.603579072, -62.276669529, 33.9)))
    p_10204_4 = fitted.Part10204_4(turn=Revolute(
        axis=(0.759839869, 0.650110278, 0.0), at=(-53.771117399, -46.504196676, 33.9)))
    p_10204_5 = fitted.Part10204_5(turn=Revolute(
        axis=(0.9363667283, 0.3510232901, 0.0), at=(-66.388208297, -25.127236119, 33.9)))
    p_10204_6 = fitted.Part10204_6(turn=Revolute(
        axis=(0.9999539409, 0.009597713, 0.0), at=(-70.933044396, -0.724164791, 33.9)))
    results_dial_type_2_1 = fitted.FittedDialType2(turn=Revolute(
        axis=(0.9429319507, -0.3329854896, 1e-10), at=(-66.857451389, 23.761646754, 33.9)))

    def render(self):
        super().render()
        self.translate(tuple(-value for value in CARRIAGE_CENTER))
        self.rotate(-CARRIAGE_CLOCKING, (0, 0, 1))


class LegacyTurnsDials(source.TurnsRegister):
    p_10203_3 = fitted.Part10203_3(turn=Revolute(
        axis=(0.650110279, -0.7598398681, 3e-10), at=(-45.928298358, 54.270661151, 33.9)))
    p_10203_4 = fitted.Part10203_4(turn=Revolute(
        axis=(0.3510232907, -0.936366728, 0.0), at=(-24.5513378, 66.887752049, 33.9)))
    p_10205_3 = fitted.Part10205_3(turn=Revolute(
        axis=(0.009597713, -0.9999539409, 0.0), at=(-0.148266473, 71.432588148, 33.9)))
    p_10205_4 = fitted.Part10205_4(turn=Revolute(
        axis=(-0.3329854899, -0.9429319506, 0.0), at=(24.337545072, 67.35699514, 33.9)))
    p_10204_7 = fitted.Part10204_7(turn=Revolute(
        axis=(-0.6354057288, -0.7721784508, 0.0), at=(45.952746591, 55.152549691, 33.9)))
    results_dial_type_2_2 = fitted.FittedDialType2(turn=Revolute(
        axis=(-0.8611866588, -0.508288834, -0.0), at=(62.090225773, 36.291288041, 33.9)))

    def render(self):
        super().render()
        self.translate(tuple(-value for value in CARRIAGE_CENTER))
        self.rotate(-CARRIAGE_CLOCKING, (0, 0, 1))


def dial_ends(bank, table):
    return tuple(getattr(bank, name).turn for name, zero in table)


def dial_angles(table):
    return lambda sources, targets: lambda request: tuple(zero + request for name, zero in table)


class ResultBench(AssemblyNode):
    time = Time.running()
    request = Driver(default=0, unit='deg')
    bank = ResultDials()
    request.drives(dial_ends(bank, RESULT_DIALS), law=dial_angles(RESULT_DIALS))


class LegacyResultBench(ResultBench):
    bank = LegacyResultDials()


class TurnsBench(AssemblyNode):
    time = Time.running()
    request = Driver(default=0, unit='deg')
    bank = TurnsDials()
    request.drives(dial_ends(bank, TURNS_DIALS), law=dial_angles(TURNS_DIALS))


class LegacyTurnsBench(TurnsBench):
    bank = LegacyTurnsDials()


class RegisterMateTest(unittest.TestCase):
    def test_every_dial_is_attached_by_its_existing_turn_joint(self):
        for bank, table in ((ResultDials, RESULT_DIALS), (TurnsDials, TURNS_DIALS)):
            with self.subTest(bank=bank.__name__):
                mates = declared_mates(bank)
                self.assertEqual(len(mates), len(table))
                self.assertEqual({mate.moving.written for mate in mates.values()},
                                 {name + '.axle' for name, zero in table})
                for mate in mates.values():
                    self.assertEqual(mate.freedom.written,
                                     mate.moving.written.rsplit('.', 1)[0] + '.turn')

    def test_legacy_and_mated_dials_keep_all_bank_values_poses_and_replay(self):
        for old, current, table in ((LegacyResultBench, ResultBench, RESULT_DIALS),
                                    (LegacyTurnsBench, TurnsBench, TURNS_DIALS)):
            with self.subTest(bank=current.__name__):
                sims = (Sim(old(), dt=.1), Sim(current(), dt=.1))
                expected_keys = {'request', *(f'bank.{name}.turn' for name, zero in table)}
                for angle in (0, 36, -72, 200, 0):
                    for sim in sims:
                        before = sim.snapshot()
                        self.assertEqual(sim.move('request', to=angle).status, 'completed')
                        after = sim.snapshot()
                        sim.restore(before)
                        self.assertEqual(sim.move('request', to=angle).status, 'completed')
                        self.assertEqual(sim.snapshot(), after)
                    self.assertEqual(set(sims[0].state), expected_keys)
                    self.assertEqual(list(sims[0].state), list(sims[1].state))
                    self.assertEqual(dict(sims[0].state), dict(sims[1].state))
                    poses = [placed_basis(sim.node) for sim in sims]
                    self.assertIn('.bank.' + table[0][0] + '.results_dial_type_1', poses[0])
                    for name, zero in table:
                        prefix = '.bank.' + name
                        self.assertIn(prefix, poses[0])
                        if not name.startswith('results_dial_type_2'):
                            self.assertTrue(any(path.startswith(prefix + '.results_dial')
                                                for path in poses[0]), name)
                    self.assertEqual(poses[0].keys(), poses[1].keys())
                    for path, points in poses[0].items():
                        for before, after in zip(points, poses[1][path]):
                            for a, b in zip(before, after):
                                self.assertAlmostEqual(a, b, places=8, msg=path)
