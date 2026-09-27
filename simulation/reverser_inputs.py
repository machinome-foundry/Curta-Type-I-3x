"""Trial counter tooth fit at both measured reversing-lever positions."""

from machinome.node import Frame
from machinome.parameters import Length
from machinome.motion.joints import Prismatic
from simulation.fit import FittedCounterPinion
from simulation.standard import printed, channels


class ReversingCounterPinion(FittedCounterPinion):
    # Native full-bank probe at crank 123 / hundreds needs .42 mm: .40
    # still intersects by .000297740 mm3 at the candidate upper position.
    # Preserve keyed bores and height; no result-channel tooth is changed.
    flank_relief = Length(.42, min=0)


class OnesInput(printed.Part10218_1):
    guide = Frame(at=channels.TurnsOnes.turn.at, z=(0, 0, -1))
    # Its three teeth need the existing .36 mm fit. Applying the higher-bank
    # .42 mm relief here loses the fork's axial capture at crank 75 degrees.
    pass


class TensInput(printed.Part10230_410008_1_419080):
    guide = Frame(at=channels.TurnsTens.turn.at, z=(0, 0, -1))
    transmission_gear_0_5 = ReversingCounterPinion()


class HundredsInput(printed.Part10230_410008_1_419068):
    guide = Frame(at=channels.TurnsHundreds.turn.at, z=(0, 0, -1))
    transmission_gear_0_5 = ReversingCounterPinion()


class FourthInput(printed.Part10230_410008_1_419182):
    guide = Frame(at=channels.TurnsDigit4.turn.at, z=(0, 0, -1))
    transmission_gear_0_5 = ReversingCounterPinion()


class FifthInput(printed.Part10230_410008_1_419105):
    guide = Frame(at=channels.TurnsDigit5.turn.at, z=(0, 0, -1))
    transmission_gear_0_5 = ReversingCounterPinion()


class SixthInput(printed.Part10230_410008_1_419237):
    guide = Frame(at=channels.TurnsDigit6.turn.at, z=(0, 0, -1))
    transmission_gear_0_5 = ReversingCounterPinion()


class ReversingOnes(channels.TurnsOnes):
    p_10218_1 = OnesInput(travel=Prismatic(axis=(0, 0, -1)))


class ReversingTens(channels.TurnsTens):
    p_10230_410008_1_419080 = TensInput(travel=Prismatic(axis=(0, 0, -1)))


class ReversingHundreds(channels.TurnsHundreds):
    p_10230_410008_1_419068 = HundredsInput(travel=Prismatic(axis=(0, 0, -1)))


class ReversingFourth(channels.TurnsDigit4):
    p_10230_410008_1_419182 = FourthInput(travel=Prismatic(axis=(0, 0, -1)))


class ReversingFifth(channels.TurnsDigit5):
    p_10230_410008_1_419105 = FifthInput(travel=Prismatic(axis=(0, 0, -1)))


class ReversingSixth(channels.TurnsDigit6):
    p_10230_410008_1_419237 = SixthInput(travel=Prismatic(axis=(0, 0, -1)))
