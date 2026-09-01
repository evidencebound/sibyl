# Demo Script

Target duration: 3 minutes 15 seconds. Maximum target: 5 minutes.

Record the terminal at readable zoom. Use a fresh checkout or clean working tree and a new database filename. Do not edit output, substitute fake PIDs, or describe unimplemented integrations.

## 0:00–0:20 — Problem

**Screen:** repository README title and one-line description.

**Narration:**

> Long-lived agents do not only remember preferences. They may remember permission to act. The dangerous failure is authority resurrection: a human revokes a grant, but a later agent session still acts from stale memory. EvidenceBound RecallGuard makes human authority a verified, fail-closed Sibyl Memory lineage.

## 0:20–0:45 — Why memory is load-bearing

**Screen:** README section “Why Sibyl is load-bearing.”

**Narration:**

> Sibyl is not used for decoration or conversation history. It is the only persistence layer carrying the human grant between independent processes. If that memory is unavailable, the controlled action is blocked. There is no prompt, JSON, environment, or cache fallback.

## 0:45–1:05 — Real SDK and tests

**Screen:** terminal.

Run:

```bash
python -m pip install -e . pytest
python -c "import importlib.metadata as m; print(m.version('sibyl-memory-client'))"
pytest -q
```

**Narration:**

> The project pins the real Sibyl Memory client at version 0.8.0. The suite covers authority evaluation, lineage failure, cross-entity filtering, real SDK recall, the three-process path, and the deletion path. The judge environment must execute all tests without skips.

Pause long enough for `0.8.0` and the passing test count to be visible.

## 1:05–2:05 — Fresh-process authority lifecycle

**Screen:** terminal.

Run with a new database path:

```bash
python scripts/judge_acceptance.py --db demo-memory.db
```

**Narration:**

> Session A writes a human grant through Sibyl and exits. Session B is a new Python process. It receives no grant payload; it reconstructs the Sibyl client, recalls the grant, and becomes authorized. It then appends a human revocation and exits. Session C is another new process. It recalls the lineage and refuses the old authority as invalidated.

Point to the three different PIDs.

> Different PIDs prove process separation. The database path is the only shared location. The grant digest is not transferred through process memory or command-line arguments.

## 2:05–2:35 — Deletion/no-memory proof

**Screen:** terminal.

Run:

```bash
python scripts/deletion_acceptance.py
```

**Narration:**

> The negative path is the critical proof. With the authority-memory layer unavailable, RecallGuard returns BLOCKED, reports AUTHORITY_MEMORY_UNAVAILABLE, and keeps governed action execution false. Memory is therefore necessary for the action, not an optional enhancement.

## 2:35–3:00 — Trust semantics

**Screen:** `src/evidencebound_recallguard/evaluator.py`, centered on the lineage validation and final state branches.

**Narration:**

> Every event must come from a human actor and form a contiguous hash-linked lineage. Evidence and policy bindings must still match. Correction and revocation invalidate the old grant. Recovery does not silently restore authority; a distinct human re-grant is required. Malformed or missing lineage fails closed.

## 3:00–3:15 — Close

**Screen:** `docs/ACCEPTANCE_EVIDENCE.md`, showing the current evidence table.

**Narration:**

> RecallGuard demonstrates a compact human control plane for persistent agents: remember authority when valid, preserve its lineage, and refuse to act when authority is missing, stale, corrected, or revoked. Every claim shown here is reproducible from the public repository and its GitHub Actions evidence.

## Recording acceptance checklist

- Repository URL is visible.
- `sibyl-memory-client` prints `0.8.0`.
- The full suite passes without skips.
- Session A, B, and C show three distinct PIDs.
- Session B shows `AUTHORIZED`.
- Session C shows `INVALIDATED`.
- Deletion output shows `BLOCKED` and `governed_action_executed=false`.
- Video duration is between 2 and 5 minutes.
- No private tokens, local usernames, notifications, or unrelated browser tabs appear.
- Final public video URL is added to the README and submission only after upload/readback verification.
