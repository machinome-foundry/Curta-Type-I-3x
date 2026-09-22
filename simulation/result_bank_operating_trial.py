"""Independent T07 remaining-result-bank parts retained as an acceptance fixture.

Every upper print keeps its source-specific frame. The production operating
root supplies the combined crank bound; this wrapper does not repeat it.
All counter channels remain exactly as in OperatingCurta.
"""

from simulation.running import OperatingCurta
from simulation.running_parts import ResultShafts, RetainedTransmission, CHANNEL_NAMES
from simulation.tools.result_bank_lockout_probe import station_channel


class TrialResultShafts(ResultShafts):
    for _station in range(3, 12):
        locals()[CHANNEL_NAMES[_station-1]] = station_channel(_station, trial=True)()
    del _station


class TrialResultTransmission(RetainedTransmission):
    result = TrialResultShafts()


class ResultBankOperatingTrial(OperatingCurta):
    transmission = TrialResultTransmission()
