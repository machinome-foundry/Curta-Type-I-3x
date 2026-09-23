"""Installed-cover experiment, pending production and browser acceptance."""

from pathlib import Path

import simulation.test_reverser_contact_trial as trial_contracts


class InstalledReverserProfileTrialTest(trial_contracts.LocalReverserContactTrialTest):
    @classmethod
    def setUpClass(cls):
        from simulation.tools.reverser_installed_trial import make_trial
        evidence = Path(__file__).parent.parent / '_build_checks' / (
            'reverser-installed-profile-reference-a428dea.jsonl')
        cls.model = make_trial(evidence)


class InnerFlankInstalledTrialTest(trial_contracts.LocalReverserContactTrialTest):
    @classmethod
    def setUpClass(cls):
        from simulation.tools.reverser_installed_trial import make_trial
        from simulation.reverser_ones_fit_trial import TrialOperatingCurta
        evidence = Path(__file__).parent.parent / '_build_checks' / (
            'reverser-inner-flank043-installed-79f3de8.jsonl')
        cls.model = make_trial(evidence, model=TrialOperatingCurta,
            evidence_sha256='4253236b35204ba03b94b4b9c948d10222a9a5f2b81ac09c4e2f8789f71de896')
