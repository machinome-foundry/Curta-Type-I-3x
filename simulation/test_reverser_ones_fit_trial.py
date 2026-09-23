"""Existing motion and capture contracts applied to an isolated fit candidate."""

import unittest

from simulation import test_running_reverser_contact_path as path_contracts
from simulation import test_reverser_seat_trial as seat_contracts
from simulation.reverser_ones_fit_trial import TrialOperatingCurta, TrialSeat, TrialOnesPinion


class OnesFitPathTrialTest(path_contracts.ReverserContactPathTest):
    model = TrialOperatingCurta


class OnesFitSeatTrialTest(seat_contracts.ReverserSeatTrialTest):
    node = TrialSeat


class OnesFlankFidelityTest(unittest.TestCase):
    def test_only_inner_flanks_are_removed_from_existing_fit(self):
        import cadquery as cq
        from simulation.fit import FittedCounterPinion

        original = FittedCounterPinion().shape()
        fitted = TrialOnesPinion().shape()
        self.assertTrue(fitted.isValid())
        self.assertEqual(len(fitted.Solids()), 1)
        box = original.BoundingBox()
        # The measured fork-capture material begins beyond R6.16. R6 is
        # a dimensional protected boundary, not an allowed overlap volume.
        allowed = cq.Solid.makeCylinder(6., box.zlen+2, (0, 0, box.zmin-1))
        added = fitted.copy().cut(original.copy())
        removed = original.copy().cut(fitted.copy())
        outside = removed.copy().cut(allowed.copy())
        for difference in (added, removed, outside):
            self.assertTrue(difference.isValid())
        self.assertEqual(added.Volume(), 0)
        self.assertGreater(removed.Volume(), 0)
        self.assertEqual(outside.Volume(), 0)
        # Preserve the keyed bearing region, not merely the outer capture.
        key = cq.Solid.makeCylinder(3.5, box.zlen+2, (0, 0, box.zmin-1))
        lost_key = removed.copy().intersect(key)
        self.assertTrue(lost_key.isValid())
        self.assertEqual(lost_key.Volume(), 0)
        self.assertEqual((fitted.BoundingBox().zmin, fitted.BoundingBox().zmax),
                         (box.zmin, box.zmax))
