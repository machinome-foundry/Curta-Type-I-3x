"""A survey may reuse rigid drums only while their complete pose is identical."""

import unittest

from simulation.tools.reverser_tooth_envelope import DRUMS, ToothEnvelopeReader


class Shape:
    def rotate(self, *args):
        return Shape()

    def translate(self, *args):
        return Shape()


class ReverserPoseCacheTest(unittest.TestCase):
    def reader(self):
        reader = object.__new__(ToothEnvelopeReader)
        reader.gear = 'gear'
        reader.axis = (1, 2, 3)
        reader.shaft = 134
        reader.height = 3.9075
        reader.native = {path: Shape() for path in ('gear', *DRUMS)}
        reader.faceted = {path: Shape() for path in ('gear', *DRUMS)}
        reader._drum_pose_key = None
        reader._posed_drums = None
        return reader

    def test_only_drums_are_reused_across_shaft_and_height_queries(self):
        reader = self.reader()
        first = reader.posed(90, 152, 0, kernel='world64')
        second = reader.posed(90, 174, -3, kernel='world64')
        self.assertIsNot(first['gear'], second['gear'])
        for path in DRUMS:
            self.assertIs(first[path], second[path])

    def test_native_drum_poses_are_fresh_even_with_an_identical_key(self):
        reader = self.reader()
        first = reader.posed(173, 207.51234436035156, -3, kernel='native')
        second = reader.posed(173, 207.5123519897461, -3, kernel='native')
        for path in DRUMS:
            self.assertIsNot(first[path], second[path])

    def test_crank_lift_or_kernel_change_invalidates_the_single_pose_cache(self):
        reader = self.reader()
        last = reader.posed(90, 152, 0, kernel='native')
        for crank, lift, kernel in ((91, 0, 'native'), (91, 1, 'native'),
                                    (91, 1, 'world64'), (90, 0, 'native')):
            current = reader.posed(crank, 152, 0, lift, kernel=kernel)
            for path in DRUMS:
                self.assertIsNot(current[path], last[path])
            last = current


if __name__ == '__main__':
    unittest.main()
