# Base fasteners: source dimensions and remaining contact

This is a diagnostic finding, not an adopted fit or a clearance waiver.
The operating source is project `388f119`, evaluated with the retained isolated
framework worktree at `1a34b3c`. No geometry, placement, motion law or acceptance
checkbox changes.

The two largest positives in the latest world64 rest inventory are the base
fasteners against the bearing plate: 46.657641410004 and 46.65764147112579 mm³.
The independent native common now confirms positive spatial solids at both
interfaces, rather than a mesh-only near-coincident-face artifact:

| Operating occurrence | Native common, mm³ | Native common Z extent, mm |
| --- | ---: | --- |
| `enclosure.m5x30_countersunk_1` | 47.33500343494145 | −138.4500001 to −133.26076941442201 |
| `enclosure.m5x30_countersunk_2` | 47.3350034349526 | −138.4500001 to −133.26076941462375 |

Both imported fasteners and the installed bearing plate are valid native
solids; each common is valid and contains one solid. The fasteners each have
native volume 1605.627217616713 mm³ (rounded), a cylindrical shank of radius
3.0 mm and an overall modeled axial extent of 54 mm. Their product name
`M5x30 countersunk` therefore cannot be used as a dimensional specification.
The corresponding plate bores are cylindrical radius 2.4 mm, through the
6 mm plate from world Z −138.45 to −132.45. Their measured axes agree with
the already recentered fastener axes to the precision of the imported
placement data; the finding does not call for another housing translation.

The project's supplied *Curta Build Manual*, page 35, labels the base fastener
M5×60 and explicitly instructs tapping the bearing plate M5. Thus the source
contains two distinct modeling questions: the fastener dimensions disagree
with its name/manual designation, and the plate represents a smooth untapped
bore rather than the finished mating thread. Merely shrinking the shank below
the bore would erase threaded retention; subtracting its entire envelope from
the plate would not establish that retention either. Neither is adopted.
This is not evidence that the author's physical build fails, and it is not a
manufacturing recommendation.

Reproduce from the project with the workspace environment and the recorded
framework worktree on `PYTHONPATH`:

```sh
python -m simulation.tools.base_fastener_contacts
```

The tool reports installed native bounds, cylinder surfaces and both complete
commons as JSON. Its successful observed run exited zero. An earlier ad-hoc
probe omitted `assemble()` after a mesh-free `Sim` and failed before obtaining
geometry; the committed tool assembles explicitly. That instrumentation error
was not a framework defect and is not counted as a contact test.

Whole-machine task 1.3 remains open. A source-backed finished fastener/thread
representation, its neighboring seats and retention checks are still needed;
none of the existing 236 positive spatial pairs is waived by this record.
