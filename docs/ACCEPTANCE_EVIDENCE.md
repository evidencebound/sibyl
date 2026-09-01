# Acceptance Evidence

This ledger separates verified current evidence from unrun or future claims. Historical local checks are not promoted to current production evidence.

## Authoritative baseline

- Repository: [evidencebound/sibyl](https://github.com/evidencebound/sibyl)
- Implementation merge commit: [`c81dec01b18f07dc1d73978365135976f1ca0baf`](https://github.com/evidencebound/sibyl/commit/c81dec01b18f07dc1d73978365135976f1ca0baf)
- Pull request: [#1 — prove real fresh-process Sibyl recall](https://github.com/evidencebound/sibyl/pull/1)
- Post-merge workflow: [GitHub Actions run 33517924901](https://github.com/evidencebound/sibyl/actions/runs/33517924901)
- Workflow conclusion: `success`
- Runner: GitHub-hosted Ubuntu 24.04
- Python: 3.12
- SDK: `sibyl-memory-client==0.8.0`

## Recorded output

The post-merge workflow installed the pinned real SDK and recorded:

```text
Successfully installed ... sibyl-memory-client-0.8.0
11 passed in 0.61s
SESSION_A AUTHORIZED pid=2390
SESSION_B AUTHORIZED pid=2391
SESSION_C INVALIDATED pid=2392
memory_available=false authority_status=BLOCKED reason=AUTHORITY_MEMORY_UNAVAILABLE governed_action_executed=false
```

PID values are run-specific. Their significance is that all three are distinct.

## Claim-to-evidence map

| Claim | Evidence class | Current result |
| --- | --- | --- |
| The official client is installed | package metadata assertion in CI | PASS — exactly `0.8.0` |
| Authority persists after Session A exits | Session B new-process recall | PASS — `AUTHORIZED` |
| Revocation survives Session B exit | Session C new-process recall | PASS — `INVALIDATED` |
| Sessions are separate OS processes | CLI output plus automated distinct-PID assertion | PASS |
| Missing memory fails closed | deletion acceptance | PASS — `BLOCKED` |
| Missing memory cannot execute the governed action | deletion acceptance | PASS — `false` |
| Unit and integration suite | pytest in the same workflow | PASS — 11/11 |
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

- Sibyl itself is tamper-proof against a host with filesystem control;
- a human identity has been cryptographically verified;
- a public SaaS deployment exists;
- production adoption or commercial impact has been measured;
- optional competition integrations have been completed.

The demonstrated guarantee is narrower and testable: given the stored Sibyl authority lineage, RecallGuard deterministically authorizes or refuses the controlled action, and missing or invalid authority memory fails closed.
