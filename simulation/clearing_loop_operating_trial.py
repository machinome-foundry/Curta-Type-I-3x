"""Preserved independent declaration of the accepted full-root loop trial."""

from machinome.simulation import Driver, Turn
from simulation.running import ReverserOperatingCurta, RadialRunningCarriage
from simulation.clearing_loop_operating_parts import LoopRetainedCarriage


class LoopRunningCarriage(RadialRunningCarriage):
    registers = LoopRetainedCarriage()


class LoopOperatingTrial(ReverserOperatingCurta):
    carriage = LoopRunningCarriage()
    loop_deployment = Driver(default=0, range=(-.4, 90.4), unit='deg')
    loop_deployment.drives(carriage.registers.clearing_ring.deployment)
    controls = {
        **ReverserOperatingCurta.controls,
        'deploy loop (simulation-only mounting)': Turn(
            carriage.registers.clearing_ring.clearing_ring, loop_deployment,
            coordinate=carriage.registers.clearing_ring.clearing_ring.swivel),
    }
