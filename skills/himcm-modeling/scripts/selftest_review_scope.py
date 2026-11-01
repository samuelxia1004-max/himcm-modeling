#!/usr/bin/env python3
"""v8.2 live raw-review scope controls. Implementation tests, not independent review.
Run with Python 3.13: selftest_review_scope.py NEW_WORKDIR [--audit-inputs AUDITDIR]
The optional frozen audit inputs are replayed unchanged with explicit legacy-ambiguity expectations.
"""
import argparse, hashlib, json, sys
from pathlib import Path
import check_gate as cg
import selftest_gate as fx


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('workdir', type=Path)
    ap.add_argument('--audit-inputs', type=Path)
    ap.add_argument('--noissues-audit-inputs', type=Path)
    ap.add_argument('--mixed-audit-inputs', type=Path)
    args = ap.parse_args(); w = args.workdir.resolve()
    w.mkdir(parents=True, exist_ok=False)
    results = []
    def sha(data): return hashlib.sha256(data).hexdigest()
    def parser(name, text, expected, required=(), noerrors=True):
        errors = []; actual = cg.parse_raw_issues(text, errors)
        ok = actual == expected and all(any(s in e for e in errors) for s in required) and (not noerrors or not errors)
        results.append(dict(case=name, kind='parser', ok=ok, input_sha256=sha(text.encode()), expected=expected, actual=actual, errors=errors, required=required))
        (w/(name+'.md')).write_text(text)
        print(('OK  ' if ok else 'BAD ') + name)
    H = 'pdf_sha256: '+'0'*64+'\nfresh_session: yes\ninherited_parent_context: no\n'
    I = '## Issues\n### 1. Defect\nSeverity: high\nLocation: p3\nVerdict: NOT FIXED\n'
    for key in ('review_kind', 'session_mode', 'review-mode', 'phase2', 'reviewer'):
        parser('explicit_metadata_'+key, H+'## Review metadata\n'+key+': independent\n\nReview verdict: NOT FIXED\n'+I, [('1','NOT FIXED')])
    parser('explicit_metadata_bare_global_rejected', H+'## Review metadata\nsession_mode: independent\nVerdict: NOT FIXED\n'+I, [('1','NOT FIXED')], ('CRITIC_RAW_AMBIGUOUS_SCOPE',),False)
    parser('opaque_same_bytes_ambiguous', H+'review_kind: independent\nVerdict: NOT FIXED\n', [('review_kind',None)], ('CRITIC_RAW_AMBIGUOUS_SCOPE',),False)
    parser('opaque_colon_verdict_only_ambiguous', H+'C1-06: denominator wrong\nVerdict: NOT FIXED\n', [('C1-06',None)], ('CRITIC_RAW_AMBIGUOUS_SCOPE',),False)
    for ident in ('review_kind','C1-06','C6'):
        parser('genuine_bare_opaque_'+ident, H+ident+': denominator wrong\nSeverity: high\nLocation: p3\nVerdict: NOT FIXED\n', [(ident,'NOT FIXED')])
        parser('explicit_opaque_only_verdict_'+ident, H+'## Issues\n'+ident+': denominator wrong\nVerdict: NOT FIXED\n', [(ident,'NOT FIXED')])
    parser('opaque_space_title',H+'C6 denominator wrong\nVerdict: NOT FIXED\n',[('C6','NOT FIXED')])
    parser('incomplete_findings',H+'## Findings\n### review_kind\nMissing evidence\n',[('review_kind',None)])
    parser('nested_findings',H+'## Open issues\n### Numerical defects\n6. Missing evidence\n',[('6',None)])
    parser('nested_heading_conflict',H+'2. Result | Verdict: FIXED\n### Recheck details\nVerdict: NOT FIXED\n',[('2',None)],('CRITIC_RAW_VERDICT_COUNT',),False)
    parser('outside_child_fields',H+'6. Result\n### Details\nSeverity: high\nLocation: p3\n',[('6',None)])
    parser('pipe_and_multiline_fields',H+'## Issues\n1. Location: p3 | Severity: high\n- Verdict:\n\nFIXED\n',[('1','FIXED')])
    parser('emphasized_fields',H+'## Issues\n1. **Location:** p3 | **Verdict:** **FIXED**\n',[('1','FIXED')])
    parser('fields_must_be_declarations',H+'## Issues\n1. Result\nOrdinary prose mentions Verdict: FIXED\n',[('1',None)])
    parser('global_never_supplies_issue_verdict',H+'## Issues\n1. Result\nSeverity: medium\nReview verdict: FIXED\n',[('1',None)])
    for name, sample in (
        ('fence','```text\nC6: Example | Verdict: FIXED\n```'),
        ('comment','<!-- C6: Example\nVerdict: FIXED -->'),
        ('inline','`C6: Example | Verdict: FIXED`'),
        ('quote','> C6: Example\n> Verdict: FIXED'),
        ('indented','    C6: Example\n    Verdict: FIXED')):
        parser(name+'_issue_example_inert',H+'## Findings\n'+sample+'\n',[])
        parser(name+'_cannot_supply_verdict',H+'## Issues\n2. Result\n'+sample+'\n',[('2',None)])
    parser('live_after_examples',H+'## Issues\n```text\n<!--\n```\n<!-- C6: example -->\n> C7: example\n\nC8: real issue\nSeverity: high\nVerdict: NOT FIXED\n',[('C8','NOT FIXED')])
    parser('live_after_inline_comment_literal',H+'## Issues\nExample: `<!--`\nC8: real issue\nSeverity: high\nVerdict: NOT FIXED\n',[('C8','NOT FIXED')])
    parser('live_after_quote_comment_literal',H+'## Issues\n> <!--\n\nC8: real issue\nSeverity: high\nVerdict: NOT FIXED\n',[('C8','NOT FIXED')])
    parser('real_comment_closes_before_inline_tick',H+'## Issues\n<!-- Example `text -->\nC8: real issue\nSeverity: high\nVerdict: NOT FIXED\n',[('C8','NOT FIXED')])
    parser('unclosed_inline_fail_closed',H+'## Issues\n2. Result\nExample: `Verdict: FIXED\n',[('2',None)],('CRITIC_RAW_AMBIGUOUS_SCOPE',),False)
    parser('lazy_quote_fail_closed',H+'## Issues\n2. Result\n> Example\nVerdict: FIXED\n',[('2',None)],('CRITIC_RAW_AMBIGUOUS_SCOPE',),False)
    parser('unsupported_id_fields_rejected',H+'## Findings\n### CRITICAL\nSeverity: high\n',[],('CRITIC_RAW_UNASSIGNED_ISSUE_FIELDS',),False)
    parser('metadata_numeric_issue_fields_rejected',H+'## Review metadata\n1. Severity: high\n'+I,[('1','NOT FIXED')],('CRITIC_RAW_AMBIGUOUS_SCOPE',),False)

    def gate(name, setup, want, must=None):
        d,g=fx.make(w/'gate'/name); setup(d,g); fx.save(d,g); code,out=fx.run(d)
        msgs='\n'.join(out.get('fail',[])+out.get('incomplete',[]))
        ok=code==want and (not must or must in msgs)
        results.append(dict(case=name,kind='gate',ok=ok,expected_exit=want,actual_exit=code,required=must,result=out))
        print(('OK  ' if ok else 'BAD ') + name+f': exit {code} (want {want})')
    def replace_final(d, value):
        p=d/'artifacts/review/r2.md';p.write_text(p.read_text().replace('2. restated | Verdict: FIXED | Evidence: p2 | none',value))
    def add_initial(d, text):
        p=d/'artifacts/review/r1.md';p.write_text(p.read_text()+'\n'+text)
    def metadata(d,g, explicit=True):
        p=d/'artifacts/review/r1.md'; lines=p.read_text().splitlines()
        body=('## Review metadata\nsession_mode: independent\nReview verdict: NOT FIXED\n## Issues\n' if explicit else 'session_mode: independent\nVerdict: NOT FIXED\n')
        p.write_text(lines[0]+'\n'+body+'\n'.join(lines[1:])+'\n')
    gate('baseline',lambda d,g:None,0)
    gate('new_metadata_no_false_issue',metadata,0)
    gate('legacy_metadata_global_ambiguous',lambda d,g:metadata(d,g,False),1,'CRITIC_RAW_AMBIGUOUS_SCOPE')
    for name, sample in (
        ('fence','```text\nVerdict: FIXED\n```'),('comment','<!--\nVerdict: FIXED\n-->'),
        ('inline','Example: `Verdict: FIXED`'),('quote','> Verdict: FIXED')):
        gate(name+'_missing_real_final',lambda d,g,s=sample:replace_final(d,'2. restated | Evidence: p2\n'+s),2,'CRITIC_FINAL_ISSUE_UNVERIFIED')
    gate('global_missing_real_final',lambda d,g:replace_final(d,'2. restated | Evidence: p2\nReview verdict: NO_BLOCKING_ISSUES'),2,'CRITIC_FINAL_ISSUE_UNVERIFIED')
    gate('nested_verdict_conflict',lambda d,g:replace_final(d,'2. restated | Verdict: FIXED\n### Details\nVerdict: NOT FIXED'),1,'CRITIC_RAW_VERDICT_COUNT')
    gate('genuine_opaque_high_unclosed',lambda d,g:add_initial(d,'review_kind: denominator wrong\nSeverity: high\nLocation: p2'),1,'CRITIC_RAW_ISSUES_NOT_CLOSED')
    gate('new_incomplete_findings',lambda d,g:add_initial(d,'## Findings\nC6: Missing evidence'),1,'CRITIC_RAW_ISSUES_NOT_CLOSED')
    gate('live_issue_after_fenced_comment',lambda d,g:add_initial(d,'## Findings\n```text\n<!--\n```\nC6: Missing evidence'),1,'CRITIC_RAW_ISSUES_NOT_CLOSED')
    def high(d,g):
        p=d/'artifacts/review/critic.md';p.write_text(p.read_text().replace('2. Issue 2 about claim C1. Severity: medium\nStatus: FIXED (verified round 2)','2. Issue 2 about claim C1. Severity: high\nStatus: WONTFIX deadline'))
    gate('high_wontfix',high,1,'CRITIC_HIGH_WONTFIX')
    gate('latest_not_fixed',lambda d,g:fx.write_critic(d,contra=True),1,'CRITIC_CONTRADICTION')
    gate('short_final_still_needs_all_prior',lambda d,g:fx.write_critic(d,round3={1:'FIXED'}),2,'CRITIC_FINAL_ISSUE_UNVERIFIED')
    def illegal_metadata(d,g):
        add_initial(d,'## Review metadata\nSeverity: high\n')
    gate('metadata_cannot_hide_fields',illegal_metadata,1,'CRITIC_RAW_AMBIGUOUS_SCOPE')

    # r2: the zero-issue path needs an authoritative result on both sides.
    decl = 'Review verdict: NO_BLOCKING_ISSUES\n'
    def noissues(d,g,raw_decl=decl,closure_decl=decl):
        digest=fx.sha(d/'final/TEAM.pdf')
        (d/'artifacts/review/final.md').write_text('pdf_sha256: '+digest+'\n## Review metadata\nfresh_session: yes\ninherited_parent_context: no\n\n'+raw_decl)
        (d/'artifacts/review/critic.md').write_text('Critic: independent fictional reviewer\nRound: 1 | critic: independent | fresh_session: yes | pdf_sha256: '+digest+' | raw: artifacts/review/final.md\n'+closure_decl)
    gate('noissues_live_positive',noissues,0)
    gate('noissues_missing_raw',lambda d,g:noissues(d,g,raw_decl=''),2,'CRITIC_NO_ISSUE_VERDICT_NOT_IN_RAW')
    gate('noissues_missing_closure',lambda d,g:noissues(d,g,closure_decl=''),2,'CRITIC: list actual issues')
    examples = {
        'fence':'```text\n'+decl+'```\n',
        'comment':'<!--\n'+decl+'-->\n',
        'inline':'`Review verdict: NO_BLOCKING_ISSUES`\n',
        'quote':'> Review verdict: NO_BLOCKING_ISSUES\n\n',
        'indented':'    Review verdict: NO_BLOCKING_ISSUES\n',
        'prose':'The reviewer mentioned Review verdict: NO_BLOCKING_ISSUES as a possible result.\n',
    }
    for side in ('raw','closure'):
        def setup(value,side=side):
            return lambda d,g:noissues(d,g,**{side+'_decl':value})
        missing='CRITIC_NO_ISSUE_VERDICT_NOT_IN_RAW' if side=='raw' else 'CRITIC: list actual issues'
        for kind,value in examples.items():
            gate('noissues_'+side+'_'+kind+'_cannot_authorize',setup(value),2,missing)
        for kind,value in {
            'duplicate':decl+decl,
            'conflict':decl+'Review verdict: NOT FIXED\n',
            'reverse_conflict':'Review verdict: NOT FIXED\n'+decl,
            'pipe_conflict':'Review verdict: NO_BLOCKING_ISSUES | Review verdict: NOT FIXED\n',
            'invalid_second':decl+'Review verdict: UNKNOWN\n',
        }.items():
            gate('noissues_'+side+'_'+kind,setup(value),1,'CRITIC_REVIEW_VERDICT_COUNT')
        # Example conclusions cannot create duplicates or override a live result.
        mixed=''.join(examples.values())+decl
        gate('noissues_'+side+'_mixed_live_examples',setup(mixed),0)
        # An actual overall negative now fails in both zero/nonzero issue
        # paths. Previously this zero-issue control returned INCOMPLETE.
        gate('noissues_'+side+'_live_negative_example_positive',setup('Review verdict: NOT FIXED\n'+examples['fence']+examples['comment']),1,missing)
        gate('noissues_'+side+'_lazy_quote_ambiguous',setup('> Example\n'+decl),1,'CRITIC_RAW_AMBIGUOUS_SCOPE')
        gate('noissues_'+side+'_unclosed_inline_ambiguous',setup('`'+decl),1,'CRITIC_RAW_AMBIGUOUS_SCOPE')
        quoted_negative='> Review verdict: NOT FIXED\n\n'+decl
        gate('noissues_'+side+'_quoted_negative_then_live',setup(quoted_negative),0)
        for kind,value in {
            'bullet':'- '+decl,
            'pipe':'Result kind: overall | '+decl,
            'multiline':'Review verdict:\nNO_BLOCKING_ISSUES\n',
            'emphasis':'**Review verdict:** **NO_BLOCKING_ISSUES**\n',
        }.items():
            gate('noissues_'+side+'_live_'+kind,setup(value),0)
        gate('noissues_'+side+'_trailing_prose_invalid',setup('Review verdict: NO_BLOCKING_ISSUES was only an example\n'),2,missing)
        gate('noissues_'+side+'_fixed_is_not_noissues',setup('Review verdict: FIXED\n'),2,missing)

    for ident in ('1.','C6:'):
        gate('noissues_issue_row_global_cannot_hide_'+ident.replace(':','colon').replace('.','dot'),lambda d,g,ident=ident:noissues(d,g,raw_decl='## Issues\n'+ident+' Location: p3 | Severity: high | Review verdict: NO_BLOCKING_ISSUES\n'),1,'CRITIC_RAW_ISSUES_NOT_CLOSED')

    # r3: global results cannot suppress adjacent live issue-control cells.
    control_values={'Severity':'high','Location':'p3','Minimal fix':'correct denominator','Verdict':'NOT FIXED'}
    for side in ('raw','closure'):
        def setup_mixed(value,side=side):
            return lambda d,g:noissues(d,g,**{side+'_decl':value})
        for control,value in control_values.items():
            token=control.lower().replace(' ','_')
            cell=control+': '+value
            for scope in ('Review metadata','Issues','Review notes'):
                row='## '+scope+'\nReview verdict: NO_BLOCKING_ISSUES | '+cell+'\n'
                gate('mixed_'+side+'_'+token+'_'+scope.replace(' ','_'),setup_mixed(row),1,'CRITIC_REVIEW_MIXED_FIELDS')
            gate('mixed_'+side+'_'+token+'_reversed',setup_mixed(cell+' | '+decl),1,'CRITIC_REVIEW_MIXED_FIELDS')
            gate('mixed_'+side+'_'+token+'_inline_example_control',setup_mixed('Review verdict: NO_BLOCKING_ISSUES | `'+cell+'`\n'),0)
        example_row='Review verdict: NO_BLOCKING_ISSUES | '+' | '.join(k+': '+v for k,v in control_values.items())+'\n'
        gate('mixed_'+side+'_fence_example_then_live',setup_mixed('```text\n'+example_row+'```\n'+decl),0)
        gate('mixed_'+side+'_comment_example_then_live',setup_mixed('<!--\n'+example_row+'-->\n'+decl),0)
        gate('mixed_'+side+'_quote_example_then_live',setup_mixed('> '+example_row+'\n'+decl),0)
        gate('mixed_'+side+'_simple_valid_global',setup_mixed(decl),0)
    for control,value in control_values.items():
        token=control.lower().replace(' ','_')
        gate('mixed_after_real_issue_'+token,lambda d,g,control=control,value=value:replace_final(d,'2. restated | Verdict: FIXED | Evidence: p2 | none\nReview verdict: NO_BLOCKING_ISSUES | '+control+': '+value),1,'CRITIC_REVIEW_MIXED_FIELDS')

    if args.mixed_audit_inputs:
        audit=args.mixed_audit_inputs.resolve()
        names={'unassigned_same_global_row','metadata_same_global_row','issue_verdict_on_global_row'}
        originals=[x for x in json.loads((audit/'results.json').read_text()) if x['case'] in names]
        if len(originals)!=3: raise ValueError('Expected all three frozen mixed-row counterexamples')
        for original in originals:
            d=audit/'inputs'/original['case']
            before={str(f.relative_to(d)):fx.sha(f) for f in d.rglob('*') if f.is_file()}
            code,out=fx.run(d)
            after={str(f.relative_to(d)):fx.sha(f) for f in d.rglob('*') if f.is_file()}
            msgs='\n'.join(out.get('fail',[])+out.get('incomplete',[]))
            must='CRITIC_REVIEW_MIXED_FIELDS'
            ok=code==original['expected_exit']==1 and before==after==original['input_sha256'] and must in msgs
            results.append(dict(case='r2_frozen_'+original['case'],kind='mixed_frozen_replay',ok=ok,original_actual_exit=original['actual_exit'],original_required=original.get('required'),expected_exit=original['expected_exit'],actual_exit=code,input_sha256=before,inputs_unchanged=before==after,result=out,required=must))
            print(('OK  ' if ok else 'BAD ')+'r2_frozen_'+original['case']+f': exit {code}')

    if args.noissues_audit_inputs:
        audit=args.noissues_audit_inputs.resolve()
        for original in json.loads((audit/'minimal-results.json').read_text()):
            d=audit/'minimal'/original['case']
            before={str(f.relative_to(d)):fx.sha(f) for f in d.rglob('*') if f.is_file() and f.name not in ('stdout.json','stderr.txt')}
            code,out=fx.run(d)
            after={str(f.relative_to(d)):fx.sha(f) for f in d.rglob('*') if f.is_file() and f.name not in ('stdout.json','stderr.txt')}
            name=original['case'];must=None
            if name in ('missing_negative','final_fence','final_comment'): must='CRITIC_NO_ISSUE_VERDICT_NOT_IN_RAW'
            if name in ('summary_fence','summary_comment'): must='CRITIC: list actual issues'
            msgs='\n'.join(out.get('fail',[])+out.get('incomplete',[]))
            ok=code==original['expected_exit'] and before==after==original['input_sha256'] and (not must or must in msgs)
            results.append(dict(case='r1_frozen_'+name,kind='noissues_frozen_replay',ok=ok,original_actual_exit=original['actual_exit'],expected_exit=original['expected_exit'],actual_exit=code,input_sha256=before,inputs_unchanged=before==after,result=out,required=must))
            print(('OK  ' if ok else 'BAD ')+'r1_frozen_'+name+f': exit {code}')

    if args.audit_inputs:
        audit=args.audit_inputs.resolve()
        # Frozen inputs requiring a changed result are explicitly named here.
        ambiguous={'actual_frozen_raw','metadata_review_kind','metadata_generic_underscore','metadata_hyphen_key','metadata_separated_global','metadata_alphanumeric_key','metadata_plain_alpha_key','opaque_bare_colon_id'}
        for old in json.loads((audit/'parser_results.json').read_text()):
            name=old['case']; data=(audit/old['input']).read_bytes(); text=data.decode()
            errs=[];got=cg.parse_raw_issues(text,errs)
            if name in ambiguous:
                # Retain opaque IDs without treating an ambiguous Verdict as authority.
                retained = {'actual_frozen_raw':'review_kind', 'metadata_review_kind':'review_kind',
                            'metadata_generic_underscore':'session_mode', 'metadata_hyphen_key':'review-mode',
                            'metadata_separated_global':'session_mode', 'metadata_alphanumeric_key':'phase2',
                            'metadata_plain_alpha_key':'inherited_parent_context', 'opaque_bare_colon_id':'C1-06'}[name]
                expected = [(retained,None)] + ([] if name=='opaque_bare_colon_id' else [tuple(x) for x in old['expected_issues']])
                ok=got==expected and any('CRITIC_RAW_AMBIGUOUS_SCOPE' in e for e in errs)
            else:
                ok=[list(x) for x in got]==old['expected_issues'] and all(any(s in e for e in errs) for s in old['expected_error_substrings']) and (bool(old['expected_error_substrings']) or not errs)
            results.append(dict(case='audit_'+name,kind='frozen_replay',ok=ok,input_sha256=sha(data),actual=got,errors=errs,reclassified_ambiguous=name in ambiguous,original_expected=old['expected_issues']))
            print(('OK  ' if ok else 'BAD ')+'audit_'+name)
        p=audit/'ambiguous_same_bytes.md'
        parser('audit_same_bytes',p.read_text(),[('review_kind',None)],('CRITIC_RAW_AMBIGUOUS_SCOPE',),False)
    # Independent 2026-10-27 counterexamples: complete verdict values,
    # explicit identity, overall disposition and uniform closure scope.
    parser('explicit_identity_beats_ordinal',H+'## Issues\n### 7. Capital definition\nIssue ID: issue1\nVerdict: FIXED\n',[('issue1','FIXED')])
    parser('explicit_heading_id_conflict',H+'## Issues\n### C6: Capital definition\nIssue ID: C7\nVerdict: FIXED\n',[('C7','FIXED')],('CRITIC_RAW_ID_CONFLICT',),False)
    parser('duplicate_explicit_identity',H+'## Issues\n### 1. Capital definition\nIssue ID: C6\nIssue ID: C7\nVerdict: FIXED\n',[('1','FIXED')],('CRITIC_RAW_ID_COUNT',),False)
    parser('invalid_explicit_identity',H+'## Issues\n### 1. Capital definition\nIssue ID: C6 or C7\nVerdict: FIXED\n',[('1','FIXED')],('CRITIC_RAW_ID_VALUE',),False)
    parser('orphan_explicit_identity','pdf_sha256: '+'0'*64+'\n## Review notes\nIssue ID: C6\nVerdict: FIXED\n',[],('CRITIC_RAW_UNASSIGNED_ISSUE_FIELDS',),False)
    for val in ['FIXED or NOT FIXED','FIXED / NOT FIXED','FIXED (implementation only; required validation NOT FIXED)','FIXED: pending data','FIXED_UNREVIEWED']:
        parser('incomplete_value_'+str(len(results)),H+'## Issues\n1. Capital definition\nVerdict: '+val+'\n',[('1',None)])
    for title in ['Critical findings','Major findings','Detailed numerical findings','Issues and required corrections']:
        parser('incomplete_title_'+str(len(results)),H+'## '+title+'\n6. Missing scientific evidence\n',[('6',None)])

    def raw_overall(d,g,value,round_=2):
        p=d/f'artifacts/review/r{round_}.md';p.write_text(p.read_text()+'\nReview verdict: '+value+'\n')
    gate('final_overall_negative_blocks',lambda d,g:raw_overall(d,g,'NOT FIXED'),1,'CRITIC_FINAL_REVIEW_NOT_FIXED')
    gate('initial_overall_negative_later_repaired',lambda d,g:raw_overall(d,g,'NOT FIXED',1),0)
    gate('final_overall_unknown_incomplete',lambda d,g:raw_overall(d,g,'BLOCKING_ISSUES'),2,'CRITIC_FINAL_REVIEW_UNRECOGNIZED')
    def closure_overall(d,g):
        p=d/'artifacts/review/critic.md';p.write_text(p.read_text()+'\nReview verdict: NOT FIXED\n')
    gate('closure_overall_negative_blocks',closure_overall,1,'CRITIC_CLOSURE_REVIEW_NOT_FIXED')
    for val in ['FIXED or NOT FIXED','FIXED / NOT FIXED','FIXED (implementation only; required validation NOT FIXED)']:
        gate('unselected_final_'+str(len(results)),lambda d,g,v=val:replace_final(d,'2. restated | Verdict: '+v+' | Evidence: p2'),2,'CRITIC_FINAL_ISSUE_UNVERIFIED')
    gate('multiline_unselected_final',lambda d,g:replace_final(d,'2. restated\nVerdict:\nFIXED or NOT FIXED'),2,'CRITIC_FINAL_ISSUE_UNVERIFIED')
    def hidden_closure(d,g,kind):
        p=d/'artifacts/review/critic.md';t=p.read_text();wrapped=('```text\n'+t+'\n```') if kind=='fence' else ('<!--\n'+t+'\n-->')
        p.write_text(wrapped+'\nReview verdict: NO_BLOCKING_ISSUES\n')
    for kind in ['fence','comment']:
        gate('closure_all_in_'+kind,lambda d,g,k=kind:hidden_closure(d,g,k),2,'CRITIC_ROUNDS_MISSING')
    def inert_open(d,g,kind):
        p=d/'artifacts/review/critic.md';extra='1. Historical example\nStatus: OPEN\n'
        extra=('```text\n'+extra+'```') if kind=='fence' else ('<!--\n'+extra+'-->')
        p.write_text(p.read_text()+'\n'+extra+'\n')
    for kind in ['fence','comment']:
        gate('closure_inert_open_'+kind,lambda d,g,k=kind:inert_open(d,g,k),0)
    def explicit_identity(d,g,replace=False):
        for rn,ident in [(1,'stable2'),(2,'replacement2' if replace else 'stable2')]:
            p=d/f'artifacts/review/r{rn}.md';p.write_text(p.read_text().replace('\n2. ','\n2. Issue ID: '+ident+' | ',1))
        p=d/'artifacts/review/critic.md';p.write_text(p.read_text()+'\nIssue alias: round 1 | raw_id: stable2 | issue: 2\nIssue alias: round 2 | raw_id: stable2 | issue: 2\n')
    gate('explicit_identity_alias_positive',explicit_identity,0)
    gate('explicit_identity_replaced_blocks',lambda d,g:explicit_identity(d,g,True),1,'CRITIC_ALIAS_UNKNOWN_RAW_ID')

    # Second independent pass: multiline/global heading scope, task state,
    # identity replacement and contradictory context records.
    parser('multiline_overall_inside_issues',H+'## Issues\nReview verdict:\nNO_BLOCKING_ISSUES\n',[])
    parser('heading_overall_inside_issues',H+'## Issues\n## Review verdict\nNO_BLOCKING_ISSUES\n',[])
    parser('late_caption_verdict_identity',H+'## Issues\n### 1. Capital definition\nIssue ID: issue1\n**Actual-data recheck:** Recomputed independently.\nVerdict: FIXED\n',[('issue1','FIXED')])
    gate('multiline_overall_no_phantom_id',lambda d,g:raw_overall(d,g,'\nNO_BLOCKING_ISSUES'),0)
    def heading_overall(d,g,closure=False,multiline=False):
        p=d/'artifacts/review'/('critic.md' if closure else 'r2.md')
        p.write_text(p.read_text()+('\n## Review verdict\nNOT FIXED\n' if multiline else '\n## Review verdict: NOT FIXED\n'))
    for side in [False,True]:
        for multi in [False,True]:
            gate('heading_overall_negative_'+str(side)+'_'+str(multi),lambda d,g,s=side,m=multi:heading_overall(d,g,s,m),1,'REVIEW_NOT_FIXED')
    gate('explicit_gate_requirement_partial',lambda d,g:g['requirements'][0].update(status='PARTIAL'),2,'REQUIREMENT_INCOMPLETE')
    def contract_status(d,g,status):
        (d/'artifacts/problem_contract.json').write_text(json.dumps({'requirements':[{'id':'R1','status':status}]}))
    gate('explicit_contract_requirement_partial',lambda d,g:contract_status(d,g,'PARTIAL'),2,'REQUIREMENT_INCOMPLETE')
    gate('explicit_contract_answered_positive',lambda d,g:contract_status(d,g,'ANSWERED'),0)
    def context_raw(d,g,text):
        p=d/'artifacts/review/r2.md';lines=p.read_text().splitlines();p.write_text(lines[0]+'\n## Review metadata\n'+text+'\n## Issues\n'+'\n'.join(lines[1:])+'\n')
    gate('raw_context_contradiction',lambda d,g:context_raw(d,g,'fresh_session: no\ninherited_parent_context: yes'),1,'CRITIC_RAW_CONTEXT_CONTRADICTION')
    gate('raw_context_canonical_positive',lambda d,g:context_raw(d,g,'fresh_session: yes\ninherited_parent_context: no'),0)
    def alias_replace(d,g):
        for rn,ident in [(1,'budget1'),(2,'font2')]:
            p=d/f'artifacts/review/r{rn}.md';p.write_text(p.read_text().replace('\n2. ','\n2. Issue ID: '+ident+' | ',1))
        p=d/'artifacts/review/critic.md';p.write_text(p.read_text()+'\nIssue alias: round 1 | raw_id: budget1 | issue: 2\nIssue alias: round 2 | raw_id: font2 | issue: 2\n')
    gate('crossround_alias_cannot_replace_stable_identity',alias_replace,1,'CRITIC_ALIAS_CROSS_ROUND_ID_REPLACEMENT')
    def late_caption(d,g):
        replace_final(d,'2. restated\n**Post-fix audit:** Independent evidence on p2.\nVerdict: FIXED')
    gate('late_caption_verdict_positive',late_caption,0)
    for status,want in [('ANSWERED',0),('PARTIAL',2)]:
        d,g=fx.make(w/'audit_controls'/status)
        (d/'artifacts/project_state.json').write_text(json.dumps({'rules_verified':True}))
        (d/'artifacts/problem_contract.json').write_text(json.dumps({'requirements':[{'id':'R1','status':status,'evidence_ids':['B1'],'paper_location':'p2'}]}))
        (d/'artifacts/evidence_registry.json').write_text(json.dumps({'bindings':[{'id':'B1','path':'final/TEAM.pdf','sha256':fx.sha(d/'final/TEAM.pdf')}]}))
        proc=fx.subprocess.run([sys.executable,'-B',str(Path(__file__).parent/'audit_project.py'),str(d)],capture_output=True,text=True)
        result=json.loads(proc.stdout);ok=proc.returncode==want
        results.append(dict(case='audit_exit_'+status,kind='audit_cli',ok=ok,expected_exit=want,actual_exit=proc.returncode,result=result))
        (d/'audit-output.json').write_text(proc.stdout)
        print(('OK  ' if ok else 'BAD ')+'audit_exit_'+status)
    (w/'results.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n')
    good=sum(bool(r['ok']) for r in results)
    print(f'REVIEW SCOPE SELFTEST {"PASS" if good==len(results) else "FAIL"} ({good}/{len(results)} cases)')
    return 0 if good==len(results) else 1

if __name__=='__main__': sys.exit(main())
