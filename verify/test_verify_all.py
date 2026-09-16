"""verify_all orchestration: which entries pay the sampled LER replica.

With --ler-base REF only entries whose codes/<slug>.json or circuits/<slug>/
changed since REF are re-measured (PR runs); without it every claim is (pushes
to main). An unusable ref falls back to re-measuring everything, so a broken
diff can only cost time, never coverage. The verifiers themselves are faked:
this tests the routing, not stim.
"""
import json
import os
import subprocess

import verify_all as VA

OK_REP = {"ok": True, "earned_distance": {"d": {"value": 1, "tier": "t"}},
          "computed": {}, "checks": []}
OK_CIRC = {"ok": True, "earned_d_circ": {"d_circ": {"value": 1}}, "checks": []}
LER = {b: {"ler_per_round": 1e-3} for b in ("X", "Z")}


def _git(cwd, *args):
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *args],
                   cwd=cwd, check=True, capture_output=True, text=True)


def _write(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)


def _repo(tmp_path):
    """Build a repo: main has three ler entries; pr edits a's JSON and b's circuit."""
    root = str(tmp_path)
    for s in ("a-1-1", "b-1-1", "c-1-1"):
        _write(root, f"codes/{s}.json", json.dumps({"name": s, "circuit": {"ler": LER}}))
        _write(root, f"circuits/{s}/memory_x.stim", "# base\n")
    _git(root, "init", "-q", "-b", "main")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "base")
    _git(root, "checkout", "-q", "-b", "pr")
    _write(root, "codes/a-1-1.json",
           json.dumps({"name": "a-1-1", "circuit": {"ler": LER}, "note": "edited"}))
    _write(root, "circuits/b-1-1/memory_x.stim", "# rescheduled\n")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "pr")
    return root


def _run(monkeypatch, argv):
    measured = []
    monkeypatch.setattr(VA, "verify", lambda doc: json.loads(json.dumps(OK_REP)))
    monkeypatch.setattr(VA, "verify_circuit", lambda doc, d: json.loads(json.dumps(OK_CIRC)))
    monkeypatch.setattr(VA, "verify_ler",
                        lambda doc, d: (measured.append(doc["name"]), {"ok": True})[1])
    rc = VA.main(argv)
    return rc, sorted(measured)


def test_pr_run_measures_only_changed_entries(tmp_path, monkeypatch, capsys):
    root = _repo(tmp_path)
    rc, measured = _run(monkeypatch, ["--root", root, "--ler-base", "main"])
    assert rc == 0
    assert measured == ["a-1-1", "b-1-1"]          # JSON edit and circuit edit; not c
    c_line = next(ln for ln in capsys.readouterr().out.splitlines() if "c-1-1.json" in ln)
    assert c_line.startswith("PASS") and "ler unchanged since base" in c_line


def test_default_run_measures_everything(tmp_path, monkeypatch):
    root = _repo(tmp_path)
    rc, measured = _run(monkeypatch, ["--root", root])
    assert rc == 0 and measured == ["a-1-1", "b-1-1", "c-1-1"]


def test_unusable_base_falls_back_to_everything(tmp_path, monkeypatch, capsys):
    root = _repo(tmp_path)
    rc, measured = _run(monkeypatch, ["--root", root, "--ler-base", "no-such-ref"])
    assert rc == 0 and measured == ["a-1-1", "b-1-1", "c-1-1"]
    assert "re-measuring every ler claim" in capsys.readouterr().out


def test_skipped_claim_cannot_hide_a_failing_entry(tmp_path, monkeypatch):
    """Skip only the replica: circuit failures on an unchanged entry still fail.

    A skipped LER re-measurement must not turn into a skipped entry.
    """
    root = _repo(tmp_path)
    bad = dict(OK_CIRC, ok=False, checks=[{"check": "dem_matches", "ok": False}])
    monkeypatch.setattr(VA, "verify", lambda doc: json.loads(json.dumps(OK_REP)))
    monkeypatch.setattr(VA, "verify_circuit",
                        lambda doc, d: json.loads(json.dumps(bad if doc["name"] == "c-1-1" else OK_CIRC)))
    monkeypatch.setattr(VA, "verify_ler", lambda doc, d: {"ok": True})
    assert VA.main(["--root", root, "--ler-base", "main"]) == 1
