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

ENTITY_ID = "judge-entity"
EVIDENCE_DIGEST = "ev1"
POLICY_VERSION = "p1"


def digest(event):
    raw = json.dumps(
        {key: value for key, value in event.items() if key != "event_digest"},
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(raw).hexdigest()


def mk(kind, sequence, predecessor_digest):
    event = {
        "entity_id": ENTITY_ID,
        "authority_id": "authority-1",
        "event_id": str(uuid.uuid4()),
        "event_kind": kind,
        "sequence": sequence,
        "predecessor_digest": predecessor_digest,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "actor_type": "HUMAN",
        "actor_id_or_label": "judge",
        "authority_scope": "controlled-action",
        "evidence_digest": EVIDENCE_DIGEST,
        "policy_version": POLICY_VERSION,
        "dependency_ids": [],
        "reason": kind.lower(),
    }
    event["event_digest"] = digest(event)
    return event


def evaluate(store):
    return evaluate_authority(
        store.load_authority_events(ENTITY_ID),
        entity_id=ENTITY_ID,
        evidence_digest=EVIDENCE_DIGEST,
        policy_version=POLICY_VERSION,
    )


def run_session(session, db):
    store = SibylAuthorityMemoryStore(client=MemoryClient.local(db))

    if session == "A":
        store.append_authority_event(mk("GRANT", 1, None))
        result = evaluate(store)
        expected = "AUTHORIZED"
    elif session == "B":
        events = store.load_authority_events(ENTITY_ID)
        result = evaluate_authority(
            events,
            entity_id=ENTITY_ID,
            evidence_digest=EVIDENCE_DIGEST,
            policy_version=POLICY_VERSION,
        )
        if result.status != "AUTHORIZED":
            print(f"SESSION_B {result.status} pid={os.getpid()}")
            return 2
        store.append_authority_event(
            mk("REVOCATION", 2, events[-1]["event_digest"])
        )
        expected = "AUTHORIZED"
    else:
        result = evaluate(store)
        expected = "INVALIDATED"

    print(f"SESSION_{session} {result.status} pid={os.getpid()}")
    return 0 if result.status == expected else 3


def orchestrate(db):
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True)
    parser.add_argument("--session", choices=("A", "B", "C"))
    args = parser.parse_args()

    if args.session:
        return run_session(args.session, args.db)
    return orchestrate(args.db)


if __name__ == "__main__":
    raise SystemExit(main())
