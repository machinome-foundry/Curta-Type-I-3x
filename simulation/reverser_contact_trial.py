"""Local 90-degree admission experiment, NEVER the production model.

The full angular profile is still being measured. This experiment asks whether
the existing Bound mechanism can express a retained-phase-dependent axial
contact and stop at the first band even when a later endpoint is clear.
Only the separately measured crank-90 fixture is constrained; all other
crank poses deliberately fall through and are NOT certified by this trial.
The temporary 72-degree phase chart is checked only by the two retained
histories in its tests, not asserted as exact five-sector source symmetry.
No print, joint axis, driver or retained shaft law is changed.
"""

from machinome.math import floor, min, max
from machinome.motion.joints import Bound
from simulation.reverser_modes import PINION_STARTS, THICKNESS
# Keep this intentionally local diagnostic independent of the adopted full
# angular restraint and its additional ones-pinion fit.
from simulation.running import RadialBallOperatingCurta as OperatingCurta


# Explicit free-side admission stand-off, not an accepted overlap volume.
AXIAL_STANDOFF = .01
LOWER_FREE_PHASE = 152.3
UPPER_FREE_PHASE = 174.0


def active_contact(crank, shaft, lift):
    # Exact fixture gating is intentional. This is not the completed angular
    # envelope; do not broaden this window or adopt this class on that basis.
    active = (crank >= -90)*(crank <= -90)*(lift >= 0)*(lift <= 0)
    phase = shaft-72*floor((shaft-134)/72)
    angular_contact = max(LOWER_FREE_PHASE-phase, phase-UPPER_FREE_PHASE)
    return active*(angular_contact > 0)


def contact_windows(lift):
    """Axial forbidden bands expanded by the named free-side stand-off."""
    row_bottom = -49.7+lift
    return tuple((row_bottom-start-.0925-THICKNESS-AXIAL_STANDOFF,
                  row_bottom+THICKNESS-start-.0925+AXIAL_STANDOFF)
                 for start in PINION_STARTS)


def local_lower_limit(own, crank, shaft, lift):
    active = active_contact(crank, shaft, lift)
    limit = -6.9425
    for low, high in contact_windows(lift):
        # Bound's own argument is the held coordinate, not a moving query.
        # Absolute planes on that held position's side stop the first band.
        chosen = active*(own >= (low+high)/2)
        limit = max(limit, chosen*high+(1-chosen)*-6.9425)
    return limit


def local_upper_limit(own, crank, shaft, lift):
    active = active_contact(crank, shaft, lift)
    limit = 3.9075
    for low, high in contact_windows(lift):
        chosen = active*(own < (low+high)/2)
        limit = min(limit, chosen*low+(1-chosen)*3.9075)
    return limit


class LocalReverserContactTrial(OperatingCurta):
    OperatingCurta.main_drive.reversing_lever.reversing_lever_1.reversing_lever_knob_1.lift.constrain(
        range=(Bound(local_lower_limit, reads=(
            OperatingCurta.main_drive.crank.turn,
            OperatingCurta.transmission.turns.ones.turn,
            OperatingCurta.main_drive.crank.lift)),
               Bound(local_upper_limit, reads=(
            OperatingCurta.main_drive.crank.turn,
            OperatingCurta.transmission.turns.ones.turn,
            OperatingCurta.main_drive.crank.lift))))
