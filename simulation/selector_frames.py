"""Source-backed connector datums for the eight input selectors.

The bottom shaft is a local-origin leaf. Top-shaft/number-roll and knob
assemblies retain their native source coordinates, so their connector
frames name their source shaft line. Shapes and internal placements stay
in standard.assembly and standard.parts.
"""

from machinome.node.frames import Frame
from simulation.standard import assembly as source


class SelectorShaftBottom(source.SelectorShaftBottom):
    axle = Frame()


class SelectorShaftTop1_419054(source.SelectorShaftTop1_419054):
    axle = Frame(at=(58.5, 0.0, -127.8))


class SelectorKnob1_419057(source.SelectorKnob1_419057):
    guide = Frame(at=(58.5, 0.0, -69.725), z=(0, 0, -1))


class SelectorShaftTop1_419153(source.SelectorShaftTop1_419153):
    axle = Frame(at=(54.972018316, -20.008178385, -127.8))


class SelectorKnob1_419152(source.SelectorKnob1_419152):
    guide = Frame(at=(54.972018316, -20.008178385, -69.725), z=(0, 0, -1))


class SelectorShaftTop1_419224(source.SelectorShaftTop1_419224):
    axle = Frame(at=(44.813599922, -37.603075167, -127.8))


class SelectorKnob1_419225(source.SelectorKnob1_419225):
    guide = Frame(at=(44.813599922, -37.603075167, -69.725), z=(0, 0, -1))


class SelectorShaftTop1_419083(source.SelectorShaftTop1_419083):
    axle = Frame(at=(29.25, -50.662486121, -127.8))


class SelectorKnob1_419084(source.SelectorKnob1_419084):
    guide = Frame(at=(29.25, -50.662486121, -69.725), z=(0, 0, -1))


class SelectorShaftTop1_419178(source.SelectorShaftTop1_419178):
    axle = Frame(at=(10.158418394, -57.611253551, -127.8))


class SelectorKnob1_419177(source.SelectorKnob1_419177):
    guide = Frame(at=(10.158418394, -57.611253551, -69.725), z=(0, 0, -1))


class SelectorShaftTop1_419142(source.SelectorShaftTop1_419142):
    axle = Frame(at=(-10.158418394, -57.611253551, -127.8))


class SelectorKnob1_419141(source.SelectorKnob1_419141):
    guide = Frame(at=(-10.158418394, -57.611253551, -69.725), z=(0, 0, -1))


class SelectorShaftTop1_419103(source.SelectorShaftTop1_419103):
    axle = Frame(at=(-29.25, -50.662486121, -127.8))


class SelectorKnob1_419102(source.SelectorKnob1_419102):
    guide = Frame(at=(-29.25, -50.662486121, -69.725), z=(0, 0, -1))


class SelectorShaftTop1_419156(source.SelectorShaftTop1_419156):
    axle = Frame(at=(-44.813599922, -37.603075167, -127.8))


class SelectorKnob1_419155(source.SelectorKnob1_419155):
    guide = Frame(at=(-44.813599922, -37.603075167, -69.725), z=(0, 0, -1))

