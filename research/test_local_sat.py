"""Regression test for the lex symmetry break in local_sat.py.

The break must yield at most one model per D4+XZ group-orbit -- a broken
break silently duplicates or drops codes instead of erroring.
lex_symmetry_selftest sits under `if __name__ == "__main__"` in
local_sat.py, which run_tests.py never executes; this module makes it a
collected test.

Run: uv run pytest research/test_local_sat.py
"""

import pytest

pytest.importorskip("pysat")

from local_sat import lex_symmetry_selftest  # noqa: E402


def test_lex_yields_at_most_one_per_d4xz_orbit():
    stats = lex_symmetry_selftest()
    assert stats["lex_yields"] == stats["lex_group_orbits"] > 0
