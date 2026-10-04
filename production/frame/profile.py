from machinome.model import Reference
from machinome.production.instruction import Markdown, Step
from machinome.production.item import Item
from machinome.production.process import Sourced
from machinome.production.profile import Production
from production.catalogue import M4_NUT
from simulation.standard.layers import FrameFasteners


class FrameNuts(Production[FrameFasteners]):
    nuts = Item(
        tuple(Reference(FrameFasteners, (f"m4_nut_{index}",)) for index in range(1, 5)),
        Sourced(M4_NUT),
    )
    assemble = Step(nuts, instructions=Markdown("assembly.md"))
