"""Input constraints and source geometry for the clocked operating surface.

Operation is a geometry-free kinematic control frame. Its bounded coordinates
feed the existing physical joints, so the request stops and the drawn motion
share one value. It retains nothing; memory belongs to the root's States.
"""

from solid_node.node import AssemblyNode
from solid_node.motion.ports import Port
from solid_node.motion.joints import Bound, Revolute, Prismatic
from simulation.clocked_laws import at_rest, at_check, ratchet_floor
from simulation.assemblies import Carriage as SourceCarriage
from simulation.mechanism import RegisterCarriage
from simulation.positioning import CarriagePositioning
from simulation.running_parts import RunningClearingAssembly, RESULT_DIALS, TURNS_DIALS
from simulation.registers import ResultDials, TurnsDials
from simulation.clocked_laws import posed_dials


def clearing_latch(sources, targets):
    return lambda crank, ring: (1 - at_check(ring)) * (1 - at_rest(crank))


class Operation(AssemblyNode):
    crank = Revolute(axis=(0, 0, 1), range=(ratchet_floor, None))
    crank_lift = Prismatic(axis=(0, 0, 1), range=(
        Bound(lambda own, crank: own * (1 - at_rest(crank)), reads=(crank,)),
        Bound(lambda own, crank: own + (9 - own) * at_rest(crank), reads=(crank,))))
    ring = Revolute(axis=(0, 0, 1))
    carriage_lift = Prismatic(axis=(0, 0, 1), range=(
        Bound(lambda own, crank, ring: own * (1 - at_rest(crank) * at_check(ring)),
              reads=(crank, ring)),
        Bound(lambda own, crank, ring: own + (6 - own) * at_rest(crank) * at_check(ring),
              reads=(crank, ring))))
    carriage_turn = Revolute(axis=(0, 0, 1), range=(
        Bound(lambda own, lift, crank: own * (1 - (lift >= 6) * at_rest(crank)),
              reads=(carriage_lift, crank)),
        Bound(lambda own, lift, crank: own + (100 - own) * (lift >= 6) * at_rest(crank),
              reads=(carriage_lift, crank))))
    # The two controls cannot simultaneously leave their rest checks. The
    # witness stays zero on every legal pose; it places no physical body.
    ring_latch = Revolute(axis=(0, 0, 1), range=(0, 0))
    (crank & ring).drives(ring_latch, law=clearing_latch)

    def render(self):
        return []


class ResultPose(ResultDials):
    value = Port()
    operand = Port()
    crank_turns = Port()
    subtract = Port()
    carriage_position = Port()
    clear = Port()
    ring = Port()
    anchor = Port()
    elevation = Port()
    (value & operand & crank_turns & subtract & carriage_position & clear &
     ring & anchor & elevation).drives(tuple(getattr(ResultDials, name).turn
        for name, zero in RESULT_DIALS), law=posed_dials(RESULT_DIALS))


class TurnsPose(TurnsDials):
    value = Port()
    operand = Port()
    crank_turns = Port()
    subtract = Port()
    carriage_position = Port()
    clear = Port()
    ring = Port()
    anchor = Port()
    elevation = Port()
    (value & operand & crank_turns & subtract & carriage_position & clear &
     ring & anchor & elevation).drives(tuple(getattr(TurnsDials, name).turn
        for name, zero in TURNS_DIALS), law=posed_dials(TURNS_DIALS, True))


class ClockedRegisterCarriage(RegisterCarriage):
    result_register = ResultPose()
    turns_register = TurnsPose()
    clearing_ring = RunningClearingAssembly(turn=Revolute(axis=(0, 0, 1)))


class ClockedCarriage(SourceCarriage):
    position = Port()
    lift = Port()
    clear = Port()
    ring = Port()
    positioning = CarriagePositioning()
    registers = ClockedRegisterCarriage(turn=Revolute(axis=(0, 0, 1)),
                                        lift=Prismatic(axis=(0, 0, 1)))
    position.drives(registers.turn, ratio=20)
    lift.drives(registers.lift, ratio=6)
    registers.lift.drives(positioning.lift)
    ring.drives(registers.clearing_ring.turn, ratio=-1)
