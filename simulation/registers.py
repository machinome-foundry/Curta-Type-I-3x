"""Dial joints and source-specific clocking; one port per register value."""

from machinome.node.assembly import AssemblyNode
from machinome.node.frames import Frame
from machinome.motion.joints import Revolute
from machinome.motion.ports import Port
from machinome.simulation import Driver
from simulation.cycle import dial_positions
from simulation.fit import CARRIAGE_CENTER, CARRIAGE_CLOCKING, INPUT_CLOCKING, BEVEL_DIAL_CLOCKING
from simulation.standard.assembly import *
from simulation.dial_frames import (FittedDialType2, Part10203_1, Part10203_2,
    Part10203_3, Part10203_4, Part10204_1, Part10204_2, Part10204_3, Part10204_4,
    Part10204_5, Part10204_6, Part10204_7, Part10205_1, Part10205_2, Part10205_3, Part10205_4)
import simulation.standard.layers as source

# Bevel teeth repeat every digit. The clearing gear's missing-tooth gap fixes
# the absolute zero: all seventeen source gaps were 142° from vertical, so four
# whole pitches place them 2° from vertical without changing bevel engagement.
CLEARING_ZERO_INDEX = 4


def dial_values(phases, counter=False):
    return lambda sources, targets: lambda *values: tuple(
        phase + BEVEL_DIAL_CLOCKING - INPUT_CLOCKING / 2 - 36 * (position + CLEARING_ZERO_INDEX) for phase, position in
        zip(phases, dial_positions(*values, len(phases), counter)))


def neutral_operation(source, targets):
    return lambda value: (0, 0, 0)


class ResultDials(source.ResultRegister):
    """The physical dial bank, independent of the pose calculator's inputs."""
    p_10203_1 = Part10203_1(turn=Revolute(
        axis=(-0.9999539409, -0.0095977127, 2e-10), at=(72.008486542, 0.647810225, 33.9)))
    p_10203_2 = Part10203_2(turn=Revolute(
        axis=(-0.9429319505, 0.3329854904, 1e-10), at=(67.932893459, -23.838001321, 33.9)))
    p_10205_1 = Part10205_1(turn=Revolute(
        axis=(-0.7721784508, 0.6354057288, 0.0), at=(55.72844801, -45.453202839, 33.9)))
    p_10205_2 = Part10205_2(turn=Revolute(
        axis=(-0.5082888339, 0.8611866588, 0.0), at=(36.867186359, -61.590682021, 33.9)))
    p_10204_1 = Part10204_1(turn=Revolute(
        axis=(-0.183092082, 0.9830957682, 0.0), at=(13.624055025, -70.304020713, 33.9)))
    p_10204_2 = Part10204_2(turn=Revolute(
        axis=(0.164188277, 0.9864290191, 0.0), at=(-11.197481322, -70.542261674, 33.9)))
    p_10204_3 = Part10204_3(turn=Revolute(
        axis=(0.491665107, 0.870784372, 0.0), at=(-34.603579072, -62.276669529, 33.9)))
    p_10204_4 = Part10204_4(turn=Revolute(
        axis=(0.759839869, 0.650110278, 0.0), at=(-53.771117399, -46.504196676, 33.9)))
    p_10204_5 = Part10204_5(turn=Revolute(
        axis=(0.9363667283, 0.3510232901, 0.0), at=(-66.388208297, -25.127236119, 33.9)))
    p_10204_6 = Part10204_6(turn=Revolute(
        axis=(0.9999539409, 0.009597713, 0.0), at=(-70.933044396, -0.724164791, 33.9)))
    results_dial_type_2_1 = FittedDialType2(turn=Revolute(
        axis=(0.9429319507, -0.3329854896, 1e-10), at=(-66.857451389, 23.761646754, 33.9)))

    # These fifteen pin-and-dial assemblies carry native source coordinates
    # inside their children. Matching full frames preserves those placements.
    p_10203_1_seat = Frame(at=(72.008486542, 0.647810225, 33.9),
                         z=(-0.9999539409, -0.0095977127, 2e-10), x=(0, 0, 1))
    p_10203_2_seat = Frame(at=(67.932893459, -23.838001321, 33.9),
                         z=(-0.9429319505, 0.3329854904, 1e-10), x=(0, 0, 1))
    p_10205_1_seat = Frame(at=(55.72844801, -45.453202839, 33.9),
                         z=(-0.7721784508, 0.6354057288, 0), x=(0, 0, 1))
    p_10205_2_seat = Frame(at=(36.867186359, -61.590682021, 33.9),
                         z=(-0.5082888339, 0.8611866588, 0), x=(0, 0, 1))
    p_10204_1_seat = Frame(at=(13.624055025, -70.304020713, 33.9),
                         z=(-0.183092082, 0.9830957682, 0), x=(0, 0, 1))
    p_10204_2_seat = Frame(at=(-11.197481322, -70.542261674, 33.9),
                         z=(0.164188277, 0.9864290191, 0), x=(0, 0, 1))
    p_10204_3_seat = Frame(at=(-34.603579072, -62.276669529, 33.9),
                         z=(0.491665107, 0.870784372, 0), x=(0, 0, 1))
    p_10204_4_seat = Frame(at=(-53.771117399, -46.504196676, 33.9),
                         z=(0.759839869, 0.650110278, 0), x=(0, 0, 1))
    p_10204_5_seat = Frame(at=(-66.388208297, -25.127236119, 33.9),
                         z=(0.9363667283, 0.3510232901, 0), x=(0, 0, 1))
    p_10204_6_seat = Frame(at=(-70.933044396, -0.724164791, 33.9),
                         z=(0.9999539409, 0.009597713, 0), x=(0, 0, 1))
    # Full triad from the source's 109.481790438-degree rotation about
    # (.706968432, .500097809, .500097809), retaining its roll as well as axis.
    results_dial_type_2_1_seat = Frame(
        at=(-66.857451389, 23.761646754, 33.9),
        x=(0.33298548958242147, 0.9429319507406433, -1.0063722077902071e-10),
        z=(0.9429319507406433, -0.33298548958242147, 1.4226686495533158e-10))

    p_10203_1_mount = p_10203_1.axle.on(p_10203_1_seat, p_10203_1.turn)
    p_10203_2_mount = p_10203_2.axle.on(p_10203_2_seat, p_10203_2.turn)
    p_10205_1_mount = p_10205_1.axle.on(p_10205_1_seat, p_10205_1.turn)
    p_10205_2_mount = p_10205_2.axle.on(p_10205_2_seat, p_10205_2.turn)
    p_10204_1_mount = p_10204_1.axle.on(p_10204_1_seat, p_10204_1.turn)
    p_10204_2_mount = p_10204_2.axle.on(p_10204_2_seat, p_10204_2.turn)
    p_10204_3_mount = p_10204_3.axle.on(p_10204_3_seat, p_10204_3.turn)
    p_10204_4_mount = p_10204_4.axle.on(p_10204_4_seat, p_10204_4.turn)
    p_10204_5_mount = p_10204_5.axle.on(p_10204_5_seat, p_10204_5.turn)
    p_10204_6_mount = p_10204_6.axle.on(p_10204_6_seat, p_10204_6.turn)
    results_dial_type_2_1_mount = results_dial_type_2_1.axle.on(
        results_dial_type_2_1_seat, results_dial_type_2_1.turn)

    def render(self):
        # The bare type-2 dial's source placement is now its mate's rest pose.
        self.translate(tuple(-value for value in CARRIAGE_CENTER))
        self.rotate(-CARRIAGE_CLOCKING, (0, 0, 1))


class ResultRegister(ResultDials):
    value = Port()
    operand = Port()
    crank_turns = Port(unit='rev')
    subtract = Port()
    carriage_position = Port()
    clear = Port()

    (value & operand & crank_turns & subtract & carriage_position & clear).drives((
        ResultDials.p_10203_1.turn,
        ResultDials.p_10203_2.turn,
        ResultDials.p_10205_1.turn,
        ResultDials.p_10205_2.turn,
        ResultDials.p_10204_1.turn,
        ResultDials.p_10204_2.turn,
        ResultDials.p_10204_3.turn,
        ResultDials.p_10204_4.turn,
        ResultDials.p_10204_5.turn,
        ResultDials.p_10204_6.turn,
        ResultDials.results_dial_type_2_1.turn,
    ), law=dial_values((3.0, -86.99999999, -126.4500831, -146.45008308, -166.45008308, -186.45008307, -206.45008308, -226.45008311, -246.45008311, -266.4500831, 3.00000002)))

class TurnsDials(source.TurnsRegister):
    """The six physical counter dials, with the same source placements."""
    p_10203_3 = Part10203_3(turn=Revolute(
        axis=(0.650110279, -0.7598398681, 3e-10), at=(-45.928298358, 54.270661151, 33.9)))
    p_10203_4 = Part10203_4(turn=Revolute(
        axis=(0.3510232907, -0.936366728, 0.0), at=(-24.5513378, 66.887752049, 33.9)))
    p_10205_3 = Part10205_3(turn=Revolute(
        axis=(0.009597713, -0.9999539409, 0.0), at=(-0.148266473, 71.432588148, 33.9)))
    p_10205_4 = Part10205_4(turn=Revolute(
        axis=(-0.3329854899, -0.9429319506, 0.0), at=(24.337545072, 67.35699514, 33.9)))
    p_10204_7 = Part10204_7(turn=Revolute(
        axis=(-0.6354057288, -0.7721784508, 0.0), at=(45.952746591, 55.152549691, 33.9)))
    results_dial_type_2_2 = FittedDialType2(turn=Revolute(
        axis=(-0.8611866588, -0.508288834, -0.0), at=(62.090225773, 36.291288041, 33.9)))

    p_10203_3_seat = Frame(at=(-45.928298358, 54.270661151, 33.9),
                         z=(0.650110279, -0.7598398681, 3e-10), x=(0, 0, 1))
    p_10203_4_seat = Frame(at=(-24.5513378, 66.887752049, 33.9),
                         z=(0.3510232907, -0.936366728, 0), x=(0, 0, 1))
    p_10205_3_seat = Frame(at=(-0.148266473, 71.432588148, 33.9),
                         z=(0.009597713, -0.9999539409, 0), x=(0, 0, 1))
    p_10205_4_seat = Frame(at=(24.337545072, 67.35699514, 33.9),
                         z=(-0.3329854899, -0.9429319506, 0), x=(0, 0, 1))
    p_10204_7_seat = Frame(at=(45.952746591, 55.152549691, 33.9),
                         z=(-0.6354057288, -0.7721784508, 0), x=(0, 0, 1))
    # Source rotation: 104.232401654 degrees about
    # (.778024743, -.444228263, -.444228263).
    results_dial_type_2_2_seat = Frame(
        at=(62.090225773, 36.291288041, 33.9),
        x=(0.5082888340098916, -0.8611866587568948, -2.5516422308413667e-11),
        z=(-0.8611866587568948, -0.5082888340098918, -4.468977965466081e-11))

    p_10203_3_mount = p_10203_3.axle.on(p_10203_3_seat, p_10203_3.turn)
    p_10203_4_mount = p_10203_4.axle.on(p_10203_4_seat, p_10203_4.turn)
    p_10205_3_mount = p_10205_3.axle.on(p_10205_3_seat, p_10205_3.turn)
    p_10205_4_mount = p_10205_4.axle.on(p_10205_4_seat, p_10205_4.turn)
    p_10204_7_mount = p_10204_7.axle.on(p_10204_7_seat, p_10204_7.turn)
    results_dial_type_2_2_mount = results_dial_type_2_2.axle.on(
        results_dial_type_2_2_seat, results_dial_type_2_2.turn)

    def render(self):
        # The bare type-2 dial's source placement is now its mate's rest pose.
        self.translate(tuple(-value for value in CARRIAGE_CENTER))
        self.rotate(-CARRIAGE_CLOCKING, (0, 0, 1))


class TurnsRegister(TurnsDials):
    value = Port()
    operand = Port()
    crank_turns = Port(unit='rev')
    subtract = Port()
    carriage_position = Port()
    clear = Port()

    (value & operand & crank_turns & subtract & carriage_position & clear).drives((
        TurnsDials.p_10203_3.turn,
        TurnsDials.p_10203_4.turn,
        TurnsDials.p_10205_3.turn,
        TurnsDials.p_10205_4.turn,
        TurnsDials.p_10204_7.turn,
        TurnsDials.results_dial_type_2_2.turn,
    ), law=dial_values((3.00000002, 3.00000001, 3.5499169, -16.45008308, -36.4500831, 3.00000002), counter=True))


class RegisterBench(AssemblyNode):
    result = Driver(default=0, range=(0, 99999999999), dtype=int)
    operand = Driver(default=1, range=(0, 99999999), dtype=int)
    crank_turns = Driver(default=0, range=(0, 1), unit='rev')
    registers = ResultRegister()
    result.drives(registers.value)
    operand.drives(registers.operand)
    crank_turns.drives(registers.crank_turns)
    result.drives((registers.subtract, registers.carriage_position, registers.clear), law=neutral_operation)
