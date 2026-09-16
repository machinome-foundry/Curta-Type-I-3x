"""Native neighbour contacts independently check the measured track stops."""

from solid_node.test import TestCase
import numpy as np
from simulation.decimal_markers import MarkerGeometryBench, LOWER_GAPS, UPPER_GAPS


class MarkerGeometryTest(TestCase):
    node = MarkerGeometryBench

    def test_tracks_capture_the_marker_radially_on_both_sides(self):
        for seat in (0, .5):
            probe = MarkerGeometryBench(radial_seat=seat)
            probe.set_state(**{f'marker_{i}': 0 for i in range(1, 11)})
            probe.assemble()
            probe.build_stls()
            try:
                self.assertIntersecting(probe.lower.decimal_marker_1.position_marker,
                                        probe.lower_housing.lower_housing)
                self.assertIntersecting(probe.upper.decimal_marker_6.position_marker,
                                        probe.upper_track)
            except AssertionError as error:
                error.add_note(f'radial seat={seat} mm')
                raise

    def test_marker_bodies_clear_their_tracks_through_a_full_turn(self):
        for bank_name, index, tracks in (
                ('lower', 1, (self.node.lower_housing.lower_housing,
                              self.node.lower_housing.bottom_housing)),
                ('upper', 6, (self.node.upper_track,))):
            marker = getattr(getattr(self.node, bank_name), f'decimal_marker_{index}')
            for angle in range(0, 361, 5):
                self.node.set_state(**{f'marker_{index}': angle})
                for track in tracks:
                    try:
                        self.assertNotIntersecting(marker.position_marker, track)
                    except AssertionError as error:
                        error.add_note(f'bank={bank_name}; marker={index}; angle={angle} deg')
                        raise

    def test_body_ball_and_spring_keep_the_same_track_radius(self):
        from simulation.decimal_markers import LOWER_CENTER
        for bank_name, index, center in (('lower', 1, LOWER_CENTER), ('upper', 6, (0, 0, 0))):
            marker = getattr(getattr(self.node, bank_name), f'decimal_marker_{index}')
            self.node.set_state(**{f'marker_{index}': 0})
            pieces = (marker.position_marker, marker.p_3mm_ball, marker.decimal_marker_spring)
            reference = [np.linalg.norm(part.mesh.vertices[:, :2] - center[:2], axis=1)
                         for part in pieces]
            self.node.set_state(**{f'marker_{index}': 90})
            for part, expected in zip(pieces, reference):
                actual = np.linalg.norm(part.mesh.vertices[:, :2] - center[:2], axis=1)
                self.assertLess(np.max(np.abs(actual - expected)), 1e-7)

    def test_each_neighbour_stop_is_clear_but_further_travel_meets_material(self):
        for bank_name, first, gaps in (('lower', 1, LOWER_GAPS), ('upper', 6, UPPER_GAPS)):
            for offset, gap in enumerate(gaps):
                index = first + offset
                pose = {f'marker_{i}': 0 for i in range(1, 11)}
                pose[f'marker_{index}'] = -gap
                self.node.set_state(**pose)
                bank = getattr(self.node, bank_name)
                marker = getattr(bank, f'decimal_marker_{index}')
                neighbour = getattr(bank, f'decimal_marker_{first + (offset + 1) % 5}')
                for a in (marker.position_marker, marker.p_3mm_ball, marker.decimal_marker_spring):
                    for b in (neighbour.position_marker, neighbour.p_3mm_ball,
                              neighbour.decimal_marker_spring):
                        self.assertNotIntersecting(a, b)
                pose[f'marker_{index}'] = -gap + .001
                self.node.set_state(**pose)
                self.assertNotIntersecting(marker.position_marker, neighbour.position_marker)
                pose[f'marker_{index}'] = -gap - .05
                self.node.set_state(**pose)
                self.assertIntersecting(marker.position_marker, neighbour.position_marker)
