---
title: "Hook-cost CNOT ordering and one flag per check take weight-6 codes to full circuit distance"
date: 2026-09-18
author: "@vprusso"
model: Claude Fable 5.1
topics: [circuit-tier, hook-errors, flag-qubits, cnot-scheduling, weight-6, calibration]
---

The circuit-tier entries of #1180 to #1203 (merged) and #1286 to #1290 (open
at the time of writing) are memory circuits of the `verify/circuit_tools.py`
`build_css_memory` shape: one ancilla per check, X block then Z block each
round, CX layers a proper edge coloring of each check type's Tanner graph.
Only the CNOT order of each check differs, and that alone decides whether
d_circ reaches d. The scheduling scripts are local staging output; the
description here is meant to be enough to rewrite them.

## Why random colorings fail at weight 6

A random coloring of [[30,4,6]] (`codes/30-4-6.json`) measured d_circ = 3/3,
and every weight-3 witness was three ancilla hooks: an X fault on an X-check
ancilla after its j-th CNOT puts X on the remaining w - j data qubits, which
modulo the check is a data error of weight min(j, w - j), up to 3 for w = 6.
Three such faults reach a weight-6 logical.

## Hook cost and the admissible orders

For a check with support Q and CNOT order (q_1, ..., q_w), let S_j =
{q_{j+1}, ..., q_w} be the suffix a hook after the j-th CNOT lands on. For a
data error set S, cost(S) is the fewest further data errors e with H_det (S
+ e) = 0 and L (S + e) != 0, where H_det holds the checks of the opposite
type and L the logicals they protect; cost(S) = cost(Q \ S) since the two
differ by the stabilizer. A single hook is 1 + cost(S_j) faults, so d_circ
<= min_j (1 + cost(S_j)) for the executed order. An order is admitted iff
every proper nonempty suffix has cost >= d - 1; the admitted set is
enumerated by DFS from the last CNOT so small suffixes prune first. Layer
assignment: each check picks an admitted order, its j-th CNOT goes in layer
j (spread over slot subsets when the check is lighter than the layer count),
no data qubit twice in a layer; solved by min-conflicts local search with
restarts.

When no order is admitted the output is a bound: for every order some hook
plus its completion is an explicit undetected logical, so d_circ <= max over
orders of min_j (1 + cost(S_j)) < d for every bare-ancilla schedule of the
code, sequential or interleaved. Surveyed codes of check weight 6 (or mixed
up to 6) with d >= 4 and no admitted order (bound for X-check / Z-check
hooks): [[12,2,4]] 3/3, [[16,4,4]] 2/2, [[19,1,5]] 4/4, [[24,6,4]] 3/3,
[[25,5,4]] 4/3, [[30,4,6]] 5/5, [[34,2,7]] 6/6, [[36,6,4]] 3/4, [[37,1,7]]
6/6, [[42,6,6]] 5/5, [[54,6,7]] 6/6. The criterion admits orders for the
merged full-distance entries [[72,12,6]], [[60,8,6]] and [[42,8,3]] (480,
112 and 720 per check) and none for [[70,6,8]] (bound 7) and [[72,8,7]]
(bound 6 on the X checks), which the RIS-only sweep of #927 had reported at
full distance: RIS false positives.

## The decoder cost is only an upper bound

The first version took cost(S) from an observable-constrained BP+OSD decode
of S's syndrome under [H_det; L_o] for each observable o. A decoder returns
a completion, not the cheapest one, so the value is an upper bound on
cost(S) and the criterion can admit an order it should reject. The first
bare staging of [[90,4,9]] (`codes/90-4-9.json`, weight 5) fell to 8: the
Z-memory witness was one X hook plus seven data errors, a suffix of true
cost 7 that the decoder had priced at >= 8. Exact costs admit 48 of 120
orders per check; BP+OSD had admitted 48 to 120.

Exact oracle: pack the m syndrome bits and k logical bits of each qubit's
column into one 64-bit word (m + k <= 64 on every code here), enumerate all
data error sets of weight <= a once into a sorted key table, and for each
target set of weight <= b find, by binary search, a partner with the same
syndrome and a different logical value; the first total weight with a hit is
cost(V), exact up to a + b = d - 2. For [[90,4,9]] (a = 4, b = 3) the table
has 2.55M entries and a suffix query takes about 40 ms.

## Hooks on different ancillas

Two hooks on different ancillas of the same type in the same block combine
to the data error S xor S' at 2 + f + f' + cost(S xor S') faults, f and f'
being 1 for a flagged hook and 0 otherwise. Bare stagings passing the
single-hook criterion lost this way: [[37,7,3]] 2/2, [[54,20,4]] 3/3,
[[54,8,6]] 5/4, [[62,10,6]] 5/6, [[112,2,10]] 9/8. Pair criterion: an order
pair of two checks is bad iff some reachable suffix pair has 2 + f + f' +
cost(S xor S') < d; the triangle bound cost(V) >= d - |V| over the four
stabilizer representatives of V settles most pairs, the rest are exact
queries, and the bad pairs enter the min-conflicts search as binary
constraints. On [[90,4,9]] this constrains 405 of the 990 check pairs per
side and forbids 126720 of 2.28M order pairs (282285 exact queries); the
schedule measures 9/9 at 23940 mechanisms per basis (#1290). A post-hoc
audit parses each check's executed slots from the committed stim files and
scores them under the exact oracle: on the six schedules of #1184 and #1286
to #1290 the cheapest single hook, same-ancilla pair and cross-ancilla pair
each cost exactly d in both bases.

## One flag per check

For order (q_1, ..., q_6) the ancilla executes CX_1, F1, CX_2, ..., CX_5,
F2, CX_6, where F is a CNOT between ancilla and flag (X check: flag in |0>,
CX(anc, flag), M; Z check: flag in |+>, CX(flag, anc), MX). The couplings
have the ancilla in the same role as the data CNOTs, so they commute with
them and cancel noiselessly; a hook between F1 and F2 also flips the flag,
and cancelling that record costs one more fault. The verifier admits this as
it stands: non-data qubits are only counted, the couplings are ordinary CX
under the canonical noise recipe, each in a layer of its own, and only
detectors that include a final-readout record are bound to the check rows,
so one single-record flag detector per round is legal. Cost: two more CX
layers per block, one more qubit per check, 17 to 30 percent more
mechanisms.

Single-fault inventory (DEPOLARIZE2 terms of CX_j): the ancilla term gives
S_j, the ancilla-and-data term gives S_{j-1}, both flagged iff 1 < j <= 5;
F2's own ancilla term gives S_5 unflagged and the hook after CX_1 gives S_1
unflagged. Admission: every single fault has 1 + [flagged] + cost >= d and
every same-ancilla pair has 2 + [statuses differ] + cost(S xor S') >= d. For
w = 6, d = 6 this reduces to: no consecutive triple of the order (positions
1-3, 2-4, 3-5, 4-6) lies inside a weight-6 logical. The first version
omitted the S_{j-1} shift, admitted 96 orders per check on [[30,4,6]], and
RIS refuted the schedule at weight 5 in 40 trials (two flagged faults on one
ancilla cancelling each other's flag, data error {q_2, q_3, q_4}); with the
shift 24 orders per check remain. Proven: one or two faults on one ancilla
plus data errors need >= d faults. Three or more ancilla faults are left to
the searches. With flags after slots 1 and n_slots - 1 every unflagged hook
is a single data error modulo the check, so at d = 4 and d = 3 the pair
criterion follows from the single one (all 720 orders per weight-6 check
admitted, zero constrained check pairs).

Results (RIS 2 x 600 trials per basis and the seeded BP+OSD search over the
stated share of mechanisms found nothing below d):

- [[30,4,6]]: 90 qubits, 7726 / 7721 mechanisms (bare 6563 / 6567), 6/6,
  full coverage; an exact MILP over H_dem stopped at dual bound 2 after 600
  s, so the claim is measured, not proven. `circuits/30-4-6/`, #1184.
- [[54,8,6]]: 24 orders per check, 11764 / 11762, 6/6, full coverage; bare
  5/4. #1286.
- [[62,10,6]]: 504 orders per check, 15996 / 15996, 6/6, coverage 15996 (X)
  and 6328 of 15996 (Z); bare 5/6. #1287.
- [[54,20,4]]: 5320 / 5316, 3/3 to 4/4, full coverage; LER 972 / 10000 (X)
  and 988 / 10000 (Z) failures at 4 rounds, 2.63e-2 and 2.68e-2 per round.
  #1288.
- [[37,7,3]] (weight-4 and weight-6 checks in 6 slots): 2890 / 2898, 2/2 to
  3/3, full coverage; LER 601 / 10000 and 566 / 10000 at 3 rounds, 2.09e-2
  and 1.96e-2 per round. #1289.
- [[90,4,9]] flagged: 28800 to 28890 mechanisms at rounds = 9, over the cap,
  hence the bare pair criterion.

## Limits

- The 25000-mechanism cap at rounds = d excludes weight-6 codes with d >= 10,
  weight-8 codes with d >= 8 and codes with check weight above about 12
  ([[90,8,10]] is at 34.6k).
- RIS does not refute at this DEM size: on the 13k to 24k DEMs, 2 x 600
  trials came back at weight 10 to 11 against d = 6 and at 17 / 19 against
  d = 9. The seeded search (per seed mechanism and observable, the
  lightest undetected set containing the seed that flips the observable)
  finds hook witnesses in seconds; on [[90,4,9]] it covered 11656 / 23940
  (X) and 7208 / 23940 (Z) seeds.
- `verify/ler_verify.py` has a 120 s replica budget per basis. [[63,3,5]]
  needed 120000 shots per basis to clear it; [[101,5,5]] (329 / 100000 and
  317 / 100000) and [[126,6,5]] (131 / 36000 and 229 / 52000) failed as
  unverifiable and carry no `ler` block; no d >= 6 rate was attempted.
- Minimum-weight structure does not predict the rate (#1024).
  `codes/16-2-4.json` and `codes/32-8-4.json`, both d_circ = 4, measure
  1.73e-3 and 1.66e-2 per round, yet exact enumeration gives 2644 weight-4
  logical fault sets per basis for [[16,2,4]] against 1048 / 1716 for
  [[32,8,4]] (mass 3.0e-8 against 3.9e-9 / 3.6e-9, hook sets under 1 percent
  of it). The gap is 1.67 against 0.87 expected faults per shot and the
  pinned decoder failing 4.8 percent of two-fault shots on [[32,8,4]] where
  0.16 percent are ambiguous. Fewer layers per round would help; a different
  order at the same depth would not.

## Open

[[7,1,3]] (weight 4, bound 2), [[42,6,6]] (bound 5), [[60,4,8]] (bound 7 on
the X checks) and [[54,6,7]] (bound 6) with flags. [[112,2,10]] (9/8 bare):
flags are over the cap, and the pair criterion at d = 10 needs an oracle
with a = b = 4 over n = 112 (6.8M-entry tables), not run. Full seeded
coverage of [[90,4,9]]. Interleaving the X and Z blocks (#1026) to cut
layers per round, which the #1024 finding says the rate needs.
