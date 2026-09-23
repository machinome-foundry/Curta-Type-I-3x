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
            'reverser-inner-flank-installed-cover-a0b4539.jsonl')
        cls.model = make_trial(evidence, model=TrialOperatingCurta,
            evidence_sha256='1cc0cf7f434318d66a813c5cb62046433ae283b0985a5117d2c671edc91da0ff')
