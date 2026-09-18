"""The non-abelian lifted-product constructor must reproduce the board's [[150,30,10]].

codes/150-30-10.json is the ZSZ(15,2,11) lifted product of notes/150-30-10.md.
Rebuilding it from the four published trinomials and comparing the check sets
pins the module's regular-representation conventions (L(g)[gh, h] = 1 for the
left blocks, R(g)[h, hg] = 1 for the right blocks) to the board file; a
convention drift shows up here as a check-set mismatch.

Run: uv run pytest research/test_nonabelian_lp.py
"""

import json
import os

import numpy as np
from css import compute_k, verify_css
from nonabelian_lp import build_150_30_10, lp_shape, rebuild, sample_nonabelian_lp, zsz

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _rows(H):
    return {tuple(int(j) for j in np.nonzero(r)[0]) for r in H}


def test_rebuilds_board_150_30_10():
    with open(os.path.join(ROOT, "codes", "150-30-10.json"), encoding="utf-8") as f:
        doc = json.load(f)
    HX, HZ = build_150_30_10()
    assert HX.shape == (len(doc["checks"]["X"]), doc["n"])
    assert HZ.shape == (len(doc["checks"]["Z"]), doc["n"])
    # Same checks in the same order, not just the same set.
    assert [list(map(int, np.nonzero(r)[0])) for r in HX] == doc["checks"]["X"]
    assert [list(map(int, np.nonzero(r)[0])) for r in HZ] == doc["checks"]["Z"]
    assert verify_css(HX, HZ)
    assert compute_k(HX, HZ) == 30


def test_sampler_yields_css_codes_matching_lp_shape():
    groups = [("ZSZ(7,3,2)", zsz(7, 3, 2)), ("ZSZ(15,2,11)", zsz(15, 2, 11))]
    A_w, B_w = [[3, 2]], [[3, 2]]
    for spec, HX, HZ in sample_nonabelian_lp(3, groups=groups, A_w=A_w, B_w=B_w, seed=1):
        n, k_min, wX, wZ = lp_shape(spec["N"], A_w, B_w)
        assert HX.shape[1] == HZ.shape[1] == n
        assert verify_css(HX, HZ)
        assert compute_k(HX, HZ) >= k_min
        assert HX.sum(1).max() <= wX and HZ.sum(1).max() <= wZ
        assert spec["w"] == max(wX, wZ) == 8
        HX2, HZ2 = rebuild(spec)
        assert _rows(HX2) == _rows(HX) and _rows(HZ2) == _rows(HZ)
