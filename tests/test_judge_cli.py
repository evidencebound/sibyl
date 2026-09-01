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


@pytest.mark.skipif(
    importlib.util.find_spec("sibyl_memory_client") is None,
    reason="real sibyl-memory-client not installed",
)
def test_physical_deletion_roundtrip_uses_three_fresh_processes(tmp_path):
    db = tmp_path / "physical-deletion.db"
    cmd = [
        sys.executable,
        "scripts/physical_deletion_acceptance.py",
        "--db",
        str(db),
    ]
    cp = subprocess.run(cmd, text=True, capture_output=True)

    assert cp.returncode == 0, cp.stdout + cp.stderr
    assert "DELETE_A AUTHORIZED" in cp.stdout
    assert "DELETE_B deleted_rows=1" in cp.stdout
    assert (
        "DELETE_C HUMAN_REQUIRED reason=NO_AUTHORITY_MEMORY "
        "governed_action_executed=false"
    ) in cp.stdout

    deletion_pids = re.findall(r"DELETE_[ABC].* pid=(\\d+)", cp.stdout)
    assert len(deletion_pids) == 3, cp.stdout
    assert len(set(deletion_pids)) == 3, (
        "Physical deletion sessions A, B, and C must execute in distinct "
        "Python processes:\\n" + cp.stdout
    )
