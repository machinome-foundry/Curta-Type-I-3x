"""Independent selected-input fit bench; the complete Curta is the neighbour fixture.

This begins with the unchanged operating source parts. Its fractional setting
never re-evaluates the complete root's calculator operand or carry law.
"""

from solid_node.node import AssemblyNode
from solid_node.simulation import Driver
from simulation.selectors import Selector1
from simulation.standard.assembly import LowerHousing1
from simulation.standard.channels import ResultOnes


class SelectorFitBench(AssemblyNode):
    setting = Driver(default=0, range=(0, 9))
    postcarry = Driver(default=0, range=(0, 1), dtype=int)
    selector = Selector1()
    channel = ResultOnes()
    housing = LowerHousing1()
    setting.drives(selector.setting)
    setting.drives(channel.setting)
    postcarry.drives(channel.turn, ratio=-648, offset=652)
    postcarry.drives(channel.carry, ratio=0)
