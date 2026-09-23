"""A partial scan is evidence for its validated cases, never full coverage."""

from copy import deepcopy
import unittest
from simulation.tools.operating_standalone_coverage import collect


class StandaloneCoverageTest(unittest.TestCase):
    def setUp(self):
        self.document = dict(program=dict(identity='program'), drivers={'a': {'default': 0}, 'b': {'default': 0}},
                             controls={'A': dict(kind='slide', input='a'),
                                       'B': dict(kind='turn', input='b')})
        self.assets = {'manifest.json': 'manifest', 'index.html': 'index',
                       'machinome-viewer.js': 'bundle'}
        self.initial = {'a': '0.0000', 'b': '0.0000'}

    def case(self, label, key):
        return dict(control=label, input=key, hover=label, errors=[],
                    release_observed=True, outcome='completed',
                    declared_inputs=['a', 'b'], before=self.initial.copy(),
                    after={**self.initial, key: '1.0000'}, validation='passed')

    def sources(self):
        shared = dict(program_identity='program', asset_sha256=self.assets, errors=[])
        scan = dict(shared, validation='pending', initial=self.initial, required=['A', 'B'],
                    cases=[self.case('A', 'a')])
        probe = dict(shared, **{k: v for k, v in self.case('B', 'b').items() if k != 'errors'})
        return [('scan.json', scan, True), ('probe.json', probe, False)]

    def test_exact_coverage_can_join_explicitly_interrupted_validated_cases(self):
        sources = self.sources()
        rows = collect(self.document, self.assets, sources)
        self.assertEqual([row['control'] for row in rows], ['A', 'B'])
        self.assertEqual(rows[0]['source_validation'], 'pending')
        self.assertTrue(rows[0]['source_interrupted'])
        self.assertEqual(sources[0][1]['validation'], 'pending')

    def test_partial_scan_alone_or_unacknowledged_pending_scan_is_not_acceptance(self):
        sources = self.sources()
        with self.assertRaises(AssertionError):
            collect(self.document, self.assets, sources[:1])
        sources[0] = ('scan.json', sources[0][1], False)
        with self.assertRaises(AssertionError):
            collect(self.document, self.assets, sources)

    def test_rejects_asset_identity_error_duplicate_and_unvalidated_case(self):
        for mutate in (
            lambda source: source[0][1].update(program_identity='other'),
            lambda source: source[0][1].update(asset_sha256={}),
            lambda source: source[0][1].update(errors=['page error']),
            lambda source: source[0][1].update(validation='failed'),
            lambda source: source[0][1]['cases'][0].update(validation='pending'),
            lambda source: source[0][1]['cases'][0].update(release_observed=False),
            lambda source: source.append(deepcopy(source[1])),
        ):
            with self.subTest(mutation=mutate):
                sources = self.sources()
                mutate(sources)
                with self.assertRaises(AssertionError):
                    collect(self.document, self.assets, sources)

    def test_rejects_wrong_declared_input_or_noninitial_case(self):
        for field, value in (('input', 'b'), ('before', {'a': '2.0000', 'b': '0.0000'})):
            sources = self.sources()
            sources[0][1]['cases'][0][field] = value
            with self.subTest(field=field), self.assertRaises(AssertionError):
                collect(self.document, self.assets, sources)
