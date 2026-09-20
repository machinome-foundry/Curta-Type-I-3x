"""Diagnostic loop/mount bench; no deployment motion is adopted yet.

The two independent pose inputs permit probing clipping and neighbouring
obstructions. A swivel about the source's first clip is a hypothesis, not
an operating hinge or an assertion that this printed loop folds in place.
"""

from machinome.node import AssemblyNode
from machinome.motion.joints import Prismatic, Revolute
from machinome.motion.ports import Port
from machinome.simulation import Driver
from simulation.standard.parts import ClearingRing
from simulation.standard.layers import CrankAssembly
from simulation.mechanism import ClearingAssembly, CarriageCovers
from simulation.running_parts import RetainedCarriageStructure
from simulation.clearing_stop_motion import PIN_DROP


class ProbeLoop(ClearingRing):
    # These coordinates belong to the source part, not the assembly site.
    swivel = Revolute(axis=(0, 0, -1), at=(40.5, 0, 0))
    rise = Prismatic(axis=(0, 0, -1))


class LoopMountAssembly(ClearingAssembly):
    deployment = Port(unit='deg')
    release_height = Port(unit='mm')
    clearing_ring = ProbeLoop()
    deployment.drives(clearing_ring.swivel)
    release_height.drives(clearing_ring.rise)


class LoopMountBench(AssemblyNode):
    deployment = Driver(default=0, unit='deg')
    release_height = Driver(default=0, unit='mm')
    loop = LoopMountAssembly()
    carrier = RetainedCarriageStructure()
    covers = CarriageCovers()
    crank = CrankAssembly()
    deployment.drives(loop.deployment)
    release_height.drives(loop.release_height)
    release_height.drives(carrier.upper_carriage_body_1.press, ratio=0, offset=PIN_DROP[0][1])
