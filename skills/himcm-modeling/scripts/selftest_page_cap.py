#!/usr/bin/env python3
"""Full-gate synthetic page-cap controls, not scientific review.

Usage: selftest_page_cap.py NEW_WORKDIR [--root-probe FROZEN_ROOT_PROBE]
                           [--r1-audit FROZEN_R1_AUDIT]
                           [--r2-audit FROZEN_R2_AUDIT]
                           [--r3-audit FROZEN_R3_AUDIT]
Creates a fresh work directory and preserves every input and complete gate output.
Rule sentences here are explicitly fictional; they do not establish any year's
official rules. Frozen probe inputs are replayed unchanged, then a distinct copy
of the modern positive is explicitly migrated to the new manifest contract.
"""
import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path
import pymupdf as fitz
import selftest_gate as fx

QUOTE = 'Fictional target-year rule: the appended AI-use report is excluded from the submission page limit.'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('workdir', type=Path)
    ap.add_argument('--root-probe', type=Path)
    ap.add_argument('--r1-audit', type=Path)
    ap.add_argument('--r2-audit', type=Path)
    ap.add_argument('--r3-audit', type=Path)
    args = ap.parse_args()
    w = args.workdir.resolve()
    w.mkdir(parents=True, exist_ok=False)
    results = []

    def record(name, d, want_exit, total, main, counted, must=None, basis=None, extra=None, output_path=None):
        code, out = fx.run(d)
        p = out.get('info', {}).get('pdf', {})
        messages = '\n'.join(out.get('fail', []) + out.get('incomplete', []) + out.get('warn', []))
        ok = (code == want_exit and p.get('total_pages') == total and p.get('main_pages') == main
              and p.get('counted_pages') == counted and (must is None or must in messages)
              and (basis is None or p.get('page_cap_basis') == basis))
        row = dict(case=name, kind='full_gate', family='original_page_cap', ok=ok, expected_exit=want_exit,
                   actual_exit=code, expected_total=total, expected_main=main,
                   expected_counted=counted, required_message=must, result=out)
        if extra:
            row.update(extra)
        results.append(row)
        (output_path or d / 'page-cap-result.json').write_text(json.dumps(row, indent=2) + '\n')
        print(('OK  ' if ok else 'BAD ') + f'{name}: exit {code}; total/main/counted={p.get("total_pages")}/{p.get("main_pages")}/{p.get("counted_pages")}', flush=True)

    def case(name, main=24, ai_pages=1, cap=25, want=0, counted=None, setup=None, refs=0, must=None, exempt=False):
        d, g = fx.make(w / name, pages=main, ai=bool(ai_pages), refs_pages=refs)
        g['rules'].update(rules_year=2024 if exempt else 2022,
                          contest_cutoff_date='2024-11-01' if exempt else '2022-11-01',
                          rules_source='Fictional target-year instructions used only for mechanical controls.',
                          max_main_pages=cap)
        g['rules'].pop('ai_report_excluded_from_main_limit', None)
        g['rules'].pop('ai_report_exclusion_rule_quote', None)
        if exempt:
            g['rules'].update(ai_report_excluded_from_main_limit=True, ai_report_exclusion_rule_quote=QUOTE)
        if not ai_pages:
            g['rules']['ai_report_required'] = False
            g['pdf'].pop('ai_report_first_text', None)
        if ai_pages > 1:
            p = d / 'final/TEAM.pdf'
            doc = fitz.open(p)
            for i in range(ai_pages - 1):
                page = doc.new_page()
                page.insert_text((50, 80), f'AI-use report continuation {i + 2}. Synthetic control.', fontsize=12)
            doc.saveIncr()
            doc.close()
            fx.write_critic(d)
        if setup:
            setup(d, g)
        fx.save(d, g)
        record(name, d, want, main + ai_pages, main,
               main + ai_pages if counted is None else counted, must)

    case('all_pages_below', main=23, counted=24)
    case('all_pages_at_cap', main=24, counted=25)
    case('all_pages_one_over', main=25, want=1, counted=26, must='PAGE_CAP_EXCEEDED')
    case('all_pages_main_alone_over', main=26, want=1, counted=27, must='PAGE_CAP_EXCEEDED')
    case('all_pages_multiple_ai_at_cap', main=22, ai_pages=3, counted=25)
    case('all_pages_multiple_ai_over', main=23, ai_pages=3, want=1, counted=26, must='PAGE_CAP_EXCEEDED')
    case('explicit_false_counts_ai', main=25, want=1, counted=26, must='PAGE_CAP_EXCEEDED',
         setup=lambda d, g: g['rules'].update(ai_report_excluded_from_main_limit=False))
    case('modern_explicit_exemption', main=25, exempt=True, counted=25)
    case('modern_multiple_ai_exemption', main=25, ai_pages=3, exempt=True, counted=25)
    case('modern_main_over_cap', main=26, exempt=True, want=1, counted=26, must='PAGE_CAP_EXCEEDED')
    case('modern_short_target_uses_main', main=17, ai_pages=3, exempt=True, counted=17, must='BELOW_INTERNAL_TARGET')
    case('all_pages_short_target_uses_main', main=17, ai_pages=3, counted=20, must='BELOW_INTERNAL_TARGET')
    case('no_ai_at_cap', main=25, ai_pages=0, counted=25)
    case('no_ai_over_cap', main=26, ai_pages=0, want=1, counted=26, must='PAGE_CAP_EXCEEDED')
    case('unknown_legacy_scope_cannot_exempt', main=25, want=1, counted=26, must='PAGE_CAP_EXCEEDED',
         setup=lambda d, g: g['rules'].update(page_cap_scope='main_excluding_ai'))
    case('malformed_legacy_scope_cannot_exempt', main=25, want=1, counted=26, must='PAGE_CAP_EXCEEDED',
         setup=lambda d, g: g['rules'].update(page_cap_scope={'unknown': True}))
    for label, flag in [('string_true', 'true'), ('integer_one', 1), ('null', None), ('array', []), ('object', {})]:
        case('invalid_flag_' + label, main=24, want=1, counted=25, must='AI_REPORT_EXEMPTION_FLAG_INVALID',
             setup=lambda d, g, value=flag: g['rules'].update(ai_report_excluded_from_main_limit=value, ai_report_exclusion_rule_quote=QUOTE))
    for label, quote in [('missing', None), ('empty', ''), ('short', 'AI excluded'), ('placeholder', '<paste exact exemption sentence>'), ('integer', 42)]:
        def bad_quote(d, g, value=quote):
            g['rules']['ai_report_excluded_from_main_limit'] = True
            if value is None:
                g['rules'].pop('ai_report_exclusion_rule_quote', None)
            else:
                g['rules']['ai_report_exclusion_rule_quote'] = value
        case('invalid_quote_' + label, main=24, want=1, counted=25, must='AI_REPORT_EXEMPTION_WITHOUT_RULE', setup=bad_quote)
    case('exemption_year_missing', main=24, exempt=True, want=2, counted=25,
         must='AI_REPORT_EXEMPTION_YEAR_UNVERIFIED', setup=lambda d, g: g['rules'].pop('rules_year'))
    case('exemption_cutoff_missing', main=24, exempt=True, want=2, counted=25,
         must='AI_REPORT_EXEMPTION_YEAR_UNVERIFIED', setup=lambda d, g: g['rules'].pop('contest_cutoff_date'))
    case('exemption_year_mismatch', main=24, exempt=True, want=1, counted=25,
         must='RULES_YEAR_MISMATCH', setup=lambda d, g: g['rules'].update(contest_cutoff_date='2022-11-01'))
    case('exemption_source_placeholder', main=24, exempt=True, want=2, counted=25,
         must='AI_REPORT_EXEMPTION_YEAR_UNVERIFIED', setup=lambda d, g: g['rules'].update(rules_source='<official source locator>'))
    refs = [{'name': 'references', 'first_text': 'References Section.', 'to_end': True,
             'rule_quote': 'Fictional target-year instructions exclude references from the page limit.'}]
    case('anchored_references_all_pages_at_cap', main=26, refs=2, counted=25,
         setup=lambda d, g: g['rules'].update(excluded_from_cap=refs))
    case('anchored_references_all_pages_over', main=27, refs=2, want=1, counted=26, must='PAGE_CAP_EXCEEDED',
         setup=lambda d, g: g['rules'].update(excluded_from_cap=refs))
    case('anchored_references_and_ai_exempt', main=27, refs=2, exempt=True, counted=25,
         setup=lambda d, g: g['rules'].update(excluded_from_cap=refs))
    case('unanchored_reference_exemption_rejected', main=24, refs=2, want=2, counted=25, must='EXCLUDED_SECTION_ANCHOR',
         setup=lambda d, g: g['rules'].update(excluded_from_cap=[dict(refs[0], first_text='No such reference section')]))

    # These are unfilled-template controls, not semantic source authentication.
    family_start = len(results)
    prompts = [
        ('todo', 'TODO: paste the exact official AI exclusion sentence here.'),
        ('square', '[PASTE THE EXACT TARGET-YEAR AI EXEMPTION SENTENCE HERE]'),
        ('mixed_case', 'tOdO: Replace this with the actual exemption quotation.'),
        ('markdown', '**TODO**: paste the exact official rule quotation here.'),
        ('code', '`TBD: insert the applicable official exclusion sentence.`'),
        ('fixme', '[FIXME: insert the exact policy quotation here]'),
        ('unicode', 'ＴＯＤＯ： paste the official exemption sentence here.'),
        ('whitespace', '\n  Please   insert the target-year exemption quotation here.\n'),
        ('quoted', '"PASTE the exact official AI exemption sentence here."'),
        ('fill_in', 'Fill in the exact target-year rule quote here.'),
        ('fill_hyphen', 'Please fill-in the actual target-year rule quotation here.'),
        ('replace', 'Replace this placeholder with the official rule sentence.'),
        ('angle', '<paste the exact official exemption quotation>'),
        ('nested_angle', '[<paste the exact official exemption quotation>]'),
        ('dash', 'TODO — the official exemption quotation is still missing.'),
    ]
    for label, prompt in prompts:
        case('policy_quote_prompt_' + label, main=20, ai_pages=5, cap=20, exempt=True,
             want=1, counted=25, must='AI_REPORT_EXEMPTION_WITHOUT_RULE',
             setup=lambda d, g, value=prompt: g['rules'].update(ai_report_exclusion_rule_quote=value))
    for label, prompt in prompts[:4]:
        case('policy_source_prompt_' + label, main=20, ai_pages=5, cap=20, exempt=True,
             want=1, counted=25, must='RULES_SOURCE_MISSING',
             setup=lambda d, g, value=prompt: g['rules'].update(rules_source=value))
        case('policy_reference_prompt_' + label, main=24, refs=2, cap=22, exempt=True,
             want=1, counted=24, must='EXCLUDED_FROM_CAP_WITHOUT_RULE',
             setup=lambda d, g, value=prompt: g['rules'].update(excluded_from_cap=[dict(refs[0], rule_quote=value)]))
    substantive = [
        ('quoted', '"The additional AI Use Report does not count toward the 25-page limit."'),
        ('citation', '[COMAP, 2024, p.2] The AI Use Report does not count toward the 25-page limit.'),
        ('todo_in_prose', 'The word "TODO" appears in an example; the AI-use report is excluded from the page limit.'),
        ('do_not_paste', 'Do not paste an AI-use report into the main solution; its pages are excluded from the cap.'),
        ('insert_report', 'Insert an AI-use report after the solution; these pages are excluded from the cap.'),
        ('provide_report', 'Provide the AI-use report separately; it does not count toward the page limit.'),
    ]
    for label, quote in substantive:
        case('substantive_policy_quote_' + label, main=20, ai_pages=5, cap=20, exempt=True, counted=20,
             setup=lambda d, g, value=quote: g['rules'].update(ai_report_exclusion_rule_quote=value))
    for label, source in [('citation', '[COMAP 2024, p.2] Contest instructions: AI-use report page exemption.'),
                          ('bracket_locator', '[Official contest instructions, 2024, page 2, AI Use Report policy]')]:
        case('substantive_policy_source_' + label, main=20, ai_pages=5, cap=20, exempt=True, counted=20,
             setup=lambda d, g, value=source: g['rules'].update(rules_source=value))
    for label, quote in [('citation', '[2] References are excluded from the submission page limit.'),
                         ('quoted', '"The bibliography does not count toward the solution page limit."')]:
        case('substantive_reference_rule_' + label, main=24, refs=2, cap=22, exempt=True, counted=22,
             setup=lambda d, g, value=quote: g['rules'].update(excluded_from_cap=[dict(refs[0], rule_quote=value)]))
    for row in results[family_start:]:
        row['family'] = 'r2_policy_placeholder'
        # Persist the same classification alongside each complete gate result.
        (w / row['case'] / 'page-cap-result.json').write_text(json.dumps(row, indent=2) + '\n')

    # Minimal pairs distinguish missing evidence from document-placement rules
    # in all three shared fields, with identical structural prefixes.
    def policy_pair_case(name, field, candidate, substantive, family='r3_policy_minimal_pairs'):
        is_section = field == 'section_quote'
        message = None if substantive else {
            'source': 'RULES_SOURCE_MISSING',
            'ai_quote': 'AI_REPORT_EXEMPTION_WITHOUT_RULE',
            'section_quote': 'EXCLUDED_FROM_CAP_WITHOUT_RULE'}[field]
        def setup(d, g):
            if is_section:
                g['rules']['excluded_from_cap'] = [dict(refs[0], rule_quote=candidate)]
            else:
                key = 'rules_source' if field == 'source' else 'ai_report_exclusion_rule_quote'
                g['rules'][key] = candidate
        case(name, main=25 if is_section else 22, ai_pages=4, refs=3 if is_section else 0,
             cap=22, exempt=True, want=0 if substantive else 1,
             counted=22 if substantive else (25 if is_section else 26), must=message, setup=setup)
        row = results[-1]
        row.update(family=family, policy_field=field,
                   policy_candidate=candidate, substantive_candidate=substantive,
                   expected_effective_exemption=is_section or substantive)
        row['ok'] &= row['result'].get('info', {}).get('pdf', {}).get('ai_report_excluded_from_main_limit') is (is_section or substantive)
        (w / name / 'page-cap-result.json').write_text(json.dumps(row, indent=2) + '\n')

    wrappers = [('blockquote', '> **{}**'), ('list', '- **{}**'), ('heading', '### {}'),
                ('ordered', '1. {}'), ('nested', '> - ### **{}**')]
    for field in ('source', 'ai_quote', 'section_quote'):
        content = 'references' if field == 'section_quote' else 'AI-use report'
        substantive = f'Insert the {content} after the solution; this rule excludes its pages from the submission cap.'
        for label, wrapper in wrappers:
            policy_pair_case(f'r3_{field}_{label}_missing', field,
                             wrapper.format('TODO: paste the exact official policy sentence here.'), False)
            policy_pair_case(f'r3_{field}_{label}_substantive', field, wrapper.format(substantive), True)
        policy_pair_case(f'r3_{field}_evidence_target', field,
                         'Insert the exact official rule quotation here.', False)
        policy_pair_case(f'r3_{field}_content_target', field,
                         f'Insert the {content} under this rule after the solution; its pages are excluded from the submission cap.', True)
        policy_pair_case(f'r3_{field}_numbered_citation', field,
                         '1. [COMAP, 2024, p.2] ' + substantive, True)

    # Citation syntax is not an unfinished prompt, and a citation prefix must
    # not shield a following known prompt. All statements remain synthetic.
    locator = 'https://policy.example.org/2024/instructions#length'
    http_locator = locator.replace('https:', 'http:', 1)
    for field in ('source', 'ai_quote', 'section_quote'):
        content = 'references section' if field == 'section_quote' else 'appended AI-use report'
        supplied = f'The {content} is excluded from the submission page cap.'
        missing = 'TODO: paste the exact official policy sentence here.'
        forms = [('angle', '<' + locator + '>'), ('plain', locator),
                 ('named', '[Official instructions](' + locator + ')')]
        for label, prefix in forms:
            for state, candidate, substantive in [('supplied', supplied, True), ('missing', missing, False)]:
                policy_pair_case(f'r4_{field}_{label}_{state}', field, prefix + ' ' + candidate,
                                 substantive, family='r4_citation_pairs')
        for state, candidate, substantive in [('supplied', supplied, True), ('missing', missing, False)]:
            policy_pair_case(f'r4_{field}_nested_http_{state}', field,
                             '> - ### **(<' + http_locator + '> ' + candidate + ')**',
                             substantive, family='r4_citation_pairs')
        policy_pair_case(f'r4_{field}_adjacent_links_supplied', field,
                         '<' + locator + '><' + locator + '> ' + supplied,
                         True, family='r4_citation_pairs')
        policy_pair_case(f'r4_{field}_adjacent_angle_prompt', field,
                         '<' + locator + '><paste the exact official policy sentence here>',
                         False, family='r4_citation_pairs')
        policy_pair_case(f'r4_{field}_angle_prompt', field,
                         '<paste the exact official policy sentence here>', False, family='r4_citation_pairs')

    if args.root_probe:
        probe = args.root_probe.resolve()
        controls = [('2022_total25_valid', 0, 25, 24, 25),
                    ('2022_total26_overcap', 1, 26, 25, 26),
                    ('2022_main26_overcap', 1, 27, 26, 27),
                    ('2024_main25_plus_ai_valid', 1, 26, 25, 26)]
        for name, code, total, main, counted in controls:
            original = probe / name
            d = w / ('unchanged_root_' + name)
            shutil.copytree(original, d)
            hashes = {str(p.relative_to(original)): hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in original.rglob('*') if p.is_file()}
            unchanged = all(hashlib.sha256((d / path).read_bytes()).hexdigest() == digest for path, digest in hashes.items())
            record('unchanged_root_' + name, d, code, total, main, counted,
                   'PAGE_CAP_EXCEEDED' if code else None,
                   extra={'original_expected_exit': 0 if name == '2024_main25_plus_ai_valid' else code,
                          'new_contract_expected_exit': code,
                          'contract_migration_required': name == '2024_main25_plus_ai_valid',
                          'original_files_unchanged': unchanged, 'original_file_hashes': hashes})
            results[-1]['ok'] &= unchanged
        d = w / 'explicitly_migrated_root_modern_positive'
        shutil.copytree(probe / '2024_main25_plus_ai_valid', d)
        g = json.loads((d / 'artifacts/gate.json').read_text())
        before = dict(g['rules'])
        g['rules'].update(ai_report_excluded_from_main_limit=True, ai_report_exclusion_rule_quote=QUOTE)
        fx.save(d, g)
        record('explicitly_migrated_root_modern_positive', d, 0, 26, 25, 25,
               basis='main_report_excluding_ai', extra={'migration': {'rules_before': before, 'rules_after': g['rules']},
               'evidence_note': 'Synthetic mechanical policy declaration, not a verified official quotation.'})

    if args.r1_audit:
        audit = args.r1_audit.resolve()
        for name in ('explicit_placeholder_todo', 'explicit_placeholder_square'):
            original = audit / 'new-controls' / name
            d = w / ('unchanged_r1_' + name)
            before = {str(p.relative_to(original)): hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in original.rglob('*') if p.is_file()}
            shutil.copytree(original, d)
            copied_exact = all(hashlib.sha256((d / path).read_bytes()).hexdigest() == digest
                               for path, digest in before.items())
            record('unchanged_r1_' + name, d, 1, 25, 20, 25,
                   'AI_REPORT_EXEMPTION_WITHOUT_RULE', basis='all_submitted_pages',
                   extra={'family': 'frozen_r1_counterexample_replay', 'original_actual_exit': 0,
                          'original_expected_exit': 1, 'original_file_hashes': before,
                          'copied_inputs_byte_exact': copied_exact})
            after = {str(p.relative_to(original)): hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in original.rglob('*') if p.is_file()}
            results[-1]['original_inputs_unchanged'] = before == after
            copied_unchanged = all(hashlib.sha256((d / path).read_bytes()).hexdigest() == digest
                                   for path, digest in before.items())
            results[-1]['copied_inputs_unchanged_after_execution'] = copied_unchanged
            results[-1]['ok'] &= copied_exact and copied_unchanged and before == after
            (d / 'page-cap-result.json').write_text(json.dumps(results[-1], indent=2) + '\n')

    if args.r2_audit:
        audit = args.r2_audit.resolve()
        batches = [
            ('control-results.json', 'controls',
             [field + '_' + variant for field in ('source', 'ai_quote', 'section_quote')
              for variant in ('block_quote', 'list_marker', 'heading', 'insert_report_rule')]),
            ('supplement-results.json', 'supplement-controls',
             ['field_specific_ai_quote_rule', 'field_specific_section_quote_rule'])]
        for result_file, dirname, names in batches:
            old_results = {row['name']: row for row in json.loads((audit / result_file).read_text())}
            for name in names:
                old = old_results[name]
                expected = old['expected']
                original = audit / dirname / name
                d = w / ('unchanged_r2_' + name)
                before = {str(p.relative_to(original)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in original.rglob('*') if p.is_file()}
                shutil.copytree(original, d)
                copied_exact = all(hashlib.sha256((d / path).read_bytes()).hexdigest() == digest
                                   for path, digest in before.items())
                main = expected['main']
                total = expected.get('total', main + expected.get('ai', 0))
                counted = expected.get('expected_count', expected.get('counted'))
                effective = expected.get('expected_effective', expected.get('effective'))
                record('unchanged_r2_' + name, d, expected['expected_exit'], total, main, counted,
                       expected.get('required_message', expected.get('must')),
                       basis='main_report_excluding_ai' if effective else 'all_submitted_pages',
                       extra={'family': 'frozen_r2_counterexample_replay', 'original_r2_expected': expected,
                              'original_actual_exit': old['actual_exit'], 'original_file_hashes': before,
                              'copied_inputs_byte_exact': copied_exact})
                after = {str(p.relative_to(original)): hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in original.rglob('*') if p.is_file()}
                row = results[-1]
                row['original_inputs_unchanged'] = before == after
                copied_unchanged = all(hashlib.sha256((d / path).read_bytes()).hexdigest() == digest
                                       for path, digest in before.items())
                row['copied_inputs_unchanged_after_execution'] = copied_unchanged
                actual_pdf = row['result'].get('info', {}).get('pdf', {})
                row['ok'] &= copied_exact and copied_unchanged and before == after and actual_pdf.get('ai_report_excluded_from_main_limit') is effective
                if 'expected_main_substance' in expected:
                    row['ok'] &= actual_pdf.get('main_report_counted_pages') == expected['expected_main_substance']
                (d / 'page-cap-result.json').write_text(json.dumps(row, indent=2) + '\n')

    if args.r3_audit:
        audit = args.r3_audit.resolve()
        output_dir = w / 'r3-replay-outputs'
        output_dir.mkdir()
        batches = [
            ('results-v2.json', [field + '_citation_autolink' for field in ('source', 'ai', 'section')],
             'frozen_r3_counterexample_replay'),
            ('supplement-results.json', ['supplement_' + field + '_' + form
             for field in ('source', 'ai', 'section') for form in ('angle', 'plain')], 'frozen_r3_syntax_repeat')]
        for result_file, names, family in batches:
            old_results = {row['name']: row for row in json.loads((audit / result_file).read_text())}
            for name in names:
                old = old_results[name]
                expected = old['expected']
                original = audit / 'controls' / name
                d = w / 'r3-replay-inputs' / name
                def hashes(directory):
                    return {str(p.relative_to(directory)): hashlib.sha256(p.read_bytes()).hexdigest()
                            for p in directory.rglob('*') if p.is_file()}
                before = hashes(original)
                shutil.copytree(original, d)
                copied_exact = hashes(d) == before
                (output_dir / (name + '.input-hashes-before.json')).write_text(json.dumps(before, indent=2) + '\n')
                record('unchanged_r3_' + name, d, expected['expected_exit'], expected['main'] + expected['ai'],
                       expected['main'], expected['expected_count'], expected['required_message'],
                       basis='main_report_excluding_ai' if expected['expected_effective'] else 'all_submitted_pages',
                       extra={'family': family, 'original_r3_expected': expected,
                              'original_actual_exit': old['actual_exit'], 'original_file_hashes': before,
                              'copied_inputs_byte_exact': copied_exact},
                       output_path=output_dir / (name + '.result.json'))
                source_after = hashes(original)
                copied_after = hashes(d)
                row = results[-1]
                row['original_inputs_unchanged'] = before == source_after
                row['copied_inputs_unchanged_after_execution'] = before == copied_after
                actual_pdf = row['result'].get('info', {}).get('pdf', {})
                row['ok'] &= (copied_exact and before == source_after == copied_after
                              and actual_pdf.get('ai_report_excluded_from_main_limit') is expected['expected_effective']
                              and actual_pdf.get('main_report_counted_pages') == expected['expected_main_substance'])
                (output_dir / (name + '.input-hashes-after.json')).write_text(
                    json.dumps({'source': source_after, 'copy': copied_after}, indent=2) + '\n')
                (output_dir / (name + '.result.json')).write_text(json.dumps(row, indent=2) + '\n')

    (w / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    good = sum(r['ok'] for r in results)
    print(f'PAGE CAP SELFTEST {"PASS" if good == len(results) else "FAIL"} ({good}/{len(results)} full-gate controls)', flush=True)
    for family in sorted({r['family'] for r in results}):
        rows = [r for r in results if r['family'] == family]
        print(f'{family}: {sum(r["ok"] for r in rows)}/{len(rows)} full-gate controls', flush=True)
    return 0 if good == len(results) else 1


if __name__ == '__main__':
    sys.exit(main())
