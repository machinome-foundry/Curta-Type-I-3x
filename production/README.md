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

The production API is a local unreleased framework addition. Validation
must use the paired framework production worktree, not a released package.
From this project worktree, the paired validation command is:

```sh
FRAMEWORK_CHECKOUT=/path/to/production-framework
env PYTHONPATH="$FRAMEWORK_CHECKOUT:$PWD" SOLID_BUILD_DIR=_build_production python -m pytest -q production/test_production.py
```

Outputs are isolated in the ignored `_build_production` directory and
temporary test directories. The existing simulation source and model
manifest remain unchanged.
