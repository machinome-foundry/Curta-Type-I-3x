"""Measure native higher-counter ingredient curves, not whole-print clearance.

These diagnostics separate the angular fields whose different axial supports
were measured with complete prints. A finite grid can miss narrow islands;
no profile or operating restraint is accepted by this measurement alone.
"""

import argparse
import json
import logging
import math

from simulation.tools.counter_lockout_probe import STATIONS, station_bench
from simulation.tools.higher_locking_envelope import pair_reader


CONTACT_PAIRS = {
    'upper_lock': ('turns_counter_locking_disc', 'pentagonal_lockout'),
    'lower_lock': ('tens_turns_counter_locking_disc', 'pentagonal_lockout'),
    'carry_tooth': ('turns_counter_carry_ring', 'transmission_gear_0_6'),
}


def component_envelope(station, carry, shaft, component, *, step=5, trial=False,
                       extra_angles=()):
    if station not in range(2, 7) or component not in CONTACT_PAIRS:
        raise ValueError('Choose a higher counter station 2..6 and a named component')
    if not all(math.isfinite(value) for value in (carry, shaft, step)):
        raise ValueError('Pose and sample spacing must be finite')
    if not 0 <= carry <= 1 or not 0 < step <= 10:
        raise ValueError('carry must be 0..1; step must be greater than 0 and at most 10')
    if any(not math.isfinite(angle) or not 0 <= angle <= 360 for angle in extra_angles):
        raise ValueError('Extra crank angles must be finite and within 0..360')
    node_type = station_bench(station, trial=trial)
    volume = pair_reader(carry, shaft, component, node_type,
                         stack_path=('shaft', STATIONS[station-1][1]),
                         contact_pairs=CONTACT_PAIRS)

    def read(angle):
        value = volume(angle)
        if not math.isfinite(value):
            raise ValueError(f'non-finite component common at crank {angle}')
        return value

    angles = sorted({0, 360, *extra_angles, *(step*i for i in range(int(360/step)+1))})
    samples = [(angle, read(angle)) for angle in angles]
    boundaries = []
    for (left, vl), (right, vr) in zip(samples, samples[1:]):
        if (vl > 0) == (vr > 0):
            continue
        enters = vr > 0
        for _ in range(20):
            middle = (left+right)/2
            vm = read(middle)
            if (vm > 0) == enters:
                right, vr = middle, vm
            else:
                left, vl = middle, vm
        boundaries.append({'left': left, 'right': right, 'enters_contact': enters,
                           'left_mm3': vl, 'right_mm3': vr})
    return {'station': station, 'carry': carry, 'shaft': shaft, 'trial': trial,
            'component': component, 'pair': list(CONTACT_PAIRS[component]),
            'kernel': 'native', 'step': step, 'extra_angles': sorted(set(extra_angles)),
            'samples': samples,
            'boundaries': boundaries}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--station', type=int, choices=range(2, 7), required=True)
    parser.add_argument('--shaft', type=float, action='append', required=True)
    parser.add_argument('--carry', type=float, required=True)
    parser.add_argument('--component', choices=CONTACT_PAIRS, action='append', required=True)
    parser.add_argument('--step', type=float, default=5)
    parser.add_argument('--sample-angle', type=float, action='append', default=[])
    parser.add_argument('--trial', action='store_true')
    args = parser.parse_args()
    for shaft in args.shaft:
        for component in args.component:
            print(json.dumps(component_envelope(args.station, args.carry, shaft, component,
                                                step=args.step, trial=args.trial,
                                                extra_angles=args.sample_angle)), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
