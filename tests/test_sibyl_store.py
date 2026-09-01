import json
import importlib.util
import pytest
from evidencebound_recallguard.sibyl_store import SibylAuthorityMemoryStore

class FakeClient:
    def __init__(self): self.rows = {}
    def set_entity(self, category, name, body): self.rows[(category,name)] = {"name": name, "body": body}
    def list_entities(self, category=None, limit=10000):
        return [v for (c,_),v in self.rows.items() if c == category][:limit]
    def delete_entity(self, category, name):
        return self.rows.pop((category, name), None) is not None


def test_adapter_writes_and_reads_authority_entities():
    client = FakeClient()
    store = SibylAuthorityMemoryStore(client=client)
    event = {"entity_id":"e1","sequence":1,"event_id":"a","event_digest":"d1"}
    store.append_authority_event(event)
    assert store.load_authority_events("e1") == [event]


def test_adapter_filters_cross_entity_rows():
    client = FakeClient(); store = SibylAuthorityMemoryStore(client=client)
    store.append_authority_event({"entity_id":"e1","sequence":1,"event_id":"a","event_digest":"d1"})
    store.append_authority_event({"entity_id":"e2","sequence":1,"event_id":"b","event_digest":"d2"})
    assert [r["entity_id"] for r in store.load_authority_events("e1")] == ["e1"]

@pytest.mark.skipif(importlib.util.find_spec("sibyl_memory_client") is None, reason="real sibyl-memory-client not installed")
def test_real_sdk_fresh_client_recall(tmp_path):
    from sibyl_memory_client import MemoryClient
    path = tmp_path / "memory.db"
    a = SibylAuthorityMemoryStore(client=MemoryClient.local(str(path)))
    event = {"entity_id":"e1","sequence":1,"event_id":"a","event_digest":"d1"}
    a.append_authority_event(event)
    b = SibylAuthorityMemoryStore(client=MemoryClient.local(str(path)))
    assert b.load_authority_events("e1") == [event]


def test_adapter_hard_deletes_only_target_entity_authority_rows():
    client = FakeClient()
    store = SibylAuthorityMemoryStore(client=client)
    store.append_authority_event({"entity_id":"e1","sequence":1,"event_id":"a","event_digest":"d1"})
    store.append_authority_event({"entity_id":"e1","sequence":2,"event_id":"b","event_digest":"d2"})
    store.append_authority_event({"entity_id":"e2","sequence":1,"event_id":"c","event_digest":"d3"})

    assert store.delete_authority_events("e1") == 2
    assert store.load_authority_events("e1") == []
    assert [row["entity_id"] for row in store.load_authority_events("e2")] == ["e2"]
