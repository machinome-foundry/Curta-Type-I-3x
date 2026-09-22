# Native red baseline — 2026-09-13

Planning commit: `7d39306b2e2e0e4d476ce137f670d1c171e1ead4`.
Unchanged production model; added independent `CarryFrameBench` and tests only.
Command: `solid test --exact simulation/carry_frame.py`, from this worktree,
using the workspace `.venv/bin/solid`, `PYTHONPATH` containing this worktree and
`solid-node/WTs/open-run-simulation`, `SOLID_BUILD_DIR=_build_open_run_evidence`,
one numerical thread, 8 GiB address-space limit and 300-second timeout.
Exit 1: **3 passed, 6 failed in 35.58 seconds**.

Import origins verified with the same interpreter and `PYTHONPATH`:

- solid-node: `/home/asa/devel/libresolid-studio/solid-node/WTs/open-run-simulation/solid_node/__init__.py`
- CadQuery: `/home/asa/devel/libresolid-studio/.venv/lib/python3.12/site-packages/cadquery/__init__.py`
- molejo: `/home/asa/devel/libresolid-studio/molejo/python/molejo/__init__.py`
- bench: this Curta worktree's `simulation/carry_frame.py`.

The passing guards establish actual 4.2 mm slider travel with stationary frame
and guides, the bench/native installed-station placement comparison, and one
valid frame solid. Both stations fail independently for the spring at the
`099` preload and for the raised and lowered slider endpoints.

The first attempted launch failed before tests because a shorthand affine
relation incorrectly named two destinations. It was corrected to two ordinary
public `drives` declarations and is not counted as mechanical red evidence.

Below is the retained failure-output excerpt. Repetitive CAD generation logs
and the two earlier passing guards are omitted; no failed test is omitted.

```text
Running CarryFrameTest.test_first_lowered_slider_clears_frame.FAIL!
Traceback (most recent call last):
  File "/home/asa/devel/libresolid-studio/solid-node/WTs/open-run-simulation/solid_node/manager/test.py", line 345, in run_test
    method()
  File "/home/asa/devel/libresolid-studio/projects/Calculators/Curta-Type-I-3x/WTs/open-run-simulation/simulation/test_carry_frame.py", line 33, in test_first_lowered_slider_clears_frame
    self.clear('first', 'slider', 4.2)
  File "/home/asa/devel/libresolid-studio/projects/Calculators/Curta-Type-I-3x/WTs/open-run-simulation/simulation/test_carry_frame.py", line 18, in clear
    self.assertNotIntersecting(moving, self.node.frame.main_body)
  File "/home/asa/devel/libresolid-studio/solid-node/WTs/open-run-simulation/solid_node/test.py", line 1860, in assertNotIntersecting
    raise AssertionError(
AssertionError: tens_slider_for_results should not intersect main_body (intersection volume 0.09922499999999423)

Running CarryFrameTest.test_first_raised_slider_clears_frame.FAIL!
Traceback (most recent call last):
  File "/home/asa/devel/libresolid-studio/solid-node/WTs/open-run-simulation/solid_node/manager/test.py", line 345, in run_test
    method()
  File "/home/asa/devel/libresolid-studio/projects/Calculators/Curta-Type-I-3x/WTs/open-run-simulation/simulation/test_carry_frame.py", line 27, in test_first_raised_slider_clears_frame
    self.clear('first', 'slider', 0)
  File "/home/asa/devel/libresolid-studio/projects/Calculators/Curta-Type-I-3x/WTs/open-run-simulation/simulation/test_carry_frame.py", line 18, in clear
    self.assertNotIntersecting(moving, self.node.frame.main_body)
  File "/home/asa/devel/libresolid-studio/solid-node/WTs/open-run-simulation/solid_node/test.py", line 1860, in assertNotIntersecting
    raise AssertionError(
AssertionError: tens_slider_for_results should not intersect main_body (intersection volume 4.626577658591654)

Running CarryFrameTest.test_first_spring_clears_frame_at_ninety_nine.FAIL!
Traceback (most recent call last):
  File "/home/asa/devel/libresolid-studio/solid-node/WTs/open-run-simulation/solid_node/manager/test.py", line 345, in run_test
    method()
  File "/home/asa/devel/libresolid-studio/projects/Calculators/Curta-Type-I-3x/WTs/open-run-simulation/simulation/test_carry_frame.py", line 21, in test_first_spring_clears_frame_at_ninety_nine
    self.clear('first', 'spring', 1.1630815)
  File "/home/asa/devel/libresolid-studio/projects/Calculators/Curta-Type-I-3x/WTs/open-run-simulation/simulation/test_carry_frame.py", line 18, in clear
    self.assertNotIntersecting(moving, self.node.frame.main_body)
  File "/home/asa/devel/libresolid-studio/solid-node/WTs/open-run-simulation/solid_node/test.py", line 1860, in assertNotIntersecting
    raise AssertionError(
AssertionError: wire should not intersect main_body (intersection volume 0.4734389673639299)

Running CarryFrameTest.test_frame_is_one_valid_solid. passed
Running CarryFrameTest.test_second_lowered_slider_clears_frame.FAIL!
Traceback (most recent call last):
  File "/home/asa/devel/libresolid-studio/solid-node/WTs/open-run-simulation/solid_node/manager/test.py", line 345, in run_test
    method()
  File "/home/asa/devel/libresolid-studio/projects/Calculators/Curta-Type-I-3x/WTs/open-run-simulation/simulation/test_carry_frame.py", line 36, in test_second_lowered_slider_clears_frame
    self.clear('second', 'slider', 4.2)
  File "/home/asa/devel/libresolid-studio/projects/Calculators/Curta-Type-I-3x/WTs/open-run-simulation/simulation/test_carry_frame.py", line 18, in clear
    self.assertNotIntersecting(moving, self.node.frame.main_body)
  File "/home/asa/devel/libresolid-studio/solid-node/WTs/open-run-simulation/solid_node/test.py", line 1860, in assertNotIntersecting
    raise AssertionError(
AssertionError: tens_slider_for_results should not intersect main_body (intersection volume 0.0992250019246522)

Running CarryFrameTest.test_second_raised_slider_clears_frame.FAIL!
Traceback (most recent call last):
  File "/home/asa/devel/libresolid-studio/solid-node/WTs/open-run-simulation/solid_node/manager/test.py", line 345, in run_test
    method()
  File "/home/asa/devel/libresolid-studio/projects/Calculators/Curta-Type-I-3x/WTs/open-run-simulation/simulation/test_carry_frame.py", line 30, in test_second_raised_slider_clears_frame
    self.clear('second', 'slider', 0)
  File "/home/asa/devel/libresolid-studio/projects/Calculators/Curta-Type-I-3x/WTs/open-run-simulation/simulation/test_carry_frame.py", line 18, in clear
    self.assertNotIntersecting(moving, self.node.frame.main_body)
  File "/home/asa/devel/libresolid-studio/solid-node/WTs/open-run-simulation/solid_node/test.py", line 1860, in assertNotIntersecting
    raise AssertionError(
AssertionError: tens_slider_for_results should not intersect main_body (intersection volume 4.626577659729441)

Running CarryFrameTest.test_second_spring_clears_frame_at_ninety_nine.FAIL!
Traceback (most recent call last):
  File "/home/asa/devel/libresolid-studio/solid-node/WTs/open-run-simulation/solid_node/manager/test.py", line 345, in run_test
    method()
  File "/home/asa/devel/libresolid-studio/projects/Calculators/Curta-Type-I-3x/WTs/open-run-simulation/simulation/test_carry_frame.py", line 24, in test_second_spring_clears_frame_at_ninety_nine
    self.clear('second', 'spring', 1.1630815)
  File "/home/asa/devel/libresolid-studio/projects/Calculators/Curta-Type-I-3x/WTs/open-run-simulation/simulation/test_carry_frame.py", line 18, in clear
    self.assertNotIntersecting(moving, self.node.frame.main_body)
  File "/home/asa/devel/libresolid-studio/solid-node/WTs/open-run-simulation/solid_node/test.py", line 1860, in assertNotIntersecting
    raise AssertionError(
AssertionError: wire should not intersect main_body (intersection volume 0.47343896304081656)


Ran 9 tests in 35.58 seconds: 3 passed, 6 failed
```
