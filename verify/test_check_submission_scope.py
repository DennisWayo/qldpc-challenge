"""Keep the scope check's notion of code data aligned with the workflow's.

codes/*.json and anything under circuits/<slug>/ are code data, so a PR
cannot pair a circuit-artifact change with a verifier edit any more than a
codes/ change.
"""
import check_submission_scope as S


def test_code_data_includes_entries_and_their_circuits():
    assert S.is_code_submission("codes/72-6-6.json")
    assert S.is_code_submission("circuits/72-6-6/memory_x.stim")
    assert S.is_code_submission("circuits/72-6-6/memory_z.dem")
    assert not S.is_code_submission("circuits/README.md")
    assert not S.is_code_submission("codes/README.md")
    assert not S.is_code_submission("verify/ler_tools.py")


def test_verifier_stack_is_critical_not_code_data():
    for f in ("verify/ler_tools.py", "uv.lock", "pyproject.toml"):
        assert S.is_critical(f) and not S.is_code_submission(f)


def test_one_entry_with_its_circuit_artifacts_is_one_submission():
    # A first circuit tier adds four files under circuits/<slug>/ next to an
    # existing codes/<slug>.json; that is one submission, not five.
    paths = ["codes/72-6-6.json", "circuits/72-6-6/memory_x.stim",
             "circuits/72-6-6/memory_x.dem", "circuits/72-6-6/memory_z.stim",
             "circuits/72-6-6/memory_z.dem"]
    assert {S.submission_slug(p) for p in paths} == {"72-6-6"}
    assert S.submission_slug("codes/168-20-14.json") == "168-20-14"
    assert {S.submission_slug(p) for p in ("codes/a-1-1.json", "circuits/b-2-2/x.stim")} == {"a-1-1", "b-2-2"}
