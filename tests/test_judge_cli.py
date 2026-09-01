import importlib.util
import subprocess, sys
import pytest

@pytest.mark.skipif(importlib.util.find_spec("sibyl_memory_client") is None, reason="real sibyl-memory-client not installed")
def test_fresh_process_judge_roundtrip(tmp_path):
    db = tmp_path / "judge.db"
    cmd = [sys.executable, "scripts/judge_acceptance.py", "--db", str(db)]
    cp = subprocess.run(cmd, text=True, capture_output=True)
    assert cp.returncode == 0, cp.stdout + cp.stderr
    assert "SESSION_B AUTHORIZED" in cp.stdout
    assert "SESSION_C INVALIDATED" in cp.stdout
