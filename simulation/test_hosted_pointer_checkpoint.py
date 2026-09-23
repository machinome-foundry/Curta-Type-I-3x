"""Progress is durable without turning an unfinished run into acceptance."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from simulation.tools.operating_pointer_matrix import checkpoint_report


class HostedPointerCheckpointTest(unittest.TestCase):
    def test_keeps_pending_status_and_completed_cases(self):
        report = dict(validation='pending', cases=[{'input': 'digit_1'}], errors=[])
        with TemporaryDirectory() as directory:
            path = Path(directory)/'report.json'
            checkpoint_report(path, report)
            self.assertEqual(json.loads(path.read_text()), report)
            report['cases'].append({'input': 'digit_2'})
            checkpoint_report(path, report)
            self.assertEqual(len(json.loads(path.read_text())['cases']), 2)
            self.assertEqual(json.loads(path.read_text())['validation'], 'pending')

    def test_failure_is_preserved_not_reclassified_as_a_pass(self):
        report = dict(validation='failed', failure='interrupted', cases=[], errors=[])
        with TemporaryDirectory() as directory:
            path = Path(directory)/'report.json'
            checkpoint_report(path, report)
            self.assertEqual(json.loads(path.read_text()), report)
