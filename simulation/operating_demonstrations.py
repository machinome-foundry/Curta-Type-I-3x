"""Named physical-action replays, separate from ordinary operating controls.

Start from a documented fresh-machine snapshot. No step edits a register,
changes a previous operand, or automatically prepares another control. Positive
durations make the motion available to the caller's normal geometry sampler.
This module does not certify all contacts or replace the legacy posed demos.
"""

from dataclasses import dataclass

from simulation.running import register_reading


@dataclass(frozen=True)
class Step:
    input: str
    kind: str
    value: float
    duration: float
    expected: tuple[int, int] | None = None


def _set(name, value, expected=None):
    return Step(name, 'to', value, .2, expected)


def _turn(result, counter):
    return Step('crank_rotation', 'by', 360, 2, (result, counter))


DEMONSTRATIONS = {
    'addition': (_set('digit_1', 3), _turn(3, 1),
                 _set('digit_1', 2, (3, 1)), _turn(5, 2)),
    'carry': (_set('digit_1', 9), _turn(9, 1),
              _set('digit_1', 1, (9, 1)), _turn(10, 2)),
    # Borrowing one from zero prepares both nines banks mechanically.
    # The second turn then demonstrates the full carry cascade to zero.
    'overflow': (_set('digit_1', 1), _set('crank_elevation', 9),
                 _turn(10**11-1, 10**6-1), _set('crank_elevation', 0),
                 _turn(0, 0)),
    'subtraction': (_set('digit_1', 3), _turn(3, 1),
                    _set('digit_1', 2), _set('crank_elevation', 9), _turn(1, 0)),
    'shift': (_set('digit_1', 9), _turn(9, 1),
              _set('carriage_elevation', 6, (9, 1)),
              _set('carriage_rotation', 40, (9, 1)),
              _set('carriage_elevation', 0), _set('digit_1', 3), _turn(309, 101)),
    'clearing': (_set('digit_1', 3), _turn(3, 1),
                 _set('carriage_elevation', 6, (3, 1)),
                 Step('clearing_rotation', 'by', 180, 1, (0, 1)),
                 Step('clearing_rotation', 'by', 180, 1, (0, 0)),
                 Step('clearing_rotation', 'by', -360, 2, (0, 0)),
                 _set('carriage_elevation', 0, (0, 0))),
}


def replay(sim, name, initial_snapshot):
    """Restore caller-owned fixture setup, replay requests, check each outcome.

The snapshot must belong to this same program and timestep and represent the
fresh machine. ``Sim.restore`` verifies compatibility. Ordinary operation does
not call this helper. Callers can attach ``sim.every`` geometry checks before
replay; they run during every timed action, not just at the final readout.
"""
    steps = DEMONSTRATIONS[name]
    sim.restore(initial_snapshot)
    if register_reading(sim) != 0 or register_reading(sim, True) != 0:
        raise ValueError('Demonstrations require the documented fresh-machine snapshot')
    results = []
    for step in steps:
        command = sim.move(step.input, **{step.kind: step.value}, duration=step.duration)
        sim.run(step.duration)
        if command.status != 'completed':
            raise AssertionError((name, step.input, step.value, command.status))
        readings = (register_reading(sim), register_reading(sim, True))
        if step.expected is not None and readings != step.expected:
            raise AssertionError((name, step.input, readings, step.expected))
        results.append((step.input, command.status, readings))
    return results
