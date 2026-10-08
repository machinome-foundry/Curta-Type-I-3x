from machinome.model import Reference
from machinome.production.instruction import Markdown, Step
from machinome.production.profile import Production
from simulation.carry_spring import MountedCarrySpring
from simulation.running_parts import RetainedResultCarries, RetainedTurnsCarries


class UnassignedWire(Production[MountedCarrySpring]):
    """The actual wire remains visible and unassigned, never bought by inference."""


class ResultWireNotes(Production[RetainedResultCarries]):
    springs = UnassignedWire(tuple(
        Reference(RetainedResultCarries, (f"results_tens_lever_assembly_{index}", "carry_lever_spring"))
        for index in range(1, 11)
    ))
    bend = Step(springs, instructions=Markdown("bend-results.md"))


class TurnsWireNotes(Production[RetainedTurnsCarries]):
    springs = UnassignedWire(tuple(
        Reference(RetainedTurnsCarries, (f"turns_tens_lever_assembly_{index}", "carry_lever_spring"))
        for index in range(1, 6)
    ))
    bend = Step(springs, instructions=Markdown("bend-turns.md"))
