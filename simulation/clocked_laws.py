"""Clocked register arithmetic and the measured clearing-rack event surfaces."""

from math import degrees
from machinome.math import floor, min, max, clamp
from simulation.arithmetic import digit, modulo
from simulation.cycle import dial_positions

RESULT_PLACES = 11
TURNS_PLACES = 6


def ratchet_floor(own):
    """Last represented tooth, without an unstable angle/pitch round trip.

    The own-read is frozen at the request's starting bank. Both selection
    and the returned stop use the SAME representable absolute angle, so a
    reverse landing cannot be classified behind that tooth on the next move.
    """
    base = 360 * floor(own / 360)
    stop = base
    for tooth in range(1, 117):
        offset = 357 * tooth / 116
        stop = max(stop, base + offset * (own >= base + offset))
    return stop

def at_rest(angle):
    return modulo(angle, 360) == 0


def at_check(angle):
    return (modulo(angle, 360) == 0) + (modulo(angle, 360) == 230)


def check_event(check, reverse=False):
    def factory(sources, targets):
        if reverse:
            return lambda ring: floor((check - ring) / 360)
        return lambda ring: floor((ring - check) / 360)
    return factory


def remember_check(sources, targets):
    return lambda angle: angle


def stroke(sources, targets):
    return lambda crank, *values: floor(crank / 360)


def advance(sources, targets):
    def law(crank, elevation, rotation, lift, *values):
        entered = sum(floor(value + .5) * 10 ** place
                      for place, value in enumerate(values[:8]))
        result = sum(value * 10 ** place for place, value in enumerate(values[8:19]))
        turns = sum(value * 10 ** place for place, value in enumerate(values[19:]))
        shift = 10 ** floor(rotation / 20 + .5)
        direction = (1 - 2 * (elevation >= 4.5)) * (lift < 3)
        result += direction * entered * shift
        turns += direction * shift
        return tuple(digit(result, place) for place in range(11)) + tuple(
            digit(turns, place) for place in range(6))
    return law


def rack(place, counter=False):
    outer = place < 2
    station = (130 if counter else 0) - 20 * place
    start = (9.75 if outer else 10.5) + ((0 if outer else -40) - station) % 360
    return start, degrees(3.75 / (52 if outer else 49.55))


def clearing_event(place, counter=False, reverse=False):
    start, pitch = rack(place, counter)
    def factory(sources, targets):
        if reverse:
            return lambda ring, lift, value: floor(
                (start + pitch * (9 - value) - ring) / 360)
        return lambda ring, lift, value: floor(
            (ring - start - pitch * (10 - value)) / 360)
    return factory


def cleared(sources, targets):
    return lambda ring, lift, value: value * (lift < 6)


def value_of(sources, targets):
    return lambda *values: sum(value * 10 ** place for place, value in enumerate(values))


def operand_of(sources, targets):
    return lambda *values: sum(floor(value + .5) * 10 ** place
                               for place, value in enumerate(values))


def phase(sources, targets):
    return lambda crank: modulo(crank / 360, 1)


def subtracting(sources, targets):
    return lambda elevation: elevation >= 4.5


def shift(sources, targets):
    return lambda rotation: floor(rotation / 20 + .5)


def rack_reach(ring, place, counter):
    start, pitch = rack(place, counter)
    offset = ring - start
    return 9 * floor(offset / 360) + min(modulo(offset, 360) / pitch, 9)


def posed_dials(table, counter=False):
    def factory(sources, targets):
        def law(value, operand, turns, subtract, shift, clear, ring, anchor, lift):
            positions = dial_positions(value, operand, turns * (lift < 3),
                                       subtract, shift, 0, len(table), counter)
            result = []
            for place, ((name, zero), position) in enumerate(zip(table, positions)):
                standing = digit(value, place)
                travel = rack_reach(ring, place, counter) - rack_reach(anchor, place, counter)
                clearing = clamp(travel, -standing, modulo(-standing, 10)) * (lift >= 6)
                result.append(zero - 36 * (position + clearing))
            return tuple(result)
        return law
    return factory
