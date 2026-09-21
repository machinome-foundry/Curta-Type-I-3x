"""Isolated T07 remaining-result-bank trial; never the manifest default.

Every upper print keeps its source-specific frame. The combined crank bound
reads actual retained shaft angles and upper travel at stations 3..11; it
does not replace the already installed ones, tens or pawl restraints. All
counter channels remain exactly as in OperatingCurta.
"""

from machinome.motion.joints import Bound
from simulation.running import OperatingCurta
from simulation.running_parts import ResultShafts, RetainedTransmission, CHANNEL_NAMES
from simulation.higher_locking_laws import result_bank_closing_limit
from simulation.tools.result_bank_lockout_probe import STATIONS, station_channel


class TrialResultShafts(ResultShafts):
    for _station in range(3, 12):
        locals()[CHANNEL_NAMES[_station-1]] = station_channel(_station, trial=True)()
    del _station


class TrialResultTransmission(RetainedTransmission):
    result = TrialResultShafts()


class ResultBankOperatingTrial(OperatingCurta):
    transmission = TrialResultTransmission()
    _readings = []
    for _station in range(3, 12):
        _shaft = getattr(transmission.result, CHANNEL_NAMES[_station-1])
        _upper = getattr(_shaft, STATIONS[_station-2][1])
        _readings.extend((_shaft.turn, _upper.travel))
    OperatingCurta.main_drive.crank.turn.constrain(range=(Bound(
        result_bank_closing_limit,
        reads=(OperatingCurta.carry_mechanism.tens_bell.turn, *_readings)), None))
    del _station, _shaft, _upper, _readings
