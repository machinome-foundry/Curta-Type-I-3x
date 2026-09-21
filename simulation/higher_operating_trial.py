"""Historical T07 full-tree entry point, now inheriting the adopted restraint.

Do not add the bound again here: the actual manifest root owns it. Original
source-fit pose comparators remain in higher_lockout.py.
"""

from simulation.running import OperatingCurta


class HigherOperatingTrial(OperatingCurta):
    pass
