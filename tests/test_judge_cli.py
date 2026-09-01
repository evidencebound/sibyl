import importlib.util
import re
import subprocess
import sys

import pytest


@pytest.mark.skipif(
    importlib.util.find_spec("sibyl_memory_client") is None,
    reason="real sibyl-memory-client not installed",
)
def test_fresh_process_judge_roundtrip(tmp_path):
    db = tmp_path / "judge.db"
    cmd = [sys.executable, "scripts/judge_acceptance.py", "--db", str(db)]
    cp = subprocess.run(cmd, text=True, capture_output=True)

    assert cp.returncode == 0, cp.stdout + cp.stderr
    assert "SESSION_B AUTHORIZED" in cp.stdout
    assert "SESSION_C INVALIDATED" in cp.stdout

    session_pids = re.findall(r"SESSION_[ABC] [A-Z]+ pid=(\d+)", cp.stdout)
    assert len(session_pids) == 3, cp.stdout
    assert len(set(session_pids)) == 3, (
        "Sessions A, B, and C must execute in distinct Python processes:\n"
        + cp.stdout
    )
