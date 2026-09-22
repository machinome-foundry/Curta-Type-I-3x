"""Unadopted counter-tens restraint candidate; complete-print checks are owed.

The upper-disc chart is the independently measured counter-ones chart in the
tens frame. Coarse native/mesh comparison supports that registration, not a
continuous certificate. Lower-disc and carry-tooth curves come from separate
counter measurements and keep their own axial supports.
"""

from machinome.math import min, max, piecewise
from simulation.running_laws import phase
from simulation.counter_locking_laws import counter_contact_gap, CONTACT_STANDOFF
from simulation.higher_counter_locking_profiles import LOWER_LOCK_SECTORS, CARRY_TOOTH_STRIPS


# The exported lower-disc face is z=-8.399999618530272, outside its native
# -8.4 mm face. World64 checks found positive contact before travel=-.6.
# Refuse the lower sector 0.001 mm before that nominal axial support: a real
# clearance (the measured free-side probe), never a common-volume tolerance.
LOWER_LOCK_AXIAL_STANDOFF = .001


def higher_counter_contact_gap(crank, shaft, travel):
    shaft = phase(shaft-114)+114
    gap = min(counter_contact_gap(crank-20, shaft+20), .9-travel)
    crank = phase(crank-180)+180
    for start, end, points in LOWER_LOCK_SECTORS:
        opening = piecewise(shaft, [(p[0], p[1]) for p in points])
        closing = piecewise(shaft, [(p[0], p[2]) for p in points])
        contact = min(min(crank-closing+CONTACT_STANDOFF,
                          opening+360+CONTACT_STANDOFF-crank),
                      min(min(shaft-start, end-shaft),
                          travel+.6+LOWER_LOCK_AXIAL_STANDOFF))
        gap = max(gap, contact)
    for start, end, points in CARRY_TOOTH_STRIPS:
        entering = piecewise(shaft, [(p[0], p[1]) for p in points])
        leaving = piecewise(shaft, [(p[0], p[2]) for p in points])
        contact = min(min(crank-entering+CONTACT_STANDOFF,
                          leaving+CONTACT_STANDOFF-crank),
                      min(min(shaft-start, end-shaft), travel-.3))
        gap = max(gap, contact)
    return max(gap, -1)


def higher_counter_closing_limit(own, rotating_part, shaft, travel):
    return rotating_part+higher_counter_contact_gap(-rotating_part, shaft, travel)
