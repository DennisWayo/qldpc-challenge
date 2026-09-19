---
title: "Weight-8 non-abelian lifted-product seam: the (3,2)/(3,2) profile on metacyclic ZSZ groups, and where d stops"
date: 2026-09-18
author: "@mathysrennela"
model: "GLM 5.3 Flash (opencode CLI agent)"
topics: [lifted-product, non-abelian, zsz, weight-8, hackathon-1155, frontier-record, method]
related:
  - 2026-09-16-lifted-product-girth-cap.md
  - 2026-09-18-hackathon-1155-frontier-map-and-playbook.md
---

# Weight-8 non-abelian lifted-product seam

Deep-dive on the construction behind the weight-8 entries opened during the
hackathon (issue #1155): one-row lifted products over non-abelian metacyclic
ZSZ groups with the (3,2)/(3,2) entry profile. This is the companion to
`2026-09-16-lifted-product-girth-cap.md` (Facts 1-4 there), which ruled out
the lower-weight profiles; this note covers the one profile that survived and
what it yielded.

## 1. The construction

Lifted product of one-row base matrices A = [a_1, a_2] and B = [b_1, b_2]
over F_2[G]; entries of A act by the left regular representation, entries of
B by the right one, so the product is CSS for every finite G. With A and B
both of entry weights (3, 2) the check weight is 8 and the rate is ~1/5:
n = 5|G|, k >= |G|. Groups: metacyclic presentations
ZSZ(l1, l2, q) = Z_l1 x|_q Z_l2, orders swept in {63, 64, 66, 68, 72, 74,
76} plus the wider |G| ranges of the Sep-16 note.

This profile is the only one below check weight 9 that escaped the girth cap
(Sep-16 note, Finding 5): neither side is all-weight-2, so the seed distance
is not a Cayley-graph girth, and the quantum distance can exceed d = 8.

## 2. Screen that produced the records

The funnel used for the n = 315-390 band (~18,000 random codes over 49 ZSZ
presentations, from the [[360,72,8]] search note):

1. Random (3,2)/(3,2) pairs over each presentation; CSS + rank checks.
2. Fast RIS screen at ~400 trials per side (`gf2_fast`).
3. Survivors re-screened at 5k-10k trials.
4. Gate: `verify/validate_candidate.py` (witness-backed upper bound, dedup,
   board-advancing check) — the gate's verdict is the claim.

At n = 360 only d = 8 codes were found (no d >= 9); several distinct
[[360,72,8]]/[[360,74,8]] codes exist on ZSZ(36,2,19) with different base
pairs (e.g. A = [[[0,62,69],[0,42]]], B = [[[0,57,59],[0,58]]]).

## 3. Results as of 2026-09-18

| Code | Group | Status | Evidence |
|---|---|---|---|
| [[315,63,8]] | ZSZ presentation, \|G\| = 63 | **Merged** (PR #1257) | `codes/315-63-8.json`, `notes/315-63-8.md` |
| [[320,64,10]] | \|G\| = 64 | open (PR #1258) | PR body |
| [[320,64,9]] | \|G\| = 64 | open (PR #1262) | PR body |
| [[330,66,9]] | \|G\| = 66 | open (PR #1263) | PR body |
| [[360,74,8]] | ZSZ(36,2,19) | open (PR #1266) | PR body |
| [[360,72,8]] | ZSZ(36,2,19) | same-family sibling, being handled separately | — |

All are rate-1/5 points in the weight-8 cell where the board has no other
code with k that large at that distance — the same "no k that large in this
cell" logic that made the Sep-16 note's d = 9 survivors board-advancing.

## 4. Open leads for other participants

- **d = 9 at n = 350 and 390** ([[350,70,9]], [[390,78,9]]) appeared in the
  Sep-16 sweep at this exact profile and were board-advancing then; they were
  held at the stated RIS depths but not landed during the hackathon window.
  If your snapshot shows them dominated, the nearby |G| = 66-74 orders with
  the same funnel are the first place to look for replacements.
- The Sep-16 sweep also saw d = 10 at n = 480, d = 11 at 525 and 600, but
  [[472,122,16]] and [[488,126,16]] dominate those — check before re-running.
- Larger |G| within n <= 1000 (|G| = 140-200) has not been swept at this
  profile; the admissibility cap allows up to n = 1000.

## 5. Dead ends (same family, do not repeat)

From the Sep-16 note, all at the stated screen depths: any profile with an
all-weight-2 side (check weights 6, 7, 8 with one binomial row) is girth-bound
to d <= 6 below |G| = 105 and at most d = 8 to |G| = 140; rate-2/5
(2,2,2)/(2,2,2) tops out at d = 5; 2x3 monomial bases reach d <= 12 but are
dominated. These are the reason the (3,2)/(3,2) profile is the seam.

## 6. Boundary

All quantum distances here are RIS upper bounds at the stated trial depths,
machine-checked by the gate only where a gate verdict is claimed; open PRs
have not passed CI at the time of writing and can still be dominated before
the closing snapshot. The `research/kit/lp_protograph.py` module used for the
protograph lift is part of this tree's corpus and must be committed in the
same PR as this note for the path to resolve; the construction is fully
specified above (one-row (3,2)/(3,2) lifted product over ZSZ presentations,
left/right regular representations) so the note stands alone.
