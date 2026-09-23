"""Retained-root acceptance using committed model data, not diagnostic files."""

from simulation import test_reverser_contact_trial as contact_contracts
from simulation import test_running_reverser_contact_path as path_contracts
from simulation import test_running_reverser_wrong_order as running_contracts
from simulation.reverser_compiled_trial import CompiledReverserTrial


class CompiledReverserTrialTest(contact_contracts.LocalReverserContactTrialTest):
    model = CompiledReverserTrial


class CompiledReverserPathTest(path_contracts.ReverserContactPathTest):
    model = CompiledReverserTrial


class CompiledReverserStrokeTest(running_contracts.RunningReverserStrokeTest):
    model = CompiledReverserTrial
