# Acceptance Evidence

This ledger separates verified current evidence from unrun or future claims. Historical local checks are not promoted to current evidence.

## Implementation baseline

- Repository: [evidencebound/sibyl](https://github.com/evidencebound/sibyl)
- Implementation merge commit: [`c81dec01b18f07dc1d73978365135976f1ca0baf`](https://github.com/evidencebound/sibyl/commit/c81dec01b18f07dc1d73978365135976f1ca0baf)
- Pull request: [#1 — prove real fresh-process Sibyl recall](https://github.com/evidencebound/sibyl/pull/1)
- Post-merge workflow: [GitHub Actions run 33517924901](https://github.com/evidencebound/sibyl/actions/runs/33517924901)
- Workflow conclusion: `success`
- Runner: GitHub-hosted Ubuntu 24.04
- Python: 3.12
- SDK: `sibyl-memory-client==0.8.0`

Recorded implementation-baseline output:

```text
Successfully installed ... sibyl-memory-client-0.8.0
11 passed in 0.61s
SESSION_A AUTHORIZED pid=2390
SESSION_B AUTHORIZED pid=2391
SESSION_C INVALIDATED pid=2392
memory_available=false authority_status=BLOCKED reason=AUTHORITY_MEMORY_UNAVAILABLE governed_action_executed=false
```

## Documentation checkpoint

- Documentation commit: [`022b37e0f4c3a12e4c878a222391c98f7bbcac1a`](https://github.com/evidencebound/sibyl/commit/022b37e0f4c3a12e4c878a222391c98f7bbcac1a)
- Branch workflow: [GitHub Actions run 33532206327](https://github.com/evidencebound/sibyl/actions/runs/33532206327)
- Workflow conclusion: `success`
- Runtime files: unchanged from `c81dec0`

Recorded documentation-checkpoint output:

```text
Successfully installed ... sibyl-memory-client-0.8.0
11 passed in 0.53s
SESSION_A AUTHORIZED pid=2385
SESSION_B AUTHORIZED pid=2386
SESSION_C INVALIDATED pid=2387
memory_available=false authority_status=BLOCKED reason=AUTHORITY_MEMORY_UNAVAILABLE governed_action_executed=false
```

PID values are run-specific. Their significance is that all three are distinct.

## Physical-deletion checkpoint

- TDD test-only commit: [`f2a7f33`](https://github.com/evidencebound/sibyl/commit/f2a7f33c649ad0e0f56da46aa0ae496cd9de4ce4)
- Expected RED: [run 33534833256](https://github.com/evidencebound/sibyl/actions/runs/33534833256) failed because the physical-deletion script did not exist.
- GREEN commit: [`92892da`](https://github.com/evidencebound/sibyl/commit/92892dad00dd65d60932cbe7166f2ad3b1595f75)
- GREEN workflow: [run 33535080048](https://github.com/evidencebound/sibyl/actions/runs/33535080048)
- Result: `13 passed`, including the real SDK three-process hard-delete test.

The acceptance writes an authorized grant, deletes one exact-entity row through Sibyl's official `delete_entity` API, then opens the same database in a third process. The final process reads zero matching rows and returns `HUMAN_REQUIRED / NO_AUTHORITY_MEMORY` with action execution false. Every updated PR head must pass a fresh CI run before merge.

## Claim-to-evidence map

| Claim | Evidence class | Current result |
| --- | --- | --- |
| The official client is installed | package metadata assertion in CI | PASS — exactly `0.8.0` |
| Authority persists after Session A exits | Session B new-process recall | PASS — `AUTHORIZED` |
| Revocation survives Session B exit | Session C new-process recall | PASS — `INVALIDATED` |
| Sessions are separate OS processes | CLI output plus automated distinct-PID assertion | PASS |
| Unavailable memory fails closed | memory-unavailable acceptance | PASS — `BLOCKED` |
| Unavailable memory cannot execute the governed action | memory-unavailable acceptance | PASS — `false` |
| Unit and integration suite | pytest in the same workflow | PASS — 13/13 at deletion checkpoint |
| Physical Sibyl row deletion | official SDK delete and fresh-process reread | PASS — one deleted, zero remaining, action false |
| Public demo video | public media URL | UNRUN / not linked |
| Competition platform submission | live platform readback | UNVERIFIED |
| User or revenue impact | production telemetry | UNMEASURED |

## TDD evidence for the fresh-process fix

The history preserves the regression cycle:

1. Test-only commit [`f608672`](https://github.com/evidencebound/sibyl/commit/f608672d2710405ed537f1454741f32a6e13fe69) required three distinct Session A/B/C PIDs.
2. [Workflow run 33517494209](https://github.com/evidencebound/sibyl/actions/runs/33517494209) failed because the prior script only created new clients inside one process.
3. Minimal implementation commit [`018fdae`](https://github.com/evidencebound/sibyl/commit/018fdae6953d73b8b6f3b8d61488295412567746) launched three subprocesses.
4. [Workflow run 33517591452](https://github.com/evidencebound/sibyl/actions/runs/33517591452) passed.
5. PR CI and post-merge CI passed again.

## Trust boundary

The acceptance supports only the claims implemented in this repository. It does not claim that:

- SQLite page remnants or the storage medium have been forensically securely erased;
- Sibyl itself is tamper-proof against a host with filesystem control;
- a human identity has been cryptographically verified;
- a public SaaS deployment exists;
- production adoption or commercial impact has been measured;
- optional competition integrations have been completed.

The demonstrated guarantee is narrower and testable: given the stored Sibyl authority lineage, RecallGuard deterministically authorizes or refuses the controlled action; the official SDK can hard-delete the selected authority entity; and a fresh process with no remaining authority rows cannot execute the action.
