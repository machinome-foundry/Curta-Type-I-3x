"""Incremental tooth passages and real-part carry latches for the running Curta.

Profiles and phase datums come from the existing measured contact benches.
No total operand, completed-turn count or arithmetic register enters a law.
"""

from math import degrees
from machinome.math import floor, clamp01, max, piecewise
from simulation.cycle import (tooth_passage, RESULT_INPUT_END, TURNS_INPUT_END,
                              RESULT_CARRY_END, TURNS_CARRY_END)
from simulation.carry_profiles import PIN_DROP, RESET_LIFT
from simulation.running_parts import RESULT_DIALS, TURNS_DIALS
from simulation.fit import INPUT_CLOCKING
from simulation.reverser_modes import counter_count
from simulation.result_modes import result_count


def phase(angle):
    return angle - 360 * floor(angle / 360)


def aligned(turn, shift):
    """Mutually exclusive detent selection, in the carriage joint's degrees."""
    return (turn >= 20 * shift - 10) * (turn < 20 * shift + 10)


def shaft_motion(channel, counter=False, lever_rest=0):
    def law(sources, target):
        def advance(crank, elevation, setting, latch):
            # Source crank clockwise is negative about +Z. Complementary drum
            # rows reach the input gears after the measured 9 mm lift.
            angle = phase(-crank)
            if counter:
                count = counter_count(channel, setting+.0925, elevation)
            else:
                entered = setting / 36 if channel < 8 else 0
                count = result_count(channel, entered, elevation)
            direct = tooth_passage(angle, count,
                                   (TURNS_INPUT_END if counter else RESULT_INPUT_END) + 20 * channel)
            carried = (tooth_passage(angle, 1,
                                    (TURNS_CARRY_END if counter else RESULT_CARRY_END) + 20 * channel)
                       * (latch - lever_rest >= 4.2 * .61)) if channel else 0
            return (130 if counter else 0) + INPUT_CLOCKING - 20 * channel + 72 * (direct + carried)
        return advance
    return law


def dial_motion(place, counter=False):
    zero = (TURNS_DIALS if counter else RESULT_DIALS)[place][1]
    def law(sources, target):
        def advance(carriage_turn, carriage_lift, ring, own, *shafts):
            driven = -.5 * sum(
                (shaft - ((130 if counter else 0) + INPUT_CLOCKING - 20 * channel))
                * aligned(carriage_turn, place - channel)
                             for channel, shaft in enumerate(shafts)
                             if 0 <= place - channel <= 5) * (carriage_lift < 3)
            return zero + driven + clearing_travel(
                ring, carriage_lift, own, zero, place, counter)
        return advance
    return law


def clearing_travel(ring, lift, own, zero, place, counter=False):
    """Nine actual rack teeth, acting only outside the zero-capture band.

    The +/-0.5-degree band is inside the measured missing-tooth clearance
    of BOTH fitted rows; +1 degree meets a tooth. It is a prescribed capture band,
    not a claim to simulate the spider spring's settling forces.
    """
    outer = place < 2
    station = (130 if counter else 0) - 20 * place
    datum = 0 if outer else -40
    start = (9.75 if outer else 10.5) + (datum - station) % 360
    pitch = degrees(3.75 / (52 if outer else 49.55))
    passage = clamp01(phase(-ring - start) / (9 * pitch))
    raised = lift >= 6
    # With the carriage seated, the own-read level is constant as well as
    # its contribution: ordinary arithmetic must not meet a clearing stop.
    # An inactive level is deliberately inside the gap, not on one of its
    # surfaces. It introduces no physical tolerance or alternative stop.
    engaged = phase(raised * (zero - own + .5) + (1 - raised) * .5) >= 1
    return -324 * passage * raised * engaged


def lever_motion(channel, rest, counter=False):
    dials = TURNS_DIALS if counter else RESULT_DIALS
    offset = (50 if counter else 0) + 20 * (channel - 1)

    def law(sources, target):
        def travel(crank, carriage_turn, carriage_lift, own, *wheels):
            selected = sum(
                (zero - wheel) * aligned(carriage_turn, place - channel + 1)
                for place, ((_, zero), wheel) in enumerate(zip(dials, wheels))
                if 0 <= place - channel + 1 <= 5)
            position = phase(selected) / 36
            pin = piecewise(position, PIN_DROP)
            # Same measured vertical release as the contact bench: lifting
            # the carriage withdraws the pin one millimetre per millimetre.
            approach = max(0, pin - carriage_lift)
            drop = max(approach,
                       4.2 * clamp01((position - 9.3) / .1) * (carriage_lift < 3))
            # The reset surface straddles 360 degrees at some stations. Put
            # its wrap on the dwell, never through the measured lifting flank.
            cam = phase(-crank - offset - 180) + 180
            lift = piecewise(cam, RESET_LIFT)
            reset = lift + (4.2 - lift) * clamp01((lift - 1.65) / .2)
            # The endpoint dwells have zero slope. Excluding them leaves
            # identical travel (their jumps move nothing), and keeps the
            # moving pin stop out of the reset law while no cam flank acts.
            resetting = (cam >= RESET_LIFT[0][0]) * (cam < 356)
            return (drop * (own < rest + 4.2)
                    - reset * (resetting * (own - rest - approach) - (1 - resetting) > 0))
        return travel
    return law


def reading(dials):
    def law(sources, target):
        return lambda *angles: sum(
            (floor((zero - angle) / 36 + .5) % 10) * 10 ** place
            for place, ((_, zero), angle) in enumerate(zip(dials, angles)))
    return law
