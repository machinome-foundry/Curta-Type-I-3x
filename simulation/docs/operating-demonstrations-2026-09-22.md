# Separate retained-operation demonstrations

`simulation.operating_demonstrations` supplies six named physical-request
sequences: addition, carry, overflow, subtraction, shift and clearing.
They are not added to the ordinary part-control surface and do not replace
any independent control. The legacy posed `Demo` is unchanged and must not
be mistaken for this operating acceptance.

Each sequence starts by restoring a caller-owned fresh-machine snapshot,
then issues only ordinary selector, crank, carriage and ring requests.
There are no register setters or arithmetic result assignments. Overflow
prepares both nines banks by physically subtracting one from zero; shifting
explicitly lifts, turns and seats the carriage; clearing explicitly lifts,
sweeps the result and counter halves, sweeps back and reseats. Every action
has a positive duration, must retire completed and checks its stated retained
readings. Ordinary operation does not call the demonstration helper.

Example Python fixture (the `.1` step is the explicit project acceptance
setting; this does not alter the browser's default timestep):

```python
from machinome.simulation import Sim
from simulation.running import OperatingCurta
from simulation.operating_demonstrations import replay

sim = Sim(OperatingCurta(), dt=.1)
initial = sim.snapshot()
outcomes = replay(sim, 'carry', initial)
```

After the missing-module red baseline, the definition and actual replay tests
pass on framework `4bff28e`: two tests in 740.222 s, observed exit zero.
The replay test runs all six sequences twice, checks every command/readout
and compares the complete snapshots and outcome lists exactly. This was the
production root before higher-counter adoption (the mechanism is unchanged
between `5872ce1` and `ad841f2`), with the new demonstration files. The retained log
`_build_checks/operating-demonstrations-first-2026-09-22.log` has SHA-256
`859f188f5f8df927d721d936ed35dc4f088aca91a5c1d0fafc735adcf5d116c4`.

Callers may install `sim.every` sampling before replay. Fresh native/world64
moving-interface checks throughout these demonstrations, current combined-bank
replay, browser demonstration delivery and final layer/whole-machine acceptance
remain separate obligations. No OpenSpec checkbox closes from this replay
result alone.
