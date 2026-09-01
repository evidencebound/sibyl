# Sibyl Hackathon Submission Draft

Status: **DRAFT — not submitted and not marked ready**

Official build page: **OWNER INPUT REQUIRED — paste the private registration link here**

## Build-page fields

### Project name

EvidenceBound RecallGuard

### One-line summary

Fail-closed authority memory that lets a fresh agent session act only under a complete, current, human-controlled Sibyl lineage.

### Public repository

https://github.com/evidencebound/sibyl

### Demo video

**TODO:** public 2–5 minute video URL after upload and anonymous readback.

### Team

- Builder: Ruslan Vrublevskyi
- Team registration/display name: **TODO — confirm against the private build page**

### Partner stacks

None claimed. Base and Virtuals are not integrated in this build.

### Memory implementation note

RecallGuard persists human authority events as structured `recallguard_authority_event` entities in Sibyl Memory. Each event is bound to an exact entity, policy version, evidence digest, and predecessor digest. A fresh Python process reconstructs `MemoryClient.local(...)`, recalls the lineage, validates it deterministically, and changes whether the controlled action may execute.

Session A writes a human grant and exits. Session B starts with only the Sibyl database path, recalls the grant, authorizes the action, writes a human revocation, and exits. Session C starts independently, recalls the revocation, and invalidates the old authority. A separate deletion acceptance hard-deletes the exact authority entity through Sibyl's official `delete_entity` API; a third process then reads zero matching rows and cannot execute the action.

Sibyl Memory is load-bearing: there is no prompt, JSON, environment, or cache fallback for authority.

### Problem and audience

Long-lived agents may retain permission after a human intended to correct or revoke it. The audience is teams deploying persistent agents into workflows where authority must survive sessions without silently becoming permanent.

### Product

RecallGuard is a compact authority-memory plane:

- persistent human grants;
- fresh-session recall;
- hash-linked correction and revocation lineage;
- exact evidence and policy binding;
- fail-closed handling of unavailable, missing, stale, or invalid memory;
- explicit hard-deletion acceptance.

### How memory made this possible

Without Sibyl, the fresh process receives no authority history and cannot act. With a valid Sibyl lineage, it can authorize the controlled action. After recall of a revocation, it refuses the same old authority. After deletion, it requires a new human decision.

### Technical evidence

- Main commit after deletion/license merge: `cbb24227d581e8720e436e4839304bbc038868d5`
- Post-merge CI: https://github.com/evidencebound/sibyl/actions/runs/33535801574
- SDK: `sibyl-memory-client==0.8.0`
- Suite: `13 passed`
- Recall lifecycle: `AUTHORIZED → AUTHORIZED → INVALIDATED`
- Physical row deletion: `deleted_rows=1 → remaining_rows=0 → HUMAN_REQUIRED`
- Memory unavailable: `BLOCKED / AUTHORITY_MEMORY_UNAVAILABLE`

### Prior Work declaration

Pre-build research was frozen outside the competition repository in `evidencebound/evidencebound-labs`, branch `research/sibyl-2026-prebuild`. The submitted implementation has an independent post-window root and commit history. No WebMCP implementation or history was imported.

### PMF evidence

No PMF bonus is claimed. No users, pilots, waitlist, revenue, or production usage are represented without public evidence.

## Demo recording gate

Use [DEMO_SCRIPT.md](DEMO_SCRIPT.md).

The fresh-session recall beat must be one continuous, unedited screen segment. Show `git rev-parse HEAD` and `date -u` immediately before running the A/B/C acceptance. The video must visibly include:

- the problem and audience;
- the working product;
- real `sibyl-memory-client==0.8.0`;
- Session A/B/C with distinct PIDs;
- fresh-session recall changing the decision;
- physical deletion and zero-row readback;
- the memory-unavailable fail-closed result.

## Required public posts

Publish only after the final video URL works anonymously.

### Demo post draft

> Demo: EvidenceBound RecallGuard makes human authority load-bearing agent memory. A fresh process recalls a Sibyl grant, acts only while its evidence-bound lineage is valid, and refuses authority after revocation or deletion. Built with Sibyl Memory 0.8.0. [VIDEO_URL] [REPO_URL] @sibylcap

### Build-log post draft

> Build log: RecallGuard stores human authority as structured, hash-linked Sibyl entities instead of prompt text. The TDD history preserves failing tests for the missing fresh-process and hard-delete paths, followed by real-SDK CI. Current proof: 13 tests, three-process recall/revocation, exact-entity deletion, and fail-closed unavailable memory. [REPO_URL] [CI_URL] @sibylcap

Replace bracketed values before publishing. Do not claim Base, Virtuals, PMF evidence, production users, or secure forensic disk erasure.

## Final owner checklist

- [ ] Open the private build-page link received during registration.
- [ ] Confirm the registered team name and builder spelling.
- [ ] Record the 2–5 minute video using the continuous fresh-session segment.
- [ ] Upload the video publicly and verify it in a signed-out browser.
- [ ] Publish the demo post tagging `@sibylcap`.
- [ ] Publish the separate build-log post tagging `@sibylcap`.
- [ ] Add repo, video, both post URLs, team, partner selection, and memory note to the private build page.
- [ ] Mark the build ready before 2026-09-10 23:59 UTC.
- [ ] Reopen/read back every saved field and public URL.
