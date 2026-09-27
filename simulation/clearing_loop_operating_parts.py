"""Independent deployment of the explicitly simulation-only captive mounting."""

from machinome.node import Frame
from machinome.motion.joints import Revolute
from machinome.motion.ports import Port
from simulation.running_parts import RunningClearingAssembly, RetainedCarriage
from simulation.clearing_loop_mounting import (
    CaptiveLoopShape, SimulationPivot, SimulationFlushPlug, MOUNT_SHOULDER_GAP,
)


class OperatingClearingLoop(CaptiveLoopShape):
    # Nominal stowed/deployed positions are 0/-90; retain measured end play.
    swivel = Revolute(axis=(0, 0, -1), at=(40.5, 0, 0), range=(-90.4, .4))


class OperatingLoopMount(RunningClearingAssembly):
    spindle = Frame()
    deployment = Port(unit='deg')
    clearing_ring = OperatingClearingLoop()
    clearing_ring_rivet_1 = SimulationPivot()
    clearing_ring_rivet_2 = SimulationFlushPlug()
    deployment.drives(clearing_ring.swivel, ratio=-1)

    def render(self):
        super().render()
        self.clearing_ring.translate((0, 0, .05))
        self.clearing_ring_rivet_1.translate((0, 0, MOUNT_SHOULDER_GAP))
        self.clearing_ring_rivet_2.translate((0, 0, MOUNT_SHOULDER_GAP))


class LoopRetainedCarriage(RetainedCarriage):
    # Both complete assemblies already share the central shaft's Z datum.
    # Their internal fitted placements and independent freedoms stay intact.
    spindle = Frame()
    clearing_seat = Frame()
    clearing_ring = OperatingLoopMount(turn=Revolute(axis=(0, 0, 1)))
    clearing_mount = clearing_ring.spindle.on(clearing_seat, clearing_ring.turn)
