"""Independent source witness for all seventeen ball guides and the spider."""

import unittest

from machinome.node import AssemblyNode
from machinome.motion.mates import declared_mates
from machinome.motion.ports import Time
from machinome.simulation import Driver, Sim
from simulation.register_detents import RegisterDetents
from simulation.mechanism import RegisterCarriage
from simulation.test_mate_refactor import placed_basis


class LegacyDetentBench(AssemblyNode):
    time = Time.running()
    rise = Driver(default=0, unit='mm')
    detents = RegisterDetents()
    for _index in range(1, 18):
        rise.drives(getattr(detents, f'p_6mm_ball_419241_{_index}').lift, ratio=_index/17)
    del _index


# Resolve the actual child outside a class body (inside one, construction
# deliberately produces a declaration reference, not a realized instance).
_ProductionDetents = type(RegisterCarriage().dial_detents)


class MatedDetentBench(LegacyDetentBench):
    detents = _ProductionDetents()


class DetentMateTest(unittest.TestCase):
    def test_all_ball_guides_and_the_complete_spider_are_attached(self):
        mates = declared_mates(type(MatedDetentBench().detents))
        self.assertEqual(len(mates), 18)
        self.assertIsNone(mates['spider_mount'].freedom)
        self.assertEqual({mate.freedom.written for mate in mates.values()
                          if mate.freedom is not None},
                         {f'p_6mm_ball_419241_{index}.lift' for index in range(1, 18)})

    def test_original_and_mated_detents_preserve_poses_shape_and_replay(self):
        sims = tuple(Sim(cls(), dt=.1) for cls in (LegacyDetentBench, MatedDetentBench))
        for rise in (0, .25, .7, 1.4, .5, 0):
            for sim in sims:
                saved = sim.snapshot()
                self.assertEqual(sim.move('rise', to=rise).status, 'completed')
                expected = sim.snapshot()
                sim.restore(saved)
                self.assertEqual(sim.move('rise', to=rise).status, 'completed')
                self.assertEqual(sim.snapshot(), expected)
            self.assertEqual(list(sims[0].state), list(sims[1].state))
            self.assertEqual(dict(sims[0].state), dict(sims[1].state))
            before, after = (placed_basis(sim.node) for sim in sims)
            self.assertEqual(before.keys(), after.keys())
            self.assertEqual(sum(path.startswith('.detents.p_6mm_ball_419241_')
                                 for path in before), 17)
            self.assertEqual(sum(path.endswith('.tip') for path in before), 17)
            self.assertEqual(sum(path.endswith('.arm') for path in before), 17)
            self.assertIn('.detents.spider_spring.mount', before)
            for path in before:
                for first, second in zip(before[path], after[path]):
                    for a, b in zip(first, second):
                        self.assertAlmostEqual(a, b, places=8, msg=path)
            for bank, count in (('result', 11), ('turns', 6)):
                for index in range(1, count + 1):
                    arms = [getattr(sim.node.detents.spider_spring,
                                    f'{bank}_{index}').arm for sim in sims]
                    for edge in ('top', 'bottom'):
                        for station in range(1, 7):
                            self.assertEqual(getattr(arms[0], f'{edge}_{station}').value,
                                             getattr(arms[1], f'{edge}_{station}').value)
