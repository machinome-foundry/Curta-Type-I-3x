"""Complete bank/other-mesh preservation and unchanged frame contracts."""

import numpy as np
import unittest

from machinome.simulation import Sim
from simulation.counter_guide_regions import maximum_shoulder_removal
from simulation.counter_guide_trial import CounterShoulderTrial
from simulation.counter_shoulder_operating_trial import (
    OriginalShoulderOperatingCurta, CounterShoulderOperatingTrial)
from simulation.test_carry_bank_trial import flexible_meshes
from simulation import test_carry_bank_frame as frame_contracts
from simulation.tools.interference import rigid_leaves


class CounterShoulderFrameTest(frame_contracts.CarryBankFrameTest):
    @classmethod
    def setUpClass(cls):
        cls.bench = CounterShoulderTrial()
        cls.bench.set_state(drop_mm=0)
        cls.bench.assemble()
        cls.bench.build_stls()

    def test_fixture_matches_the_operating_root_at_rest(self):
        # The inherited fixture identity contract applies to the candidate
        # operating root, not the deliberately unchanged production root.
        self.bench.set_state(drop_mm=0)
        sim = Sim(CounterShoulderOperatingTrial(), dt=.1, meshes=True)
        from simulation.tools.interference import world_solids
        from simulation.carry_bank_frame import stations
        installed = world_solids(sim.node, include_flexible=True)
        bench = self.native()
        mapping = {'Curta.frame.main_body': 'Curta.frame.upper_frame.main_body'}
        for path, node, slider in stations(self.bench):
            for suffix in (slider, 'tens_slide_bearing', 'carry_lever_spring.wire'):
                mapping['Curta.'+path+'.'+suffix] = 'Curta.carry_mechanism.'+path+'.'+suffix
        for path, counterpart in mapping.items():
            with self.subTest(path=path):
                a, b = bench[path], installed[counterpart]
                self.assertTrue(a.isValid() and b.isValid())
                self.assertEqual(a.cut(b).Volume(), 0)
                self.assertEqual(b.cut(a).Volume(), 0)


class CounterShoulderOperatingIdentityTest(unittest.TestCase):
    model = CounterShoulderOperatingTrial

    def test_all_other_geometry_and_complete_banks_match(self):
        before = Sim(OriginalShoulderOperatingCurta(), dt=.1, meshes=True)
        after = Sim(self.model(), dt=.1, meshes=True)
        for angle in (0, 180):
            if angle:
                for sim in (before, after):
                    command = sim.move('crank_rotation', to=angle, duration=1)
                    sim.run(1)
                    self.assertEqual(command.status, 'completed')
            self.assertEqual(dict(before.state), dict(after.state))
            self.assertEqual(len(after.state), 214)
            a, b = dict(rigid_leaves(before.node)), dict(rigid_leaves(after.node))
            self.assertEqual(set(a), set(b))
            changed = set()
            for path in a:
                if path.endswith('.tens_slider_for_turns_counter'):
                    old, new = a[path].shape(), b[path].shape()
                    self.assertEqual(new.cut(old).Volume(), 0)
                    removed = old.cut(new)
                    self.assertGreater(removed.Volume(), 0)
                    self.assertEqual(removed.cut(maximum_shoulder_removal()).Volume(), 0)
                    changed.add(path)
                else:
                    np.testing.assert_array_equal(a[path].mesh.vertices, b[path].mesh.vertices, err_msg=path)
                    np.testing.assert_array_equal(a[path].mesh.faces, b[path].mesh.faces, err_msg=path)
            self.assertEqual(len(changed), 5)
            fa, fb = dict(flexible_meshes(before.node)), dict(flexible_meshes(after.node))
            self.assertEqual(set(fa), set(fb))
            self.assertGreater(len(fa), 30)
            for path in fa:
                np.testing.assert_array_equal(fa[path].vertices, fb[path].vertices, err_msg=path)
                np.testing.assert_array_equal(fa[path].faces, fb[path].faces, err_msg=path)
