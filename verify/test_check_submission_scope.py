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
