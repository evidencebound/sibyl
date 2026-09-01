from __future__ import annotations
from typing import Any

AUTHORITY_CATEGORY = "recallguard_authority_event"

class SibylAuthorityMemoryStore:
    def __init__(self, *, client: Any):
        self._client = client

    def append_authority_event(self, event: dict[str, Any]) -> None:
        name = f"{event['entity_id']}:{int(event['sequence']):08d}:{event['event_id']}"
        existing = [r for r in self._client.list_entities(category=AUTHORITY_CATEGORY, limit=10_000)
                    if r.get("name") == name]
        if existing:
            if existing[0].get("body") == event:
                return
            raise ValueError("conflicting authority event")
        self._client.set_entity(AUTHORITY_CATEGORY, name, event)

    def load_authority_events(self, entity_id: str) -> list[dict[str, Any]]:
        rows = self._client.list_entities(category=AUTHORITY_CATEGORY, limit=10_000)
        events = [r["body"] for r in rows if isinstance(r.get("body"), dict) and r["body"].get("entity_id") == entity_id]
        events.sort(key=lambda e: int(e["sequence"]))
        return events
