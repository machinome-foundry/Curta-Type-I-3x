# Addition

A film of this project declared in Python and drawn by its own template:
the event-driven Curta adds 23 and 145, and the film shows how, then shows the
Python that says it. `takes.py` declares the take (the steps the clocked
model is asked to make, its cameras, the layer that opens the case and the
source excerpts), `movie.py` is the whole screenplay, `stage.tsx` and
`stage.css` are the look (the sets `Curta` and `CurtaSplit` and the sum
element), `spec.md` says what each shot is written to prove, and
`description.md` is the draft of the upload description, which carries the
attribution the film's frames do not.

The movie is declared in the project's `pyproject.toml` under
`[tool.machinome.movies]` as `addition`. It films the clocked model
`event_driven_curta` (`simulation.event_driven:EventDrivenCurta`) through its export, with
a machinome-viewer bundle that draws a clocked document on demand (viewer
API 29); the framework's `machinome viewer` report names the installed
bundle.

## The export

The film reads `export/event_driven_curta/`, a build product that is not
committed. Make it from this directory, by the project's real path (the
framework's simulation fails through a symlinked path):

```sh
machinome export event_driven_curta -o export/event_driven_curta --no-widget
git rev-parse HEAD > export/event_driven_curta/source-revision.txt
ln -s ../../STLs export/event_driven_curta/STLs
```

The framework writes no `source-revision.txt`; Videomaker pins the film to
it, and evaluation records it as the model's source revision. The link is a
workaround: the export's manifest names each imported piece's source file
(`pieces[].sources`, relative to this project), and Videomaker's `preview`
and `render` serve every `.stl` path the manifest names relative to the
export, so without it they stop on the first source file
(`ENOENT … export/event_driven_curta/STLs/…`). The viewer never reads them. Remake the
export and rewrite the revision with every change of the model, then
evaluate again: the take is recorded from the model, and the export must be
the same machine (the evaluation and the viewer both check its identity).

## Produce it

From a Videomaker checkout that films clocked takes, with the workspace's
Python and `machinome_movie` from that checkout, and the speech key
available to the `speech` command:

```sh
python -m machinome_movie evaluate <this project> addition
node bin/videomaker.mjs speech  <this project>/videos/addition/_build/movie.json
node bin/videomaker.mjs check   <this project>/videos/addition/_build/movie.json --viewer <bundle>
node bin/videomaker.mjs preview <this project>/videos/addition/_build/movie.json --viewer <bundle>
node bin/videomaker.mjs render  <this project>/videos/addition/_build/movie.json --viewer <bundle>
```

`evaluate` runs the take's steps once through the framework's `Sim` of
`EventDrivenCurta` and writes `_build/movie.json`, the data document the tool
reads, with the requests the machine returned and its bank at every mark.
`check` bundles `stage.tsx` with the tool's stage runtime into
`_build/stage/`, type-checks it, measures the sets for the reframe, and
writes `_build/movie-resolved.json` once the narration takes exist. All of
`_build/` is a build product, ignored by Git; the Python files are the
source. Render at the movie's own frame rate.

## What came out

Five chapters, thirteen shots, 126.23 s at 1920×1080 and 30 fps (3787
frames); the narrator sets the pace and every cut follows her. The five
narration takes (11.60, 29.60, 34.56, 33.68 and 10.16 s) were bought once,
after the screenplay was reviewed, and reused unchanged. The take is 18.75 s
of the clocked model's time: seven requests, eight marks, the dials reading
23 and then 168, two turns on the counter; the renderer replayed every step
on the viewer before the first frame and held every frame to the record.
The second stroke plays again beside the Python that declares the machine,
the Curta moving from the full frame into the right half by a reframe with
its camera held. Nothing was released: the film is a rehearsal
(`releaseReady` false, no published model or source address yet).

`_build/rehearsal.mp4` with `rehearsal.srt` beside it, `storyboard.jpg`,
`preview/report.json`, the review pack under `review-packs/` and
`rehearsal-manifest.json` (which records the stage bundle's hash, the
viewer's and the model's) are the evidence. `spec.md` says where the film
departed from its first version; findings went to Videomaker's campaign
record.
