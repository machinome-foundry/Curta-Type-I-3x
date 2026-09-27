"""Source marker, ball and spring travel together around their circular track."""

from machinome.node import AssemblyNode, Frame
from machinome.motion.joints import Bound, Revolute
from machinome.simulation import Driver
from machinome.parameters import Length
from math import hypot
from simulation.standard import assembly as source
from simulation.clearing import ClearingGrooveCover

# Clockwise free travel to the next source marker, including the last-to-first
# interval across the back of the track. Native contact discovery is rounded
# down to .001 degree. The coarse source mesh overstates the gap by ~.02 deg.
LOWER_CENTER = (-.406900356, .745841949, 0)
UPPER_SOURCE_CENTER = (.386511579, -.028412332, 0)
LOWER_GAPS = (.076, .226, .149, .149, 328.808)
UPPER_GAPS = (.139, .316, .346, .286, 318.039)

# Source position-marker origins; all five in each bank lie on the measured
# track circle. Kept independently of mesh extrema and its tessellation.
DATUMS = ((62.963296296, -35.43893629), (58.68878941, -42.065598708),
          (53.59584881, -48.333920505), (47.914989084, -53.936102063),
          (41.65698207, -58.884266178), (53.397106005, -13.059025462),
          (50.955964028, -20.586877231), (47.366368705, -27.827927155),
          (42.728727038, -34.482102846), (37.198287488, -40.337383472))


def radial_direction(index):
    center = LOWER_CENTER if index < 6 else UPPER_SOURCE_CENTER
    x, y = (a - b for a, b in zip(DATUMS[index - 1], center))
    radius = hypot(x, y)
    return x / radius, y / radius, 0


def marker(part, previous=None, gap=0, first=None, closing_gap=0, center=LOWER_CENTER):
    # Each adjacent contact is stated once. A Bound is checked along the
    # whole run path: moving either of its two participants into the other
    # stops the pushing input, even when the bounded participant is held.
    upper = None if previous is None else Bound(
        lambda own, neighbour: neighbour + gap, reads=(previous,))
    lower = None if first is None else Bound(
        lambda own, neighbour: neighbour - closing_gap, reads=(first,))
    return part(turn=Revolute(axis=(0, 0, 1), at=center, range=(lower, upper)))


class MountedMarker1(source.DecimalMarker1):
    track = Frame(at=LOWER_CENTER)


class MountedMarker2(source.DecimalMarker2):
    track = Frame(at=LOWER_CENTER)


class MountedMarker3(source.DecimalMarker3):
    track = Frame(at=LOWER_CENTER)


class MountedMarker4(source.DecimalMarker4):
    track = Frame(at=LOWER_CENTER)


class MountedMarker5(source.DecimalMarker5):
    track = Frame(at=LOWER_CENTER)


class MountedMarker6(source.DecimalMarker6):
    track = Frame(at=UPPER_SOURCE_CENTER)


class MountedMarker7(source.DecimalMarker7):
    track = Frame(at=UPPER_SOURCE_CENTER)


class MountedMarker8(source.DecimalMarker8):
    track = Frame(at=UPPER_SOURCE_CENTER)


class MountedMarker9(source.DecimalMarker9):
    track = Frame(at=UPPER_SOURCE_CENTER)


class MountedMarker10(source.DecimalMarker10):
    track = Frame(at=UPPER_SOURCE_CENTER)


def track_seat(index, center):
    """The measured radial seating, evaluated with the bank's parameter."""
    direction = radial_direction(index)
    return Frame(at=lambda bank: tuple(origin + bank.radial_seat * radial
                                       for origin, radial in zip(center, direction)))


class LowerTrackPlacement(AssemblyNode):
    radial_seat = Length(.06, min=0)

    def render(self):
        for index in range(1, 6):
            getattr(self, f'decimal_marker_{index}').translate(
                tuple(self.radial_seat * value for value in radial_direction(index)))


class LowerMovableMarkers(AssemblyNode):
    radial_seat = Length(.06, min=0)
    marker_1_seat = track_seat(1, LOWER_CENTER)
    marker_2_seat = track_seat(2, LOWER_CENTER)
    marker_3_seat = track_seat(3, LOWER_CENTER)
    marker_4_seat = track_seat(4, LOWER_CENTER)
    marker_5_seat = track_seat(5, LOWER_CENTER)
    decimal_marker_1 = marker(MountedMarker1)
    decimal_marker_2 = marker(MountedMarker2, decimal_marker_1.turn, LOWER_GAPS[0])
    decimal_marker_3 = marker(MountedMarker3, decimal_marker_2.turn, LOWER_GAPS[1])
    decimal_marker_4 = marker(MountedMarker4, decimal_marker_3.turn, LOWER_GAPS[2])
    decimal_marker_5 = marker(MountedMarker5, decimal_marker_4.turn, LOWER_GAPS[3],
                              decimal_marker_1.turn, LOWER_GAPS[4])
    marker_1_mount = decimal_marker_1.track.on(marker_1_seat, decimal_marker_1.turn)
    marker_2_mount = decimal_marker_2.track.on(marker_2_seat, decimal_marker_2.turn)
    marker_3_mount = decimal_marker_3.track.on(marker_3_seat, decimal_marker_3.turn)
    marker_4_mount = decimal_marker_4.track.on(marker_4_seat, decimal_marker_4.turn)
    marker_5_mount = decimal_marker_5.track.on(marker_5_seat, decimal_marker_5.turn)


class UpperTrackPlacement(AssemblyNode):
    radial_seat = Length(.06, min=0)

    def render(self):
        # The working clearing cover is centred on the shaft, just like the
        # already recentered carriage covers. Preserve each source marker's
        # position on its own track while bringing that track to the same axis.
        for index in range(6, 11):
            getattr(self, f'decimal_marker_{index}').translate(
                tuple(self.radial_seat * direction - center for direction, center
                      in zip(radial_direction(index), UPPER_SOURCE_CENTER)))


class UpperMovableMarkers(AssemblyNode):
    radial_seat = Length(.06, min=0)
    # The working upper track is recentered on the shaft; the source children
    # keep their original track datum and internal placements.
    marker_6_seat = track_seat(6, (0, 0, 0))
    marker_7_seat = track_seat(7, (0, 0, 0))
    marker_8_seat = track_seat(8, (0, 0, 0))
    marker_9_seat = track_seat(9, (0, 0, 0))
    marker_10_seat = track_seat(10, (0, 0, 0))
    decimal_marker_6 = marker(MountedMarker6, center=(0, 0, 0))
    decimal_marker_7 = marker(MountedMarker7, decimal_marker_6.turn, UPPER_GAPS[0], center=(0, 0, 0))
    decimal_marker_8 = marker(MountedMarker8, decimal_marker_7.turn, UPPER_GAPS[1], center=(0, 0, 0))
    decimal_marker_9 = marker(MountedMarker9, decimal_marker_8.turn, UPPER_GAPS[2], center=(0, 0, 0))
    decimal_marker_10 = marker(MountedMarker10, decimal_marker_9.turn, UPPER_GAPS[3],
                               decimal_marker_6.turn, UPPER_GAPS[4], center=(0, 0, 0))
    marker_6_mount = decimal_marker_6.track.on(marker_6_seat, decimal_marker_6.turn)
    marker_7_mount = decimal_marker_7.track.on(marker_7_seat, decimal_marker_7.turn)
    marker_8_mount = decimal_marker_8.track.on(marker_8_seat, decimal_marker_8.turn)
    marker_9_mount = decimal_marker_9.track.on(marker_9_seat, decimal_marker_9.turn)
    marker_10_mount = decimal_marker_10.track.on(marker_10_seat, decimal_marker_10.turn)


class LowerGeometryMarkers(LowerTrackPlacement):
    decimal_marker_1 = marker(source.DecimalMarker1)
    decimal_marker_2 = marker(source.DecimalMarker2)
    decimal_marker_3 = marker(source.DecimalMarker3)
    decimal_marker_4 = marker(source.DecimalMarker4)
    decimal_marker_5 = marker(source.DecimalMarker5)


class UpperGeometryMarkers(UpperTrackPlacement):
    decimal_marker_6 = marker(source.DecimalMarker6, center=(0, 0, 0))
    decimal_marker_7 = marker(source.DecimalMarker7, center=(0, 0, 0))
    decimal_marker_8 = marker(source.DecimalMarker8, center=(0, 0, 0))
    decimal_marker_9 = marker(source.DecimalMarker9, center=(0, 0, 0))
    decimal_marker_10 = marker(source.DecimalMarker10, center=(0, 0, 0))


class MarkerBench(AssemblyNode):
    marker_1 = Driver(default=0, unit='deg')
    marker_2 = Driver(default=0, unit='deg')
    marker_3 = Driver(default=0, unit='deg')
    marker_4 = Driver(default=0, unit='deg')
    marker_5 = Driver(default=0, unit='deg')
    marker_6 = Driver(default=0, unit='deg')
    marker_7 = Driver(default=0, unit='deg')
    marker_8 = Driver(default=0, unit='deg')
    marker_9 = Driver(default=0, unit='deg')
    marker_10 = Driver(default=0, unit='deg')
    lower = LowerMovableMarkers()
    upper = UpperMovableMarkers()
    for _i, _driver in enumerate((marker_1, marker_2, marker_3, marker_4, marker_5,
                                  marker_6, marker_7, marker_8, marker_9, marker_10), 1):
        _driver.drives(getattr(lower if _i < 6 else upper, f'decimal_marker_{_i}').turn)
        del _driver
    del _i


class MarkerGeometryBench(MarkerBench):
    """Same source parts and axes, without stops, to probe beyond contact."""
    radial_seat = Length(.06, min=0)
    lower = LowerGeometryMarkers(radial_seat=radial_seat)
    upper = UpperGeometryMarkers(radial_seat=radial_seat)
    lower_housing = source.LowerHousing1()
    upper_track = ClearingGrooveCover()

    def render(self):
        self.upper_track.rotate(180, (.797150916, -.603780106, 0))
        self.upper_track.translate((0, 0, 57.1))
