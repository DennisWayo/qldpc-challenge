---
title: "Triplet reverse-engineering: manifold subtraction of the multi-band family, executed"
date: 2026-08-29
author: "@mathysrennela"
model: "GLM 5.3 Flash"
topics: [frontier-theory, multiband, manifold-subtraction, sat-reverse-engineering, planning]
related:
  - fieldnotes/2026-08-29-g-parity-agenda.md
  - fieldnotes/2026-09-18-hackathon-1155-frontier-map-and-playbook.md
---

# Triplet reverse-engineering, the ladder family, and the manifold subtraction

Continues the 2026-08-29 g-parity agenda note; this note holds the
ladder's closed form, the reverse-engineering verdict, and the executed
manifold subtraction.

## Can we reverse-engineer codes for each (n, k, d) triplet?

The parity constraint hands a finite target list (~10^5 triplets under the
soft k <= n/2 prior). Reverse engineering would mean solving, per triplet,
a weight-4 planar cellulation with honest r = sqrt(2) layout, exact (n, k),
and d >= d0. Verdict: **not viable per-triplet; viable as manifold mapping
with one tractable band (d = 3).**

1. **Coverage is the first blocker, and it is structural.** Known
   mechanisms cover O(10) points: the ladder is a 1-D curve per d (now
   exhausted), the raised-pitch variant (k = m) is a second unmapped curve,
   the chamfer family a cloud at d = 3 only. Between curves: nothing;
   filling an arbitrary gap means inventing a mechanism, not running a
   search.

2. **The realizable set is topological, the admissible set is arithmetic.**
   Simply-connected cellulations give k = 1; k >= 2 requires multi-boundary
   segments (the ladder's escape) or holes (moat cost); rank arithmetic
   constrains k to discrete ladders; CSS commutation is fragile. The
   interesting mathematics is the boundary between the two sets.

3. **Complexity stratifies by d, and d = 3 is special.** d >= 3 for CSS
   means no weight-<=2 nontrivial logical: given weight-4 rows, that is (per
   side) no zero/duplicate columns plus no low-weight rowspace sums --
   pairwise/triple row-overlap constraints, a polynomial slack-free CNF much
   lighter than the general t = 2 detection encoding that blocked the prior
   locality-SAT campaign (absorbed into the 2026-09-18 consolidated SAT
   note; tooling: `research/sat_search.py`). The specialized encoding is a
   genuinely new angle. First step: reuse the anchor/incidence design of
   the locality-constrained extension (anchors as SAT variables on a grid,
   incidence gated by Euclidean radius, so every decoded code ships an
   honest layout) and swap the detection encoding for the duplicate-column
   + row-overlap constraints. A d = 3 specialized encoder plus SAT-UNSAT
   bisection on k would map the achievable k/n region at d = 3 -- the band
   where the record (1.564) lives; every +0.01 k/n is +0.09 g.

4. **d = 4-5: CEGIS, expensive but bounded.** Solve -> RIS finds a light
   logical -> exclude it -> repeat. Worth it only for high-g uncovered
   points. d >= 7: SAT is hopeless at n <= 700; "reverse engineering" means
   inventing families -- the chamfer-d >= 4 question.

5. **Recommended program.** (a) The triplet set is the target list.
   (b) For each mechanism, compute its reachable manifold (including the
   raised-pitch k = m curve -- cheap arithmetic) and subtract it. (c) Aim the
   d = 3 specialized SAT at the highest-g uncovered region (record sprint).
   (d) Keep chamfer-d >= 4 as the highest-leverage open mechanism (g ~ 2.7
   potential). The d = 3 campaign is the immediate payoff; the manifold
   subtraction keeps later searches on uncovered high-g triplets; the
   chamfer bet is the only route to a scalable constant above 4/3.


## Update 2 (2026-08-29, later still): manifold subtraction executed, four survivors staged

Program step (b) executed: two corrections and one payoff.

**Correction 1: the "second, unmapped curve" is on the board.** The
raised-pitch variant is a 2-D manifold of @Xo1otl's 2026-08-20 multi-band
family ([[126,6,5]], [[168,8,5]], [[202,10,5]], [[278,14,5]], [[676,36,5]],
[[418,10,7]], [[615,15,7]], [[666,10,9]], [[398,54,3]], [[570,78,3]], plus
d = 3 deeper entries), parameterized as rows x m x pitch with

    k = rows*m - fl(rows/2)   (the full patch count),

even bands carry m patches, odd bands m - 1 offset half a horizontal pitch,
at pitch = pitch_min(d) (6/10/12 measured at d = 5/7/9; the d = 3 entries
use pitch 4, threshold unmeasured). The subtraction below is therefore a
subtraction of a known family's full reachable set, not a first map.

**The builder is reconstructed and validated.** Mask = per-band union
rule (window interiors at (x+y)%2==0; vertical edge columns at phase
%4 in {0,2}; horizontal edge rows at the reverse phase -- the published
conditions in `research/build_dense_surface.py`, generalized). Validated
bit-exact (coordinates, check supports) against build_dense_surface.build
at rows=2, pitch=d-1 for d = 3, 5, 7, and by exact (n, k) reproduction of
all 15 board points -- CSS-commuting, single component, max weight 4.

**Correction 2: the multi-band family beats the ladder's fixed-d
ceiling.** The exact n shows the boundary overhead c = n - P(3d^2+1)/4
turns negative as rows*m grows (c = 12 at rows=4; c = -16 at rows=8, m=6),
so at fixed d the family asymptotes above 4d^2/(3d^2+1) -- [[676,36,5]]
sits at 1.3314, above the ladder's 1.3158. The d -> inf constant is still
4/3 (overhead O(m rows), marginal cost O(d^2)): fixed-d ceilings are
higher than the ladder note claimed; the sup-g question is unchanged in
d. Mechanism, not exploit -- the second stagger refunds boundary.

**The subtraction** (a local enumeration script; method stated here in
full): walk all (rows, m) at pitch_min(d) with n <= 700 (higher pitch only
adds n at fixed k, so is dominated), filter to CSS / single-component /
weight <= 4, score g = kd^2/n, subtract every board (n, k, d). Results:

| d | manifold points under cap | uncovered | best covered g | best uncovered g |
|---|---|---|---|---|
| 3 | 263 | 261 | 1.2316 ([[570,78,3]]) | 1.2353 ([[663,91,3]]) |
| 5 | 77 | 71 | 1.3314 ([[676,36,5]]) | 1.3278 ([[659,35,5]]) |
| 7 | 22 | 20 | 1.1951 ([[615,15,7]]) | 1.1869 ([[578,14,7]]) |
| 9 | 10 | 9 | 1.2162 ([[666,10,9]]) | 1.1970 ([[609,9,9]], dominated by [[569,9,9]]) |

d = 11, 13 stay unmapped: pitch_min there is an RIS screening job, not
arithmetic.

**Four survivors staged** (witness-backed via make_submission into local
staging output; staged for human review):

- **[[659,35,5]]** (rows=10, m=4, pitch 6), g = 1.3278, witnessed d = 5
  both sides. **Dominates [[671,35,5]]** (PR #745's terminal rung) at the
  same k and d with 12 fewer qubits; the d = 5 terminal was not terminal
  for the mechanism, only for the two-band curve.
- **[[663,91,3]]** (rows=14, m=7, pitch 4), g = 1.2353 -- the family's new
  best at d = 3; **dominates both [[672,85,3]] and [[700,85,3]]**. Far below
  the 1.564 record; value is parity club + Pareto + family point.
- **[[578,14,7]]** (rows=4, m=4, pitch 10), g = 1.1869 -- fills the k-gap
  between [[418,10,7]] and [[615,15,7]]; mutually non-dominated.
- **[[625,33,5]]** (rows=6, m=6, pitch 6), g = 1.3200 -- new Pareto point at
  d = 5 between the ladder rungs and [[676,36,5]].

All four witnessed their target distances (20k-trial RIS; witnesses from
make_submission's own search). Remaining uncovered points are dominated or
near-neighbours of these four; left unstaged per the refutation-budget
policy.

**Submission outcomes** (same session, @mathysrennela, GLM 5.3 Flash):
[[659,35,5]] -> #749 (g = 1.328, dominates #745's rung); [[663,91,3]] ->
#750 (1.235, dominates [[672,85,3]], [[700,85,3]]); [[578,14,7]] -> #751
(1.187, fills the d = 7 k-gap); [[625,33,5]] -> #752 (1.320, new d = 5
Pareto point). Each passed CLI verification (witnesses + 2M-trial
accelerator refutation) and the prose gate before push.

**Consequence:** step (b) is done for d <= 9; the known mechanisms'
manifolds leave only scattered Pareto openings, all staged or on the board.
The open frontier: chamfer-d >= 4, and the d = 3 specialized SAT campaign --
which targets the region *between* manifolds, confirmed empty at d = 3
beyond g ~ 1.235.

## The ladder is already a scalable g > 1 family

The freed-m generalization ([[367,19,5]]) has the closed form

    n = ((3d^2 + 1)m - (d^2 + 1))/2,    k = 2m - 1,    w = 4,    r = sqrt(2)

Its asymptotics are arithmetic: g -> 4/3 at fixed m and at fixed d (the
joint limit agrees). The m = 3 column asymptotes to 5/4 (n = 4d^2 + 1,
k = 5 -- visible in the 1.2437 -> 1.2482 drift from d = 7 to 13). Submitted
rungs climb toward 4/3 from below as the formula predicts (1.244 -> 1.294
as m grows at d = 5).

**So the holy grail as stated -- a scalable family with g >= 1 -- already exists
on the board.** The refined question is: how high above 1 can the asymptotic
constant c be pushed at weight-4, r = sqrt(2)? Empirical floor today: c >= 4/3 ~
1.333 (ladder) with the d = 3 chamfer codes demonstrating that specific small-d
constructions can exceed it (1.564). BPT does not obstruct: it caps kd^2/n at a
weight-dependent constant c(w), unknown at w = 4, and the tile code shows
c(8) >= 12.7 (at r ~ 5.83, which is why it scores g ~ 0.04 -- the r⁴ pricing is
the whole game).

Mechanism: the ladder buys logicals with **perimeter, not area** --
k = 2m - 1 logicals on a simply-connected patch carrying 4m alternating
boundary segments; each extra logical costs O(d) of boundary, not the O(d^2)
"moat" that hole-based constructions pay. That evades the homological
one-logical-per-d^2 accounting that pins standard constructions to g = 1.

## What is worth submitting, concretely

In priority order: (1) unclaimed ladder rungs -- at d = 5, n = 38m - 13
gives m = 18 -> [[671,35,5]] at g ~ 1.3040, the highest under the cap
(m = 19 is over cap), plus [[641,17,7]] at 1.2995 and [[691,11,9]] at
1.289; each is a parity-club member, family data point, and likely Pareto
record in local-2d-single x weight-4. (2) Certification of the small rungs
([[101,5,5]], [[197,5,7]]) via exact MILP -- the family claim rests entirely
on upper-bound distances, and one refuted witness collapses a rung.
(3) Parity-set members outside the ladder -- any (n, k, d) with k d^2 > n
and an honest r = sqrt(2) layout.
