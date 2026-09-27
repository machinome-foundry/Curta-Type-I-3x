"""Frozen track placements independently witness decimal-marker attachment."""

import unittest

from machinome.motion.joints import Bound, Revolute
from machinome.motion.mates import declared_mates
from machinome.motion.ports import Time
from machinome.parameters import Length
from machinome.simulation import Sim
from simulation.standard import assembly as source
from simulation.decimal_markers import (
    LOWER_CENTER, LOWER_GAPS, UPPER_GAPS, MarkerBench,
    LowerMovableMarkers, UpperMovableMarkers,
    LowerTrackPlacement, UpperTrackPlacement,
)
from simulation.test_mate_refactor import placed_basis


def old_marker(part, previous=None, gap=0, first=None, closing_gap=0, center=LOWER_CENTER):
    upper = None if previous is None else Bound(
        lambda own, neighbour: neighbour + gap, reads=(previous,))
    lower = None if first is None else Bound(
        lambda own, neighbour: neighbour - closing_gap, reads=(first,))
    return part(turn=Revolute(axis=(0, 0, 1), at=center, range=(lower, upper)))


class LegacyLowerMarkers(LowerTrackPlacement):
    decimal_marker_1 = old_marker(source.DecimalMarker1)
    decimal_marker_2 = old_marker(source.DecimalMarker2, decimal_marker_1.turn, LOWER_GAPS[0])
    decimal_marker_3 = old_marker(source.DecimalMarker3, decimal_marker_2.turn, LOWER_GAPS[1])
    decimal_marker_4 = old_marker(source.DecimalMarker4, decimal_marker_3.turn, LOWER_GAPS[2])
    decimal_marker_5 = old_marker(source.DecimalMarker5, decimal_marker_4.turn, LOWER_GAPS[3],
                                  decimal_marker_1.turn, LOWER_GAPS[4])


class LegacyUpperMarkers(UpperTrackPlacement):
    decimal_marker_6 = old_marker(source.DecimalMarker6, center=(0, 0, 0))
    decimal_marker_7 = old_marker(source.DecimalMarker7, decimal_marker_6.turn, UPPER_GAPS[0], center=(0, 0, 0))
    decimal_marker_8 = old_marker(source.DecimalMarker8, decimal_marker_7.turn, UPPER_GAPS[1], center=(0, 0, 0))
    decimal_marker_9 = old_marker(source.DecimalMarker9, decimal_marker_8.turn, UPPER_GAPS[2], center=(0, 0, 0))
    decimal_marker_10 = old_marker(source.DecimalMarker10, decimal_marker_9.turn, UPPER_GAPS[3],
                                   decimal_marker_6.turn, UPPER_GAPS[4], center=(0, 0, 0))


class LegacyMarkerBench(MarkerBench):
    time = Time.running()
    radial_seat = Length(.06, min=0)
    lower = LegacyLowerMarkers(radial_seat=radial_seat)
    upper = LegacyUpperMarkers(radial_seat=radial_seat)


class MatedMarkerBench(LegacyMarkerBench):
    lower = LowerMovableMarkers(radial_seat=LegacyMarkerBench.radial_seat)
    upper = UpperMovableMarkers(radial_seat=LegacyMarkerBench.radial_seat)


class MarkerMateTest(unittest.TestCase):
    def test_each_marker_references_its_original_bounded_joint(self):
        for owner, first in ((LowerMovableMarkers, 1), (UpperMovableMarkers, 6)):
            with self.subTest(bank=owner.__name__):
                mates = declared_mates(owner)
                self.assertEqual(len(mates), 5)
                self.assertEqual({mate.freedom.written for mate in mates.values()},
                                 {f'decimal_marker_{i}.turn' for i in range(first, first + 5)})

    def test_original_and_mated_tracks_preserve_poses_stops_and_replay(self):
        # Non-default seats exercise frame callables; they are placement
        # witnesses only, not claims of clearance at those diagnostic seats.
        for seat in (0, .06, .12):
            with self.subTest(radial_seat=seat):
                sims = tuple(Sim(cls(radial_seat=seat), dt=.1)
                             for cls in (LegacyMarkerBench, MatedMarkerBench))

                def compare():
                    self.assertEqual(list(sims[0].state), list(sims[1].state))
                    self.assertEqual(dict(sims[0].state), dict(sims[1].state))
                    before, after = (placed_basis(sim.node) for sim in sims)
                    self.assertEqual(before.keys(), after.keys())
                    for index in range(1, 11):
                        bank = 'lower' if index < 6 else 'upper'
                        for part in ('position_marker', 'p_3mm_ball', 'decimal_marker_spring'):
                            path = f'.{bank}.decimal_marker_{index}.{part}'
                            self.assertIn(path, before)
                            for first, second in zip(before[path], after[path]):
                                for a, b in zip(first, second):
                                    self.assertAlmostEqual(a, b, places=8, msg=path)

                compare()
                # Every neighbour stop, then space-opening travel, full turns
                # and repeated blocked requests without moving the neighbour.
                requests = [(i, -1) for i in range(1, 11)]
                requests += [(i, 20) for i in range(1, 11)]
                requests += [(i, 380) for i in range(1, 11)]
                requests += [(2, 400), (2, 400), (1, 390), (2, 390)]
                for index, target in requests:
                    statuses = []
                    for sim in sims:
                        saved = sim.snapshot()
                        statuses.append(sim.move(f'marker_{index}', to=target).status)
                        expected = sim.snapshot()
                        sim.restore(saved)
                        self.assertEqual(sim.move(f'marker_{index}', to=target).status, statuses[-1])
                        self.assertEqual(sim.snapshot(), expected)
                    self.assertEqual(*statuses)
                    compare()
