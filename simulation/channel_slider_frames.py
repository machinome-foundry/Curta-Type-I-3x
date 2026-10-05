"""Shaft-line datums on unmodified source result-channel sliding prints.

The prints contain their source placements. A guide names that same shaft
line at source Z=0; matched channel seats leave their native placement intact.
The fitted uppers and reversing inputs declare their datums beside their fits.
"""

from machinome.node.frames import Frame
from simulation.standard import channels, printed


class ResultOnesInput(printed.Part10219_410002_1):
    guide = Frame(at=channels.ResultOnes.turn.at, z=(0, 0, -1))


class ResultOnesCarry(printed.Part10221_1):
    guide = Frame(at=channels.ResultOnes.turn.at, z=(0, 0, -1))


class ResultTensInput(printed.Part10230_410008_1_419229):
    guide = Frame(at=channels.ResultTens.turn.at, z=(0, 0, -1))


class ResultHundredsInput(printed.Part10230_410008_1_419088):
    guide = Frame(at=channels.ResultHundreds.turn.at, z=(0, 0, -1))


class ResultDigit4Input(printed.Part10230_410008_1_419232):
    guide = Frame(at=channels.ResultDigit4.turn.at, z=(0, 0, -1))


class ResultDigit5Input(printed.Part10230_410008_1_419092):
    guide = Frame(at=channels.ResultDigit5.turn.at, z=(0, 0, -1))


class ResultDigit6Input(printed.Part10230_410008_1_419066):
    guide = Frame(at=channels.ResultDigit6.turn.at, z=(0, 0, -1))


class ResultDigit7Input(printed.Part10230_410008_1_419032):
    guide = Frame(at=channels.ResultDigit7.turn.at, z=(0, 0, -1))


class ResultDigit8Input(printed.Part10230_410008_1_419075):
    guide = Frame(at=channels.ResultDigit8.turn.at, z=(0, 0, -1))


class ResultDigit9Input(printed.Part10230_410008_1_419137):
    guide = Frame(at=channels.ResultDigit9.turn.at, z=(0, 0, -1))


class ResultDigit10Input(printed.Part10230_410008_1_419118):
    guide = Frame(at=channels.ResultDigit10.turn.at, z=(0, 0, -1))


class ResultDigit11Input(printed.Part10230_410008_1_419111):
    guide = Frame(at=channels.ResultDigit11.turn.at, z=(0, 0, -1))
