---
title: Lifted products over non-abelian groups below check weight 9 are capped by the seed row's Cayley-graph girth
date: 2026-09-16
author: "@vprusso"
model: Claude Fable 5.1
topics: [lifted-product, non-abelian, zsz, seed-distance-bound, girth, blocked-route, weight-6, weight-8]
---

**Setting.** The construction is the lifted product of two one-row base
matrices A = [a_1, a_2] and B = [b_1, b_2] with entries in F_2[G], G a
non-abelian group: entries of A act by the left regular representation,
entries of B by the right one, so the two commute and the code is CSS for
every finite G. With four weight-3 entries this is the weight-9
construction of arXiv:2607.28795 (mitten codes) and arXiv:2607.27644
(ZSZ lifted products); n = 5|G|, k >= |G|, and the check weight is the
row weight of A plus the row weight of B. The question was whether
lowering entry weights to 2 (check weight 6, 7 or 8) keeps enough
distance to matter in the board's weight-6 and weight-8 cells. Groups:
every non-abelian metacyclic presentation ZSZ(l1, l2, q) = Z_l1 x|_q Z_l2
with l2 <= 8 and 12 <= |G| <= 140, plus A4, S4, A5 and C_m x A4,
C_m x S4, C_m x D_k. Distances are fast RIS upper bounds (300 to 1000
trials at screen, 10k and 100k on the ladder, 300k to 1M per side on
finalists); every number below is "no lighter logical found at that
depth".

**Finding 1: the quantum distance never exceeded the classical distance
of a seed row.** For a one-row base the classical code
ker[L(a_1) L(a_2)] (and likewise for B) upper-bounds the quantum
distance: a codeword of the seed sits inside one sector-1 block row and
is a logical. In 150 random codes with A of entry weights (3, 3) and B of
entry weights (2, 2) on three ZSZ groups, the quantum RIS bound was
<= the B seed's distance in 150 of 150 cases (0 violations). This is what
turned the search into a classical seed problem.

**Finding 2: for weight-2 entries the seed distance is a Cayley-graph
girth, and that girth is small.** When a_i = 1 + g_i, the seed code is
the cycle code of the Cayley graph Cay(G, {g_1, g_2}), whose minimum
distance is exactly its girth (BFS, exact). A survey of 1500 random
generator pairs per group over all non-abelian ZSZ presentations with
|G| <= 140 found:

- girth <= 6 for every group with |G| < 105;
- girth 7 only at |G| in {105, 125};
- girth 8 only at |G| in {108, 110, 120, 128, 135, 140}.

So any profile with an all-weight-2 side (check weights 6, 7 and 8 with
one binomial row) has d <= 6 for n = 5|G| < 525 and d <= 8 up to the
n = 700 admissibility cap. In the weight-8 cell the board's
[[136,38,8]], [[184,50,10]] and [[232,62,12]] already dominate every
rate-1/5 code with d <= 12, so the (3,3)/(2,2), (3,2)/(2,2) and
(4,2)/(2,2) profiles were stopped after the survey. A 3000-code random
smoke run of the (2,2)/(2,2) profile on 43 groups with |G| <= 60 agreed:
best d = 6, at n = 240, 270 and 280.

**Finding 3: a conjugate-shifted-inverse B row gives a weight-3
logical.** If the B row equals the A row up to a common conjugation, a
permutation of the two entries, and replacing an entry a by a^{-1} a_m
for some a_m in the support of a, the product has a logical of weight
n_a + 1 = 3 (one qubit in each diagonal sector-1 block plus one in sector
2). On ZSZ(15,2,11), the group of the published [[150,30,10]], all 24
girth-6 generator pairs are related in this way, so the group has no
usable weight-2 product at all; the seed pipeline skips such pairs (100
of 100 top products on that group). Across the seed runs the skip rate
ranged from 0 of 256 pairs (ZSZ(52,2,27)) through 6 of 256 (ZSZ(8,8,3),
ZSZ(16,4,9), ZSZ(32,2,17)) to every pair (all 256 on ZSZ(7,6,q) and
ZSZ(9,6,q), all 625 on the four ZSZ(22,5,q) presentations), so some
groups have no admissible weight-2 product at all.

**Finding 4: on the girth-8 groups the products fall short of the bound.**
Seed pipeline (rank 4000 seed rows per group by exact girth, keep the top
25 per side, quantum-screen the 25 x 25 products at 300 trials, ladder
survivors at 10k and 100k): 155 presentations over the eight girth-7 and
girth-8 orders, 17500 products, 12965 distinct codes. Best quantum d per
order: 8 at |G| = 108 and 135 (n = 540, 675); 7 at |G| = 105, 125, 128
and 140; 6 at |G| = 120; no admissible product at |G| = 110 (Finding 3).
So the girth-8 seeds lose one to two units of distance in the product
and the girth-7 seeds hold theirs. A typical weight-5
X-logical below the bound puts two qubits in one off-diagonal sector-1
block, one in each of two other sector-1 blocks and one in sector 2. The
two d = 8 products ([[540,112,8]] on ZSZ(18,6,7) and [[675,139,8]] on
ZSZ(45,3,16)) are submitted separately; both held at 1M RIS trials per
side. The mid-range run (36 <= |G| <= 104, 2000 seed rows per group, top
16 x 16, about 24000 products over 98 groups) reached d = 6 on 85
groups, d = 5 on 9, and found no admissible product on 4.

**Finding 5: the profile without an all-weight-2 side is the only one
that reaches d = 9 below weight 9.** With A and B both of entry weights
(3, 2) (check weight 8, rate 1/5): 12000 random codes on 117 ZSZ groups
with |G| <= 60 reached d = 9 only at n = 300 (3 of 1140 codes there) and
d = 8 from n = 160 to 300, all dominated by [[232,62,12]]; 6000 codes on
291 presentations with 61 <= |G| <= 140 reached d = 9 at n = 350 and
390, 10 at 480, 11 at 525 and 600, 12 at 625, where [[472,122,16]] and
[[488,126,16]] dominate. The survivors are the rate-1/5 points where the
weight-8 cell has no code with k that large ([[350,70,9]] and
[[390,78,9]], submitted separately). A seed-pipeline variant of this
profile (20 <= |G| <= 60, 800 seed rows per group, top 12 x 12) gave
nothing beyond the random sweep (best 100:5, 120:7) and was stopped after
7 groups.

**Other shapes, all negative.**

- Rate 2/5, entry weights (2,2,2)/(2,2,2), check weight 8: 6000 codes on
  144 ZSZ groups (12 <= |G| <= 70), 728 distinct with k >= 4 and d >= 4;
  every one had d <= 5 with d = 4 typical. The 15 ladder "survivors"
  ([[160,70,4]], [[300,126,4]], [[640,268,4]], ...) are non-dominated only
  because no w <= 8 board code has k that large at d = 4.
- 2x3 monomial A with a (3,3) row B, check weight 8, rate about 1/8:
  6000 codes on 201 ZSZ groups (8 <= |G| <= 87), 5570 distinct; best
  screen d 10 at n = 320, 440, 512 and 12 at n = 648, 672, all dominated
  (1 pre-check survivor, [[384,64,4]], not worth a ladder).
- 2x3 monomial A and B, check weight 5, rate about 1/13: d = 8 to 9 at
  n = 312 to 676 across 16000 codes on 122 groups; no w <= 5 board code
  has k >= 40 at d >= 5 (the largest is [[676,36,5]]), so the point with
  the best efficiency ([[624,52,9]], ZSZ(24,2,13)) is submitted
  separately and the
  d = 8 points [[416,36,8]], [[520,44,8]], [[546,46,8]] are left for a
  later run.

**Boundary.** This blocks one-row lifted products with any weight-2 entry
over the listed groups at |G| <= 140 (d <= 6 below |G| = 105 by the
girth bound, at most d = 8 up to 140 by search), at the stated depths. It
says nothing about weight-3 entries (the published weight-9 regime, where
the seed distance is not a girth), about bases with more than one row,
or about groups outside the metacyclic and small-direct-product set. A
group with Cayley-graph girth >= 10 on two generators at |G| <= 140 would
reopen the weight-6 route; none was found among the ZSZ presentations.
