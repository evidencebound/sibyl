# Judge Guide

This path verifies the central implemented claim in about five minutes: Sibyl Memory is the only persistence layer carrying human authority across independent processes, and revoked authority does not resurrect.

## 1. Install

Python 3.12 is verified in GitHub Actions. Project metadata permits Python 3.10 or newer.

```bash
python -m pip install -e . pytest
python -c "import importlib.metadata as m; print(m.version('sibyl-memory-client'))"
```

Required version:

```text
0.8.0
```

## 2. Run the complete suite

```bash
pytest -q
```

Expected result:

```text
11 passed
```

No real-SDK test may be skipped in the judge environment. The CI job installs the pinned dependency before running the suite.

## 3. Prove real fresh-process recall

Pass a database path that does not already exist:

```bash
python scripts/judge_acceptance.py --db judge-memory.db
```

Expected shape:

```text
SESSION_A AUTHORIZED pid=<pid-a>
SESSION_B AUTHORIZED pid=<pid-b>
SESSION_C INVALIDATED pid=<pid-c>
```

Acceptance conditions:

- all three lines appear;
- all three PIDs are different;
- Session B is `AUTHORIZED`;
- Session C is `INVALIDATED`;
- the command exits with status 0.

What happens:

1. The parent orchestrator launches Session A as a child process.
2. Session A writes a human `GRANT` through `MemoryClient.local(...)`, evaluates it, prints its PID, and exits.
3. The parent launches Session B with only the database path and session name.
4. Session B reconstructs the Sibyl client, recalls the grant, evaluates it as `AUTHORIZED`, appends a human `REVOCATION`, prints its PID, and exits.
5. The parent launches Session C.
6. Session C reconstructs the client, recalls the full lineage, evaluates the old authority as `INVALIDATED`, and exits.

The grant digest is not passed through stdout, arguments, environment variables, JSON, or parent-process memory. Session B obtains it by reading Sibyl.

Use a new database filename before repeating this command; the acceptance intentionally creates an append-only authority lineage.

## 4. Prove memory-unavailable behavior

```bash
python scripts/deletion_acceptance.py
```

Expected output:

```text
memory_available=false authority_status=BLOCKED reason=AUTHORITY_MEMORY_UNAVAILABLE governed_action_executed=false
```

This proves the evaluator fails closed when its authority-memory input is unavailable. The script name is historical: it passes `None` to the evaluator and does not physically delete a Sibyl entity or database. Physical deletion acceptance is not yet implemented and remains an open competition gate.

## 5. Inspect the load-bearing boundary

The smallest useful review surface is:

- `src/evidencebound_recallguard/sibyl_store.py`
- `src/evidencebound_recallguard/evaluator.py`
- `scripts/judge_acceptance.py`
- `scripts/deletion_acceptance.py`
- `tests/test_judge_cli.py`
- `.github/workflows/ci.yml`

The store owns Sibyl reads and writes. The evaluator owns deterministic authorization. The acceptance scripts demonstrate the cross-process and memory-unavailable behaviors. CI pins the real SDK and executes every current gate.

## Independent evidence

The implementation merge commit is [`c81dec0`](https://github.com/evidencebound/sibyl/commit/c81dec01b18f07dc1d73978365135976f1ca0baf). Its post-merge GitHub Actions run is [33517924901](https://github.com/evidencebound/sibyl/actions/runs/33517924901).

The documentation checkpoint [`022b37e`](https://github.com/evidencebound/sibyl/commit/022b37e0f4c3a12e4c878a222391c98f7bbcac1a) also passed the same runtime gates in [run 33532206327](https://github.com/evidencebound/sibyl/actions/runs/33532206327). Final PR CI is required before merge.

See [Acceptance Evidence](ACCEPTANCE_EVIDENCE.md) for the exact recorded outputs and claim boundaries.
