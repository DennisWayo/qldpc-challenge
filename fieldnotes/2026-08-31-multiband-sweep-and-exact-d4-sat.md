---
title: "The d = 3 / d >= 4 exact SAT encoders, the multiband sweep, and the corrected multi-band asymptote"
date: 2026-08-31
author: "@mathysrennela"
model: "GLM 5.3 Flash"
topics: [sat-search, exact-encoder, multiband, asymptote, pitch-min, weight-4]
related:
  - fieldnotes/2026-08-29-g-parity-agenda.md
  - fieldnotes/2026-09-18-hackathon-1155-frontier-map-and-playbook.md
---

# Exact SAT encoders and the corrected multi-band asymptote

## Update 5: the d = 3 exact-SAT campaign — [[36,4,3]] submitted

Closes reverse-engineering step (c): the d = 3-specialized SAT search
was built, made *exact*, and produced a board-advancing code. Variables
are anchors on the board-standard orthogonal grid (checkerboard weight-4
faces + phased boundary weight-2s); two proven constraint families:

- *Weight-1*: every vertex carries an active opposite-type anchor. Exact:
  all anchors have even weight, so rowspace(H) has no weight-1 vector
  (chains lifting e_q impossible by parity; verified by exact GF(2) rank
  over all 2^15 L=4 configs, zero violations).
- *Weight-2*: per pair {p,q}, an own-type w2 on {p,q} active, or an
  opposite-type anchor meeting exactly one active. Exact: same-type faces
  share only corners and w2s border only opposite-type faces, so no XOR
  chain of active checks yields a weight-2 rowspace element (zero chain
  hits over all L=4).

Cross-validation: the CNF reproduces the exhaustive L=4 frontier; all 11
clean annealer configs satisfy it, one stale dirty artifact is rejected.
**The earlier UNSAT lines were wrong:** the intermediate encoder (no
weight-1 clauses, after an illusory counterexample) gave frontier lines of
19/33/69 anchors at L = 6/8/12; the exact CNF moves these to 34/62/~74.
The old small-L candidates ([[16,3,3]], [[36,3,3]], [[64,5,3]]-as-k=5,
[[100,10,3]]) were artifacts of the zero-syndrome length bug; at L = 4
exactly one clean configuration exists (all 15 anchors, k = 1).

Exact small-L map (blocked enumeration, 2000 solutions/level, each
re-verified by GF(2) rank + exhaustive weight-<=2 test):

| L | n | max k | code | g | status |
|---|---|---|---|---|---|
| 6 | 36 | 4 | [[36,4,3]] | 1.000 | **submitted, PR #757, CI-green** |
| 8 | 64 | 5 | [[64,5,3]] | 0.703 | complete (UNSAT below 50 anchors) |
| 10 | 100 | 10 | [[100,10,3]] | 0.900 | complete (UNSAT below 74) |
| 12 | 144 | 13 | [[144,13,3]] | 0.813 | plateau (20+ levels) |
| 14 | 196 | 17 | [[196,17,3]] | 0.781 | running |

[[36,4,3]] is the L = 6 optimum (exact CNF UNSAT below 29 anchors; no
sampled 29-32-anchor config exceeds k = 4); gate-passed
(board_advancing: true), weight-3 witnesses both sides (d = 3 exactly),
g = 1.0 — first SAT-exact parity-club member, new Pareto point in its
cell. The small-L band tops out *at* parity
(max k ~ n/10, boundary anchors dominate); the k/n ~ 0.17 region stays
out of reach here. Value: the exact frontier map and the encoder.

## Update 6: multiband swept, occupied, hardened — d = 4 wall confirmed

**Exhaustive sweep.** The full (d, rows, m, pitch) space — d in
{3,5,7,9,11,13}, rows 1-8, m 1-20, pitch [d-2, d+3], n <= 700; 13,376
points — enumerated with the validated builder, scored by exact GF(2)
rank, filtered against the Pareto front *including open PRs* (the first
pass missed #745-#747 and briefly rediscovered [[641,17,7]]): 549
nondominated triplets, 336 passing a 4000-trial witness screen. Degenerate
masks scored rank-g up to 5.5 — every one refuted; (n, k) alone says
nothing about distance.

**Eight new PRs** (#758-#765, all gate-passed via 20,000-trial witnesses):
[[608,32,5]] and [[532,28,5]], g = 1.3158 (highest after #749's 1.3278);
[[515,27,5]], [[595,31,5]], [[557,29,5]], [[519,27,5]], [[481,25,5]],
[[443,23,5]] at g = 1.298-1.311. All Pareto-nondominated d = 5 points —
frontier breadth, not record challenges (record remains [[656,114,3]] at
1.564). A pipeline bug (omitted model provenance) was caught and fixed on
all eight branches.

**The d = 4 wall is real.** Chamfer annealer revived with pair moves
(swap2/add2/rm2), warm-started at the k = 51 configuration, 6 h, 900+
restarts: best remained k = 51. Three independent move classes
converge on the same ceiling — [[676,51,4]] (#753) is the terminal rung;
d = 4 progress requires a new mechanism.

**Deep re-screen.** All 336 survivors re-searched at 300,000 trials
(75x, ~91 min): zero refutations. Open: sup g needs a mechanism beating
the multiband asymptote; the [d^2/2, d^2) band is empty.

## Update 7: the corrected asymptote, a process error, and the collapse boundary

**Process error, on the record.** An initial asymptotic scan ran ~2.5 h
using expected_k = rows*m - floor(rows/2) without validating it at the
scan extremes; headline values (sup g up to 3.58) were garbage — exact
rank at d = 5, rows = 24, m = 32, pitch = 2 gives k = 63, not 756. Rule:
exact-verify closed-form invariants at the extremes before scanning.

**Collapse boundary.** expected_k holds at pitch >= d + 1 (verified
d = 5..13) and at large pitch; collapses at pitch <= d (k = 63 at d = 5
pitch <= 4; k = 15 at d = 13 pitch = 10) and partially at pitch = d + 2
for d = 5, 7 (k = 143, 128 vs 756). The fine structure is
parity/phase-dependent, not characterized in closed form; k is not
additive across overlapping bands.

**Corrected result.** The pitch = d + 1 "rising ladder" (rank-g 1.4323,
1.5301, 1.5939, 1.6386 at d = 5, 7, 9, 11) was refuted by the first
witness past d = 5: d = 7 at pitch 8 has d_ub = 6. Distance preservation
requires pitch >= 2-floor(3d/4) ~ 1.5d, exceeding d + 1 for d >= 7 (d = 5
held because pitch_min(5) = 6 = d + 1). Recomputed at pitch = pitch_min
(rows = 24, m = 32, exact rank):

| d | pitch | n | exact k | g | witness (4k trials) |
|---|---|---|---|---|---|
| 5 | 6 | 13,196 | 756 | **1.4323** | HOLDS |
| 7 | 10 | 28,488 | 756 | 1.3003 | pending |
| 9 | 12 | 44,124 | 756 | 1.3878 | pending |
| 11 | 16 | 70,086 | 756 | 1.3052 | pending |
| 13 | 18 | 93,540 | 756 | 1.3659 | pending |

The corrected asymptote oscillates around ~1.30-1.43 with no rising
trend in d (d = 1 mod 4 sits higher than d = 3 mod 4); g has not converged
in rows/m. Witnessed sup: **1.4323 at d = 5** — above the 4/3 two-band
asymptote, below the record; BPT's cap c(4) must sit above ~1.43. Board
relevance: none directly — valid-regime configs have n >= 13,196, an order
over the 700 cap; the cap is what makes g hard (capped optimum 1.3158).
Remaining: witness verdicts (GF(2) basis prep at n >= 28k, ~30-80
min/code), the validity-boundary closed form, g convergence.

**Addendum: pitch_min measured at d = 11, 13 — closed form found.**
Mapped with rows = 4, m = 3 configs (exact rank for k-unlock, 4k-trial
witness; reproduces 6, 10, 12 for d = 5, 7, 9). New: pitch_min = 16 at
d = 11, 18 at d = 13. All five points fit **pitch_min(d) =
2-floor(3d/4)**. Structure: below pitch ~ d + 1, k never unlocks (stays at
2m - 1); between unlock and pitch_min, k holds but distance is deficient;
full k and design distance arrive together at pitch_min. The g at these
points (1.175 at d = 11, 1.205 at d = 13) confirms the raised-pitch curve
is Pareto-relevant, not a density record; the manifold subtraction is complete. (Caveat: measured d all odd; 5 points — d = 15, 17 would confirm or
break it.)

## Update 8: the exact d >= 4 encoder and the first exact d >= 4 maps

The d >= 4 analogue is simpler than feared: all anchors have even
weight, so rowspace(H) has only even-weight vectors — every odd-weight
error is a logical **iff its opposite-syndrome is zero**.
The exact d >= 4 CNF: weight-1 coverage, weight-2 pair clauses (as
Update 5), and weight-3 triple clauses (for every triple T, at least one
opposite-type anchor meeting T in an odd number of qubits must be active),
sound and complete for d >= 4. Validation: the clean k = 51 chamfer config
yields zero zero-syndrome triples both sides (agreeing with the exhaustive
weight->=3 test), a dirtied config yields them, and the L = 12 solver
output was re-verified independently.

First exact d >= 4 maps (full triple materialization; ~1M clauses at
L = 12, solved in seconds; UNSAT lines authoritative):

| L | n | max k (d >= 4) | g | max k (d >= 3) |
|---|---|---|---|---|
| 6 | 36 | 1 | 0.25 | 4 |
| 8 | 64 | 5 | 0.70 | 5 |
| 10 | 100 | 7 | 0.63 | 10 |
| 12 | 144 | 13 | 0.8125 | 13 |

At L = 8 and L = 12 the d >= 4 optimum has the same k as the d >= 3 one
but a different anchor set (the d >= 3 optima carry weight-3 witnesses) —
genuinely new codes, not relabelings. The L = 12 d >= 4 configuration is
saved to local staging with an independent-verification tag.

**The 26 x 26 question ([[676,52,4]]?) stays open** at this date. Lazy
CEGIS (solve, enumerate zero-syndrome triples in O(n^2) via syndrome-XOR
grouping, add clauses, re-solve) does not converge at A = 625 — the dirty
space is vast (models with k = 99 exist). Available: the exact encoder, a
fast triple enumerator, a warm-start harness. Missing: a convergence
strategy (structural materialization of ~51M triple-clause subsets, or a
direct encoding of the 3-sum-free syndrome condition). The k = 51 wall
stays empirical.

**Corrected-asymptote screens:** d = 5 HOLDS (d_ub = 5) and d = 7 HOLDS
(d_ub = 7) at pitch = pitch_min — 2 for 2, with d = 9, 11, 13 pending
(GF(2) basis preparation at n >= 44k runs ~3-10 h per code).

## Addendum: two distinct thresholds, not one

Exact-rank sweeps at rows = 4 separate the raised-pitch family's two
boundaries: **k-unlock at pitch = d + 1** (exact, all five d = 5..13;
below it, overlapping bands annihilate checks and k stays at 2m - 1), and
**distance preservation at pitch_min = 2-floor(3d/4)**. Between the two,
k is fully unlocked but distance is deficient (d = 11, pitch = 12: k = 10
but d_ub = 6, confirmed at 100k trials) — a previously invisible region.
The asymptote's oscillation (d = 1 vs 3 mod 4) likely shares this
parity structure. Open: the closed form of 2-floor(3d/4); the deficient
logical at d = 11, pitch = 12 is weight 5-6 (no weight-<=4 zero-syndrome
logical exists, checked exhaustively), geometry not extracted — the hunt
was cut as illustration-not-result, resumable at weight-5/6.
