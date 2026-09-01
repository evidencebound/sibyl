# Build status

Status date: 2026-09-01 UTC

## Decision

**Core Sibyl authority-memory acceptance: PASS.**

**Physical deletion acceptance and competition submission: NOT YET COMPLETE.**

The implementation baseline is commit [`c81dec0`](https://github.com/evidencebound/sibyl/commit/c81dec01b18f07dc1d73978365135976f1ca0baf). GitHub Actions run [33517924901](https://github.com/evidencebound/sibyl/actions/runs/33517924901) completed successfully on that exact merge commit.

The documentation review checkpoint is commit [`022b37e`](https://github.com/evidencebound/sibyl/commit/022b37e0f4c3a12e4c878a222391c98f7bbcac1a). Branch run [33532206327](https://github.com/evidencebound/sibyl/actions/runs/33532206327) completed successfully with the same runtime gates. Subsequent changes in this PR narrow evidence wording only; PR CI remains the merge gate.

## Verified evidence

| Gate | Result | Evidence |
| --- | --- | --- |
| Public repository | PASS | `evidencebound/sibyl` is public |
| Independent build history | PASS | root commit `06fecef`, created after `2026-09-01T00:00:00Z` |
| Real Sibyl package | PASS | CI installed and asserted `sibyl-memory-client==0.8.0` |
| Automated suite | PASS | `11 passed in 0.61s` on implementation baseline |
| Session A | PASS | `AUTHORIZED`, PID `2390` |
| Session B fresh process | PASS | `AUTHORIZED`, PID `2391` |
| Session C fresh process | PASS | `INVALIDATED`, PID `2392` |
| Distinct processes | PASS | three distinct PIDs asserted by test |
| Memory-unavailable path | PASS | `BLOCKED / AUTHORITY_MEMORY_UNAVAILABLE` |
| Governed action without memory | PASS | `governed_action_executed=false` |
| Documentation checkpoint CI | PASS | run 33532206327: success |
| Physical Sibyl deletion | UNRUN | no entity/database deletion is performed by the current script |

## What the evidence proves

- A human grant written through the real Sibyl 0.8.0 client survives process exit.
- A second Python process recalls the grant from the same Sibyl database and authorizes the bound action.
- That process appends a human revocation.
- A third Python process recalls the lineage and returns `INVALIDATED`.
- Passing unavailable authority memory into the evaluator does not fall back to prompt text, environment state, JSON, or cache.
- The controlled action remains refused when memory is unavailable.

## Directly tested behaviors

The current 11-test suite directly exercises:

- unavailable memory;
- valid human grant;
- revocation non-resurrection;
- recovery requiring a distinct re-grant;
- lineage sequence gaps;
- stale policy binding;
- adapter read/write;
- cross-entity filtering;
- real SDK fresh-client recall;
- real three-process grant/recall/revocation acceptance;
- memory-unavailable fail-closed acceptance.

## Implemented validation without a dedicated isolated test

The evaluator or store implements these branches, but the current suite does not directly isolate them:

- empty event history;
- `CORRECTION`;
- invalid predecessor digest;
- invalid canonical event digest;
- stale evidence binding;
- exact replay idempotency;
- conflicting duplicate rejection.

They must not be presented as independently tested until tests exist.

## Open gates

These items are not claimed as complete:

- a physical Sibyl entity/database deletion acceptance has not been implemented;
- the 2–5 minute public demo video has not been recorded or linked;
- final submission fields have not been entered or verified on the competition platform;
- the current `LICENSE` file names MIT but does not yet contain the complete standard MIT license text;
- any optional partner multiplier or external integration is unimplemented;
- user adoption, revenue, and impact metrics are unmeasured and must not be invented.

## Prior-work boundary

Pre-build research is frozen outside this repository in [`evidencebound/evidencebound-labs`](https://github.com/evidencebound/evidencebound-labs), branch [`research/sibyl-2026-prebuild`](https://github.com/evidencebound/evidencebound-labs/tree/research/sibyl-2026-prebuild). The public competition repository retains its own post-window root and subsequent implementation history.
