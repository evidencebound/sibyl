# Build status

Status date: 2026-09-01 UTC

## Decision

**Core Sibyl authority-memory acceptance: PASS.**

**Competition submission: NOT YET COMPLETE.**

The implementation baseline is commit [`c81dec0`](https://github.com/evidencebound/sibyl/commit/c81dec01b18f07dc1d73978365135976f1ca0baf). GitHub Actions run [33517924901](https://github.com/evidencebound/sibyl/actions/runs/33517924901) completed successfully on that exact merge commit.

## Verified evidence

| Gate | Result | Evidence |
| --- | --- | --- |
| Public repository | PASS | `evidencebound/sibyl` is public |
| Independent build history | PASS | root commit `06fecef`, created after `2026-09-01T00:00:00Z` |
| Real Sibyl package | PASS | CI installed and asserted `sibyl-memory-client==0.8.0` |
| Automated suite | PASS | `11 passed in 0.61s` |
| Session A | PASS | `AUTHORIZED`, PID `2390` |
| Session B fresh process | PASS | `AUTHORIZED`, PID `2391` |
| Session C fresh process | PASS | `INVALIDATED`, PID `2392` |
| Distinct processes | PASS | three distinct PIDs asserted by test |
| Deletion/no-memory path | PASS | `BLOCKED / AUTHORITY_MEMORY_UNAVAILABLE` |
| Governed action on missing memory | PASS | `governed_action_executed=false` |
| Code review | PASS | PR #1: no Critical or Important findings |
| Post-merge CI | PASS | run 33517924901: success |

## What the evidence proves

- A human grant written through the real Sibyl 0.8.0 client survives process exit.
- A second Python process recalls the grant from the same Sibyl database and authorizes the bound action.
- That process appends a human revocation.
- A third Python process recalls the lineage and returns `INVALIDATED`.
- Removing the authority-memory input does not fall back to prompt text, environment state, JSON, or cache.
- The controlled action remains refused when memory is unavailable.

## Tested failure modes

The current suite covers:

- unavailable memory;
- no remembered authority;
- valid human grant;
- correction/revocation non-resurrection;
- recovery requiring a distinct re-grant;
- lineage gaps;
- predecessor and digest validation;
- stale policy or evidence binding;
- cross-entity filtering;
- exact replay idempotency;
- conflicting duplicate rejection;
- real SDK fresh-client recall;
- real three-process judge acceptance;
- deletion/no-memory acceptance.

## Open gates

These items are not claimed as complete:

- the 2–5 minute public demo video has not been recorded or linked;
- final submission fields have not been entered or verified on the competition platform;
- the current `LICENSE` file names MIT but does not yet contain the complete standard MIT license text;
- any optional partner multiplier or external integration is unimplemented;
- user adoption, revenue, and impact metrics are unmeasured and must not be invented.

## Prior-work boundary

Pre-build research is frozen outside this repository in `evidencebound/evidencebound-labs`, branch `research/sibyl-2026-prebuild`. The public competition repository retains its own post-window root and subsequent implementation history.
