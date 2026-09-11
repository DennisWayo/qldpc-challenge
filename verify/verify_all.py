"""Verify every submission under codes/ and the verify/fixtures/ test inputs, and flag possible
duplicates by permutation-invariant signature. Used by CI. Exit 0 only if all
pass and no two codes/ entries share a signature.

This runs the cheap structural checks (schema, n/k/CSS/weight, witness validity,
duplicates) on every entry, plus the circuit-tier fast path (circuit_verify:
determinism, noise recipe, code binding, DEM + d_circ witness -- all
deterministic and cheap) on entries declaring one. Distance refutation is NOT
run here -- it is the per-submission job of gate_changed.py (changed files) and
the weekly job of refute_board.py (whole board, random seed)."""

import argparse
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from qldpc_verify import file_size_error, verify
from circuit_verify import verify_circuit
from ler_verify import verify_ler

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Temporary migration exception for entries that predate issue #921. The hard
# verifier still rejects these graphs; this board sweep reports them as warnings
# until the follow-up cleanup PR removes the entries and this set.
LEGACY_DISCONNECTED = frozenset({
    "codes/112-8-5.json",
    "codes/120-5-8.json",
    "codes/128-12-8.json",
    "codes/144-16-8.json",
    "codes/144-24-6.json",
    "codes/153-5-9.json",
    "codes/162-36-4.json",
    "codes/176-22-4.json",
    "codes/192-24-4.json",
    "codes/192-6-8.json",
    "codes/214-15-11.json",
    "codes/216-15-11.json",
    "codes/231-5-11.json",
    "codes/242-2-11.json",
    "codes/261-16-12.json",
    "codes/263-16-12.json",
    "codes/288-32-8.json",
    "codes/288-48-6.json",
    "codes/299-5-13.json",
    "codes/324-4-9.json",
    "codes/338-2-13.json",
    "codes/360-16-14.json",
    "codes/360-24-10.json",
    "codes/360-32-6.json",
    "codes/45-5-4.json",
    "codes/484-4-11.json",
    "codes/66-5-5.json",
    "codes/676-4-13.json",
    "codes/78-6-5.json",
    "codes/88-8-7.json",
    "codes/90-6-5.json",
    "codes/91-5-7.json",
    "codes/96-12-4-mvb.json",
    "codes/96-12-4.json",
})


def allow_legacy_disconnected(path, report):
    """Downgrade only the reviewed legacy connectivity failure to a warning."""
    failed = [c["check"] for c in report["checks"] if not c["ok"]]
    if path not in LEGACY_DISCONNECTED or failed != ["tanner_connected"]:
        return False
    detail = next(c["detail"] for c in report["checks"]
                  if c["check"] == "tanner_connected")
    print(f"WARN  {path}  -> {detail} (legacy entry; cleanup pending)")
    report["ok"] = True
    return True


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=ROOT,
                    help="repository tree containing codes/ to verify; verifier "
                         "code and fixtures still come from this checkout")
    args = ap.parse_args()
    code_root = os.path.abspath(args.root)
    code_paths = sorted(glob.glob(os.path.join(code_root, "codes", "*.json")))
    fixture_paths = sorted(glob.glob(os.path.join(ROOT, "verify", "fixtures", "*.json")))
    paths = code_paths + fixture_paths
    if not paths:
        print("no submissions found")
        sys.exit(0)
    failed = []
    sigs = {}
    fps = {}
    for p in paths:
        is_code = os.path.abspath(p).startswith(
            os.path.join(code_root, "codes") + os.sep)
        rel = os.path.relpath(p, code_root if is_code else ROOT)
        ferr = file_size_error(p)
        if ferr:
            failed.append(rel)
            print(f"FAIL  {rel}  -> file_size_within_limit: {ferr}")
            continue
        with open(p) as f:
            doc = json.load(f)
        rep = verify(doc)   # structural checks; refutation lives in gate_changed / refute_board
        allow_legacy_disconnected(rel, rep)
        circ = ""
        if rep["ok"] and is_code and doc.get("circuit"):
            slug = os.path.splitext(os.path.basename(p))[0]
            circuits_dir = os.path.join(code_root, "circuits", slug)
            crep = verify_circuit(doc, circuits_dir)
            if crep["ok"]:
                circ = (f", d_circ<="
                        f"{crep['earned_d_circ']['d_circ']['value']}")
            else:
                rep["ok"] = False
                rep["checks"] += [c for c in crep["checks"] if not c["ok"]]
            # measured-rate tier: an ler claim is re-measured,
            # never trusted; a missing decoder fails the claim rather than
            # skipping it, so an unverifiable number cannot merge.
            if rep["ok"] and (doc["circuit"] or {}).get("ler"):
                lrep = verify_ler(doc, circuits_dir)
                if lrep["ok"]:
                    lers = [doc["circuit"]["ler"][s]["ler_per_round"]
                            for s in ("X", "Z")]
                    circ += f", ler/round<={max(lers):.3g}"
                else:
                    rep["ok"] = False
                    rep["checks"] += [c for c in lrep["checks"]
                                      if not c["ok"]]
        if rep["ok"]:
            ed = rep["earned_distance"].get("d", {})
            print(f"PASS  {rel}  -> d{ed.get('value','?')} "
                  f"({ed.get('tier','-')}){circ}")
            if is_code:
                if "signature" in rep:
                    sigs.setdefault(rep["signature"]["hash"], []).append(rel)
                if "fingerprint" in rep:
                    fps.setdefault(rep["fingerprint"], []).append(rel)
        else:
            failed.append(rel)
            bad = [c["check"] for c in rep["checks"] if not c["ok"]]
            print(f"FAIL  {rel}  -> {', '.join(bad)}")

    # identical codes (same stabilizer group, same labeling): a hard error.
    identical = {h: v for h, v in fps.items() if len(v) > 1}
    if identical:
        print("\nIDENTICAL CODES (same stabilizer group) -- reject:")
        for h, v in identical.items():
            print(f"  {', '.join(v)}")
    # same WL signature but not identical: likely permutation-equivalent, flag
    # for human review (WL is a strong necessary condition, not a proof).
    soft = {h: v for h, v in sigs.items()
            if len(v) > 1 and not any(set(v) <= set(iv)
                                      for iv in identical.values())}
    if soft:
        print("\nPOSSIBLE EQUIVALENT CODES (same Weisfeiler-Leman signature; "
              "review):")
        for h, v in soft.items():
            print(f"  {h}: {', '.join(v)}")

    print(f"\n{len(paths)-len(failed)}/{len(paths)} passed")
    sys.exit(1 if (failed or identical) else 0)
