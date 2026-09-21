"""Local closing-bell diagnostic; not the production operating model.

Validated sequence: selector 1 to 3, crank to 90 then 120 degrees, selector
back to zero, request 150. The ones shaft is retained at 189.6 degrees.
The complete bell is clear at 125.32 in OCCT and its published mesh; first
contacts are 125.33066 and 125.32259 respectively. See the dated evidence.

Only this phase neighbourhood and the prepared 120..150-degree window have
been sampled. The fallback permits a one-turn request, not a certified law
outside that window. Never select this diagnostic as the operating model.
Upstream CAD, assemblies, original stops and all controls are unchanged.

The operating parent now includes its certified five-flat ones restraint.
This historical extra local bound is retained for ancestor-intersection
regression; the stricter parent stops the prepared case at 125.22323837.
"""

from machinome.motion.joints import Bound
from simulation.running import OperatingCurta

LAST_FREE = 125.32
PHASE = 189.6
PHASE_SAMPLES = (189.599, 189.6, 189.601)


def closing_window(own, shaft):
    active = ((shaft >= PHASE_SAMPLES[0]) * (shaft <= PHASE_SAMPLES[-1])
              * (own <= -120) * (own >= -150))
    return -LAST_FREE * active + (own-360) * (1-active)


class AncestorLockoutCurta(OperatingCurta):
    OperatingCurta.main_drive.crank.turn.constrain(range=(Bound(
        closing_window, reads=(OperatingCurta.transmission.result.ones.turn,)), None))
