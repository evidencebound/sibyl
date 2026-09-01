from evidencebound_recallguard.evaluator import evaluate_authority


def event(kind, seq, digest, pred=None, evidence="ev1", policy="p1"):
    return {"event_kind": kind, "sequence": seq, "event_digest": digest,
            "predecessor_digest": pred, "evidence_digest": evidence,
            "policy_version": policy, "actor_type": "HUMAN"}


def test_no_store_fails_closed():
    r = evaluate_authority(None, entity_id="e1", evidence_digest="ev1", policy_version="p1")
    assert (r.status, r.reason, r.governed_action_executed) == ("BLOCKED", "AUTHORITY_MEMORY_UNAVAILABLE", False)


def test_valid_grant_authorizes():
    r = evaluate_authority([event("GRANT", 1, "d1")], entity_id="e1", evidence_digest="ev1", policy_version="p1", verify_digest=False)
    assert r.status == "AUTHORIZED"


def test_revocation_never_resurrects():
    rows = [event("GRANT", 1, "d1"), event("REVOCATION", 2, "d2", "d1")]
    r = evaluate_authority(rows, entity_id="e1", evidence_digest="ev1", policy_version="p1", verify_digest=False)
    assert r.status == "INVALIDATED"


def test_recovery_does_not_resurrect():
    rows = [event("GRANT", 1, "d1"), event("REVOCATION", 2, "d2", "d1"), event("RECOVERY", 3, "d3", "d2")]
    r = evaluate_authority(rows, entity_id="e1", evidence_digest="ev1", policy_version="p1", verify_digest=False)
    assert r.status == "HUMAN_REQUIRED"


def test_gap_fails_closed():
    rows = [event("GRANT", 1, "d1"), event("REVOCATION", 3, "d3", "d1")]
    r = evaluate_authority(rows, entity_id="e1", evidence_digest="ev1", policy_version="p1", verify_digest=False)
    assert r.status == "BLOCKED" and r.reason == "LINEAGE_INVALID"


def test_policy_mismatch_is_stale():
    r = evaluate_authority([event("GRANT", 1, "d1")], entity_id="e1", evidence_digest="ev1", policy_version="p2", verify_digest=False)
    assert r.status == "STALE"
