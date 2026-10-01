# Addition

A film of this project declared in Python and drawn by its own template:
the clocked Curta adds 23 and 145, and the film shows how, then shows the
Python that says it. `takes.py` declares the take (the steps the clocked
model is asked to make, its cameras, the layer that opens the case and the
source excerpts), `movie.py` is the whole screenplay, `stage.tsx` and
`stage.css` are the look (the sets `Curta` and `CurtaSplit` and the sum
element), `spec.md` says what each shot is written to prove, and
`description.md` is the draft of the upload description, which carries the
attribution the film's frames do not.

The movie is declared in the project's `pyproject.toml` under
`[tool.machinome.movies]` as `addition`. It films the clocked model
`clocked_curta` (`simulation.clocked:ClockedCurta`) through its export, with
a machinome-viewer bundle that draws a clocked document on demand (viewer
API 29); the framework's `machinome viewer` report names the installed
bundle.

## The export

The film reads `export/clocked_curta/`, a build product that is not
committed. Make it from this directory, by the project's real path (the
framework's simulation fails through a symlinked path):

```sh
machinome export clocked_curta -o export/clocked_curta --no-widget
git rev-parse HEAD > export/clocked_curta/source-revision.txt
```

The framework writes no `source-revision.txt`; Videomaker pins the film to
it, and evaluation records it as the model's source revision. Remake the
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
`ClockedCurta` and writes `_build/movie.json`, the data document the tool
reads, with the requests the machine returned and its bank at every mark.
`check` bundles `stage.tsx` with the tool's stage runtime into
`_build/stage/`, type-checks it, measures the sets for the reframe, and
writes `_build/movie-resolved.json` once the narration takes exist. All of
`_build/` is a build product, ignored by Git; the Python files are the
source. Render at the movie's own frame rate.

## Status

First launch, 1 October 2026: the screenplay written and evaluated (the
take recorded: 18.75 s of take time, the result reading 23 and then 168,
two turns on the counter); no speech bought, nothing rendered. The
narration is reviewed before the speech is bought.
