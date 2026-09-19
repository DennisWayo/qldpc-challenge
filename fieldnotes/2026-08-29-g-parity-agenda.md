---
title: "The g >= 1 parity agenda: thresholds, ladder, board state, and what was submitted"
date: 2026-08-29
author: "@mathysrennela"
model: "GLM 5.3 Flash"
topics: [geometric-efficiency, surface-code-parity, scalable-families, dense-packed-surface-code]
related:
  - fieldnotes/2026-08-29-triplet-reverse-engineering-and-manifold-subtraction.md
  - fieldnotes/2026-08-30-chamfer-d4-closed-and-wall.md
  - fieldnotes/2026-08-31-multiband-sweep-and-exact-d4-sat.md
  - fieldnotes/2026-09-18-hackathon-1155-frontier-map-and-playbook.md
---

# The g >= 1 parity agenda: thresholds, ladder, and what was submitted

## Campaign final summary (2026-09-01)

**Outcome: the g >= 1 frontier of the weight-4 x local-2d-single cell was
mapped, occupied, and hardened. 100 PRs opened, 100 gate-passed, credited
@mathysrennela / model "GLM 5.3 Flash"; the maintainer merged 100 within
two days.**

1. **Manifold subtraction complete.** Every curve of the two-band ladder
   and raised-pitch/multi-band family is mapped: terminal rungs under the
   n <= 700 cap submitted, pitch_min measured at d = 11, 13 and fitted as
   **pitch_min(d) = 2-floor(3d/4)** (five points, validated on d = 5, 7, 9).
2. **Two distinct thresholds.** k unlocks at pitch = d + 1 (exact);
   distance is preserved only above 2-floor(3d/4). Between them:
   unlocked-k, deficient-distance configs -- a new region.
3. **sup g at w = 4 moved.** The multiband corrected asymptote (witnessed
   at pitch_min) is **1.30-1.43, above the 4/3 ladder asymptote** -- 4 of 5
   points hold; BPT's cap c(4) must sit above ~1.43.
4. **Two exact SAT encoders.** d >= 3 (weight-1 coverage + weight-2 pairs,
   proven exact) produced [[36,4,3]] -- first SAT-exact parity-club code,
   g = 1.0 -- and the exact small-L d = 3 maps; d >= 4 (weight-3 triples,
   exact by even-weight) gave the first exact d >= 4 maps at L = 6/8/10/12.
5. **Negatives of equal weight.** Chamfer does not lift to d = 4 (k = 51
   wall, three move classes); small-L d = 3 tops out at parity; the 1.6+
   asymptote ladder was an artifact (caught, corrected).

**Decisions at close:** enumeration is complete (29,376 configs, pitch
1..2d+1, rows <= 12, m <= 24; residual yield is interpolation rungs on
curves the board already holds -- no further sweeps without a new
mechanism); the d = 13 witness screen runs to completion (4/5 holding;
the >= 1.43 bound does not hinge on it); and the science queue was the
[[676,52,4]] d >= 4 SAT question (since closed, see the session close),
the closed form behind 2-floor(3d/4), the empty [d^2/2, d^2) density
band, and MILP certification of small rungs. The update sections are the
audit trail, including two process errors caught in flight.

## Operating policy

Four decision rules, stated up front so the rest of the note is just their
consequences:

1. **Any g >= 1 code is worth submitting.** Surface-code parity under
   honest layout pricing is the physically meaningful bar; a board-advancing
   g >= 1 code has value independent of the record chase.
2. **The parity condition pre-filters the search space.** In the frontier
   regime (r = sqrt(2), weight-4, single layer) g = k d^2/n, so g >= 1 is
   k/n >= 1/d^2: for each d we know which (n, k) pairs qualify, and search
   effort goes only to those triplets.
3. **Scalable g >= 1 families are where the value is.** Every code of a scaling
   family is worth submitting -- each rung is simultaneously a family data
   point, a Pareto-record candidate in `local-2d-single x weight-4`, and a
   parity-club member. One-off exploits are second priority.
4. **All leads are tracked open problems** (listed below).

## The two thresholds, exactly

The record to beat on the g board is [[656,114,3]] at g = 513/328 ~=
1.56403. In-regime (g = k d^2/n), both goals are integer predicates on
(n, k, d):

| goal | predicate | k/n threshold |
|---|---|---|
| beat the record | 328 k d^2 > 513 n | > 1.564/d^2 |
| parity club (g >= 1) | k d^2 > n (g = 1 ties the surface code) | > 1/d^2 |

The parity threshold is 1.56x looser, and it is the one that matters for
families: k/n held at c/d^2 scales at g = c, so the family question is what constant
c > 1 is achievable asymptotically at weight-4, r = sqrt(2).

**Triplet envelope**: d >= 3 (the site's GEO_MIN_D guard), n <= 700
(schema cap), n >= d^2/2 as an optimistic geometric floor (width >= d;
Blaschke-Lebesgue gives area >= d^2/sqrt(3)). All known constructions sit
at n ~ d^2, so the [d^2/2, d^2) band is "denser than anything known" --
frontier territory. The floor caps d at 37.

Smallest qualifying k per (n, d): parity k_min = ceil(n/d^2); record
k_min = floor(513n/(328 d^2))+1 -- closed forms; a 40-line script
regenerates the full per-(n, d) map. Parity k_min at n = 700: d=3 -> 78,
d=5 -> 28, d=7 -> 15, d=9 -> 9, d=11 -> 6, d=13 -> 5, d=16 -> 3, d=20 -> 2,
d >= 27 -> 1. For d >= 34, 0.64 d^2 > 700, so every board-legal [[n,1,d]]
auto-clears parity -- but d^2 > 700 there too, so such codes would be denser than anything known. In-set arithmetically,
practically the hardest region.

## State of the board (2026-08-29)

Recomputing g for every laid-out code (the site's geo_score recipe) gives
**33 codes at g >= 1**, spanning d = 3..13 -- not 3. The club, grouped:

- **The dense-packed ladder** (this contributor, arXiv:2511.06758 base):
  [[101,5,5]], [[197,5,7]], [[325,5,9]], [[485,5,11]], [[677,5,13]] at
  m = 3, plus freed-m rungs [[177,9,5]], [[215,11,5]], [[253,13,5]],
  [[367,19,5]], [[569,9,9]], [[667,7,11]]; g runs 1.19 -> 1.294.
- **@npdeep's d = 3 checkerboard/chamfer family**: [[656,114,3]] (1.564,
  the record), [[676,110,3]] (1.464).
- **@Xo1otl's high-k series**: [[398,54,3]], [[570,78,3]], [[672,85,3]],
  [[700,85,3]] (g 1.09-1.23 at d = 3) and d = 5-11 rungs up to 1.294;
  d = 4-5 mid-size ([[676,36,5]], 1.331); assorted single-parity codes
  ([[25,1,5]] ... [[81,1,9]] at exactly g = 1).

All club distances are witness-backed **upper bounds**, not certified
exact -- every g figure inherits that tier.

## Open problems (all tracked, per policy (4))

1. **Chamfer at d >= 4** (see the 2026-08-30 note for its closure).
2. **sup g at w = 4, r = sqrt(2)** -- the true asymptotic constant; known
   >= 4/3 (ladder), <= c(4) (BPT, unknown). Any construction above 4/3 at
   scaling d is a genuine result.
3. **Priority on the closed form** (m-generalization of arXiv:2511.06758);
   the exact m = 3 reproduction via `research/build_dense_surface.py` shows
   faithful generalization, but priority is a claim about the literature.
4. **The [d^2/2, d^2) density band** -- no known construction lives below
   n ~ d^2 at distance d; the width bound only forces n >= 0.577 d^2.
5. **Rule-change exposure** -- the site's GEO_MIN_D comment anticipates
   raising the headline threshold if small-d packing exploits proliferate;
   family claims are immune, isolated d = 3 exploits are not.

## Update (2026-08-29, later): terminal rungs submitted

Three terminal rungs were built, gate-passed, and submitted
(board_advancing: true, witness-backed upper bounds, single fused Tanner
component, builder anchored against `research/build_dense_surface.py`):

- [[671,35,5]] (d=5, m=18), g = 1.3040 -- PR #745
- [[641,17,7]] (d=7, m=9), g = 1.2995 -- PR #746
- [[691,11,9]] (d=9, m=6), g = 1.2894 -- PR #747

The terminal-rung map under n <= 700 is complete: d=5 -> m=18 (671),
d=7 -> m=9 (641), d=9 -> m=6 (691), d=11 -> m=4 (667, on board), d=13 -> m=3
(677, on board); d >= 15 has no rung under the cap (m=3 already gives
n = 4d^2+1 >= 901). Remaining unsubmitted ladder points are near-neighbours
(m = 11..17 at d = 5, g 1.296-1.302), skipped per the refutation-budget
policy.

**The ladder mechanism is exhausted under the cap** -- further g gains
need new mechanisms: the chamfer-at-d >= 4 generalization and SAT
reverse-engineering, assessed in the 2026-08-29 triplet note.

## Method note

Thresholds and club counts were recomputed from codes/*.json using the
site's own scoring (site/build.py::geo_score): r is the max check diameter
from stored coordinates, rho from locality.layers, g = 4kd^2/(n rho^2 r^4),
with the d >= 3 guard. Tables are regenerable from the closed forms alone.


## Session close (2026-08-31): campaign outcome and what remains

**Campaign outcome.** The maintainer merged in waves: batches 1-2
(#745-#747, #749-#753, #757-#770) within two days, batch 3 (#772-#832)
overnight; batch 4 (24 codes, batch4.json -- the self-Pareto frontier of
the full-range re-sweep, cross-checked against batch3 domination) went
24/24 with zero failures. Final open-PR count at close: 76 (100 opened,
100 gate-passed, 0 lost); maintainer's merged total from this account: 100.

**Still open, carried from the session:**

1. **[[676,52,4]] feasibility -- the d >= 4 SAT question.** Since closed:
   [[676,52,4]] proven UNSAT and [[676,51,4]] terminal in the 2026-09-04
   SAT audit.
2. **Validity-boundary closed form** -- why pitch = d + 1 holds at d = 5
   and d + 2 partially collapses; the parity/phase structure behind
   2-floor(3d/4). Small linear-algebra problem, sharpens every pitch claim.
3. **g convergence in rows/m** -- asymptote g still rising at 24x32;
   larger configs tighten the >= 1.43 bound (rank ~10 min/code).
4. **Certification** of small rungs ([[36,4,3]], [[101,5,5]], [[197,5,7]])
   via exact MILP -- maintainer-run.
5. **Literature watch** on arXiv:2511.06758 follow-ups (clear as of the
   2026-08-30 note).

Staging artifacts described in the 2026-08-31 note are working output,
not evidence, and are intentionally not committed. Method rules paid for
here: exact-verify any closed-form invariant at the scan domain's extremes
before scanning (the 2.5 h waste); JSON round-trips turn tuples into lists
(convert on load); persist every candidate through the kit path; the
trusted gate is the only authority on board advancement -- local Pareto
arithmetic is a pre-filter, not a verdict.

The ladder closed form, reverse-engineering program, and manifold
subtraction are in the 2026-08-29 triplet note; the chamfer d >= 4 closure
and k = 51 wall reformulation in the 2026-08-30 chamfer note; the exact
SAT encoders, multiband sweep, and corrected asymptote in the 2026-08-31
multiband note.
