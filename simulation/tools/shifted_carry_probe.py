"""Reduced changing carry association, not Curta geometry or a production law.

At shift zero the fixed carry lever reads the lower wheel and drives the
higher wheel. At shift one it reads the higher wheel; its driven wheel has
moved beyond this two-wheel fixture. No active position closes a drive loop.
The union of those mutually exclusive connections nevertheless has a cycle.
"""

from solid_node.node import AssemblyNode
from solid_node.motion.joints import Revolute, Prismatic
from solid_node.motion.ports import Time
from solid_node.simulation import Driver, Sim, UnsupportedLaw


class Shaft(AssemblyNode):
    turn = Revolute(axis=(0, 0, 1))

    def simulate(self):
        if self.turn.value is None:
            self.turn = 0


class Latch(AssemblyNode):
    travel = Prismatic(axis=(0, 0, 1))

    def simulate(self):
        if self.travel.value is None:
            self.travel = 0


class ShiftedCarry(AssemblyNode):
    time = Time.running()
    crank = Driver(default=0)
    shift = Driver(default=0)
    clearing = Driver(default=0)
    lower = Shaft()
    higher = Shaft()
    carry = Latch()
    (crank & shift & clearing & lower.turn).drives(lower.turn,
        law=lambda sources, target: lambda c, s, r, own:
        c * (s < .5) + r * (own > .5))
    (crank & shift & clearing & carry.travel & higher.turn).drives(higher.turn,
        law=lambda sources, target: lambda c, s, r, latch, own:
        c * (s >= .5) + c * (s < .5) * (latch >= .5) + r * (own > .5))
    (lower.turn & higher.turn & shift & carry.travel).drives(carry.travel,
        law=lambda sources, target: lambda lo, hi, s, own:
        (lo * (s < .5) + hi * (s >= .5)) * (own < 1))


def fixed_fixture(position):
    """The same connections, specialized to either mechanically active graph."""
    class FixedCarry(AssemblyNode):
        time = Time.running()
        crank = Driver(default=0)
        clearing = Driver(default=0)
        lower = Shaft()
        higher = Shaft()
        carry = Latch()

        if position == 0:
            (crank & clearing & lower.turn).drives(lower.turn,
                law=lambda sources, target: lambda c, r, own:
                c + r * (own > .5))
            (crank & clearing & carry.travel & higher.turn).drives(higher.turn,
                law=lambda sources, target: lambda c, r, latch, own:
                c * (latch >= .5) + r * (own > .5))
            (lower.turn & carry.travel).drives(carry.travel,
                law=lambda sources, target: lambda lo, own: lo * (own < 1))
        else:
            (clearing & lower.turn).drives(lower.turn,
                law=lambda sources, target: lambda r, own: r * (own > .5))
            (crank & clearing & higher.turn).drives(higher.turn,
                law=lambda sources, target: lambda c, r, own:
                c + r * (own > .5))
            (higher.turn & carry.travel).drives(carry.travel,
                law=lambda sources, target: lambda hi, own: hi * (own < 1))
    return FixedCarry()


def probe():
    for position in (0, 1):
        sim = Sim(fixed_fixture(position), dt=.02)
        command = sim.move('crank', by=2)
        print(f'Fixed position {position}: {command.status}, {sim.state}')
    try:
        Sim(ShiftedCarry(), dt=.02)
    except UnsupportedLaw as error:
        print(f'Live carriage selection: {type(error).__name__}: {error}')
        return False
    print('Live carriage selection: constructed')
    return True


if __name__ == '__main__':
    raise SystemExit(0 if probe() else 1)
