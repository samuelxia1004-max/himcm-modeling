#!/usr/bin/env python3
"""v8.1 parser regressions. Fictional projects; authentic raw text copied unchanged.
Usage: python selftest_raw_issues.py WORKDIR [--baseline-only | --r2-only] (new directory; no deletion).
This is implementation testing, not independent review or a whole-problem run.
"""
import importlib.util, json, sys
from pathlib import Path
import selftest_gate as fixtures
import check_gate as cg
HERE = Path(__file__).resolve().parent
REAL = HERE.parent / 'validation/v81/fixtures'

def main():
    w = Path(sys.argv[1]).resolve(); results = []
    def case(name, text, expected, must=None, setup=None):
        d, g = fixtures.make(w / name)
        p = d/'artifacts/review/r1.md'
        p.write_text(p.read_text() + '\n' + text)
        if setup: setup(d, g)
        fixtures.save(d, g)
        code, out = fixtures.run(d)
        msgs = '\n'.join(out.get('fail', []) + out.get('incomplete', []))
        ok = code == expected and (not must or must in msgs)
        results.append({'case':name, 'ok':ok, 'actual_exit':code, 'expected_exit':expected, 'required_message':must, 'result':out})
        print(('OK  ' if ok else 'BAD ') + f'{name}: exit {code} (want {expected})' + (f' needs {must}' if must else ''))
    case('coverage_list_not_issues', '## All task closures\n1. Answered.\n2. Answered.\n3. Answered.\n4. Answered.\n5. Answered.\n6. Answered.\n', 0)
    case('read_pages_references_recompute_lists', '## Pages read\n1. Page one\n6. Page six\n## References\n1. Source one\n7. Source seven\n## Independent calculations\n1. Recomputed total\n8. Checked boundary\n', 0)
    case('field_issue_outside_container', '## Review notes\n6. New numerical defect\n- Location: p3\n- Severity: high\n- Minimal fix: correct the denominator\n', 1, 'CRITIC_RAW_ISSUES_NOT_CLOSED')
    case('findings_missing_all_fields', '## Findings\n6. A real uncovered problem with incomplete report fields\n', 1, 'CRITIC_RAW_ISSUES_NOT_CLOSED')
    case('issues_nested_missing_fields', '## Open issues\n### Numerical defects\n6. Missing supporting result\n', 1, 'CRITIC_RAW_ISSUES_NOT_CLOSED')
    case('field_lookahead_stops_at_section', '## Task closure\n6. Complete answer\n## General report\nLocation: full paper\n', 0)
    case('duplicate_ids_still_rejected', '## Findings\n2. Duplicate despite omitted fields\n', 1, 'CRITIC_RAW_DUPLICATE_ISSUE')
    def multiline(d,g):
        p=d/'artifacts/review/r2.md'; p.write_text(p.read_text().replace(' | Verdict:', '\n- Verdict:'))
    case('multiline_verdict', '', 0, setup=multiline)
    def nofinal(d,g):
        p=d/'artifacts/review/r2.md';p.write_text(p.read_text().replace('2. restated | Verdict: FIXED | Evidence: p2 | none', '2. Location: p2 | Severity: medium | Minimal fix: still unresolved'))
    case('missing_final_verdict_still_incomplete', '', 2, 'CRITIC_FINAL_ISSUE_UNVERIFIED', nofinal)
    def highwont(d,g):
        p=d/'artifacts/review/critic.md';p.write_text(p.read_text().replace('1. Issue 1 about claim C1. Severity: medium\nStatus: FIXED (verified round 2)', '1. Issue 1 about claim C1. Severity: high\nStatus: WONTFIX because inconvenient'))
    case('high_wontfix_still_fails', '', 1, 'CRITIC_HIGH_WONTFIX', highwont)
    def real(d,g, mapped=True):
        fixtures.write_critic(d,n_issues=3)
        raw=(REAL/'critic_round1_corrected_header_raw.md').read_text()
        (d/'artifacts/review/r1.md').write_text(raw)
        p=d/'artifacts/review/critic.md'; t=p.read_text().replace('pdf_sha256: '+'0'*64, raw.splitlines()[0])
        if mapped: t += ''.join(f'Issue alias: round 1 | raw_id: C1-0{i} | issue: {i}\n' for i in range(1,4))
        p.write_text(t)
    case('authentic_round1_explicit_aliases', '', 0, setup=real)
    case('authentic_round1_no_suffix_guess', '', 1, 'CRITIC_RAW_ISSUES_NOT_CLOSED', lambda d,g:real(d,g,False))
    def badalias(d,g):
        real(d,g); p=d/'artifacts/review/critic.md';p.write_text(p.read_text()+'Issue alias: round 1 | raw_id: C1-01 | issue: 2\n')
    case('duplicate_alias_rejected', '', 1, 'CRITIC_ALIAS_DUPLICATE', badalias)
    def unknownalias(d,g):
        real(d,g); p=d/'artifacts/review/critic.md';p.write_text(p.read_text()+'Issue alias: round 1 | raw_id: C1-99 | issue: 9\n')
    case('unknown_alias_rejected', '', 1, 'CRITIC_ALIAS_UNKNOWN_RAW_ID', unknownalias)
    if '--baseline-only' not in sys.argv[2:]:
        # r2 regressions from the separately preserved fresh audit's counterexamples.
        case('bare_named_heading_is_issue', '## Findings\n### C1-06\nSeverity: high\nLocation: p3\n', 1, 'CRITIC_RAW_ISSUES_NOT_CLOSED')
        case('colon_named_id_is_issue', '## Findings\nC1-06: Silent unit error\nSeverity: high\nLocation: p3\n', 1, 'CRITIC_RAW_ISSUES_NOT_CLOSED')
        case('plain_alphanumeric_id_punctuation', '## Findings\nC1. Silent unit error\nSeverity: high\nLocation: p3\n', 1, 'CRITIC_RAW_ISSUES_NOT_CLOSED')
        case('plain_alphanumeric_id_space', '## Findings\nC1 Silent unit error\nSeverity: high\nLocation: p3\n', 1, 'CRITIC_RAW_ISSUES_NOT_CLOSED')
        case('fields_under_child_heading', '## Review notes\n6. Silent unit error\n### Details\nSeverity: high\nLocation: p3\n', 1, 'CRITIC_RAW_ISSUES_NOT_CLOSED')
        case('unsupported_heading_id_fail_closed', '## Findings\n### CRITICAL\nSeverity: high\nLocation: p3\n', 1, 'CRITIC_RAW_UNASSIGNED_ISSUE_FIELDS')
        case('missing_id_fail_closed', '## Findings\nSeverity: high\nLocation: p3\n', 1, 'CRITIC_RAW_UNASSIGNED_ISSUE_FIELDS')
        def verdicts(d,g,new):
            p=d/'artifacts/review/r2.md'
            p.write_text(p.read_text().replace('2. restated | Verdict: FIXED | Evidence: p2 | none', new))
        case('conflicting_verdicts_multiline', '', 1, 'CRITIC_RAW_VERDICT_COUNT', lambda d,g:verdicts(d,g,'2. restated | Verdict: FIXED | Evidence: p2\n- Verdict: NOT FIXED\n'))
        case('conflicting_verdicts_same_line', '', 1, 'CRITIC_RAW_VERDICT_COUNT', lambda d,g:verdicts(d,g,'2. restated | Verdict: FIXED | Verdict: NOT FIXED | Evidence: p2'))
        case('negative_then_positive_verdict', '', 1, 'CRITIC_RAW_VERDICT_COUNT', lambda d,g:verdicts(d,g,'2. restated | Verdict: NOT FIXED\n- Verdict: FIXED\n'))
        case('duplicate_identical_verdicts', '', 1, 'CRITIC_RAW_VERDICT_COUNT', lambda d,g:verdicts(d,g,'2. restated | Verdict: FIXED\n- Verdict: FIXED\n'))
        case('invalid_second_verdict_rejected', '', 1, 'CRITIC_RAW_VERDICT_COUNT', lambda d,g:verdicts(d,g,'2. restated | Verdict: FIXED\n- Verdict: OPEN\n'))
        def overall(d,g):
            p=d/'artifacts/review/r2.md';p.write_text(p.read_text()+'\nReview verdict: NO_BLOCKING_ISSUES\n')
        case('overall_review_declaration_not_issue_verdict', '', 0, setup=overall)
    if '--baseline-only' not in sys.argv[2:]:
        # Alias examples/comments are documentation, never mapping declarations.
        def comment_example(d,g):
            import re
            text=(HERE.parent/'assets/critic_template.md').read_text()
            sample=next(x for x in re.findall(r'<!--.*?-->',text,re.S) if 'Issue alias:' in x)
            p=d/'artifacts/review/critic.md';p.write_text(p.read_text()+'\n'+sample+'\n')
        case('remaining_default_template_comment_inert', '', 0, setup=comment_example)
        def quoted_aliases(d,g,opener,closer):
            real(d,g)
            p=d/'artifacts/review/critic.md';t=p.read_text()
            lines=t.splitlines(); aliases=[line for line in lines if line.startswith('Issue alias:')]
            t='\n'.join(line for line in lines if not line.startswith('Issue alias:'))+'\n'
            p.write_text(t+opener+'\n'+'\n'.join(aliases)+'\n'+closer+'\n')
        case('html_comment_cannot_authorize_alias', '', 1, 'CRITIC_RAW_ISSUES_NOT_CLOSED', lambda d,g:quoted_aliases(d,g,'<!--','-->'))
        case('backtick_fence_cannot_authorize_alias', '', 1, 'CRITIC_RAW_ISSUES_NOT_CLOSED', lambda d,g:quoted_aliases(d,g,'```text','```'))
        case('tilde_fence_cannot_authorize_alias', '', 1, 'CRITIC_RAW_ISSUES_NOT_CLOSED', lambda d,g:quoted_aliases(d,g,'~~~','~~~'))
        def active_after_example(d,g):
            real(d,g);p=d/'artifacts/review/critic.md'
            p.write_text('<!--\nIssue alias: round 1 | raw_id: EXAMPLE-99 | issue: 99\n-->\n```\nIssue alias: round 1 | raw_id: EXAMPLE-98 | issue: 98\n```\n'+p.read_text())
        case('outside_alias_after_examples_remains_active', '', 0, setup=active_after_example)
    if '--baseline-only' not in sys.argv[2:]:
        def quoted_comment_opener(d,g):
            real(d,g);p=d/'artifacts/review/critic.md'
            p.write_text('```text\n<!--\n```\n'+p.read_text())
        case('fenced_comment_opener_cannot_hide_active_alias', '', 0, setup=quoted_comment_opener)
    if '--baseline-only' not in sys.argv[2:] and '--r2-only' not in sys.argv[2:]:
        # r3: default numeric raw has no parent section. ### is child detail.
        def child_detail(d,g,line):
            p=d/'artifacts/review/r2.md'
            p.write_text(p.read_text().replace('2. restated | Verdict: FIXED | Evidence: p2 | none', '2. restated | Verdict: FIXED | Evidence: p2 | none\n### Recheck details\n'+line))
        case('default_no_section_child_conflict', '', 1, 'CRITIC_RAW_VERDICT_COUNT', lambda d,g:child_detail(d,g,'- Verdict: NOT FIXED'))
        case('default_no_section_child_duplicate', '', 1, 'CRITIC_RAW_VERDICT_COUNT', lambda d,g:child_detail(d,g,'- Verdict: FIXED'))
        case('default_no_section_child_invalid_verdict', '', 1, 'CRITIC_RAW_VERDICT_COUNT', lambda d,g:child_detail(d,g,'- Verdict: OPEN'))
        case('default_no_section_child_evidence_control', '', 0, setup=lambda d,g:child_detail(d,g,'- Evidence: p2 correct denominator independently recomputed'))
        case('default_task_and_reference_sections_control', '6. Task coverage complete\n## References\nLocation: source library\n1. Read first reference\n7. Read additional reference\n## Recalculation\n8. Verified total independently\n', 0)
    expected = [('C1-01',None),('C1-02',None),('C1-03',None)]
    actual = cg.parse_raw_issues((REAL/'critic_round1_corrected_header_raw.md').read_text())
    final = cg.parse_raw_issues((REAL/'critic_final_fresh_raw.md').read_text())
    ok = actual == expected and final == [(str(i),'FIXED') for i in range(1,4)]
    results.append({'case':'authentic_raw_exact_issue_sets', 'ok':ok, 'round1':actual,'final':final})
    print(('OK  ' if ok else 'BAD ')+'authentic_raw_exact_issue_sets')
    (w/'results.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n')
    passed = all(x['ok'] for x in results)
    print(f'RAW SELFTEST {"PASS" if passed else "FAIL"} ({len(results)} cases)')
    sys.exit(0 if passed else 1)
if __name__ == '__main__': main()
