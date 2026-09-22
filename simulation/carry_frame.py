"""Installed result-carry stations against the operating upper frame.

This independently driven bench preserves the source placements. The complete
Curta remains the neighbour-sweep fixture; this bench isolates the frame proof.
"""

from machinome.node import AssemblyNode
from machinome.simulation import Driver
from simulation.mechanism import UpperFrame
from simulation.standard.carry import ResultsLever1, ResultsLever2


class CarryFrameBench(AssemblyNode):
    drop_mm = Driver(default=0, range=(0, 4.2), unit='mm')
    frame = UpperFrame()
    first = ResultsLever1()
    second = ResultsLever2()
    drop_mm.drives(first.engage, ratio=1/4.2)
    drop_mm.drives(second.engage, ratio=1/4.2)
