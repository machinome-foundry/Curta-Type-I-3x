"""Bounded shoulder trial: preserve interfaces before fitting material."""

import json
import unittest
import manifold3d as manifold

from machinome.exact import intersect_shapes
from simulation.carry_heads import TurnsSlider
from simulation.carry_bank_frame import FittedCarryBankFrameBench, stations
from simulation.carry_bank_regions import COUNTER_ANGLES
from simulation.counter_guide_regions import (
    in_counter_station, maximum_relieved, maximum_shoulder_removal, region)
from simulation.cover_fits import mesh_solid
from simulation.counter_guide_trial import CounterShoulderTrial, InsufficientCounterShoulderTrial
from simulation.counter_guide_shoulder import ShoulderClearedTurnsSlider
from simulation.tools.higher_locking_envelope import faceted_common_volume
from simulation.tools.interference import world_solids


class CounterShoulderRegionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = TurnsSlider().shape()
        cls.maximum = maximum_relieved(cls.original)

    def test_maximum_removal_preserves_valid_connected_material(self):
        self.assertTrue(self.maximum.isValid())
        self.assertEqual(len(self.maximum.Solids()), 1)
        self.assertEqual(self.maximum.cut(self.original).Volume(), 0)
        removed = self.original.cut(self.maximum)
        self.assertGreater(removed.Volume(), 0)
        self.assertLess(removed.Volume(), maximum_shoulder_removal().Volume())
        self.assertEqual(removed.cut(maximum_shoulder_removal()).Volume(), 0)
        print(json.dumps(dict(maximum_removed_mm3=removed.Volume())), flush=True)

    def test_all_curved_source_surfaces_including_detents_are_unchanged(self):
        checked = 0
        for index, face in enumerate(self.original.Faces()):
            if face.geomType() == 'PLANE':
                continue
            checked += 1
            with self.subTest(face=index, kind=face.geomType()):
                lost = face.cut(self.maximum)
                self.assertTrue(lost.isValid())
                self.assertEqual(lost.Area(), 0)
        self.assertGreater(checked, 0)

    def test_measured_running_faces_and_tip_keep_their_source_surfaces(self):
        # Face identification tolerances select measured native planes; no
        # positive removed area or overlap is excused by a tolerance.
        checked = set()
        for face in self.original.Faces():
            if face.geomType() != 'PLANE':
                continue
            box = in_counter_station(face).BoundingBox()
            selected = None
            if box.xmax-box.xmin < 1e-5:
                for x, name in ((54.225, 'left guide'), (60.225, 'right guide')):
                    if abs(box.xmin-x) < 1e-5:
                        selected = name
            if box.zmax-box.zmin < 1e-5 and abs(box.zmax-31.15) < 1e-5:
                selected = 'pin tip'
            if selected:
                checked.add(selected)
                with self.subTest(surface=selected):
                    self.assertEqual(face.cut(self.maximum).Area(), 0)
        self.assertEqual(checked, {'left guide', 'right guide', 'pin tip'})

    def test_fork_shoe_and_guide_back_material_is_preserved(self):
        for name, low, high in (
                ('fork and reset shoe', (-80, -80, -100), (52, 80, 80)),
                ('guide stem and back', (54.225, -8, -26.2), (60.225, -6.3, 31.2))):
            local = in_counter_station(region(low, high), inverse=True)
            protected = self.original.intersect(local)
            with self.subTest(region=name):
                self.assertTrue(protected.isValid())
                self.assertGreater(protected.Volume(), 0)
                self.assertEqual(protected.cut(self.maximum).Volume(), 0)


class CounterGuideShoulderTest(unittest.TestCase):
    node_type = CounterShoulderTrial
    clears = True

    @classmethod
    def setUpClass(cls):
        cls.root = cls.node_type()
        cls.root.set_state(drop_mm=0)
        cls.root.assemble()
        cls.root.build_stls()

    def test_every_counter_shoulder_clears_the_guide_ledge_at_full_drop(self):
        self.root.set_state(drop_mm=4.2)
        for path, node, slider in stations(self.root):
            if not path.startswith('turns_carries'):
                continue
            names = ('Curta.'+path+'.'+slider, 'Curta.'+path+'.tens_slide_bearing')
            shapes = world_solids(self.root, selected=set(names))
            native = intersect_shapes(shapes[names[0]], shapes[names[1]], *names).Volume()
            body_mesh = mesh_solid(getattr(node, slider).mesh)
            guide_mesh = mesh_solid(node.tens_slide_bearing.mesh)
            mesh = faceted_common_volume(body_mesh ^ guide_mesh)
            angle = COUNTER_ANGLES[int(path.rsplit('_', 1)[-1])-1]
            # Independently measured ledge window, not the removal allowance
            # or an overlap-derived cutter. Complete-guide measurements above
            # remain explicit even when this localized interface clears.
            window = region((60.30, -8, -17.30), (61.90, -6.30, -16.70)).rotate(
                (0, 0, 0), (0, 0, 1), angle)
            ledge = intersect_shapes(shapes[names[1]], window, names[1], 'ledge window')
            ledge_native = intersect_shapes(shapes[names[0]], ledge,
                                            names[0], 'guide ledge').Volume()
            mesh_window = manifold.Manifold.cube((1.60, 1.70, .60)).translate(
                (60.30, -8, -17.30)).rotate((0, 0, angle))
            ledge_mesh = faceted_common_volume(body_mesh ^ guide_mesh ^ mesh_window)
            print(json.dumps(dict(station=path, drop_mm=4.2,
                                  native_mm3=native, world64_mm3=mesh,
                                  ledge_native_mm3=ledge_native,
                                  ledge_world64_mm3=ledge_mesh)), flush=True)
            with self.subTest(station=path, kernel='native'):
                if self.clears:
                    self.assertEqual(ledge_native, 0)
                else:
                    self.assertGreater(ledge_native, 0)
            with self.subTest(station=path, kernel='world64'):
                if self.clears:
                    self.assertEqual(ledge_mesh, 0)
                else:
                    self.assertGreater(ledge_mesh, 0)


class OriginalCounterGuideNegativeTest(CounterGuideShoulderTest):
    node_type = FittedCarryBankFrameBench
    clears = False


class InsufficientCounterGuideNegativeTest(CounterGuideShoulderTest):
    node_type = InsufficientCounterShoulderTrial
    clears = False


class CounterShoulderMaterialTest(unittest.TestCase):
    def test_fitted_material_is_only_removed_inside_the_independent_allowance(self):
        original = TurnsSlider().shape()
        fitted = ShoulderClearedTurnsSlider().shape()
        self.assertTrue(fitted.isValid())
        self.assertEqual(len(fitted.Solids()), 1)
        self.assertEqual(fitted.cut(original).Volume(), 0)
        removed = original.cut(fitted)
        self.assertGreater(removed.Volume(), 0)
        self.assertEqual(removed.cut(maximum_shoulder_removal()).Volume(), 0)
        self.assertEqual(maximum_relieved(original).cut(fitted).Volume(), 0)

    def test_native_shoulder_sweep_has_a_strict_ledge_gap(self):
        root = CounterShoulderTrial()
        root.set_state(drop_mm=0)
        root.assemble()
        for path, node, slider in stations(root):
            if not path.startswith('turns_carries'):
                continue
            angle = COUNTER_ANGLES[int(path.rsplit('_', 1)[-1])-1]
            names = ('Curta.'+path+'.'+slider, 'Curta.'+path+'.tens_slide_bearing')
            shapes = world_solids(root, selected=set(names))
            body, guide = (shapes[name].rotate((0, 0, 0), (0, 0, 1), -angle)
                           for name in names)
            shoulder = intersect_shapes(body, region((60.30, -8, -30), (61.90, -6.30, 35)),
                                        names[0], 'full-height shoulder window')
            ledge = intersect_shapes(guide, region((60.30, -8, -17.30), (61.90, -6.30, -16.70)),
                                     names[1], 'guide ledge window')
            self.assertGreater(shoulder.Volume(), 0)
            self.assertGreater(ledge.Volume(), 0)
            moving, fixed = shoulder.BoundingBox(), ledge.BoundingBox()
            # Every intermediate translated shoulder lies in this box: the
            # fixed guide and 4.2 mm pure axial travel are independently known.
            swept = region((moving.xmin, moving.ymin, moving.zmin-4.2),
                           (moving.xmax, moving.ymax, moving.zmax))
            with self.subTest(station=path):
                self.assertGreater(moving.zmin-4.2, fixed.zmax)
                self.assertEqual(intersect_shapes(swept, ledge,
                                 'continuous shoulder enclosure', names[1]).Volume(), 0)

    def test_world64_shoulder_sweep_has_a_strict_ledge_gap(self):
        root = CounterShoulderTrial()
        root.set_state(drop_mm=0)
        root.assemble()
        root.build_stls()
        for path, node, slider in stations(root):
            if not path.startswith('turns_carries'):
                continue
            angle = COUNTER_ANGLES[int(path.rsplit('_', 1)[-1])-1]
            body = mesh_solid(getattr(node, slider).mesh).rotate((0, 0, -angle))
            guide = mesh_solid(node.tens_slide_bearing.mesh).rotate((0, 0, -angle))
            shoulder = body ^ manifold.Manifold.cube((1.6, 1.7, 65)).translate((60.30, -8, -30))
            ledge = guide ^ manifold.Manifold.cube((1.6, 1.7, .6)).translate((60.30, -8, -17.30))
            self.assertGreater(faceted_common_volume(shoulder), 0)
            self.assertGreater(faceted_common_volume(ledge), 0)
            low_x, low_y, low_z, high_x, high_y, high_z = shoulder.bounding_box()
            swept = manifold.Manifold.cube((high_x-low_x, high_y-low_y, high_z-low_z+4.2)).translate(
                (low_x, low_y, low_z-4.2))
            with self.subTest(station=path):
                self.assertGreater(low_z-4.2, ledge.bounding_box()[5])
                self.assertEqual(faceted_common_volume(swept ^ ledge), 0)

    def test_insufficient_native_relief_preserves_a_positive_obstruction(self):
        root = FittedCarryBankFrameBench()
        root.set_state(drop_mm=4.2)
        root.assemble()
        insufficient = in_counter_station(
            ShoulderClearedTurnsSlider(shoulder_relief=.2).shape()).translate((0, 0, -4.2))
        for path, node, slider in stations(root):
            if not path.startswith('turns_carries'):
                continue
            angle = COUNTER_ANGLES[int(path.rsplit('_', 1)[-1])-1]
            name = 'Curta.'+path+'.tens_slide_bearing'
            guide = world_solids(root, selected={name})[name]
            body = insufficient.rotate((0, 0, 0), (0, 0, 1), angle)
            with self.subTest(station=path):
                self.assertGreater(intersect_shapes(body, guide,
                                   'insufficient .2 mm relief', name).Volume(), 0)
