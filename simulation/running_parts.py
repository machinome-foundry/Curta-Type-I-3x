"""Existing fitted parts, with history on their actual moving coordinates.

The pose benches remain available. These specializations replace only the
pose-driven bindings; they neither duplicate physical parts nor add memory.
"""

from solid_node.node import AssemblyNode
from solid_node.motion.joints import Revolute, Prismatic
from simulation import assemblies
from simulation.mechanism import MainDrive, RegisterCarriage, TensBellAssembly, CarriageStructure, ClearingAssembly
from simulation.running_pawl import RunningAntiReversal
from simulation.cover_fits import FittedAxleCarrier
from simulation.clearing_stop_motion import following as clearing_stop_following
from simulation.registers import ResultDials, TurnsDials
from simulation.selectors import IndependentSelectors
from simulation.standard.layers import CrankAssembly
from simulation.decimal_markers import LowerMovableMarkers, UpperMovableMarkers
import simulation.standard.carry as carry
import simulation.standard.channels as channels


RESULT_DIALS = (
    ('p_10203_1', -146), ('p_10203_2', -235.99999999),
    ('p_10205_1', -275.4500831), ('p_10205_2', -295.45008308),
    ('p_10204_1', -315.45008308), ('p_10204_2', -335.45008307),
    ('p_10204_3', -355.45008308), ('p_10204_4', -375.45008311),
    ('p_10204_5', -395.45008311), ('p_10204_6', -415.4500831),
    ('results_dial_type_2_1', -145.99999998),
)
TURNS_DIALS = (
    ('p_10203_3', -145.99999998), ('p_10203_4', -145.99999999),
    ('p_10205_3', -145.4500831), ('p_10205_4', -165.45008308),
    ('p_10204_7', -185.4500831), ('results_dial_type_2_2', -145.99999998),
)
RESULT_RESTS = (-4.2, 0, 0, 0, 0, -4.2, 0, -4.2, -4.2, -4.2)
TURNS_RESTS = (-1.8,) * 5
CHANNEL_NAMES = ('ones', 'tens', 'hundreds', 'digit_4', 'digit_5', 'digit_6',
                 'digit_7', 'digit_8', 'digit_9', 'digit_10', 'digit_11')


class RetainedResultDials(ResultDials):
    def simulate(self):
        for name, zero in RESULT_DIALS:
            dial = getattr(self, name)
            if dial.turn.value is None:
                dial.turn = zero


class RetainedTurnsDials(TurnsDials):
    def simulate(self):
        for name, zero in TURNS_DIALS:
            dial = getattr(self, name)
            if dial.turn.value is None:
                dial.turn = zero


class RetainedAxleCarrier(FittedAxleCarrier):
    pin_drive = FittedAxleCarrier.clearing_pin.slide.drives(FittedAxleCarrier.press)


class RetainedCarriageStructure(CarriageStructure):
    upper_carriage_body_1 = RetainedAxleCarrier()


class RunningClearingAssembly(ClearingAssembly):
    decimal_markers = UpperMovableMarkers()


class RunningEnclosure(assemblies.Enclosure):
    decimal_markers = LowerMovableMarkers()


class RetainedCarriage(RegisterCarriage):
    result_register = RetainedResultDials()
    turns_register = RetainedTurnsDials()
    carrier = RetainedCarriageStructure()
    clearing_ring = RunningClearingAssembly(turn=Revolute(axis=(0, 0, 1)))
    clearing_follower = clearing_ring.turn.drives(
        carrier.upper_carriage_body_1.clearing_pin.slide, law=clearing_stop_following)


class IndependentInputs(assemblies.Inputs):
    selectors = IndependentSelectors()


class RunningMainDrive(MainDrive):
    # Driver ranges only describe the control panel; the moving crank's
    # joint admits the measured addition-to-subtraction stroke in Python too.
    crank = CrankAssembly(turn=Revolute(axis=(0, 0, 1)),
                          lift=Prismatic(axis=(0, 0, 1), range=(0, 9)))
    anti_reversal = RunningAntiReversal()


def retained_lever(base, rest, counter=False):
    """Reverse the named pose binding: the real slider now owns its history."""
    slider = 'tens_slider_for_turns_counter' if counter else 'tens_slider_for_results'

    class RetainedLever(base):
        slider_drive = getattr(base, slider).travel.drives(
            base.engage, ratio=1 / 4.2, offset=-rest / 4.2)

        def simulate(self):
            body = getattr(self, slider)
            if body.travel.value is None:
                body.travel = rest

    return RetainedLever


class RetainedResultCarries(carry.ResultsCarry):
    results_tens_lever_assembly_1 = retained_lever(carry.ResultsLever1, -4.2)()
    results_tens_lever_assembly_2 = retained_lever(carry.ResultsLever2, 0)()
    results_tens_lever_assembly_3 = retained_lever(carry.ResultsLever3, 0)()
    results_tens_lever_assembly_4 = retained_lever(carry.ResultsLever4, 0)()
    results_tens_lever_assembly_5 = retained_lever(carry.ResultsLever5, 0)()
    results_tens_lever_assembly_6 = retained_lever(carry.ResultsLever6, -4.2)()
    results_tens_lever_assembly_7 = retained_lever(carry.ResultsLever7, 0)()
    results_tens_lever_assembly_8 = retained_lever(carry.ResultsLever8, -4.2)()
    results_tens_lever_assembly_9 = retained_lever(carry.ResultsLever9, -4.2)()
    results_tens_lever_assembly_10 = retained_lever(carry.ResultsLever10, -4.2)()


class RetainedTurnsCarries(carry.TurnsCarry):
    turns_tens_lever_assembly_1 = retained_lever(carry.TurnsLever1, -1.8, True)()
    turns_tens_lever_assembly_2 = retained_lever(carry.TurnsLever2, -1.8, True)()
    turns_tens_lever_assembly_3 = retained_lever(carry.TurnsLever3, -1.8, True)()
    turns_tens_lever_assembly_4 = retained_lever(carry.TurnsLever4, -1.8, True)()
    turns_tens_lever_assembly_5 = retained_lever(carry.TurnsLever5, -1.8, True)()


class RetainedCarries(assemblies.CarryMechanism):
    tens_bell = TensBellAssembly(turn=Revolute(axis=(0, 0, 1)))
    result_carries = RetainedResultCarries()
    turns_carries = RetainedTurnsCarries()


class ResultShafts(AssemblyNode):
    ones = channels.ResultOnes()
    tens = channels.ResultTens()
    hundreds = channels.ResultHundreds()
    digit_4 = channels.ResultDigit4()
    digit_5 = channels.ResultDigit5()
    digit_6 = channels.ResultDigit6()
    digit_7 = channels.ResultDigit7()
    digit_8 = channels.ResultDigit8()
    digit_9 = channels.ResultDigit9()
    digit_10 = channels.ResultDigit10()
    digit_11 = channels.ResultDigit11()

    def simulate(self):
        from simulation.fit import INPUT_CLOCKING
        for index, name in enumerate(CHANNEL_NAMES[1:], 1):
            shaft = getattr(self, name)
            if shaft.turn.value is None:
                shaft.turn = INPUT_CLOCKING - 20 * index


class TurnsShafts(AssemblyNode):
    ones = channels.TurnsOnes()
    tens = channels.TurnsTens()
    hundreds = channels.TurnsHundreds()
    digit_4 = channels.TurnsDigit4()
    digit_5 = channels.TurnsDigit5()
    digit_6 = channels.TurnsDigit6()

    def simulate(self):
        from simulation.fit import INPUT_CLOCKING
        for index, name in enumerate(CHANNEL_NAMES[1:6], 1):
            shaft = getattr(self, name)
            if shaft.turn.value is None:
                shaft.turn = 130 + INPUT_CLOCKING - 20 * index


class RetainedTransmission(AssemblyNode):
    result = ResultShafts()
    turns = TurnsShafts()
