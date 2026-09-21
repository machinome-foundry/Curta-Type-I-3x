"""Test candidate rigid registrations of the source bell ingredients.

This is not a contact-profile compiler. Different complete solids cannot
prove shared contact curves, even if some of their working surfaces agree.
The original native parts are read unchanged; axial rebasing only puts the
compared ingredients on one measuring plane.
"""

import json

from simulation.standard import parts


PAIRS = (
    ('upper_lock', 'ResultsLockingDisc', 'TurnsCounterLockingDisc'),
    ('lower_lock', 'TensResultsLockingDisc', 'TensTurnsCounterLockingDisc'),
    ('carry_tooth', 'ResultsCounterCarryRing', 'TurnsCounterCarryRing'),
)


def main():
    for label, result_name, counter_name in PAIRS:
        result = getattr(parts, result_name)().shape()
        counter = getattr(parts, counter_name)().shape()
        dz = result.BoundingBox().zmin-counter.BoundingBox().zmin
        for angle in (0, 180, 181.25, 182):
            aligned = counter.rotate((0, 0, 0), (0, 0, 1), angle).translate((0, 0, dz))
            missing, extra = result.cut(aligned), aligned.cut(result)
            assert missing.isValid() and extra.isValid()
            print(json.dumps({
                'pair': label, 'counter_rotation': angle, 'z_alignment': dz,
                'source_volumes': (result.Volume(), counter.Volume()),
                'result_only_mm3': missing.Volume(), 'counter_only_mm3': extra.Volume(),
            }), flush=True)


if __name__ == '__main__':
    main()
