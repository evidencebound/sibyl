# Build status

Status date: 2026-09-01 UTC

## Decision

**Core Sibyl authority-memory acceptance: PASS.**

**Physical Sibyl row-deletion acceptance: PASS in feature CI. Competition submission: NOT YET COMPLETE.**

The implementation baseline is commit [`c81dec0`](https://github.com/evidencebound/sibyl/commit/c81dec01b18f07dc1d73978365135976f1ca0baf). GitHub Actions run [33517924901](https://github.com/evidencebound/sibyl/actions/runs/33517924901) completed successfully on that exact merge commit.

The documentation review checkpoint is commit [`022b37e`](https://github.com/evidencebound/sibyl/commit/022b37e0f4c3a12e4c878a222391c98f7bbcac1a). Branch run [33532206327](https://github.com/evidencebound/sibyl/actions/runs/33532206327) completed successfully with the same runtime gates.

The physical-deletion TDD checkpoint is commit [`92892da`](https://github.com/evidencebound/sibyl/commit/92892dad00dd65d60932cbe7166f2ad3b1595f75). Branch run [33535080048](https://github.com/evidencebound/sibyl/actions/runs/33535080048) passed the 13-test suite, including the real SDK, three-process hard-delete readback. Every updated PR head must pass fresh CI before merge.

## Verified evidence

| Gate | Result | Evidence |
| --- | --- | --- |
| Public repository | PASS | `evidencebound/sibyl` is public |
| Independent build history | PASS | root commit `06fecef`, created after `2026-09-01T00:00:00Z` |
| Real Sibyl package | PASS | CI installed and asserted `sibyl-memory-client==0.8.0` |
| Automated suite | PASS | baseline `11 passed`; deletion checkpoint `13 passed` |
| Session A | PASS | `AUTHORIZED`, PID `2390` |
| Session B fresh process | PASS | `AUTHORIZED`, PID `2391` |
| Session C fresh process | PASS | `INVALIDATED`, PID `2392` |
| Distinct processes | PASS | three distinct PIDs asserted by test |
| Memory-unavailable path | PASS | `BLOCKED / AUTHORITY_MEMORY_UNAVAILABLE` |
| Governed action without memory | PASS | `governed_action_executed=false` |
| Documentation checkpoint CI | PASS | run 33532206327: success |
| Physical Sibyl row deletion | PASS | official `delete_entity`; fresh process reads zero authority rows in run 33535080048 |
| Complete MIT text | PASS | standard MIT grant and warranty disclaimer in `LICENSE` |

## What the evidence proves

- A human grant written through the real Sibyl 0.8.0 client survives process exit.
- A second Python process recalls the grant from the same Sibyl database and authorizes the bound action.
- That process appends a human revocation.
- A third Python process recalls the lineage and returns `INVALIDATED`.
- Passing unavailable authority memory into the evaluator does not fall back to prompt text, environment state, JSON, or cache.
- The controlled action remains refused when memory is unavailable.
- A separate process hard-deletes the exact entity's authority row through the official SDK.
- A third process reads zero remaining rows and returns `HUMAN_REQUIRED / NO_AUTHORITY_MEMORY` with action execution false.

## Directly tested behaviors

The current 13-test suite directly exercises:

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
- memory-unavailable fail-closed acceptance;
- exact-entity hard deletion without cross-entity deletion;
- real three-process hard-delete and fresh-read acceptance.

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

- the 2–5 minute public demo video has not been recorded, publicly posted, or anonymously read back;
- the required public build-log post tagging `@sibylcap` has not been published;
- the private Sibyl build page URL has not been provided in this workspace;
- final build-page fields have not been entered, marked ready, or independently read back;
- any optional partner multiplier or external integration is unimplemented;
- user adoption, revenue, and impact metrics are unmeasured and must not be invented.

## Prior-work boundary

Pre-build research is frozen outside this repository in [`evidencebound/evidencebound-labs`](https://github.com/evidencebound/evidencebound-labs), branch [`research/sibyl-2026-prebuild`](https://github.com/evidencebound/evidencebound-labs/tree/research/sibyl-2026-prebuild). The public competition repository retains its own post-window root and subsequent implementation history.
