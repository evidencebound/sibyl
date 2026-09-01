from evidencebound_recallguard.evaluator import evaluate_authority

def test_same_entity_without_memory_cannot_execute():
    r = evaluate_authority(None, entity_id="judge-entity", evidence_digest="ev1", policy_version="p1")
    assert r.status == "BLOCKED"
    assert r.reason == "AUTHORITY_MEMORY_UNAVAILABLE"
    assert r.governed_action_executed is False
