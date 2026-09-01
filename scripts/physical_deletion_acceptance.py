from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sibyl_memory_client import MemoryClient

from evidencebound_recallguard.evaluator import evaluate_authority
from evidencebound_recallguard.sibyl_store import SibylAuthorityMemoryStore

ENTITY_ID = "physical-deletion-entity"
EVIDENCE_DIGEST = "physical-deletion-evidence"
POLICY_VERSION = "physical-deletion-policy"


def make_grant() -> dict[str, object]:
    event: dict[str, object] = {
        "entity_id": ENTITY_ID,
        "authority_id": "physical-deletion-authority",
        "event_id": str(uuid.uuid4()),
        "event_kind": "GRANT",
        "sequence": 1,
        "predecessor_digest": None,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "actor_type": "HUMAN",
        "actor_id_or_label": "judge",
        "authority_scope": "controlled-action",
        "evidence_digest": EVIDENCE_DIGEST,
        "policy_version": POLICY_VERSION,
        "dependency_ids": [],
        "reason": "physical-deletion-acceptance",
    }
    raw = json.dumps(
        event,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode()
    event["event_digest"] = hashlib.sha256(raw).hexdigest()
    return event


def evaluate(store: SibylAuthorityMemoryStore):
    return evaluate_authority(
        store.load_authority_events(ENTITY_ID),
        entity_id=ENTITY_ID,
        evidence_digest=EVIDENCE_DIGEST,
        policy_version=POLICY_VERSION,
    )


def run_session(session: str, db: str) -> int:
    store = SibylAuthorityMemoryStore(client=MemoryClient.local(db))

    if session == "A":
        store.append_authority_event(make_grant())
        result = evaluate(store)
        print(f"DELETE_A {result.status} pid={os.getpid()}")
        return 0 if result.status == "AUTHORIZED" else 2

    if session == "B":
        deleted_rows = store.delete_authority_events(ENTITY_ID)
        print(f"DELETE_B deleted_rows={deleted_rows} pid={os.getpid()}")
        return 0 if deleted_rows == 1 else 3

    remaining_events = store.load_authority_events(ENTITY_ID)
    result = evaluate_authority(
        remaining_events,
        entity_id=ENTITY_ID,
        evidence_digest=EVIDENCE_DIGEST,
        policy_version=POLICY_VERSION,
    )
    action = str(result.governed_action_executed).lower()
    print(
        f"DELETE_C {result.status} reason={result.reason} "
        f"governed_action_executed={action} "
        f"remaining_rows={len(remaining_events)} pid={os.getpid()}"
    )
    expected = (
        result.status == "HUMAN_REQUIRED"
        and result.reason == "NO_AUTHORITY_MEMORY"
        and result.governed_action_executed is False
        and remaining_events == []
    )
    return 0 if expected else 4


def orchestrate(db: str) -> int:
    script = Path(__file__).resolve()
    for session in ("A", "B", "C"):
        completed = subprocess.run(
            [sys.executable, str(script), "--db", db, "--session", session],
            text=True,
            capture_output=True,
        )
        sys.stdout.write(completed.stdout)
        sys.stderr.write(completed.stderr)
        if completed.returncode:
            return completed.returncode
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True)
    parser.add_argument("--session", choices=("A", "B", "C"))
    args = parser.parse_args()

    if args.session:
        return run_session(args.session, args.db)
    return orchestrate(args.db)


if __name__ == "__main__":
    raise SystemExit(main())
