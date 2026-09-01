from __future__ import annotations
from dataclasses import dataclass
import hashlib, json
from typing import Iterable, Mapping, Any

@dataclass(frozen=True)
class AuthorityResult:
    status: str
    reason: str
    governed_action_executed: bool = False
    history: tuple[Mapping[str, Any], ...] = ()


def _canonical_digest(event: Mapping[str, Any]) -> str:
    body = {k: v for k, v in event.items() if k != "event_digest"}
    raw = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(raw).hexdigest()


def evaluate_authority(events: Iterable[Mapping[str, Any]] | None, *, entity_id: str,
                       evidence_digest: str, policy_version: str,
                       verify_digest: bool = True) -> AuthorityResult:
    if events is None:
        return AuthorityResult("BLOCKED", "AUTHORITY_MEMORY_UNAVAILABLE")
    rows = list(events)
    if not rows:
        return AuthorityResult("HUMAN_REQUIRED", "NO_AUTHORITY_MEMORY")
    try:
        rows.sort(key=lambda r: int(r["sequence"]))
        if [int(r["sequence"]) for r in rows] != list(range(1, len(rows) + 1)):
            raise ValueError("gap")
        prev = None
        for r in rows:
            if r.get("predecessor_digest") != prev:
                raise ValueError("predecessor")
            if r.get("event_kind") not in {"GRANT", "CORRECTION", "REVOCATION", "RECOVERY"}:
                raise ValueError("kind")
            if r.get("actor_type") != "HUMAN":
                raise ValueError("actor")
            if verify_digest and r.get("event_digest") != _canonical_digest(r):
                raise ValueError("digest")
            prev = r.get("event_digest")
    except (KeyError, TypeError, ValueError):
        return AuthorityResult("BLOCKED", "LINEAGE_INVALID", history=tuple(rows))

    current = rows[-1]
    kind = current["event_kind"]
    if kind in {"CORRECTION", "REVOCATION"}:
        return AuthorityResult("INVALIDATED", "AUTHORITY_REVOKED_OR_CORRECTED", history=tuple(rows))
    if kind == "RECOVERY":
        return AuthorityResult("HUMAN_REQUIRED", "EXPLICIT_REGRANT_REQUIRED", history=tuple(rows))
    if current.get("policy_version") != policy_version or current.get("evidence_digest") != evidence_digest:
        return AuthorityResult("STALE", "AUTHORITY_BINDING_MISMATCH", history=tuple(rows))
    return AuthorityResult("AUTHORIZED", "ACTIVE_HUMAN_GRANT", True, tuple(rows))
