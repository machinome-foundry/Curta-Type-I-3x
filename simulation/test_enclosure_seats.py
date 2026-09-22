"""The sleeve and base need matching seats, not a volume-tolerance waiver."""

from machinome.test import TestCase
import numpy as np
from simulation.enclosure_seats import EnclosureSeatBench


class EnclosureSeatTest(TestCase):
    node = EnclosureSeatBench

    def test_lower_housing_clears_the_seated_base_plate(self):
        self.assertNotIntersecting(self.node.lower_housing_1.lower_housing,
                                   self.node.base_plate)

    def test_upper_sleeve_clears_the_bottom_housing(self):
        self.assertNotIntersecting(self.node.upper_outer_sleeve,
                                   self.node.lower_housing_1.bottom_housing)

    def test_base_seat_has_small_locational_clearance_and_a_physical_stop(self):
        self.assertFreeWithin(self.node.base_plate, .02,
                              against=self.node.lower_housing_1.lower_housing,
                              along=(0, 0, 1))
        # The imported plate is upside down: local -Z approaches the seat.
        self.assertBlockedBeyond(self.node.base_plate, .1,
                                 against=self.node.lower_housing_1.lower_housing,
                                 along=(0, 0, -1), directions='forward')
        self.assertFreeWithin(self.node.base_plate, .1,
                              against=self.node.lower_housing_1.lower_housing,
                              along=(1, 0, 0))
        self.assertBlockedBeyond(self.node.base_plate, .3,
                                 against=self.node.lower_housing_1.lower_housing,
                                 along=(1, 0, 0))

    def test_sleeve_keeps_radial_capture(self):
        self.assertFreeWithin(self.node.lower_housing_1.bottom_housing, .1,
                              against=self.node.upper_outer_sleeve, along=(1, 0, 0))
        self.assertBlockedBeyond(self.node.lower_housing_1.bottom_housing, .6,
                                 against=self.node.upper_outer_sleeve, along=(1, 0, 0))

    def test_lower_group_is_recentered_without_moving_upper_fittings(self):
        from simulation.assemblies import Enclosure
        from simulation.decimal_markers import LowerMovableMarkers
        source = Enclosure()
        source.assemble()
        source.build_stls()
        # The later bounded lower-frame fit changes this one print's mesh,
        # not its datum. Its independent source-removal proof lives in
        # test_lower_frame_seat; compare placement with that fitted local print.
        from simulation.lower_frame_parts import SeatedLowerHousing
        fitted_lower = SeatedLowerHousing()
        fitted_lower.assemble()
        fitted_lower.build_stls()
        for path in ('lower_housing_1.lower_housing', 'lower_housing_1.bottom_housing',
                     'base_plate', 'm4x10_419010_6', 'm5x30_countersunk_1',
                     'm5x30_countersunk_2', 'upper_outer_sleeve', 'cover_ring',
                     'm3x10_pan_1', 'm3x10_countersink_screw_1'):
            first, second = source, self.node
            for name in path.split('.'):
                first, second = getattr(first, name), getattr(second, name)
            if path == 'lower_housing_1.bottom_housing':
                first = fitted_lower.bottom_housing
            lower = path.startswith(('lower_housing_1', 'base_plate', 'm4x10', 'm5x30'))
            z = -.05 if path.startswith(('base_plate', 'm5x30')) else 0
            delta = (.406900356, -.745841949, z) if lower else (0, 0, 0)
            np.testing.assert_allclose(second.mesh.vertices, first.mesh.vertices + delta,
                                       rtol=0, atol=.00001, err_msg=path)
        markers = LowerMovableMarkers()
        markers.assemble()
        markers.build_stls()
        for index in range(1, 6):
            first = getattr(markers, f'decimal_marker_{index}')
            second = getattr(self.node.decimal_markers, f'decimal_marker_{index}')
            for name in ('position_marker', 'p_3mm_ball', 'decimal_marker_spring'):
                np.testing.assert_allclose(getattr(second, name).mesh.vertices,
                    getattr(first, name).mesh.vertices + (.406900356, -.745841949, 0),
                    rtol=0, atol=.00001, err_msg=f'marker {index} {name}')
