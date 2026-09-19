---
title: "Quadricycle (rank-4 multivariate bicycle): constructor, calibration, first find"
date: 2026-09-19
author: "@mathysrennela"
model: "GLM 5.3 Flash (Zed agent)"
topics: [multivariate-bicycle, quadricycle, generalized-bicycle, weight-4, calibration]
status: staged
related:
  - 2026-08-23-univariate-bicycle-sweep.md
  - 2026-07-01-trial-depth-floors.md
---

## The family, and the distinction that matters

A bicycle code is two block polynomials A, B over a group algebra F_2[G]:
H_X = [A | B], H_Z = [Bᵀ | Aᵀ], n = 2·|G|, check weight
|supp(A)| + |supp(B)|. What "multivariate" means depends on whether the
variables are *independent*:

- The trivariate codes of arXiv:2406.19151 use a **dependent** third
  variable z = x·y, so every trivariate code reduces exactly to an ordinary
  rank-2 BB code on a larger torus (verified: the kit's `bb.build_bb`
  rebuilds them exactly).
- A **quadricycle** takes four **independent** cyclic shifts on the rank-4
  torus G = Z_l1 × Z_l2 × Z_l3 × Z_l4. No rank-2 torus reproduces a genuine
  rank-4 code, so at fixed check weight and n this is a strictly larger
  search family: more distinct monomial-support geometries per unit n. CSS
  commutation is automatic (abelian group algebra).

Constructor committed in this PR: `research/quadricycle.py` (`build_quad`,
`sample_quadricycle`, `quad_shape`), same `(spec, HX, HZ)` shape as the
`research/kit/search.py` samplers. Sanity anchor: degenerate dims
(l, m, 1, 1) reproduces `research/kit/bb.py` array-exactly on the
[[112,2,10]] monomial set.

## Calibration (numbers, not adjectives)

- Backend: 100 RIS trials at n = 630 take 0.03 s with gf2_fast
  (`backend="auto"`) vs 3.1 s with NumPy; at n = 1250, 0.1 s vs 14.5 s.
  ~100×. Always screen with `backend="auto"`.
- Sampler: dims each in [2, 11] with prod ≤ 350 (n = 2·prod ≤ 700 cap),
  weight 2+2. Pilot of 200 candidates (seed 1), screened at 400 RIS trials
  with min_k = 2, min_d = 6: 50 survived (25%). Rank-4 sampling at small
  moduli produces many k ≤ 1 codes, so min_k screening matters.

## First find (submitted separately)

[[630,2,21]] on Z_3 × Z_3 × Z_5 × Z_7, A = 1 + x1·x2²·x3³·x4⁴,
B = x1²·x2·x3·x4⁶ + x2²·x3⁴·x4² — drawn by hand as the sampler's demo
instance, before any sweep. Confirmation ladder 2k → 8k → 30k RIS
trials/side flat at d ≤ 21, both sides witnessed. Trusted gate: passed, not
refuted (8k RIS), no exact or WL-equivalent duplicate, board-advancing in
weight-4 × unrestricted (previous best witnessed distance in the cell: 14).
Reproduction recipe and full evidence trail in its submission note.

## Boundary and reopen conditions

- The planned 4,000-candidate sweep was interrupted before completion; **no
  family-level negative result is claimed**. Unsearched: higher-k
  quadricycles (k ≥ 4), weight-6 (3+3) supports, dims outside [2, 11].
- Open question: one find does not establish the mechanism. Whether rank-4
  beats plain BB at fixed (n, w) beyond this point is exactly what the
  interrupted sweep would have started to answer; reopen with a completed
  sweep before concluding either way.
