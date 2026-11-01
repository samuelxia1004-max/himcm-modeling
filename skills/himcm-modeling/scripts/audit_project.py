#!/usr/bin/env python3
"""Check evidence bindings and requirement coverage; this is not a math evaluator."""
import argparse,json,hashlib,sys
from pathlib import Path

def audit(root):
    errors=[];unverified=[];checked=0
    def load(rel):
        p=root/rel
        if not p.exists():errors.append('MISSING:'+rel);return {}
        try:return json.loads(p.read_text())
        except Exception:errors.append('INVALID_JSON:'+rel);return {}
    state=load('artifacts/project_state.json');contract=load('artifacts/problem_contract.json');reg=load('artifacts/evidence_registry.json')
    if not state.get('rules_verified'):unverified.append('CURRENT_RULES_NOT_VERIFIED')
    req=contract.get('requirements',[])
    if not req:unverified.append('NO_REQUIREMENTS_REGISTERED')
    for r in req:
        if not r.get('id') or r.get('status')!='ANSWERED' or not r.get('evidence_ids') or not r.get('paper_location'):unverified.append('REQUIREMENT_INCOMPLETE:'+str(r.get('id')))
    ids=set()
    for b in reg.get('bindings',[]):
        ident=b.get('id');rel=b.get('path');digest=b.get('sha256')
        if not ident or ident in ids:errors.append('MISSING_OR_DUPLICATE_BINDING_ID');continue
        ids.add(ident)
        if not isinstance(rel,str) or not digest:errors.append('INCOMPLETE_BINDING:'+ident);continue
        p=(root/rel).resolve()
        if Path(rel).is_absolute() or not p.is_relative_to(root):errors.append('PATH_OUTSIDE_PROJECT:'+ident);continue
        if not p.is_file():errors.append('MISSING_EVIDENCE:'+ident);continue
        if hashlib.sha256(p.read_bytes()).hexdigest()!=digest:errors.append('STALE_EVIDENCE:'+ident);continue
        checked+=1
    if not ids:unverified.append('NO_EVIDENCE_BINDINGS')
    for r in req:
        for ident in r.get('evidence_ids',[]):
            if ident not in ids:errors.append('UNKNOWN_REQUIREMENT_EVIDENCE:'+str(ident))
    for c in reg.get('claims',[]):
        if not c.get('evidence_ids'):unverified.append('UNBOUND_CLAIM:'+str(c.get('id')))
        for ident in c.get('evidence_ids',[]):
            if ident not in ids:errors.append('UNKNOWN_CLAIM_EVIDENCE:'+str(ident))
    return {'status':'FAIL' if errors else 'STRUCTURE_PASS_WITH_UNVERIFIED_ITEMS' if unverified else 'STRUCTURE_PASS','bindings_checked':checked,'errors':errors,'unverified':unverified,'mathematics_and_semantics':'NOT_CHECKED'}

def main():
    p=argparse.ArgumentParser();p.add_argument('project');a=p.parse_args();r=audit(Path(a.project).resolve());print(json.dumps(r,ensure_ascii=False,indent=2));sys.exit(1 if r['errors'] else 2 if r['unverified'] else 0)

if __name__=='__main__':main()
