"""Local experiment only: full angular/bank acceptance remains outstanding."""

import simulation.test_running_reverser_wrong_order as contracts
from simulation.reverser_contact_trial import LocalReverserContactTrial


class LocalReverserContactTrialTest(contracts.RunningReverserWrongOrderTest):
    model = LocalReverserContactTrial
