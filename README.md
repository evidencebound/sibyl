# EvidenceBound RecallGuard

**Fail-closed authority memory for agents.**

RecallGuard uses Sibyl Memory to answer a dangerous question: *may this agent still act under a human decision made in an earlier session?*

Long-lived agents can remember preferences, context, and permissions. The failure mode is not simply forgetting. An agent may keep acting from an old grant after a human corrected or revoked it. RecallGuard stores human authority as a hash-linked Sibyl lineage and evaluates that lineage before the governed action can execute.

## Why Sibyl is load-bearing

This project does not use memory as decoration or chat history.

| Without Sibyl authority memory | With a valid Sibyl lineage |
| --- | --- |
| The evaluator receives no authority history. | A fresh process recalls the human grant. |
| Status is `BLOCKED`. | Exact evidence and policy bindings can produce `AUTHORIZED`. |
| The governed action does not execute. | A later correction or revocation produces `INVALIDATED`. |
| There is no JSON, environment, prompt, or cache fallback. | Recovery still requires a distinct human re-grant. |

The controlled action is allowed only when Sibyl returns a complete, valid, current human authority chain. Missing memory, malformed lineage, sequence gaps, digest tampering, non-human authority, stale evidence, and stale policy all fail closed.

## Judge quick start

Environment:

- Python 3.12 is verified in GitHub Actions
- project metadata permits Python 3.10 or newer
- network access is required for the first package installation
- use a new local database path for each judge acceptance run

```bash
python -m pip install -e . pytest
python -c "import importlib.metadata as m; assert m.version('sibyl-memory-client') == '0.8.0'"
pytest -q
python scripts/judge_acceptance.py --db judge-memory.db
python scripts/physical_deletion_acceptance.py --db physical-deletion.db
python scripts/deletion_acceptance.py
```

Expected acceptance shape:

```text
13 passed
SESSION_A AUTHORIZED pid=<pid-a>
SESSION_B AUTHORIZED pid=<pid-b>
SESSION_C INVALIDATED pid=<pid-c>
DELETE_A AUTHORIZED pid=<pid-a>
DELETE_B deleted_rows=1 pid=<pid-b>
DELETE_C HUMAN_REQUIRED reason=NO_AUTHORITY_MEMORY governed_action_executed=false remaining_rows=0 pid=<pid-c>
memory_available=false authority_status=BLOCKED reason=AUTHORITY_MEMORY_UNAVAILABLE governed_action_executed=false
```

The three PIDs must be different. Session A writes the human grant and exits. Session B starts in a new Python process, recalls the grant from Sibyl, authorizes the controlled action, writes a human revocation, and exits. Session C starts in another new process, recalls the lineage, and refuses the old authority.

The physical-deletion command writes an active grant, hard-deletes its Sibyl entity through the official `delete_entity` API in a second process, and proves from a third process that no authority rows remain and the action cannot execute. The final command separately proves fail-closed behavior when the entire authority-memory input is unavailable.

For the shortest evaluation path, see [Judge Guide](docs/JUDGE_GUIDE.md). Verified runs and exact evidence are in [Acceptance Evidence](docs/ACCEPTANCE_EVIDENCE.md).

## Authority state model

| Latest valid event | Result | Governed action |
| --- | --- | --- |
| No memory layer | `BLOCKED / AUTHORITY_MEMORY_UNAVAILABLE` | refused |
| No authority events | `HUMAN_REQUIRED / NO_AUTHORITY_MEMORY` | refused |
| Current `GRANT` with matching bindings | `AUTHORIZED / ACTIVE_HUMAN_GRANT` | permitted |
| `CORRECTION` or `REVOCATION` | `INVALIDATED / AUTHORITY_REVOKED_OR_CORRECTED` | refused |
| `RECOVERY` | `HUMAN_REQUIRED / EXPLICIT_REGRANT_REQUIRED` | refused |
| Evidence or policy mismatch | `STALE / AUTHORITY_BINDING_MISMATCH` | refused |
| Invalid lineage | `BLOCKED / LINEAGE_INVALID` | refused |

## Data flow

1. A human authority event is written through `SibylAuthorityMemoryStore`.
2. Sibyl stores it under the `recallguard_authority_event` category.
3. A later process lists and filters the events for the exact entity.
4. The evaluator verifies contiguous sequence numbers, predecessor digests, canonical event digests, human actor type, evidence binding, and policy binding.
5. Only `AUTHORIZED` sets `governed_action_executed=true`.
6. Revocation and correction remain in the lineage; they are not erased or silently overridden.
7. Recovery is not authority. A new human grant is required.
8. An explicit hard-delete operation removes only the selected entity's authority rows; a fresh process then requires new human authority.

## Repository map

- `src/evidencebound_recallguard/evaluator.py` — deterministic fail-closed authority evaluation.
- `src/evidencebound_recallguard/sibyl_store.py` — Sibyl entity adapter and cross-entity filtering.
- `scripts/judge_acceptance.py` — real SDK, three-process grant/recall/revocation acceptance.
- `scripts/physical_deletion_acceptance.py` — real SDK, three-process hard-delete and fresh-read acceptance.
- `scripts/deletion_acceptance.py` — memory-unavailable fail-closed acceptance.
- `tests/` — evaluator, adapter, real SDK, CLI, physical-deletion, and memory-unavailable tests.
- `.github/workflows/ci.yml` — pinned SDK, test, judge, and fail-closed gates.
- `docs/DEMO_SCRIPT.md` — recording-ready 2–5 minute demo narrative.

## Build-period boundary

This is a competition build with an independent public history created after the build window opened. Pre-build research remains separately frozen in [`evidencebound/evidencebound-labs`](https://github.com/evidencebound/evidencebound-labs) on [`research/sibyl-2026-prebuild`](https://github.com/evidencebound/evidencebound-labs/tree/research/sibyl-2026-prebuild); it is not represented here as build-period implementation.

See [Build Status](BUILD_STATUS.md) for the current verified and unverified scope.
