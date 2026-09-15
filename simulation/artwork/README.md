# Paint-only derivatives of the author's artwork

The upstream `Drawings/` files remain untouched. These SVGs keep selected
original path data, coordinates, physical dimensions and ancestor transforms:

| Asset | Original | Preparation |
| --- | --- | --- |
| `input-digits.svg` | `Input_Digits-new.svg` | Keep the ten white digits; omit the black backing rectangle and open guide. The roll's presentation colour supplies the black ground. |
| `input-places.svg` | `lower_housing.svg` | Keep digits 8–1; omit open cutting guides and editor definitions. |
| `sleeve-branding.svg` | `upper_outer_sleeve.svg` | Keep CURTA and both arrows; omit the closed cutting border and two screw-registration circles. Correct the mistaken `in` unit to `mm`, preserving the numeric viewBox. |

The sleeve unit correction agrees with the original
`Drawings/cricut-images/README.md` (62 mm height) and the 64.5 mm source sleeve,
whose outer band begins at z=2.55 mm. These are not redrawn fonts or replacement
geometry. Their provenance and licensing remain those of the upstream artwork;
no new licence is asserted for them.

`../tools/prepare_marking_artwork.py` contains the explicit source path IDs and
reproduces these assets. From the project root:

```sh
python -m simulation.tools.prepare_marking_artwork --check
```

Without `--check` it prints an `apply_patch` patch for review; it never writes
the assets or runs as a model-build side effect. Reassess the path selection
if an upstream drawing changes.

`results_dial.svg` and `reversing_lever_arrows.svg` are used directly from
`Drawings/`. The framework drops the result sheet's open border. The reversing
sheet's small centre dot is retained between its two arrows.

`upper_housing_numbers.svg` is deliberately not converted: its conical
development needs a placement not supported by the current flat/cylindrical
API. See [the markings record](../docs/markings.md).
