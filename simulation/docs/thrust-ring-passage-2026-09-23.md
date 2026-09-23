# Bounded thrust-ring passage for the radial-ball trial

Status: the bounded ring fit is adopted in `SeatedCarriagePositioning` and its
production and paired-neighbour checks pass. Ball-motion adoption remains separate.
Project planning commit `8d6490c`, framework worktree
`follow-two-clearance-surfaces` at `f4c48f6`. The original desired native/world64
red and source section are in the [positioning-ball investigation](positioning-ball-following-2026-09-22.md).
This is simulation-owned fitting under standing autonomous completion authority,
not a manufacturing or structural recommendation. Upstream assets are untouched.

## Source and protected material

The native positioning ball is a single spherical face, radius
3.7499999999999996 mm, centre (9.627860318, 0, 30). Its published mesh's maximum
radius is 3.750000115587718 mm. The ring is the original 1.5 mm annulus with
radii 12.3..16.35, phase 35.717779468 degrees, installed bottom Z33.05. Its
upper plane area is 364.52684957765837 mm² and remains entirely unchanged.

The independent permitted region is installed X12..14.3, Y±2.4,
Z33.05..33.85 mm, transformed back into the ring's original local frame. The
production cutter does not import it. Before fitting, 205 probes at five
lifts 0..6 and 41 collar phases -100..100 degrees confirm that neither the
downward .1 mm ring/collar retaining common nor the downward .2 mm spring/
ring retaining common reaches that region. Both commons remain positive.
Native upper-plane intersection with the permitted region is exactly empty.

The first support instrument correctly rejected an obsolete fixture: its
collar was the earlier source print, not the current shoulder/facing fit and
-90-degree operating phase. `InstalledThrustBench` now uses the current
`SeatedCollar`; its world vertices match the operating root to 1e-9 mm, and
the ring vertices match exactly. This positional comparison tolerance does
not accept any positive collision volume. Actual root commands prove +6 mm
ring translation, purely radial ball translation, and unchanged ball/ring
world placement while the raised carriage shifts 20, 50 and 100 degrees.

## Candidate and proof

`BallPassageThrustRing` removes the swept R3.80 running gauge along centre
radii 8.332135134696959..11.949090957641602 at world Z30. The source part
remains one valid connected solid; 2.428916246671126 mm³ is removed and
544.3613583002075 mm³ remains. Nothing is added, all removal lies in the
independent maximum region, and the complete upper .7 mm and outer R14.5..16.35
support material survive exactly. Fresh adjustment and built native geometry
have zero material difference both ways. Trial gaps .04, .05 and .06 mm are
measured as those actual native ball/ring distances at the outer radial limit.

The unsampled-path proof deliberately rounds the sphere radius up to 3.751 mm
and centre interval outward to 8.332..11.950 mm. The resulting continuous
capsule has exactly zero common with the fitted ring. It encloses the measured
native sphere and every triangle of its published mesh (the sphere is convex).
Because the entire ring is above the ball centre, lifting the ring 0..6 mm
can only shrink each ball section in ring coordinates. Thus the same zero-lift
enclosure bounds the complete radial/lift rectangle, including retained slack,
not just the measured contact endpoints. The actual frame-motion checks above
are premises of this proof; carriage shift does not rotate the passage.

Independent dense checks cover 41 radii ×61 lifts: all 2,501 native/world64
questions return exactly zero. This rectangular domain also includes inadmitted
combinations, making it conservative for the actual follower. Ring mesh
deflections are .005 mm linear/.1 angular to resolve the concave passage;
this is representation refinement, not a tolerance on positive common volume.

The original ring and a 20-degree misplaced cut both restore positive native
obstruction. Excessive top-face removal violates the independent bounds.
Five material/enclosure/negative tests pass in 17.120 s. An initial launch
omitted building the isolated part before asking for its STL; it fails with
FileNotFoundError and is not a mechanical pass. With explicit assembly/build,
the full six-test material and actual Follow-contact batch passes in 59.653 s.
Existing seat, free-play, retained-stop, wire/connectivity and source-negative
contracts pass 5/5 native in 39.56 s and 5/5 world64 in 17.49 s.

## Installed-root and pixel checks

The static-ball candidate is compared with an explicit original-ring reference
at rest, crank 180 degrees, and after returning home, lifting 6 mm and shifting
40 degrees. The entire 213-coordinate bank, all other 388 rigid meshes and all
flexible meshes are array-identical. Only the ring loses permitted material.
That check passes in 55.416 s. Neither candidate silently adopts radial motion.

The inspected three-panel native section shows the original lower inner lip,
the candidate passage and unchanged top face at rest, outer radial limit and
raised carriage. A second inspected version includes the current collar and
spring mesh sections; the outer collar ledge remains outside the relief.
The intact assembly render retains all supports, but the enclosing collar
occludes the ring. That image proves context, not visibility of a .05 mm gap.

## Production adoption and paired neighbours

Only the seated positioning assembly's ring type changes. The original
source-pose ring and explicit original-ring operating reference remain intact.
The production root-identity and actual radial-trial ring-contact batch passes
2/2 in 98.395 s. The default operating root's existing support, full lift,
indexed shift, exact retained replay and every-rigid-neighbour rest checks
pass 2/2 native in 181.69 s and 2/2 faceted in 37.02 s.

The static-ball candidate completes all 44 addition samples in 191.610 s
with the expected (5, 2) registers. Compared with the adopted-frame baseline,
all 45 rest/sample inventories are identical: no pair added, removed or changed.
The separately paired radial Follow baseline and fitted-ring trial complete
44 samples in 345.680/348.613 s. Across all 45 rows the correction removes
exactly the ball/ring contact, adds none, and changes no other pair volume.
Every inventory includes all rigid parts and has no refused intersection;
flexible leaves are covered by the named seat checks, not that rigid inventory.

The ring cycle is locally complete. Production still has the original static
ball and 213 coordinates. The radial candidate's complete bell/collar/frame
and retained-motion acceptance, final viewer controls and other whole-machine
findings remain open. No positive contact is waived and no umbrella checkbox
is closed by this correction.

## Evidence

Artifacts under `_build_checks/`, SHA-256:

| Artifact | Hash |
|---|---|
| Obsolete-collar instrument refusal | `8c273a529a6328cd5a7722ac0101150b760a82d4e34e2baa95f5a4d06e008a5d` |
| `thrust-ring-protected-current-collar-8d6490c.jsonl` | `42ecf33b45a845fcd52f823274d65f834ed4ee9706bdda8b89a5d00f0075eb1a` |
| Initial missing-build batch | `d7e3c6576f80d94b298fdb5aafaed2410a9d9afa2a6ba971b12de7e912392fc8` |
| `thrust-ring-candidate-material-built-8d6490c.log` | `fce8ab04cac70efab7343fb732a104b745aa2c71b5b63eae70671af3ea06fd20` |
| `thrust-ring-candidate-material-follow-built-8d6490c.log` | `fac41c1232ca9739e14fbcbbbadc22c16cbf052963d9600cf7684dd13ffb0fca` |
| `thrust-ring-candidate-seats-exact-8d6490c.log` | `169bb5878958558f1b2718ee080a985af3f65f74247b9e22806d18e96cb01fcd` |
| `thrust-ring-candidate-seats-faceted-8d6490c.log` | `64f2c44dd06497f7879d2d79a5aa9e4d840ab83e6c16a2510d0e7516fb74ea5b` |
| `thrust-ring-candidate-dense-8d6490c.jsonl` | `85d750e07683df82a31560f97a31c06fa123613239b078bf1bfbc2c822b78543` |
| `thrust-ring-candidate-dense-supported-8d6490c.jsonl` | `b434d6a0101014879410345ad4f020590afd452c9067f030c6af57757173ce0b` |
| `thrust-ring-candidate-root-identity-8d6490c.log` | `c3ae958bf3a94daf0ec638ccbf6141d1549368a11d1917c3369881be08f4257b` |
| `thrust-ring-candidate-sections-8d6490c.png` | `2c1a8409ea3190d3bfc50efb0d2848c04e2baf2673c0852d4903ad01704a0d80` |
| `thrust-ring-candidate-supported-sections-8d6490c.png` | `85985d8ae742d6a18b37a5ef94e4606d0fd7ea9b82f194b72c9821b25e0dcac6` |
| `thrust-ring-supported-assembly-8d6490c.png` | `b74d1d1e0d565fe5d09fbcfa9e5e713f6738d287b5951b32765c68ecbe5d62df` |
| `thrust-ring-production-root-follow-8d6490c.log` | `d972068ea6daeb1a2477298e9cbe2f88390d239a22bf1d53cab409f848ff0cc2` |
| `thrust-ring-production-supports-exact-8d6490c.log` | `b9042dd4b4afc341ce0bb032521b06e963ba1e296ef558834bed3037f0730cc1` |
| `thrust-ring-production-supports-faceted-8d6490c.log` | `ac36ea49ad36626ef25244b61d91559c511ae6cce1ee3d38e6856f8eb7bf9d2c` |
| `thrust-ring-static-trial-addition-8d6490c.jsonl` | `a7c0145400382b1fe7ebc94e122d1ee2d077bb631c85e121fdaea6c25c658da3` |
| `thrust-ring-follow-original-addition-8d6490c.jsonl` | `96c2c9c38e5678dae8c18f6b992d68af1fbd4be1ad602084eabaa15eea425011` |
| `thrust-ring-follow-trial-addition-8d6490c.jsonl` | `98da265737f27ba3c70f6f2a2a2965acb1201d4e54df3e34bc3a1c36e644de48` |
| `thrust-ring-paired-contact-comparison-8d6490c.json` | `61357052c6fa7e8e7ba1946faf841eba7be3ff6e566a9f7e7b95b9106f4e983b` |
