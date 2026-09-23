"""Self-contained installed restraint awaiting production-root acceptance."""

from machinome.motion.joints import Bound
from simulation.reverser_ones_fit_trial import TrialOperatingCurta
from simulation.reverser_profile_laws import lower_limit, upper_limit


class CompiledReverserTrial(TrialOperatingCurta):
    _reads = (TrialOperatingCurta.main_drive.crank.turn,
              TrialOperatingCurta.transmission.turns.ones.turn,
              TrialOperatingCurta.transmission.turns.tens.turn,
              TrialOperatingCurta.transmission.turns.hundreds.turn,
              TrialOperatingCurta.transmission.turns.digit_4.turn,
              TrialOperatingCurta.transmission.turns.digit_5.turn,
              TrialOperatingCurta.transmission.turns.digit_6.turn,
              TrialOperatingCurta.main_drive.crank.lift)
    TrialOperatingCurta.main_drive.reversing_lever.reversing_lever_1.reversing_lever_knob_1.lift.constrain(
        range=(Bound(lower_limit, reads=_reads), Bound(upper_limit, reads=_reads)))
    del _reads
