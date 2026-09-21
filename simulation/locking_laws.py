"""Measured ones bell/lockout relationships shared by bench and operating root.

The ones stack has fixed axial seating. These profiles do not certify the
other channels' sliding carry stacks. No source print geometry is changed.
"""

from machinome.math import min, max, piecewise, floor
from simulation.running_laws import phase
from simulation.locking_profiles import SECTORS

# Free-side angular stand-off certified against native solids and published
# meshes at profile boundaries and the seven retained first-contact poses.
CONTACT_STANDOFF = .1


def contact_gap(crank, shaft):
    """Positive only inside the measured forbidden angle region."""
    # Put the cyclic cut in the common open window, not the closed land.
    crank = phase(crank-90)+90
    shaft = phase(shaft-4)+4
    gaps = []
    for start, end, points in SECTORS:
        opening = piecewise(shaft, [(p[0], p[1]) for p in points])
        closing = piecewise(shaft, [(p[0], p[2]) for p in points])
        gap = min(crank-closing+CONTACT_STANDOFF,
                  opening+360+CONTACT_STANDOFF-crank)
        gaps.append(min(gap, min(shaft-start, end-shaft)))
    gap = gaps[0]
    for other in gaps[1:]:
        gap = max(gap, other)
    return gap


def closing_limit(own, rotating_part, shaft):
    """Next closing surface, reading the actual co-rotating bell and shaft."""
    shaft = phase(shaft-4)+4
    angle = -rotating_part
    free = rotating_part-1
    limit = free
    for start, end, points in SECTORS:
        opening = piecewise(shaft, [(p[0], p[1]) for p in points])+CONTACT_STANDOFF
        closing = piecewise(shaft, [(p[0], p[2]) for p in points])-CONTACT_STANDOFF
        cycle = floor((angle-opening)/360)
        active = (shaft >= start)*(shaft <= end)
        limit += active*(-360*cycle-closing-free)
    # Inactive slack follows a real co-rotating joint; it is not a travel cap.
    return limit
