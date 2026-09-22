"""Measure each installed result station before sharing the tens contact law.

These source-backed pose instruments never seed an operating run. The default
selects the production fit; --trial retains its independent measured parts,
and --source selects the pre-adoption .15 mm baseline for preservation and
negative controls. Each keeps its source assembly, pivot, upper-stack placement
and carry stroke. All modes use the same native-equivalent refined bell mesh.
"""

import argparse
import json
import logging

from machinome.node import AssemblyNode
from machinome.motion.joints import Prismatic, Revolute
from machinome.parameters import Count
from machinome.simulation import Driver
from simulation.standard import channels, printed
from simulation.higher_lockout_trial import TrialContactBell, TrialTensLockout
from simulation.higher_lockout_parts import ContactTens
from simulation.result_bank_lockout_parts import contact_result_channel
from simulation.tools.higher_locking_envelope import contact_reader


STATIONS = (
    (channels.ResultTens, 'p_10220_410003_1_419227'),
    (channels.ResultHundreds, 'p_10220_410003_1_419086'),
    (channels.ResultDigit4, 'p_10220_410003_1_419234'),
    (channels.ResultDigit5, 'p_10220_410003_1_419093'),
    (channels.ResultDigit6, 'p_10220_410003_1_419064'),
    (channels.ResultDigit7, 'p_10220_410003_1_419039'),
    (channels.ResultDigit8, 'p_10220_410003_1_419074'),
    (channels.ResultDigit9, 'p_10220_410003_1_419139'),
    (channels.ResultDigit10, 'p_10220_410003_1_419117'),
    (channels.ResultDigit11, 'p_10220_410003_1_419114'),
)


def station_channel(station, trial=False, *, source=False):
    """Reuse a source-specific channel declaration in a bench or full trial."""
    if station not in range(2, 12):
        raise ValueError('Choose a higher result station 2..11')
    if source and trial:
        raise ValueError('Choose source or trial, not both')
    channel, upper_name = STATIONS[station-2]
    if trial:
        # A declared child replacement, not an edit of any source class.
        upper = getattr(printed, 'Part'+upper_name[2:])

        class TrialUpper(upper):
            # The factory's class name is shared, but its source solid is
            # not: each imported print contains its station's placement.
            # Include that source selection in the public artifact identity.
            source_station = Count(station, min=station, max=station)
            linear_deflection = .01
            angular_deflection = .1
            pentagonal_lockout = TrialTensLockout()

        class TrialChannel(channel):
            source_station = Count(station, min=station, max=station)
            locals()[upper_name] = TrialUpper(travel=Prismatic(axis=(0, 0, -1)))

        channel = TrialChannel
    elif not source:
        channel = ContactTens if station == 2 else contact_result_channel(station)
    return channel


def station_bench(station, trial=False, *, source=False):
    channel = station_channel(station, trial, source=source)

    class ResultStation(AssemblyNode):
        source_station = Count(station, min=station, max=station)
        trial_fit = Count(int(trial), min=int(trial), max=int(trial))
        source_fit = Count(int(source), min=int(source), max=int(source))
        shaft_angle = Driver(default=4-20*(station-1), unit='deg')
        crank_angle = Driver(default=0, unit='deg')
        carry_position = Driver(default=0, range=(0, 1))
        shaft = channel()
        bell = TrialContactBell(turn=Revolute(axis=(0, 0, 1)))
        shaft_angle.drives(shaft.turn)
        shaft_angle.drives(shaft.setting, ratio=0)
        carry_position.drives(shaft.carry)
        crank_angle.drives(bell.turn, ratio=-1)

    return ResultStation


def station_reader(station, carry, shaft, trial=False, *, source=False, world_precision=32):
    """Arguments/results use tens-local angles; placement stays source-owned."""
    shift = 20*(station-2)
    read = contact_reader(carry, reference=140+shift, shaft=shaft-shift,
                          node_type=station_bench(station, trial, source=source),
                          stack_path='Curta.shaft.'+STATIONS[station-2][1],
                          world_precision=world_precision)
    return lambda crank, kernel: read(crank+shift, kernel)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--station', type=int, choices=range(2, 12), action='append')
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument('--trial', action='store_true')
    selection.add_argument('--source', action='store_true')
    args = parser.parse_args()
    for station in args.station or range(2, 12):
        for carry in (0, 1):
            for flat in range(5):
                shaft = -16+72*flat
                read = station_reader(station, carry, shaft, args.trial, source=args.source)
                values = {kernel: read(180, kernel) for kernel in ('native', 'faceted')}
                print(json.dumps({'station': station, 'carry': carry, 'flat': flat,
                                  'trial': args.trial, 'source': args.source,
                                  'indexed_mm3': values}), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    main()
