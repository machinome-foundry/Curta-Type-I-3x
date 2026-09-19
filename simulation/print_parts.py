"""Author-supplied prints for unreliable STEP representations.

No mesh repair: these are the standard upstream print files, in the same local
frames. Exact tests deliberately use the faceted backend at these interfaces.
See docs/measurements.md for the source comparison and boolean findings.
"""

from simulation.colors import BLACK, ALUMINUM, STEEL
from pathlib import Path
from machinome.node import StlNode

PRINTS = Path(__file__).resolve().parents[1] / 'STLs'


class DigitsCover(StlNode):
    part = 'digits cover'
    stl_source = str(PRINTS / '42 - Digit Cover & Upper Housing/digits cover.stl')
    color = BLACK


class UpperHousing(StlNode):
    part = 'upper housing'
    stl_source = str(PRINTS / '42 - Digit Cover & Upper Housing/upper housing.stl')
    color = BLACK


class CrankCollar(StlNode):
    part = 'crank collar'
    stl_source = str(PRINTS / '43 - Clearing Cover & Collar/crank collar.stl')
    color = ALUMINUM


class CounterBodyStopPin(StlNode):
    """The source STEP gives contradictory native boolean/containment answers.

    Use the author's unchanged watertight print, not a repaired or redrawn pin.
    Exact-runner assertions involving it explicitly use the faceted backend.
    See tools/carriage_pin_fit.py and the operating completion record.
    """

    part = 'counter body stop pin'
    stl_source = str(PRINTS / '39 - Clearing Stop Pin & Digit Axles/carriage body stop pin.stl')
    color = STEEL
