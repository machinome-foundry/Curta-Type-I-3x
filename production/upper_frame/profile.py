from machinome.model import Reference
from machinome.production.instruction import Markdown, Step
from machinome.production.item import Item
from machinome.production.process import Sourced
from machinome.production.profile import Production
from production.catalogue import M4_NUT
from simulation.mechanism import UpperFrame


class UpperFrameNuts(Production[UpperFrame]):
    nuts = Item(
        tuple(Reference(UpperFrame, (f"m4_nut_{index}",)) for index in range(1, 4)),
        Sourced(M4_NUT),
    )
    assemble = Step(nuts, instructions=Markdown("assembly.md"))
