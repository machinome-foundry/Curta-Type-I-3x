"""Independent source-placement witness for the fifteen carry stations."""

import unittest

from machinome.node import AssemblyNode
from machinome.motion.mates import declared_mates
from machinome.motion.ports import Time
from machinome.simulation import Driver, Sim
from simulation.standard import carry
from simulation.running_parts import (
    RetainedResultCarries, RetainedTurnsCarries, retained_lever,
    RESULT_RESTS, TURNS_RESTS,
)
from simulation.test_mate_refactor import placed_basis
from simulation import counter_guide_trial
from simulation.counter_shoulder_running_parts import ShoulderRetainedTurnsCarries


class LegacyResultCarries(carry.ResultsCarry):
    for _index, _rest in enumerate(RESULT_RESTS, 1):
        locals()[f'results_tens_lever_assembly_{_index}'] = retained_lever(
            getattr(carry, f'ResultsLever{_index}'), _rest)()
    del _index, _rest


class LegacyTurnsCarries(carry.TurnsCarry):
    for _index, _rest in enumerate(TURNS_RESTS, 1):
        locals()[f'turns_tens_lever_assembly_{_index}'] = retained_lever(
            getattr(carry, f'TurnsLever{_index}'), _rest, True)()
    del _index, _rest


class LegacyCarryBench(AssemblyNode):
    time = Time.running()
    stroke = Driver(default=0, unit='mm')
    result = LegacyResultCarries()
    turns = LegacyTurnsCarries()
    for _index, _rest in enumerate(RESULT_RESTS, 1):
        stroke.drives(getattr(result, f'results_tens_lever_assembly_{_index}')
                      .tens_slider_for_results.travel, offset=_rest)
    for _index, _rest in enumerate(TURNS_RESTS, 1):
        stroke.drives(getattr(turns, f'turns_tens_lever_assembly_{_index}')
                      .tens_slider_for_turns_counter.travel, offset=_rest)
    del _index, _rest


class MatedCarryBench(LegacyCarryBench):
    result = RetainedResultCarries()
    turns = RetainedTurnsCarries()


class LegacyShoulderCarries(carry.TurnsCarry):
    for _index, _rest in enumerate(TURNS_RESTS, 1):
        locals()[f'turns_tens_lever_assembly_{_index}'] = retained_lever(
            getattr(counter_guide_trial, f'TurnsLever{_index}'), _rest, True)()
    del _index, _rest


class LegacyShoulderBench(LegacyCarryBench):
    turns = LegacyShoulderCarries()


class MatedShoulderBench(MatedCarryBench):
    turns = ShoulderRetainedTurnsCarries()


class CarryMateTest(unittest.TestCase):
    legacy = LegacyCarryBench
    mated = MatedCarryBench

    def test_each_station_attaches_its_slider_bearing_and_spring(self):
        root = self.mated()
        for bank_name, prefix, count, slider in (
                ('result', 'results', 10, 'tens_slider_for_results'),
                ('turns', 'turns', 5, 'tens_slider_for_turns_counter')):
            bank = getattr(root, bank_name)
            for index in range(1, count + 1):
                station = getattr(bank, f'{prefix}_tens_lever_assembly_{index}')
                with self.subTest(bank=bank_name, station=index):
                    mates = declared_mates(type(station))
                    self.assertEqual(len(mates), 3)
                    self.assertEqual(mates['slider_mount'].freedom.written, f'{slider}.travel')
                    self.assertIsNone(mates['bearing_mount'].freedom)
                    self.assertIsNone(mates['spring_mount'].freedom)

    def test_source_stations_preserve_poses_state_spring_shape_and_replay(self):
        sims = tuple(Sim(cls(), dt=.1) for cls in (self.legacy, self.mated))
        for stroke in (0, .84, 2.1, 2.94, 4.2, 1.05, 0):
            for sim in sims:
                saved = sim.snapshot()
                self.assertEqual(sim.move('stroke', to=stroke).status, 'completed')
                expected = sim.snapshot()
                sim.restore(saved)
                self.assertEqual(sim.move('stroke', to=stroke).status, 'completed')
                self.assertEqual(sim.snapshot(), expected)
            self.assertEqual(list(sims[0].state), list(sims[1].state))
            self.assertEqual(dict(sims[0].state), dict(sims[1].state))
            before, after = (placed_basis(sim.node) for sim in sims)
            self.assertEqual(before.keys(), after.keys())
            for ending, count in (('.tens_slider_for_results', 10),
                                  ('.tens_slider_for_turns_counter', 5),
                                  ('.tens_slide_bearing', 15),
                                  ('.carry_lever_spring.wire', 15)):
                self.assertEqual(sum(path.endswith(ending) for path in before), count)
            for path in before:
                for first, second in zip(before[path], after[path]):
                    for a, b in zip(first, second):
                        self.assertAlmostEqual(a, b, places=8, msg=path)
            for bank_name, prefix, count in (('result', 'results', 10), ('turns', 'turns', 5)):
                for index in range(1, count + 1):
                    wires = [getattr(getattr(sim.node, bank_name),
                        f'{prefix}_tens_lever_assembly_{index}').carry_lever_spring.wire
                        for sim in sims]
                    for parameter in ('left_mid', 'left_root', 'left_bridge',
                                      'right_bridge', 'right_mid', 'right_tip'):
                        self.assertEqual(getattr(wires[0], parameter).value,
                                         getattr(wires[1], parameter).value)


class ShoulderCarryMateTest(CarryMateTest):
    legacy = LegacyShoulderBench
    mated = MatedShoulderBench
