"""Installed six-input angular covers select ordinary absolute axial limits.

The model data covers complete native prints and their published meshes.
No CAD executes inside these laws. Contact remains pointwise: the framework's
ordinary Bound sampling decides a requested path, not a swept-solid solver.
"""

from machinome.math import cos, sin, min as math_min, max as math_max
from machinome.simulation.profile import ConvexProfile, profile_overlap
from simulation.reverser_profile_data import DATA


PROFILES = tuple(ConvexProfile([[row['points'][i] for i in polygon]
                              for polygon in row['polygons']])
                 for row in DATA['profiles'])
GEARS = tuple((PROFILES[row['profile']], tuple(row['axis']), row['reference'],
               row['height'], tuple(map(tuple, row['bands']))) for row in DATA['gears'])
DRUMS = tuple((PROFILES[row['profile']], row['low'], row['high']) for row in DATA['drums'])
LOW, HIGH = DATA['range']


def limit(upper, own, crank, shafts, lift):
    value = HIGH if upper else LOW
    for (gear, (x, y), reference, height, bands), shaft in zip(GEARS, shafts):
        delta = shaft-reference
        # Profiles are in their proved initial world XY frame. Preserve the
        # same rotate-then-translate order used by the independent trial.
        translation = (x-cos(delta)*x+sin(delta)*y,
                       y-sin(delta)*x-cos(delta)*y)
        for drum, dlo, dhi in DRUMS:
            active = profile_overlap(gear, drum, delta, crank, left_xy=translation)
            for glo, ghi in bands:
                low, high = dlo-ghi+height+lift, dhi-glo+height+lift
                chosen = active*(own < (low+high)/2 if upper else own >= (low+high)/2)
                if upper:
                    value = math_min(value, chosen*low+(1-chosen)*HIGH)
                else:
                    value = math_max(value, chosen*high+(1-chosen)*LOW)
    return value


def lower_limit(own, crank, ones, tens, hundreds, fourth, fifth, sixth, lift):
    return limit(False, own, crank, (ones, tens, hundreds, fourth, fifth, sixth), lift)


def upper_limit(own, crank, ones, tens, hundreds, fourth, fifth, sixth, lift):
    return limit(True, own, crank, (ones, tens, hundreds, fourth, fifth, sixth), lift)
