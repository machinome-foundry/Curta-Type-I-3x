"""Four real crank occurrences; two retain existing simulation fit edits."""

from machinome.model import Reference
from machinome.production.instruction import Markdown, Step
from machinome.production.item import Item
from machinome.production.process import Printed
from machinome.production.profile import Production
from simulation.standard.layers import CrankAssembly


class CrankDraft(Production[CrankAssembly]):
    pin = Item(Reference(CrankAssembly, ("crank_handle_pin",)), Printed())
    pin_screw = Item(
        Reference(CrankAssembly, ("crank_handle_1", "crank_handle_pin_screw")),
        Printed(),
    )
    crank = Item(Reference(CrankAssembly, ("crank_handle_1", "main_crank")), Printed())
    handle = Item(Reference(CrankAssembly, ("crank_handle_1", "crank_handle")), Printed())

    print_pin = Step(pin, instructions=Markdown("pin.md"))
    thread_pin = Step(pin_screw, instructions=Markdown("thread-pin.md"))
    fitted_parts = Step(crank, handle, instructions=Markdown("existing-fits.md"))
    assemble = Step(pin, pin_screw, crank, handle, instructions=Markdown("assembly.md"))
