"""Direct-operation migration on the source-backed Curta parts.

The manifest selects this root. Selection is not acceptance: the outstanding
interlock, reverser, clearing-loop and whole-machine geometry contracts remain
recorded in the project-owned operating completion record.
"""

from functools import reduce
from operator import and_

from machinome.node import AssemblyNode
from machinome.motion.ports import Time, Port
from machinome.simulation import Driver, Instruction, Button, Turn, Slide
from simulation.assemblies import LayeredSource
from simulation.mechanism import Frame
from simulation.positioning import CarriagePositioning
from simulation.running_parts import (IndependentInputs, RetainedCarriage, RunningMainDrive, RunningEnclosure,
    RetainedCarries, RetainedTransmission, RESULT_DIALS, TURNS_DIALS,
    RESULT_RESTS, TURNS_RESTS, CHANNEL_NAMES)
from simulation.running_laws import shaft_motion, dial_motion, lever_motion, reading


def sources(*ends):
    return reduce(and_, ends)


def wheel_ends(register, table):
    return tuple(getattr(register, name).turn for name, zero in table)


def shaft_ends(bank, count):
    return tuple(getattr(bank, name).turn for name in CHANNEL_NAMES[:count])


def lever_ends(bank, count, counter):
    return tuple(getattr(getattr(bank,
        f'{"turns" if counter else "results"}_tens_lever_assembly_{index + 1}'),
        'tens_slider_for_turns_counter' if counter else 'tens_slider_for_results').travel
        for index in range(count))


class RunningCarriage(AssemblyNode):
    positioning = CarriagePositioning()
    registers = RetainedCarriage()
    registers.lift.drives(positioning.lift)


class OperatingCurta(LayeredSource):
    time = Time.running()
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

    enclosure = RunningEnclosure()
    input_selectors = IndependentInputs()
    frame = Frame()
    main_drive = RunningMainDrive()
    carriage = RunningCarriage()
    carry_mechanism = RetainedCarries()
    transmission = RetainedTransmission()

    instructions = {'Turn crank': Instruction(by={'crank_rotation': 360}, duration=2)}
    controls = {
        'turn crank': Turn(main_drive.crank.crank_handle_1, crank_rotation,
                           coordinate=main_drive.crank.turn),
        'one revolution': Button(main_drive.crank.crank_handle_1, 'Turn crank',
                                 coordinate=main_drive.crank.turn),
        'lift crank': Slide(main_drive.crank.crank_handle_1, crank_elevation,
                            coordinate=main_drive.crank.lift),
        'shift carriage': Turn(carriage.registers.covers.upper_housing, carriage_rotation,
                               coordinate=carriage.registers.turn),
        'lift carriage': Slide(carriage.registers.covers.upper_housing, carriage_elevation,
                               coordinate=carriage.registers.lift),
        'clear registers': Turn(carriage.registers.clearing_ring.clearing_ring,
                                clearing_rotation,
                                coordinate=carriage.registers.clearing_ring.turn),
    }

    crank_rotation.drives(main_drive.turn, ratio=-1)
    crank_elevation.drives(main_drive.subtract, ratio=1 / 9)
    crank_rotation.drives(carry_mechanism.tens_bell.turn, ratio=-1)
    crank_elevation.drives(carry_mechanism.tens_bell.subtract, ratio=1 / 9)
    carriage_rotation.drives(carriage.registers.turn)
    carriage_elevation.drives(carriage.registers.lift)
    clearing_rotation.drives(carriage.registers.clearing_ring.turn, ratio=-1)

    for _index, _input in enumerate((marker_1_rotation, marker_2_rotation, marker_3_rotation,
            marker_4_rotation, marker_5_rotation, marker_6_rotation, marker_7_rotation,
            marker_8_rotation, marker_9_rotation, marker_10_rotation), 1):
        _marker = getattr(enclosure.decimal_markers if _index < 6 else
                          carriage.registers.clearing_ring.decimal_markers,
                          f'decimal_marker_{_index}')
        _input.drives(_marker.turn)
        controls[f'move decimal marker {_index}'] = Turn(
            _marker.position_marker, _input, coordinate=_marker.turn)
        del _marker, _input

    # Explicit names preserve physical identities; these loops declare laws
    # once in the class body, never mutate a run or maintain a second state.
    for _index, _input in enumerate((digit_1, digit_2, digit_3, digit_4,
                                     digit_5, digit_6, digit_7, digit_8), 1):
        _selector = getattr(input_selectors.selectors, f'digit_selector_axle_{_index}')
        _input.drives(_selector.setting)
        _knob = ("selector_knob_1_419057", "selector_knob_1_419152", "selector_knob_1_419225",
                 "selector_knob_1_419084", "selector_knob_1_419177", "selector_knob_1_419141",
                 "selector_knob_1_419102", "selector_knob_1_419155")[_index - 1]
        controls[f'set digit {_index}'] = Slide(getattr(_selector, _knob), _input)
        del _selector, _input

    for _counter, _dial_table, _rests, _bank_name in (
            (False, RESULT_DIALS, RESULT_RESTS, 'result'),
            (True, TURNS_DIALS, TURNS_RESTS, 'turns')):
        _bank = getattr(transmission, _bank_name)
        _register = getattr(carriage.registers, f'{_bank_name}_register')
        _levers = getattr(carry_mechanism, f'{_bank_name}_carries')
        _wheel_ends = wheel_ends(_register, _dial_table)
        _shaft_ends = shaft_ends(_bank, len(_dial_table))
        _lever_ends = lever_ends(_levers, len(_rests), _counter)

        for _index, _name in enumerate(CHANNEL_NAMES[:len(_dial_table)]):
            _shaft = getattr(_bank, _name)
            _setting = (getattr(input_selectors.selectors,
                               f'digit_selector_axle_{_index + 1}').selector_shaft_bottom.turn
                        if not _counter and _index < 8 else crank_elevation)
            # Inactive higher input channels have a constant zero setting.
            if not _counter and _index < 8:
                _setting.drives(_shaft.setting, ratio=1 / 36)
            else:
                crank_elevation.drives(_shaft.setting, ratio=0,
                                       offset=-.75 if _counter else 0)
            if _index:
                _lever_ends[_index - 1].drives(_shaft.carry, ratio=1 / 4.2,
                                              offset=-_rests[_index - 1] / 4.2)
            else:
                crank_elevation.drives(_shaft.carry, ratio=0)
            sources(main_drive.crank.turn, main_drive.crank.lift,
                    _setting, _lever_ends[_index - 1] if _index else carriage.registers.lift).drives(
                _shaft.turn, law=shaft_motion(_index, _counter,
                                             _rests[_index - 1] if _index else 0))
            del _shaft, _setting

        for _index, _wheel in enumerate(_wheel_ends):
            sources(carriage.registers.turn, carriage.registers.lift,
                    carriage.registers.clearing_ring.turn, _wheel, *_shaft_ends).drives(
                _wheel, law=dial_motion(_index, _counter))
            del _wheel
        for _index, (_lever, _rest) in enumerate(zip(_lever_ends, _rests), 1):
            sources(main_drive.crank.turn, carriage.registers.turn,
                    carriage.registers.lift, _lever, *_wheel_ends).drives(
                _lever, law=lever_motion(_index, _rest, _counter))
            del _lever
        del _bank, _register, _levers
    del _index, _knob, _counter, _dial_table, _rests, _bank_name
    del _wheel_ends, _shaft_ends, _lever_ends, _name, _rest


def register_reading(sim, counter=False):
    """Decode the committed joint bank; this readout never drives a part."""
    table = TURNS_DIALS if counter else RESULT_DIALS
    bank = 'turns' if counter else 'result'
    state = sim.state
    return reading(table)(None, None)(*(state[
        f'carriage.registers.{bank}_register.{name}.turn'] for name, zero in table))
