"""Partial Curta3x assets; adding them never registers a production on the model."""

from machinome.model import Reference
from machinome.production.instruction import Markdown, Step
from machinome.production.profile import Production
from production.upper_frame.profile import UpperFrameNuts
from production.carry.profile import ResultWireNotes, TurnsWireNotes
from production.crank.profile import CrankDraft
from production.frame.profile import FrameNuts
from simulation.mechanistic import MechanisticCurta


class CurtaDraft(Production[MechanisticCurta]):
    crank = CrankDraft(Reference(MechanisticCurta, ("main_drive", "crank")))
    frame_nuts = FrameNuts(Reference(MechanisticCurta, ("frame", "fasteners")))
    upper_frame_nuts = UpperFrameNuts(Reference(MechanisticCurta, ("frame", "upper_frame")))
    result_wires = ResultWireNotes(Reference(MechanisticCurta, ("carry_mechanism", "result_carries")))
    turns_wires = TurnsWireNotes(Reference(MechanisticCurta, ("carry_mechanism", "turns_carries")))
    limitations = Step(crank, frame_nuts, upper_frame_nuts, result_wires, turns_wires,
                       instructions=Markdown("limitations.md"))


class ControlledReview(Production[MechanisticCurta]):
    """Regression asset, not an author-approved second manufacturing workshop."""
    crank = CrankDraft(Reference(MechanisticCurta, ("main_drive", "crank")))
    frame_nuts = FrameNuts(Reference(MechanisticCurta, ("frame", "fasteners")))
    upper_frame_nuts = UpperFrameNuts(Reference(MechanisticCurta, ("frame", "upper_frame")))
    result_wires = ResultWireNotes(Reference(MechanisticCurta, ("carry_mechanism", "result_carries")))
    turns_wires = TurnsWireNotes(Reference(MechanisticCurta, ("carry_mechanism", "turns_carries")))
    limitations = Step(crank, frame_nuts, upper_frame_nuts, result_wires, turns_wires,
                       instructions=Markdown("controlled-review.md"))
