"""Upstream paint artwork on the measured rigid-part surfaces.

These mixins add no children, geometry or calculator state. Clocking is in the
source part's local frame, including the existing simulation's fitted zero.
See docs/markings.md for registration evidence and the deferred conical sheet.
"""

from math import degrees

from machinome.node.markings import Marking, Svg, Wrapped


class RegisterDigits:
    # Both source dial types have the same R9.45 band at z=.9..11.4.
    # Local -124 degrees faces world +Z at the calibrated register zero.
    digits = Marking(
        Svg('../Drawings/results_dial.svg'),
        Wrapped(axis=(0, 0, 1), radius=9.45, at=(0, 0, 11.4),
                start=-124, origin=(-3.2388, 0), zero=(1, 0, 0)),
        color='#111111',
    )


class InputDigits:
    # The source roll is upside down in the assembly. -Z makes the artwork
    # upright, and its descending 9..0 strip agrees with the +36-degree driver.
    digits = Marking(
        Svg('artwork/input-digits.svg'),
        Wrapped(axis=(0, 0, -1), radius=9.3, at=(0, 0, 15),
                start=175.6, origin=(55.5123, 0), zero=(1, 0, 0)),
        color='#FFFFFF',
    )


class InputPlaces:
    # The index band is on LowerHousing's upper collar, not on the taller
    # BottomHousing behind it. Undo the source part's 72-degree placement.
    input_places = Marking(
        Svg('artwork/input-places.svg'),
        Wrapped(axis=(0, 0, 1), radius=68.1625, at=(0, 0, 49.4),
                start=-72, origin=(190.27, 0), zero=(1, 0, 0)),
        color='#FFFFFF',
    )


class SleeveBranding:
    # The first arrow points to the units input; the other is ~130 degrees
    # away, at the turns counter. The logo is centered over the input bank.
    branding = Marking(
        Svg('artwork/sleeve-branding.svg'),
        Wrapped(axis=(0, 0, 1), radius=71.25, at=(0, 0, 14.41233),
                start=0, origin=(119.10667, 0), zero=(1, 0, 0)),
        color='#111111',
    )


class ReversingArrows:
    # A 10 mm circumferential offset keeps the arrows beside the reversing
    # knob instead of painting its bore. The exposed pad's center is 27 mm
    # above the source lever origin: world -55.2575, housing-local 95.1925.
    reversing_arrows = Marking(
        Svg('../Drawings/reversing_lever_arrows.svg'),
        Wrapped(axis=(0, 0, 1), radius=68.1, at=(0, 0, 95.1925),
                start=72 + degrees(10 / 68.1), zero=(1, 0, 0)),
        color='#FFFFFF',
    )
