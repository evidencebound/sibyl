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
13 passed
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

## 4. Prove physical Sibyl row deletion

Use another database path that does not already exist:

```bash
python scripts/physical_deletion_acceptance.py --db physical-deletion.db
```

Expected shape:

```text
DELETE_A AUTHORIZED pid=<pid-a>
DELETE_B deleted_rows=1 pid=<pid-b>
DELETE_C HUMAN_REQUIRED reason=NO_AUTHORITY_MEMORY governed_action_executed=false remaining_rows=0 pid=<pid-c>
```

Session A writes and authorizes a grant. Session B is a new process and permanently removes that exact authority entity through Sibyl's official `delete_entity` API. Session C is a third process, reads the same database, observes zero matching authority rows, and refuses action until a human grants new authority. All three PIDs must differ.

This is an application-level SQLite row hard delete through the official SDK. It does not claim forensic secure erasure of the database file or storage medium.

## 5. Prove memory-unavailable behavior

```bash
python scripts/deletion_acceptance.py
```

Expected output:

```text
memory_available=false authority_status=BLOCKED reason=AUTHORITY_MEMORY_UNAVAILABLE governed_action_executed=false
```

This separately proves the evaluator fails closed when its entire authority-memory input is unavailable. It passes `None` to the evaluator; it is not the physical-deletion test.

## 6. Inspect the load-bearing boundary

The smallest useful review surface is:

- `src/evidencebound_recallguard/sibyl_store.py`
- `src/evidencebound_recallguard/evaluator.py`
- `scripts/judge_acceptance.py`
- `scripts/physical_deletion_acceptance.py`
- `scripts/deletion_acceptance.py`
- `tests/test_judge_cli.py`
- `.github/workflows/ci.yml`

The store owns Sibyl reads, writes, and exact-entity deletion. The evaluator owns deterministic authorization. The acceptance scripts independently demonstrate cross-process recall/revocation, physical row deletion, and memory-unavailable behavior. CI pins the real SDK and executes every current gate.

## Independent evidence

The implementation merge commit is [`c81dec0`](https://github.com/evidencebound/sibyl/commit/c81dec01b18f07dc1d73978365135976f1ca0baf). Its post-merge GitHub Actions run is [33517924901](https://github.com/evidencebound/sibyl/actions/runs/33517924901).

The documentation checkpoint [`022b37e`](https://github.com/evidencebound/sibyl/commit/022b37e0f4c3a12e4c878a222391c98f7bbcac1a) passed the prior runtime gates in [run 33532206327](https://github.com/evidencebound/sibyl/actions/runs/33532206327). The physical-deletion checkpoint [`92892da`](https://github.com/evidencebound/sibyl/commit/92892dad00dd65d60932cbe7166f2ad3b1595f75) passed 13 tests in [run 33535080048](https://github.com/evidencebound/sibyl/actions/runs/33535080048). Every updated PR head requires fresh CI before merge.

See [Acceptance Evidence](ACCEPTANCE_EVIDENCE.md) for the exact recorded outputs and claim boundaries.
