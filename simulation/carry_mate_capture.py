"""Existing full-bank capture contracts on the actual mated carry stations."""

from machinome.node import AssemblyNode
from machinome.simulation import Driver
from simulation.running_parts import (
    RetainedResultCarries, RetainedTurnsCarries, RESULT_RESTS, TURNS_RESTS,
)
from simulation.counter_shoulder_running_parts import ShoulderRetainedTurnsCarries


class CarryMateCaptureBench(AssemblyNode):
    drop_mm = Driver(default=0, range=(0, 4.2), unit='mm')
    result_carries = RetainedResultCarries()
    turns_carries = ShoulderRetainedTurnsCarries()
    for _index, _rest in enumerate(RESULT_RESTS, 1):
        drop_mm.drives(getattr(result_carries, f'results_tens_lever_assembly_{_index}')
                       .tens_slider_for_results.travel, offset=_rest)
    for _index, _rest in enumerate(TURNS_RESTS, 1):
        drop_mm.drives(getattr(turns_carries, f'turns_tens_lever_assembly_{_index}')
                       .tens_slider_for_turns_counter.travel, offset=_rest)
    del _index, _rest
