"""A full installed-profile Bound experiment, never the production default.

Consumes the pinned complete-print coverage record. No CAD is evaluated by
the law, no angle sector is copied and no physical input is repositioned.
Retained requests and browser parity remain acceptance gates for adoption.
"""

from collections import defaultdict
import hashlib
import json


EVIDENCE_SHA256 = 'd41e1b46ee7f4c92b61d2ddae586f01242574213942d7dd93f0e9c4aefad01a3'
LOW, HIGH = -6.9425, 3.9075


def make_limits(evidence, *, evidence_sha256=EVIDENCE_SHA256):
    from machinome.math import cos, sin, min as math_min, max as math_max
    from machinome.simulation.profile import ConvexProfile, profile_overlap
    from simulation.tools.reverser_profile_cover import axial_allowance

    raw = evidence.read_bytes()
    if hashlib.sha256(raw).hexdigest() != evidence_sha256:
        raise ValueError('Installed-profile trial requires its complete pinned evidence')
    rows = [json.loads(line) for line in raw.splitlines()]
    profiles = [r for r in rows if r['kind'] == 'installed_profile']
    verdicts = [r for r in rows if r['kind'] == 'installed_mesh_verdict']
    if len(verdicts) != 8 or not all(r['separated'] for r in verdicts):
        raise ValueError('Incomplete installed-print coverage verdicts')

    # Complete lower-drum profiles were checked, not guessed away. Their
    # highest possible covered tooth remains below the lowest input cover.
    inputs = [r for r in profiles if '.transmission.turns.' in r['path']]
    lower_drum = [r for r in profiles if r['path'].endswith('drum_bottom_1')]
    lowest_input = min(r['source_height'][0]-axial_allowance(r)
                       + LOW-r['reference_reverser_height'] for r in inputs)
    highest_lower = max(r['source_height'][1]+axial_allowance(r)+9 for r in lower_drum)
    if not lowest_input > highest_lower:
        raise ValueError('Lower drum cannot be axially excluded')

    groups = defaultdict(list)
    for row in profiles:
        if row['path'].endswith('drum_top_1'):
            groups[tuple(row['source_height'])].append(row)
    drums = []
    for (low, high), members in groups.items():
        loops = [[r['points'][i] for i in loop]
                 for r in members for loop in r['polygons']]
        allowance = max(axial_allowance(r) for r in members)
        drums.append((ConvexProfile(loops), low-allowance, high+allowance))

    gears = []
    for name in ('ones', 'tens', 'hundreds', 'digit_4', 'digit_5', 'digit_6'):
        bands = [r for r in inputs if f'.turns.{name}.' in r['path']]
        first = bands[0]
        if any(r['points'] != first['points'] or r['polygons'] != first['polygons']
               for r in bands):
            raise ValueError(f'Input bands do not share an XY profile: {name}')
        profile = ConvexProfile([[first['points'][i] for i in loop]
                                 for loop in first['polygons']])
        heights = [(r['source_height'][0]-axial_allowance(r),
                    r['source_height'][1]+axial_allowance(r)) for r in bands]
        gears.append((profile, first['axis'][:2], first['reference_shaft_angle'],
                      first['reference_reverser_height'], heights))

    def limit(upper, own, crank, shafts, lift):
        value = HIGH if upper else LOW
        for (gear, (x, y), reference, height, bands), shaft in zip(gears, shafts):
            delta = shaft-reference
            translation = (x-cos(delta)*x+sin(delta)*y,
                           y-sin(delta)*x-cos(delta)*y)
            for drum, dlo, dhi in drums:
                active = profile_overlap(gear, drum, delta, crank, left_xy=translation)
                for glo, ghi in bands:
                    low, high = dlo-ghi+height+lift, dhi-glo+height+lift
                    chosen = active*(own < (low+high)/2 if upper else own >= (low+high)/2)
                    if upper:
                        value = math_min(value, chosen*low+(1-chosen)*HIGH)
                    else:
                        value = math_max(value, chosen*high+(1-chosen)*LOW)
        return value

    def lower(own, crank, ones, tens, hundreds, fourth, fifth, sixth, lift):
        return limit(False, own, crank, (ones, tens, hundreds, fourth, fifth, sixth), lift)

    def upper(own, crank, ones, tens, hundreds, fourth, fifth, sixth, lift):
        return limit(True, own, crank, (ones, tens, hundreds, fourth, fifth, sixth), lift)

    return lower, upper


def make_trial(evidence, *, evidence_sha256=EVIDENCE_SHA256, model=None):
    from machinome.motion.joints import Bound
    from simulation.running import OperatingCurta

    model = OperatingCurta if model is None else model
    lower, upper = make_limits(evidence, evidence_sha256=evidence_sha256)
    reads = (model.main_drive.crank.turn,
             model.transmission.turns.ones.turn,
             model.transmission.turns.tens.turn,
             model.transmission.turns.hundreds.turn,
             model.transmission.turns.digit_4.turn,
             model.transmission.turns.digit_5.turn,
             model.transmission.turns.digit_6.turn,
             model.main_drive.crank.lift)

    class InstalledReverserProfileTrial(model):
        model.main_drive.reversing_lever.reversing_lever_1.reversing_lever_knob_1.lift.constrain(
            range=(Bound(lower, reads=reads), Bound(upper, reads=reads)))

    return InstalledReverserProfileTrial
