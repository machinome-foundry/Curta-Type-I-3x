"""Existing fitted parts, with history on their actual moving coordinates.

The pose benches remain available. These specializations replace only the
pose-driven bindings; they neither duplicate physical parts nor add memory.
"""

from machinome.node import AssemblyNode
from machinome.motion.joints import Bound, Revolute, Prismatic
from simulation import assemblies
from simulation.mechanism import MainDrive, RegisterCarriage, TensBellAssembly, CarriageStructure, ClearingAssembly
from simulation.running_pawl import RetainedAntiReversal, reverse_stop
from simulation.higher_lockout_parts import ContactTens, ContactBell
from simulation.cover_fits import FittedAxleCarrier
from simulation.clearing_stop_motion import following as clearing_stop_following
from simulation.registers import ResultDials, TurnsDials
from simulation.selectors import IndependentSelectors
from simulation.standard.layers import CrankAssembly
from simulation.print_parts import CounterBodyStopPin
from simulation.clearing_seat_fit import FittedClearingPin
from simulation.carriage_frame_fit import FittedCounterBody
from simulation.carriage_index_motion import minimum_carriage_lift
from simulation.operating_collar_parts import SeatedCollar, SeatedCollarWasher
from simulation.counter_lockout_parts import ContactCounterOnes
from simulation.decimal_markers import LowerMovableMarkers, UpperMovableMarkers, LOWER_CENTER
from simulation.reverser_following import FollowingReverser
from simulation.reverser_seat_trial import TrialKnob
from simulation.reverser_inputs import (ReversingTens, ReversingHundreds,
    ReversingFourth, ReversingFifth, ReversingSixth)
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
# Manual p39 leaves "about 4 mm" exposed. The exported insertion leaves
# 4.355589482 mm and penetrates the frame. Native contact ends at +.455580 mm;
# seat the unchanged pin .51 mm deeper for at least .05 mm clearance.
STOP_PIN_SEATING_RISE = .51


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
    counter_body = FittedCounterBody()
    counter_body_stop_pin = CounterBodyStopPin()
    clearing_pin = FittedClearingPin(slide=Prismatic(axis=(0, 0, -1)))
    pin_drive = clearing_pin.slide.drives(FittedAxleCarrier.press)

    def render(self):
        super().render()
        self.counter_body_stop_pin.translate((0, 0, STOP_PIN_SEATING_RISE))


class RetainedCarriageStructure(CarriageStructure):
    upper_carriage_body_1 = RetainedAxleCarrier()
    crank_collar = SeatedCollar()
    crank_collar_washer = SeatedCollarWasher()

    def render(self):
        super().render()
        # Source +/-Y collar bores face the recentered +/-X carrier pins.
        # The independent seat bench proves the final -90 degree clocking.
        self.crank_collar.rotate(54.282220532, (0, 0, 1))
        # Retain the measured nut Z and thread geometry, at world phase 40.
        self.crank_collar_nut.rotate(94.282220532, (0, 0, 1))


class RunningClearingAssembly(ClearingAssembly):
    decimal_markers = UpperMovableMarkers()


class RunningEnclosure(assemblies.Enclosure):
    decimal_markers = LowerMovableMarkers()

    def render(self):
        super().render()
        # Native circular datums put the source lower shell .8496 mm off the
        # sleeve/main shaft. Carry its marker track and fitted hardware with it.
        recenter = tuple(-value for value in LOWER_CENTER)
        for name in ('lower_housing_1', 'decimal_markers', 'base_plate',
                     'm4x10_419010_6', 'm5x30_countersunk_1', 'm5x30_countersunk_2'):
            getattr(self, name).translate(recenter)
        # A named .05 mm locational seat, not an overlap tolerance. The source
        # is exactly flush natively but its encoded faces slightly interpenetrate.
        # The two countersunk heads stay seated in the unchanged plate.
        for name in ('base_plate', 'm5x30_countersunk_1', 'm5x30_countersunk_2'):
            getattr(self, name).translate((0, 0, -.05))


class RetainedCarriage(RegisterCarriage):
    result_register = RetainedResultDials()
    turns_register = RetainedTurnsDials()
    carrier = RetainedCarriageStructure()
    clearing_ring = RunningClearingAssembly(turn=Revolute(axis=(0, 0, 1)))
    turn = Revolute(axis=(0, 0, 1), range=(0, 100))
    lift = Prismatic(axis=(0, 0, 1), range=(Bound(minimum_carriage_lift,
        reads=(carrier.upper_carriage_body_1.clearing_pin.slide, turn)), 6))
    clearing_follower = clearing_ring.turn.drives(
        carrier.upper_carriage_body_1.clearing_pin.slide, law=clearing_stop_following)


class IndependentInputs(assemblies.Inputs):
    selectors = IndependentSelectors()


class RunningReverser(FollowingReverser):
    reversing_lever_knob_1 = TrialKnob(
        lift=Prismatic(axis=(0, 0, 1), range=(-6.9425, 3.9075)))


class RunningReversingAssembly(AssemblyNode):
    reversing_lever_1 = RunningReverser()


class RunningMainDrive(MainDrive):
    # Driver ranges only describe the control panel; the moving crank's
    # joint admits the measured addition-to-subtraction stroke in Python too.
    anti_reversal = RetainedAntiReversal()
    reversing_lever = RunningReversingAssembly()
    crank = CrankAssembly(turn=Revolute(axis=(0, 0, 1), range=(None,
                          Bound(reverse_stop, reads=(anti_reversal.reverse_rotation_prevention_pawl.turn,)))),
                          lift=Prismatic(axis=(0, 0, 1), range=(0, 9)))


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


class ContactBellAssembly(TensBellAssembly):
    tens_bell_1 = ContactBell()


class RetainedCarries(assemblies.CarryMechanism):
    tens_bell = ContactBellAssembly(turn=Revolute(axis=(0, 0, 1)))
    result_carries = RetainedResultCarries()
    turns_carries = RetainedTurnsCarries()


class ResultShafts(AssemblyNode):
    ones = channels.ResultOnes()
    tens = ContactTens()
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
    ones = ContactCounterOnes()
    tens = ReversingTens()
    hundreds = ReversingHundreds()
    digit_4 = ReversingFourth()
    digit_5 = ReversingFifth()
    digit_6 = ReversingSixth()

    def simulate(self):
        from simulation.fit import INPUT_CLOCKING
        for index, name in enumerate(CHANNEL_NAMES[1:6], 1):
            shaft = getattr(self, name)
            if shaft.turn.value is None:
                shaft.turn = 130 + INPUT_CLOCKING - 20 * index


class RetainedTransmission(AssemblyNode):
    result = ResultShafts()
    turns = TurnsShafts()
