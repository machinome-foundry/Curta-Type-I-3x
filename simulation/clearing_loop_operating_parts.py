"""Independent deployment of the explicitly simulation-only captive mounting."""

from machinome.node.frames import Frame
from machinome.motion.joints import Revolute
from machinome.motion.ports import Port
from simulation.running_parts import RunningClearingAssembly, RetainedCarriage
from simulation.source_frames import source_frame
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


class FramedOperatingClearingLoop(OperatingClearingLoop):
    datum = Frame()


class FramedOperatingLoopMount(OperatingLoopMount):
    loop_seat = source_frame(at=(50.343540869, -28.04260917, 62.56 + .05),
                             angle=180, axis=(.603780106, .797150916, 0))
    clearing_ring = FramedOperatingClearingLoop()
    loop_mount = clearing_ring.datum.on(loop_seat, clearing_ring.swivel)

    def render(self):
        # The intrinsic swivel acts in the loop's source frame. The mate only
        # replaces its fixed attachment; all unchanged cover/fastener seats stay.
        self.m4x10_419010_1.rotate(47.531056002, (-.129842301, .94068028, .313467044))
        self.m4x10_419010_1.translate((43.908248282, 12.219569698, 45.574328291))
        self.clearing_ring_rivet_1.rotate(-74.282220532, (0, 0, 1))
        self.clearing_ring_rivet_1.translate((39.372124643, 10.943003894, 50.5))
        self.clearing_ring_rivet_2.rotate(-74.282220532, (0, 0, 1))
        self.clearing_ring_rivet_2.translate((37.348717788, -16.582726336, 50.5))
        self.clearing_ring_rivet_1.translate((0, 0, MOUNT_SHOULDER_GAP))
        self.clearing_ring_rivet_2.translate((0, 0, MOUNT_SHOULDER_GAP))
        self.clearing_cover.rotate(180, (.797150916, -.603780106, 0))
        self.clearing_cover.translate((0, 0, 57.1))
        self.tooth_stack.rotate(180, (.797150916, -.603780106, 0))
        self.tooth_stack.translate((0, 0, 57.1))


class LoopRetainedCarriage(RetainedCarriage):
    # Both complete assemblies already share the central shaft's Z datum.
    # Their internal fitted placements and independent freedoms stay intact.
    spindle = Frame()
    clearing_seat = Frame()
    clearing_ring = FramedOperatingLoopMount(turn=Revolute(axis=(0, 0, 1)))
    clearing_mount = clearing_ring.spindle.on(clearing_seat, clearing_ring.turn)
