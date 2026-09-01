from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import argparse, hashlib, json, os, uuid
from datetime import datetime, timezone
from sibyl_memory_client import MemoryClient
from evidencebound_recallguard.sibyl_store import SibylAuthorityMemoryStore
from evidencebound_recallguard.evaluator import evaluate_authority

def digest(e):
    raw=json.dumps({k:v for k,v in e.items() if k!='event_digest'},sort_keys=True,separators=(',',':')).encode()
    return hashlib.sha256(raw).hexdigest()

def mk(kind, seq, pred, *, evidence='ev1', policy='p1'):
    e={'entity_id':'judge-entity','authority_id':'authority-1','event_id':str(uuid.uuid4()),'event_kind':kind,
       'sequence':seq,'predecessor_digest':pred,'created_at':datetime.now(timezone.utc).isoformat(),
       'actor_type':'HUMAN','actor_id_or_label':'judge','authority_scope':'controlled-action',
       'evidence_digest':evidence,'policy_version':policy,'dependency_ids':[],'reason':kind.lower()}
    e['event_digest']=digest(e); return e

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--db',required=True); args=ap.parse_args()
    entity='judge-entity'
    a=SibylAuthorityMemoryStore(client=MemoryClient.local(args.db)); g=mk('GRANT',1,None); a.append_authority_event(g)
    print('SESSION_A AUTHORIZED', os.getpid())
    b=SibylAuthorityMemoryStore(client=MemoryClient.local(args.db)); r=evaluate_authority(b.load_authority_events(entity),entity_id=entity,evidence_digest='ev1',policy_version='p1')
    print('SESSION_B', r.status, os.getpid())
    if r.status!='AUTHORIZED': return 2
    rev=mk('REVOCATION',2,g['event_digest']); b.append_authority_event(rev)
    c=SibylAuthorityMemoryStore(client=MemoryClient.local(args.db)); r2=evaluate_authority(c.load_authority_events(entity),entity_id=entity,evidence_digest='ev1',policy_version='p1')
    print('SESSION_C', r2.status, os.getpid())
    return 0 if r2.status=='INVALIDATED' else 3
if __name__=='__main__': raise SystemExit(main())
