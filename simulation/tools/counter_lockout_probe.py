"""Measure counter locking prints in their own installed source frames.

This pose instrument uses actual shaft and crank angles, not result-side
phase normalization. It adopts no production fit or restraint. Higher counter
carry travel is -1.8..2.4 mm; the fixed ones lockout does not share that travel.
The refined bell is native-equivalent to production; upper prints are the
existing source-backed fits by default. --trial measures a separately bounded
T08 .15 -> .16 mm outer skin with refined upper meshes, not an operating fit.
"""

import argparse
import json
import logging

from machinome.node import AssemblyNode
from machinome.motion.joints import Prismatic, Revolute
from machinome.parameters import Count, Length
from machinome.simulation import Driver
from simulation.reverser_inputs import (
    ReversingOnes, ReversingTens, ReversingHundreds,
    ReversingFourth, ReversingFifth, ReversingSixth,
)
from simulation.higher_lockout_trial import TrialContactBell
from simulation.fit import FittedCarryLockout
from simulation.counter_lockout_parts import ContactCounterOnes
from simulation.standard import printed
from simulation.tools.higher_locking_envelope import contact_reader


SOURCE_STATIONS = (
    (ReversingOnes, 'p_10222_1'),
    (ReversingTens, 'p_10220_410003_1_419081'),
    (ReversingHundreds, 'p_10220_410003_1_419070'),
    (ReversingFourth, 'p_10220_410003_1_419181'),
    (ReversingFifth, 'p_10220_410003_1_419107'),
    (ReversingSixth, 'p_10220_410003_1_419238'),
)
# Ones has adopted T08; the remaining defaults retain their earlier fits.
# Keep an explicit source baseline for removal tests instead of comparing
# an adopted production print with an identical candidate.
STATIONS = ((ContactCounterOnes, 'p_10222_1'), *SOURCE_STATIONS[1:])


class TrialCounterLockout(FittedCarryLockout):
    flank_relief = Length(.16, min=0)


def station_bench(station, trial=False, *, source=False):
    if station not in range(1, 7):
        raise ValueError('Counter station must be 1..6')
    if source and trial:
        raise ValueError('Choose the source baseline or the trial, not both')
    channel, upper_name = (SOURCE_STATIONS if source else STATIONS)[station-1]
    if trial:
        upper = getattr(printed, 'Part'+upper_name[2:])

        class TrialUpper(upper):
            source_station = Count(station, min=station, max=station)
            linear_deflection = .01
            angular_deflection = .1
            pentagonal_lockout = TrialCounterLockout()

        class TrialChannel(channel):
            source_station = Count(station, min=station, max=station)
            locals()[upper_name] = TrialUpper(travel=Prismatic(axis=(0, 0, -1)))

        channel = TrialChannel

    class CounterStation(AssemblyNode):
        source_station = Count(station, min=station, max=station)
        source_fit = Count(int(source), min=int(source), max=int(source))
        trial_fit = Count(int(trial), min=int(trial), max=int(trial))
        shaft_angle = Driver(default=134-20*(station-1), unit='deg')
        crank_angle = Driver(default=0, unit='deg')
        carry_position = Driver(default=0, range=(0, 1))
        shaft = channel()
        bell = TrialContactBell(turn=Revolute(axis=(0, 0, 1)))
        shaft_angle.drives(shaft.turn)
        # Lower input position cannot change the upper lockout's datum.
        # Retain the operating root's normal -4 mm input position as well.
        shaft_angle.drives(shaft.setting, ratio=0, offset=-4/6)
        carry_position.drives(shaft.carry)
        crank_angle.drives(bell.turn, ratio=-1)

    return CounterStation


def station_reader(station, carry, shaft, reference=0, trial=False, *, world_precision=32):
    return contact_reader(
        carry, reference=reference, shaft=shaft, node_type=station_bench(station, trial),
        stack_path='Curta.shaft.'+STATIONS[station-1][1], world_precision=world_precision)


CounterOnesLockoutBench = station_bench(1)
CounterTensLockoutBench = station_bench(2)
CounterOnesLockoutTrial = station_bench(1, trial=True)
CounterTensLockoutTrial = station_bench(2, trial=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--station', type=int, choices=range(1, 7), action='append')
    parser.add_argument('--carry', type=float, choices=(0, .5, 1), action='append')
    parser.add_argument('--crank', type=float, action='append')
    parser.add_argument('--trial', action='store_true')
    args = parser.parse_args()
    for station in args.station or range(1, 7):
        for carry in args.carry or (0, 1):
            for flat in range(5):
                shaft = 134-20*(station-1)+72*flat
                read = station_reader(station, carry, shaft, trial=args.trial)
                for crank in args.crank or (0, 180):
                    values = {kernel: read(crank, kernel)
                              for kernel in ('native', 'faceted')}
                    print(json.dumps({'station': station, 'carry': carry,
                                      'flat': flat, 'shaft': shaft, 'crank': crank,
                                      'trial': args.trial,
                                      'common_mm3': values}), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
