# Curta3x draft production assets

`production.profile.CurtaDraft` binds the current
`simulation.mechanistic.MechanisticCurta` instance. It assigns four crank
printed units and seven DIN 934 M4x0.7 nuts through nested production
profiles. Fifteen made-wire carry springs remain unassigned with scoped
bending instructions. All other unresolved coverage is explicit.

```python
from production.profile import CurtaDraft
from simulation.mechanistic import MechanisticCurta

model = MechanisticCurta()
production = CurtaDraft(model)
findings = production.findings
steps = production.steps
crank_lines = production.crank.bom
lines = production.bom
production.export("_build_production/draft")
```

Construction binds without geometry work. Findings and instructions need
structure; manufactured BOM lines and export request the selected geometry.
There is no evaluate step and no active production registered on the model.

`ControlledReview` is a regression asset with a different review instruction,
not a second author-approved manufacturing workshop. It reuses the same
child production definitions against the same actual 3x model instance.
Neither asset changes the model, selects an alternate scale, invents a
polymer or measures mass.

The current main crank and grip are existing simulation fit replacements.
The current clearing-loop mounting is simulation-only; complete geometry
acceptance remains open. A retaining spring represented by five mixed
patches has no reconciled finished-part boundary. Read the scope and
evidence record in `production/evidence.md` and the exported limitations.
No bundle constitutes a complete BOM or fabrication-ready calculator.

These profiles use the Machinome 0.8 production API. The framework's 0.8.0
source is at released state but has not been uploaded to PyPI; use the
workspace environment backed by that checkout. The simulation's 0.8
adaptations and these profiles are integrated together on this project's
`main`. From the project root, run the production acceptance and attachment
regressions with that environment's Python:

```sh
env SOLID_BUILD_DIR=_build_production python -m pytest -q production/test_production.py simulation/test_remaining_mates.py simulation/test_transmission_mates.py
```

The tests check the four exported STL artifacts and their hashes, seven
standard nuts, scoped instructions, incomplete coverage and mass, and
preservation of a live simulation's state. They do not certify whole-machine
geometry or fabrication readiness. Outputs are isolated in the ignored
`_build_production` directory and temporary test directories.
