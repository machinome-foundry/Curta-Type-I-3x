"""Full-root adoption trial; the manifest still selects the unchanged root."""

from machinome.simulation import Driver, Turn
from simulation.running import OperatingCurta, RadialRunningCarriage
from simulation.clearing_loop_operating_parts import LoopRetainedCarriage


class LoopRunningCarriage(RadialRunningCarriage):
    registers = LoopRetainedCarriage()


class LoopOperatingTrial(OperatingCurta):
    carriage = LoopRunningCarriage()
    loop_deployment = Driver(default=0, range=(-.4, 90.4), unit='deg')
    loop_deployment.drives(carriage.registers.clearing_ring.deployment)
    controls = {
        **OperatingCurta.controls,
        'deploy loop (simulation-only mounting)': Turn(
            carriage.registers.clearing_ring.clearing_ring, loop_deployment,
            coordinate=carriage.registers.clearing_ring.clearing_ring.swivel),
    }
