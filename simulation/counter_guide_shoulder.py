"""Local counter-shoulder relief; independent of the operating assembly."""

from machinome.parameters import Length
from simulation.carry_heads import TurnsSlider
from simulation.counter_guide_regions import in_counter_station, region


class ShoulderClearedTurnsSlider(TurnsSlider):
    shoulder_relief = Length(.35)

    def adjust(self, shape):
        fitted = super().adjust(shape)
        # Measured underside is -12.90 at rest; the guide ledge is -16.80
        # and travel is 4.20. Raise this underside only, leaving .05 gap.
        cutter = region((60.275, -7.95, -12.95),
                        (61.80, -6.35, -12.90 + self.shoulder_relief))
        return fitted.cut(in_counter_station(cutter, inverse=True))
