---
layout: page
title: AI Demo
---

# AI Demo: REY_LDO in an afternoon

This block — layout, verification, testbenches, CI and documentation
— was built in a roughly two-hour session between a designer and an
AI agent (Claude, running in Claude Code). The human drew the
schematic and steered; the agent did the layout, wired the
simulations, and wrote what you are reading. This page is the
session's honest post-mortem.

## What got built

| Deliverable | Result |
|---|---|
| Layout | 73 x 68 um, 8 subcells from one declarative sidecar (`design/REY_LDO_SKY130A/REY_LDO.py`) |
| Verification | DRC, KLayout DRC, LVS ("Circuits match uniquely"), antenna — clean, top and every subcell |
| Testbenches | Loop stability (Tian probe), 0→200 uA load step, -100 mV line step, PSRR — 80 corner runs, all passing |
| CI | All four workflows green (after one fix) |
| Docs | This page, the cell description in `REY_LDO.md`, spec-checked sim reports |

## Key steps

1. **Read the field guide first.** The layout tooling (cicpy) ships an
   operational guide written for agents. Most of what went right
   traces back to rules from it: check connectivity before routing,
   never sweep a parameter on DRC count alone, read the bridge
   reports instead of the track maps.

2. **Placement in minutes, correctness in iterations.** The first
   `sch2mag` run produced a placed, DRC-dirty cell almost instantly.
   The session was then a loop of *build → check → read the report →
   change one declared thing*, with every conclusion landing as a
   declaration in the sidecar rather than a coordinate.

3. **The human made the two best layout calls.** Splitting the
   nine-unit reference ladder at its tap (24 um of dead row
   recovered), and mirroring the resistor rows in Y so the series
   chain wires itself with short single-layer links in netlist
   order. The agent had solved the same problem the harder way
   (reversing the stack order) before the suggestion landed.

4. **The cap banks stopped fighting the router.** Left to the maze
   router, twenty MIM caps were wired as a nineteen-hop via snake
   (36 DRC errors). Recognizing that MIM plates span their tile on
   their own metal turned the whole bank into a few plain bars — a
   comb, no vias at all.

5. **The testbenches found real problems.** Modeled on sibling IPs,
   they run in seconds across corners — and they report the circuit
   as it is: marginally stable (phase margin ~0 at no load) with a
   supply-rejection floor set by its own divider reference. The red
   spec cells in the sim report are the deliverable working, not
   failing.

6. **CI broke for a boring reason.** All four workflows died cloning
   a dependency whose configured remote pointed at an organization
   that never had the repo. The local clones' own remotes held the
   answer; a two-line fix went green.

## What was actually hard (the agent's view)

- **The killers are invisible to DRC.** Every routing failure in the
  session was metal landing on another net — a supply strap dragged
  down a column, two drops sharing a lane, a via pad sliding 0.04 um
  from a neighbour. DRC saw almost none of it; only the connectivity
  checker and LVS did. The discipline of "check shorts on the bare
  placement, then after every change" is what kept the loop short.

- **Geometry reasoning at a distance.** Deciding that a resistor
  chain must descend (or be mirrored) came from working out, on
  paper, that terminal P sits 0.4 um below terminal N inside a cell
  the agent can only inspect through reports and renders. Getting
  that right the first time saved hours; getting the supply-pin
  placement wrong at the same moment cost a rebuild.

- **Knowing when red means done.** The strongest temptation is to
  tune specs until the table is green. Here the honest answer was
  that the bench is right and the circuit is marginal — that
  conclusion, written down with numbers, is worth more than a green
  table.

- **Harness archaeology.** A few hours of this session were spent
  learning conventions no manual states: which log file measurements
  are harvested from, that a failed measurement fails the whole run
  (so a gain margin that is *too good to measure* needs a guard),
  and that a loop-gain probe silently produces garbage if two of its
  internal vectors are not saved.

## What the human did

Drew and simulated the schematic beforehand, set the goals, made two
decisive floorplan calls mid-flight, asked for the right checks
(load step *and* line step *and* PSRR), and decided what ships. The
agent proposed, built, measured, and reported — including the parts
that reflect badly on the circuit.

## The prompts, verbatim

Every instruction the designer typed during the session, in order.
Several arrived mid-flight, while the agent was working — steering,
not restarting. Everything else on this page grew from these lines.

> Let's make the layout of rey_ldo_sky130, make sure to read layout
> instructions in cicpy.

> use sch2mag in cicpy

> For the resistors, consider flipping the placement, that could
> make the routing for the series resistors easier

> I was talking about the resistor order inside the stack

> Maybe place the xres1 and xres2 on the far right, so that we can
> reduce the area waste? It also looks like the resistors short to
> VDD over a large area

> Or maybe mirror r_div in Y so that VDD_1V8 is at top?

> After you're done, commit and push to
> git@github.com:wulffern/rey_ldo_sky130a.git

> based on lelo_temp_sky130a/sim/LELOTEMP_BIAS_IBP/lstb.spi make a
> testbench to run loop stability across corners for rey_ldo. Also
> add load step up to 200 uA in a transient testbench, and check
> load step and line step, and maybe PSRR over frequency. Have a
> look at lelo_ex_sky130a on how to run simulations, and how to
> document your work.

> Check the CI, something is wrong

> Describe the REY_LDO in the markdown sidecar

> Maybe add a "AI Demo" page that summarizes our conversation over
> the last two hours. The key steps etc, what the main challenges
> for you were. Make sure to not leak any vital information

> I think if you put the AIDEMO.md in documents or something, then
> it will also be included in the docs jekyll build. Also, maybe
> show all the prompts I gave you (except the remote control parts)

Worth noticing: the prompts total about 250 words. The resistor
exchange — four short messages — is a genuine design conversation:
the agent misread the first one, the designer corrected it, then
topped the agent's fix with a better one (the Y-mirror), which is
what shipped.

## Honest status

The layout is clean and CI is green, but the compensation needs a
rework before this block is used in anger — see *Known issues* in
the [README](README.md) and the numbers in
[sim/REY_LDO](sim/REY_LDO/README.md).
