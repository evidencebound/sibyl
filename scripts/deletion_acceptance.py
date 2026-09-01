import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from evidencebound_recallguard.evaluator import evaluate_authority
r = evaluate_authority(None, entity_id="judge-entity", evidence_digest="ev1", policy_version="p1")
print(f"memory_available=false authority_status={r.status} reason={r.reason} governed_action_executed={str(r.governed_action_executed).lower()}")
raise SystemExit(0 if (r.status, r.reason, r.governed_action_executed) == ("BLOCKED", "AUTHORITY_MEMORY_UNAVAILABLE", False) else 1)
