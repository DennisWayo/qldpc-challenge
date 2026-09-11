"""Tests for the issue #921 legacy Tanner-connectivity migration."""

import verify_all


def _disconnected_report():
    return {
        "ok": False,
        "checks": [{
            "check": "tanner_connected",
            "ok": False,
            "detail": "Tanner graph has 2 connected component(s)",
        }],
    }


def test_legacy_allowlist_is_explicit_and_bounded():
    assert len(verify_all.LEGACY_DISCONNECTED) == 34
    assert all(path.startswith("codes/") for path in verify_all.LEGACY_DISCONNECTED)


def test_legacy_disconnected_entry_is_warned_and_allowed(capsys):
    report = _disconnected_report()
    path = "codes/112-8-5.json"

    assert verify_all.allow_legacy_disconnected(path, report)
    assert report["ok"]
    assert "legacy entry; cleanup pending" in capsys.readouterr().out


def test_new_disconnected_entry_is_not_allowed():
    report = _disconnected_report()

    assert not verify_all.allow_legacy_disconnected("codes/new.json", report)
    assert not report["ok"]


def test_legacy_entry_with_another_failure_is_not_allowed():
    report = _disconnected_report()
    report["checks"].append({
        "check": "css_commutation",
        "ok": False,
        "detail": "not commuting",
    })

    assert not verify_all.allow_legacy_disconnected("codes/112-8-5.json", report)
    assert not report["ok"]
