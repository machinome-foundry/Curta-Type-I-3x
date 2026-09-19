"""The third Curta sibling: framework-owned event memory and a closed-form pose."""

from functools import reduce
from operator import and_

from machinome.node import AssemblyNode
from machinome.motion.ports import Port
from machinome.simulation import Driver, State, Instruction
from simulation.assemblies import LayeredSource
from simulation.clocked_parts import Operation, ClockedCarriage
from simulation.clocked_laws import (stroke, advance, clearing_event, cleared, value_of,
    operand_of, phase, subtracting, shift, check_event, remember_check)
from simulation.running_parts import RunningEnclosure, IndependentInputs
from simulation.mechanism import MainDrive, CarryMechanism, Frame
from simulation.transmission import Transmission


def sources(*ends):
    return reduce(and_, ends)


class MemoryDigit(AssemblyNode):
    value = State(default=0, range=(0, 9), dtype=int)

    def render(self):
        return []

def pose_inputs(sources, targets):
    return lambda *values: values


class PoseValues(AssemblyNode):
    """Intermediate pose values; none belongs to the retained bank."""

    operand = Port()
    crank_turns = Port()
    subtract = Port()
    carriage_position = Port()
    clear = Port()
    result = Port()
    turns_counter = Port()

    def render(self):
        return []


class ClockedCurta(LayeredSource):
    """Same fitted machine; requests retain digits and latches, not the pose tree."""

    values = PoseValues()

    digit_1 = Driver(default=0, range=(0, 9), unit='digit')
    digit_2 = Driver(default=0, range=(0, 9), unit='digit')
    digit_3 = Driver(default=0, range=(0, 9), unit='digit')
    digit_4 = Driver(default=0, range=(0, 9), unit='digit')
    digit_5 = Driver(default=0, range=(0, 9), unit='digit')
    digit_6 = Driver(default=0, range=(0, 9), unit='digit')
    digit_7 = Driver(default=0, range=(0, 9), unit='digit')
    digit_8 = Driver(default=0, range=(0, 9), unit='digit')
    crank_rotation = Driver(default=0, unit='deg')
    crank_elevation = Driver(default=0, range=(0, 9), unit='mm')
    carriage_rotation = Driver(default=0, range=(0, 100), unit='deg')
    carriage_elevation = Driver(default=0, range=(0, 6), unit='mm')
    clearing_rotation = Driver(default=0, unit='deg')
    clearing_check = State(default=0, unit='deg')
    marker_1_rotation = Driver(default=0, unit='deg')
    marker_2_rotation = Driver(default=0, unit='deg')
    marker_3_rotation = Driver(default=0, unit='deg')
    marker_4_rotation = Driver(default=0, unit='deg')
    marker_5_rotation = Driver(default=0, unit='deg')
    marker_6_rotation = Driver(default=0, unit='deg')
    marker_7_rotation = Driver(default=0, unit='deg')
    marker_8_rotation = Driver(default=0, unit='deg')
    marker_9_rotation = Driver(default=0, unit='deg')
    marker_10_rotation = Driver(default=0, unit='deg')
    result_0 = MemoryDigit()
    result_1 = MemoryDigit()
    result_2 = MemoryDigit()
    result_3 = MemoryDigit()
    result_4 = MemoryDigit()
    result_5 = MemoryDigit()
    result_6 = MemoryDigit()
    result_7 = MemoryDigit()
    result_8 = MemoryDigit()
    result_9 = MemoryDigit()
    result_10 = MemoryDigit()
    turns_0 = MemoryDigit()
    turns_1 = MemoryDigit()
    turns_2 = MemoryDigit()
    turns_3 = MemoryDigit()
    turns_4 = MemoryDigit()
    turns_5 = MemoryDigit()

    instructions = {'Turn crank': Instruction(by={'crank_rotation': 360}, duration=6)}
    operation = Operation()
    enclosure = RunningEnclosure()

    for _check in (0, 230):
        for _reverse in (False, True):
            clearing_rotation.commits(clearing_check, at=check_event(_check, _reverse),
                                      law=remember_check)
    del _check, _reverse

    _digits = (digit_1, digit_2, digit_3, digit_4, digit_5, digit_6, digit_7, digit_8,)
    _results = (result_0.value, result_1.value, result_2.value, result_3.value, result_4.value, result_5.value, result_6.value, result_7.value, result_8.value, result_9.value, result_10.value,)
    _turns = (turns_0.value, turns_1.value, turns_2.value, turns_3.value, turns_4.value, turns_5.value,)
    sources(crank_rotation, crank_elevation, carriage_rotation, carriage_elevation,
            *_digits, *_results, *_turns).commits(
                _results + _turns, at=stroke, law=advance)
    for _counter, _bank in ((False, _results), (True, _turns)):
        for _place, _value in enumerate(_bank):
            for _reverse in (False, True):
                sources(clearing_rotation, carriage_elevation, _value).commits(
                    _value, at=clearing_event(_place, _counter, _reverse), law=cleared)
            del _value
    sources(*_results).drives(values.result, law=value_of)
    sources(*_turns).drives(values.turns_counter, law=value_of)
    sources(*_digits).drives(values.operand, law=operand_of)
    crank_rotation.drives(values.crank_turns, law=phase)
    crank_elevation.drives(values.subtract, law=subtracting)
    carriage_rotation.drives(values.carriage_position, law=shift)
    clearing_rotation.drives(values.clear, ratio=0)
    crank_rotation.drives(operation.crank)
    crank_elevation.drives(operation.crank_lift)
    carriage_rotation.drives(operation.carriage_turn)
    carriage_elevation.drives(operation.carriage_lift)
    clearing_rotation.drives(operation.ring)
    del _digits, _results, _turns, _counter, _bank, _place, _reverse

    input_selectors = IndependentInputs()
    frame = Frame()
    main_drive = MainDrive()
    carriage = ClockedCarriage()
    carry_mechanism = CarryMechanism()
    transmission = Transmission()

    for _index, _input in enumerate((digit_1, digit_2, digit_3, digit_4,
                                     digit_5, digit_6, digit_7, digit_8), 1):
        _input.drives(getattr(input_selectors.selectors,
                             f'digit_selector_axle_{_index}').setting)
        del _input
    del _index
    operation.crank.drives(main_drive.turn, ratio=-1)
    operation.crank_lift.drives(main_drive.subtract, ratio=1 / 9)
    operation.crank.drives(carry_mechanism.tens_bell.turn, ratio=-1)
    operation.crank_lift.drives(carry_mechanism.tens_bell.subtract, ratio=1 / 9)
    operation.carriage_turn.drives(carriage.position, ratio=1 / 20)
    operation.carriage_lift.drives(carriage.lift, ratio=1 / 6)
    values.clear.drives(carriage.clear)
    operation.ring.drives(carriage.ring)
    clearing_rotation.drives(carriage.registers.result_register.ring)
    clearing_rotation.drives(carriage.registers.turns_register.ring)
    clearing_check.drives(carriage.registers.result_register.anchor)
    clearing_check.drives(carriage.registers.turns_register.anchor)
    carriage_elevation.drives(carriage.registers.result_register.elevation)
    carriage_elevation.drives(carriage.registers.turns_register.elevation)
    transmission.result.tens.carry.drives(carry_mechanism.result_carries.results_tens_lever_assembly_1.engage)
    transmission.result.hundreds.carry.drives(carry_mechanism.result_carries.results_tens_lever_assembly_2.engage)
    transmission.result.digit_4.carry.drives(carry_mechanism.result_carries.results_tens_lever_assembly_3.engage)
    transmission.result.digit_5.carry.drives(carry_mechanism.result_carries.results_tens_lever_assembly_4.engage)
    transmission.result.digit_6.carry.drives(carry_mechanism.result_carries.results_tens_lever_assembly_5.engage)
    transmission.result.digit_7.carry.drives(carry_mechanism.result_carries.results_tens_lever_assembly_6.engage)
    transmission.result.digit_8.carry.drives(carry_mechanism.result_carries.results_tens_lever_assembly_7.engage)
    transmission.result.digit_9.carry.drives(carry_mechanism.result_carries.results_tens_lever_assembly_8.engage)
    transmission.result.digit_10.carry.drives(carry_mechanism.result_carries.results_tens_lever_assembly_9.engage)
    transmission.result.digit_11.carry.drives(carry_mechanism.result_carries.results_tens_lever_assembly_10.engage)
    transmission.turns.tens.carry.drives(carry_mechanism.turns_carries.turns_tens_lever_assembly_1.engage)
    transmission.turns.hundreds.carry.drives(carry_mechanism.turns_carries.turns_tens_lever_assembly_2.engage)
    transmission.turns.digit_4.carry.drives(carry_mechanism.turns_carries.turns_tens_lever_assembly_3.engage)
    transmission.turns.digit_5.carry.drives(carry_mechanism.turns_carries.turns_tens_lever_assembly_4.engage)
    transmission.turns.digit_6.carry.drives(carry_mechanism.turns_carries.turns_tens_lever_assembly_5.engage)
    values.result.drives(carriage.registers.result_register.value)
    values.turns_counter.drives(carriage.registers.turns_register.value)
    values.result.drives(transmission.result.value)
    values.turns_counter.drives(transmission.turns.value)
    carriage.registers.lift.drives(transmission.result.carriage_lift)
    carriage.registers.lift.drives(transmission.turns.carriage_lift)
    (values.operand & values.crank_turns & values.subtract & values.carriage_position).drives((
        transmission.result.operand, transmission.result.crank_turns,
        transmission.result.subtract, transmission.result.carriage_position,
    ), law=pose_inputs)
    (values.operand & values.crank_turns & values.subtract & values.carriage_position).drives((
        transmission.turns.operand, transmission.turns.crank_turns,
        transmission.turns.subtract, transmission.turns.carriage_position,
    ), law=pose_inputs)
    (values.operand & values.crank_turns & values.subtract & values.carriage_position & values.clear).drives((
        carriage.registers.result_register.operand,
        carriage.registers.result_register.crank_turns,
        carriage.registers.result_register.subtract,
        carriage.registers.result_register.carriage_position,
        carriage.registers.result_register.clear,
    ), law=pose_inputs)
    (values.operand & values.crank_turns & values.subtract & values.carriage_position & values.clear).drives((
        carriage.registers.turns_register.operand,
        carriage.registers.turns_register.crank_turns,
        carriage.registers.turns_register.subtract,
        carriage.registers.turns_register.carriage_position,
        carriage.registers.turns_register.clear,
    ), law=pose_inputs)

    for _index, _input in enumerate((marker_1_rotation, marker_2_rotation, marker_3_rotation, marker_4_rotation, marker_5_rotation, marker_6_rotation, marker_7_rotation, marker_8_rotation, marker_9_rotation, marker_10_rotation), 1):
        _marker = getattr(enclosure.decimal_markers if _index < 6 else
                          carriage.registers.clearing_ring.decimal_markers,
                          f'decimal_marker_{_index}')
        _input.drives(_marker.turn)
        del _input, _marker
    del _index


def register_reading(sim, counter=False):
    """Read committed digits, distinct from a mid-stroke dial's moving reading."""
    prefix, count = ('turns', 6) if counter else ('result', 11)
    state = sim.state
    return sum(int(state[f'{prefix}_{place}.value']) * 10 ** place
               for place in range(count))
