#!/usr/bin/env python3
"""Self-test for check_gate.py (v8) and check_pdf.py on fictional, problem-neutral projects.
Usage: selftest_gate.py WORKDIR   (creates WORKDIR/fixture_*; never deletes anything; does not use /tmp)
Each case states the expected exit code and, where relevant, a substring that must appear in fail/incomplete/warn."""
import json, subprocess, sys, hashlib, re
from pathlib import Path
import pymupdf as fitz
HERE = Path(__file__).resolve().parent
LOREM = ("The model allocates a fixed weekly budget across service routes and compares the plan with the current schedule. "
         "Each route has a demand forecast, a cost per trip and a capacity, and the objective balances coverage and cost. ") * 14
TAIL = "END OF SUMMARY TEXT MARKER."

UNI_FONTS = ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/System/Library/Fonts/Supplemental/Arial.ttf',
             '/Library/Fonts/Arial Unicode.ttf', 'C:/Windows/Fonts/arial.ttf']
UNI = next((f for f in UNI_FONTS if Path(f).exists()), None)   # needed to render curly quotes / en dashes in the fixture

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def build_pdf(d, pages=19, spill=False, ai=True, extra_text=None, img_pages=(), refs_pages=0):
    doc = fitz.open(); p = doc.new_page()
    summ = ("Summary Sheet. We plan weekly service for a fictional town. Result: coverage rises from 61.0% to 74.5% at equal cost. "
            "Hold-out validation on 2015-2016 demand: MAPE 8.2% versus 14.9% for the naive last-year baseline. "
            "Sensitivity: the plan changes only if fuel cost rises above 1.40 per km. ")
    if spill:
        p.insert_textbox(fitz.Rect(50, 50, 545, 800), summ * 9, fontsize=12); p2 = doc.new_page(); p2.insert_text((50, 80), TAIL, fontsize=12)
    else: p.insert_textbox(fitz.Rect(50, 50, 545, 800), summ + TAIL, fontsize=12)
    pix = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, 60, 40), 0); pix.clear_with(200)
    while len(doc) < pages:
        q = doc.new_page(); n = len(doc)
        if n in img_pages:          # big figure at the top, nothing else: half-empty page with an image
            q.insert_image(fitz.Rect(60, 60, 535, 300), pixmap=pix); q.insert_text((60, 320), f"Figure {n}. A figure.", fontsize=12); continue
        if refs_pages and n > pages - refs_pages:
            q.insert_textbox(fitz.Rect(50, 50, 545, 800), ("References Section. " if n == pages - refs_pages + 1 else "") + LOREM, fontsize=12); continue
        body = f"Section {n}. " + (extra_text + " " if (extra_text and n == 4) else "") + LOREM[:-400 if (extra_text and n == 4) else None]
        if n == 3: body = f"Section {n}. See Figure 1 and Table 1. " + LOREM
        if extra_text and n == 4 and UNI: q.insert_textbox(fitz.Rect(50, 50, 545, 800), body, fontsize=12, fontname='uni', fontfile=UNI)
        else: q.insert_textbox(fitz.Rect(50, 50, 545, 800), body, fontsize=12)
    if ai: a = doc.new_page(); a.insert_text((50, 80), "Report on Use of AI. This fictional report was produced for a self-test.", fontsize=12)
    doc.save(d / 'final/TEAM.pdf')

def write_critic(d, n_issues=5, verified=True, sha_override=None, raw_has_sha=True, fresh='yes', contra=False, round3=None, new_issue=False):
    s = sha(d / 'final/TEAM.pdf') if sha_override is None else sha_override
    (d / 'artifacts/review/r1.md').write_text("pdf_sha256: " + "0" * 64 + "\n" + "".join(f"{i}. Location: p{i} | Evidence: issue {i} | Severity: medium | Minimal fix: fix {i}\n" for i in range(1, n_issues + 1)) + "x" * 200)
    s2 = "1" * 64 if round3 else s      # with a third round, round 2 reviewed an earlier PDF
    (d / 'artifacts/review/r2.md').write_text(("pdf_sha256: " + s2 + "\n" if raw_has_sha else "") + "".join(
        f"{i}. restated | Verdict: {'NOT FIXED' if (contra and i == 2) else 'FIXED'} | Evidence: p{i} | none\n" for i in range(1, n_issues + 1))
        + (f"{n_issues + 1}. Location: p9 | Evidence: new problem | Severity: high | Minimal fix: x\n" if new_issue else "") + "y" * 200)
    if round3: (d / 'artifacts/review/r3.md').write_text("pdf_sha256: " + s + "\n" + "".join(f"{i}. restated | Verdict: {v} | Evidence: p{i} | none\n" for i, v in round3.items()) + "z" * 200)
    txt = ("Critic: fresh-context reviewer (self-test)\n"
           "Round: 1 | critic: test | fresh_session: yes | pdf_sha256: " + "0" * 64 + " | raw: artifacts/review/r1.md\n"
           f"Round: 2 | critic: test | fresh_session: {fresh} | pdf_sha256: {s2} | raw: artifacts/review/r2.md\n"
           + (f"Round: 3 | critic: test | fresh_session: yes | pdf_sha256: {s} | raw: artifacts/review/r3.md\n" if round3 else ""))
    txt += "".join(f"{i}. Issue {i} about claim C1. Severity: medium\nStatus: FIXED" + (" (verified round 2)" if verified else "") + "\n" for i in range(1, n_issues + 1))
    (d / 'artifacts/review/critic.md').write_text(txt)

def make(dirp, pages=19, **kw):
    d = Path(dirp)
    for sub in ('artifacts/review', 'data', 'final'): (d / sub).mkdir(parents=True, exist_ok=True)
    build_pdf(d, pages=pages, **kw)
    (d / 'data/source_log.md').write_text("| Parameter | Value | Class | Use | Source |\n|---|---|---|---|---|\n"
        "| demand 2010-2014 | table | observed | calibration | city open data |\n| demand 2015-2016 | table | observed | validation | city open data holdout file |\n"
        "| fuel cost | 1.1 | external | input | agency report |\n| driver wage | 20 | assumed | input | range 15-25 |\n")
    (d / 'artifacts/independent_ideas.md').write_text("Baseline: last-year plan\n1. Coverage-weighted routing by demand density\n2. Queue model of peak loads at hubs\n3. Budget-constrained knapsack over routes\nChosen core contribution: idea 1, because it can be tested on held-out demand and it changes the plan.\n")
    write_critic(d)
    # Explicitly fictional policy, not a claim about actual 2016 rules. Earlier
    # fixtures relied on the gate's implicit AI-page exemption; v8.3 registers it.
    g = {"rules": {"rules_year": 2016, "rules_source": "fictional instructions: summary + 24 pages", "max_main_pages": 25, "target_min_pages": 18, "contest_cutoff_date": "2016-11-01",
                   "ai_report_excluded_from_main_limit": True,
                   "ai_report_exclusion_rule_quote": "Fictional 2016 fixture rule: the appended AI-use report does not count toward the page limit."},
         "pdf": {"main_pages": pages, "summary_last_text": TAIL, "ai_report_first_text": "Report on Use of AI. This fictional report"},
         "requirements": [{"id": "R1", "result_excerpt": "coverage rises from 61.0% to 74.5% at equal cost", "interpretation_excerpt": "The model allocates a fixed weekly budget", "exhibits": ["Figure 1", "Table 1"]}],
         "validations": [{"id": "V1", "kind": "external_holdout", "outcome": "pass", "paper_excerpt": "MAPE 8.2% versus 14.9% for the naive last-year baseline",
                          "data_source": "city open data 2015-2016", "source_log_match": "city open data holdout", "metric": "MAPE", "metric_direction": "lower_is_better",
                          "model_value": 8.2, "baseline_name": "last-year", "baseline_value": 14.9,
                          "pre_cutoff": True, "planned_before_results": True, "used_for_model_selection": False}],
         "claims": [{"id": "C1", "type": "prediction", "summary_excerpt": "coverage rises from 61.0% to 74.5%", "validation_ids": ["V1"]}],
         "attachments": []}
    sp = d / 'data/source_log.md'
    lines = sp.read_text().splitlines()
    converted=[]
    names={'demand 2010-2014':('D0','city open data 2010-2014'),'demand 2015-2016':('D1','city open data 2015-2016'),'fuel cost':('P1','agency fuel price'),'driver wage':('P2','assumed driver wage')}
    for line in lines:
        if line.startswith('| Parameter'): converted.append(line+' ID | Dataset |')
        elif line.startswith('|---'): converted.append(line+'---|---|')
        elif line.startswith('|'):
            param=line.split('|')[1].strip(); sid,ds=names[param];converted.append(line+f' {sid} | {ds} |')
        else: converted.append(line)
    sp.write_text('\n'.join(converted)+'\n')
    g['validations'][0]['source_ids']=['D1']
    save(d, g); return d, g

def save(d, g): (d / 'artifacts/gate.json').write_text(json.dumps(g, indent=1))

def run(d):
    r = subprocess.run([sys.executable, str(HERE / 'check_gate.py'), str(d), '--pdf', 'final/TEAM.pdf'], capture_output=True, text=True)
    try: return r.returncode, json.loads(r.stdout)
    except Exception: return r.returncode, {'status': 'CRASH', 'fail': [r.stderr[-300:]], 'incomplete': [], 'warn': []}

def main():
    w = Path(sys.argv[1]).resolve(); C = {}   # name -> (expected_code, must_contain or None, result)
    def case(name, code, must=None, setup=None, **kw):
        d, g = make(w / f'fixture_{name}', **kw)
        if setup: setup(d, g); save(d, g)
        C[name] = (code, must, run(d))
    # --- v7 cases (kept) ---
    case('good', 0)
    case('short', 0, 'BELOW_INTERNAL_TARGET', pages=12)
    case('spill', 1, 'SUMMARY_SPILLS', spill=True)
    case('reused', 1, 'used to choose', setup=lambda d, g: g['validations'][0].update(used_for_model_selection=True))
    def short_exc(d, g):
        with open(d / 'artifacts/review/critic.md', 'a') as f: f.write('SHORT_EXCEPTION_APPROVED: every sub-question answered and validated; extra pages would only repeat results.\n')
    case('short_exc', 0, 'BELOW_TARGET_WITH_CRITIC_EXCEPTION', pages=12, setup=short_exc)
    def html(d, g):
        (d / 'inputs').mkdir(exist_ok=True); (d / 'inputs/data.xlsx').write_text('<!DOCTYPE html><html>404 Not Found</html>')
        g['attachments'] = [{'id': 'A1', 'path': 'inputs/data.xlsx', 'used_in': ['R1'], 'conversion_notes': 'read sheet 1'}]
    case('html_attachment', 1, 'HTML page', setup=html)
    def post(d, g):
        with open(d / 'data/source_log.md', 'a') as f: f.write('| unit cost | 0.8 | external | calibration | later industry report (post-contest) |\n')
    case('postcontest', 1, 'post-contest', setup=post)
    case('fail_no_disposition', 1, 'no disposition', setup=lambda d, g: g['validations'][0].update(outcome='fail'))
    case('normative', 0, setup=lambda d, g: g.update(claims=[{'id': 'C1', 'type': 'normative', 'summary_excerpt': 'coverage rises from 61.0% to 74.5%', 'validation_ids': ['V1']}]))
    # --- fix 1: critic re-review evidence ---
    case('critic_unreviewed', 2, 'FIXED_UNREVIEWED', setup=lambda d, g: write_critic(d, verified=False))
    case('critic_explicit_unreviewed', 2, 'FIXED_UNREVIEWED', setup=lambda d, g: (d / 'artifacts/review/critic.md').write_text(
        (d / 'artifacts/review/critic.md').read_text().replace('Status: FIXED (verified round 2)', 'Status: FIXED_UNREVIEWED', 1)))
    case('critic_not_final_pdf', 1, 'FINAL_CRITIC_ROUND_NOT_ON_FINAL_PDF', setup=lambda d, g: write_critic(d, sha_override='a' * 64))
    case('critic_sha_not_in_raw', 1, 'SHA_NOT_IN_RAW', setup=lambda d, g: write_critic(d, raw_has_sha=False))
    case('critic_contradiction', 1, 'CRITIC_CONTRADICTION', setup=lambda d, g: write_critic(d, contra=True))
    case('critic_not_fresh', 1, 'fresh_session', setup=lambda d, g: write_critic(d, fresh='no'))
    case('critic_later_not_fixed', 1, 'CRITIC_CONTRADICTION', setup=lambda d, g: write_critic(d, round3={1: 'FIXED', 2: 'NOT FIXED', 3: 'FIXED', 4: 'FIXED', 5: 'FIXED'}))
    case('critic_raw_new_issue', 1, 'CRITIC_RAW_ISSUES_NOT_CLOSED', setup=lambda d, g: write_critic(d, new_issue=True))
    case('critic_bullets', 1, 'not under a numbered issue', setup=lambda d, g: (d / 'artifacts/review/critic.md').write_text(
        re.sub(r'(?m)^(\d+)\. ', '- ', (d / 'artifacts/review/critic.md').read_text())))
    case('critic_no_rounds', 2, 'CRITIC_ROUNDS_MISSING', setup=lambda d, g: (d / 'artifacts/review/critic.md').write_text(
        re.sub(r'(?m)^Round:.*\n', '', (d / 'artifacts/review/critic.md').read_text())))
    # --- fix 2: excerpt normalization (curly quotes, hyphen line breaks, markdown emphasis, en dash) ---
    def norm_setup(d, g):
        g['requirements'][0]['interpretation_excerpt'] = 'the household\'s **"pre-registered"** test covers 2015-2016'
    if not UNI: print('NOTE: no Unicode TTF found; excerpt_normalized uses base-14 font and may fail')
    case('excerpt_normalized', 0, extra_text="Note: the household\u2019s \u201cpre-\nregistered\u201d test covers 2015\u20132016.", setup=norm_setup)
    case('excerpt_really_missing', 1, 'first', setup=lambda d, g: g['requirements'][0].update(interpretation_excerpt='The model allocates a variable monthly budget'))
    # --- fix 3: ideas "Chosen" regex (first colon, multi-line) ---
    case('ideas_colons', 0, setup=lambda d, g: (d / 'artifacts/independent_ideas.md').write_text(
        "Baseline: last-year plan\n1. Coverage-weighted routing by demand density\n2. Queue model of peak loads at hubs\n3. Budget-constrained knapsack over routes\n"
        "Chosen core contribution and why (testable? changes the decision?): idea 1, testable on held-out demand: yes\n"))
    case('ideas_nextline', 0, setup=lambda d, g: (d / 'artifacts/independent_ideas.md').write_text(
        "Baseline: x\n1. Coverage-weighted routing by demand density\n2. Queue model of peak loads at hubs\n3. Budget-constrained knapsack over routes\n"
        "Chosen core contribution and why (testable? changes the decision?):\nIdea 1, because it is testable on held-out demand and changes the plan.\n"))
    case('ideas_filler_after_empty', 2, 'IDEAS: chosen', setup=lambda d, g: (d / 'artifacts/independent_ideas.md').write_text(
        "Baseline: x\n1. Coverage-weighted routing by demand density\n2. Queue model of peak loads at hubs\n3. Budget-constrained knapsack over routes\n"
        "Chosen core contribution and why:\n\nNotes: unrelated scratch text that is long enough to look like content.\n"))
    case('ideas_empty', 2, 'IDEAS: chosen', setup=lambda d, g: (d / 'artifacts/independent_ideas.md').write_text(
        "Baseline: x\n1. Coverage-weighted routing by demand density\n2. Queue model of peak loads at hubs\n3. Budget-constrained knapsack over routes\n"
        "Chosen core contribution and why (testable? changes the decision?):\n"))
    # --- fix 4: main_pages required / auto-detected, never silently = total ---
    case('main_autodetect', 0, 'MAIN_PAGES_AUTODETECTED', setup=lambda d, g: g['pdf'].update(main_pages=None))
    case('main_autodetect_short', 0, 'BELOW_INTERNAL_TARGET', pages=17, setup=lambda d, g: g['pdf'].update(main_pages=None))
    case('main_mismatch', 1, 'MAIN_PAGES_MISMATCH', setup=lambda d, g: g['pdf'].update(main_pages=17))
    case('main_unknown_no_ai', 2, 'PDF_MAIN_PAGES_UNKNOWN', ai=False, setup=lambda d, g: (g['pdf'].update(main_pages=None), g['pdf'].pop('ai_report_first_text')))
    # --- fix 5: year-aware page rules ---
    case('rules_year_mismatch', 1, 'RULES_YEAR_MISMATCH', setup=lambda d, g: g['rules'].update(rules_year=2021))
    case('rules_year_missing', 2, 'RULES_YEAR_MISSING', setup=lambda d, g: g['rules'].pop('rules_year'))
    case('cap_refs_counted', 1, 'PAGE_CAP_EXCEEDED', pages=24, refs_pages=2, setup=lambda d, g: g['rules'].update(max_main_pages=22))
    case('cap_refs_excluded', 0, None, pages=24, refs_pages=2, setup=lambda d, g: g['rules'].update(max_main_pages=22, excluded_from_cap=[{'name': 'references', 'first_text': 'References Section.', 'to_end': True, 'rule_quote': 'fictional rule: references are not counted'}]))
    case('excl_no_rule', 1, 'EXCLUDED_FROM_CAP_WITHOUT_RULE', pages=24, refs_pages=2, setup=lambda d, g: g['rules'].update(max_main_pages=22, excluded_from_cap=[{'name': 'refs', 'first_text': 'References Section.', 'to_end': True}]))
    case('excl_bad_end', 1, 'EXCLUDED_SECTION_ANCHOR', pages=24, refs_pages=2, setup=lambda d, g: g['rules'].update(max_main_pages=22, excluded_from_cap=[{'name': 'refs', 'first_text': 'References Section.', 'last_text': 'no such closing text', 'rule_quote': 'fictional rule: references are not counted'}]))
    case('excl_no_end', 1, 'EXCLUDED_SECTION_END', pages=24, refs_pages=2, setup=lambda d, g: g['rules'].update(max_main_pages=22, excluded_from_cap=[{'name': 'refs', 'first_text': 'References Section.', 'rule_quote': 'fictional rule: references are not counted'}]))
    # --- fix 6: half-empty pages including pages with images ---
    case('half_empty_images', 0, 'HALF_EMPTY_PAGES', img_pages=(5, 8, 11))
    case('half_empty_one', 0, 'HALF_EMPTY_PAGES', img_pages=(5,))
    case('half_empty_last_page', 0, 'HALF_EMPTY_PAGES', img_pages=(5, 8, 19))
    case('half_empty_excused', 0, None, img_pages=(5, 8, 11), setup=lambda d, g: g['pdf'].update(short_page_reasons={str(p): 'full-width figure must stay with its section' for p in (5, 8, 11)}))
    # --- fix 7: model loses to pre-registered baseline ---
    case('baseline_loss', 1, 'MODEL_LOSES_TO_BASELINE', setup=lambda d, g: g['validations'][0].update(model_value=16.0))
    case('baseline_higher_better', 1, 'MODEL_LOSES_TO_BASELINE', setup=lambda d, g: g['validations'][0].update(metric_direction='higher_is_better'))
    case('baseline_no_direction', 2, 'metric_direction', setup=lambda d, g: g['validations'][0].pop('metric_direction'))
    case('baseline_string_value', 2, 'finite numbers', setup=lambda d, g: g['validations'][0].update(model_value='16'))
    case('baseline_empty_disclosure', 1, 'the paper must say so', setup=lambda d, g: g['validations'][0].update(model_value=16.0, baseline_loss_excerpt=''))
    # --- fix 8: every validation source has a source_log row with Use = validation ---
    case('srclog_missing_row', 1, 'no data/source_log.md row', setup=lambda d, g: g['validations'][0].update(source_log_match='national survey 2015'))
    case('srclog_wrong_use', 1, 'expected validation', setup=lambda d, g: g['validations'][0].update(source_log_match='agency report'))
    case('srclog_no_key', 2, 'source_log_match', setup=lambda d, g: g['validations'][0].pop('source_log_match'))
    case('srclog_ambiguous', 2, 'matches 2 rows', setup=lambda d, g: g['validations'][0].update(source_log_match='city open data'))
    def notval(d, g):
        (d / 'data/source_log.md').write_text((d / 'data/source_log.md').read_text().replace('| observed | validation | city open data holdout', '| observed | not validation | city open data holdout'))
    case('srclog_not_validation', 1, 'expected validation', setup=notval)
    case('srclog_unrelated_source', 1, 'VALIDATION_DATASET_MISMATCH', setup=lambda d, g: g['validations'][0].update(data_source='national weather archive'))
    # v8 regressions originate in independent counterexamples; fixtures are fictional.
    case('external_check_reuse', 1, 'changing its kind', setup=lambda d, g: g['validations'][0].update(kind='external_check', used_for_model_selection=True, planned_before_results=False))
    def high_wontfix(d, g):
        write_critic(d, contra=True)
        p = d / 'artifacts/review/critic.md'
        p.write_text(p.read_text().replace('2. Issue 2 about claim C1. Severity: medium\nStatus: FIXED (verified round 2)', '2. Issue 2 about claim C1. Severity: high\nStatus: WONTFIX deadline; retain the unsupported result'))
    case('high_wontfix', 1, 'CRITIC_HIGH_WONTFIX', setup=high_wontfix)
    case('final_review_omits', 2, 'CRITIC_FINAL_ISSUE_UNVERIFIED', setup=lambda d, g: write_critic(d, round3={1:'FIXED'}))
    def wrong_round(d, g):
        p=d/'artifacts/review/critic.md'; p.write_text(p.read_text().replace('verified round 2', 'verified round 1', 1))
    case('wrong_verified_round', 2, 'FIXED_UNREVIEWED', setup=wrong_round)
    def post_context(d, g):
        p=d/'data/source_log.md'; p.write_text(p.read_text().replace('validation | city open data holdout file', 'validation, context | city open data holdout file (post-contest)'))
    case('postcontest_plus_context', 1, 'post-contest', setup=post_context)
    def withdrawn(d, g):
        g['validations'][0].update(outcome='fail', failure_action={'kind':'withdraw','paper_excerpt':'We withdraw claim C1 because the validation failed.'})
    case('withdrawn_headline', 1, 'WITHDRAWN_VALIDATION_SUPPORTS_ACTIVE_CLAIM', extra_text='We withdraw claim C1 because the validation failed.', setup=withdrawn)
    case('ai_report_absent', 2, 'AI_REPORT_REQUIRED_MISSING', ai=False, setup=lambda d, g:g['pdf'].pop('ai_report_first_text'))
    def nested(d, g):
        p=d/'artifacts/review/critic.md'; p.write_text(p.read_text().replace('Status:', '  - Evidence: substantive explanation for this same issue\nStatus:'))
    case('nested_evidence', 0, setup=nested)
    case('duplicate_validation_id', 1, 'DUPLICATE_IDS', setup=lambda d, g:g['validations'].append(dict(g['validations'][0])))
    def noissues(d, g):
        raw='pdf_sha256: '+sha(d/'final/TEAM.pdf')+'\nReview verdict: NO_BLOCKING_ISSUES\nThe original tasks and results were reviewed in full.\n'
        (d/'artifacts/review/noissues.md').write_text(raw)
        (d/'artifacts/review/critic.md').write_text('Critic: independent self-test fixture\nRound: 1 | critic: test | fresh_session: yes | pdf_sha256: '+sha(d/'final/TEAM.pdf')+' | raw: artifacts/review/noissues.md\nReview verdict: NO_BLOCKING_ISSUES\n')
    case('genuine_no_issues', 0, setup=noissues)
    def assumed_validation(d, g):
        p=d/'data/source_log.md';p.write_text(p.read_text().replace('| observed | validation | city open data holdout', '| assumed | validation | city open data holdout'))
    case('assumed_validation', 1, 'INDEPENDENT_SOURCE_IS_ASSUMED', setup=assumed_validation)
    def duplicate_status(d, g):
        p=d/'artifacts/review/critic.md';t=p.read_text();t=t.replace('Status: FIXED (verified round 2)', 'Status: FIXED (verified round 2)\nStatus: FIXED (verified round 2)',1)
        # Remove issue 2 status; global counts are unchanged, but its closure is missing.
        t=t.replace('2. Issue 2 about claim C1. Severity: medium\nStatus: FIXED (verified round 2)', '2. Issue 2 about claim C1. Severity: high')
        p.write_text(t)
    case('duplicate_status_hides_missing', 1, 'CRITIC_ISSUE_STATUS_COUNT', setup=duplicate_status)
    case('source_generic_word_collision', 1, 'VALIDATION_DATASET_MISMATCH', setup=lambda d, g:g['validations'][0].update(data_source='city airport weather archive 2015-2016'))
    def duplicate_raw(d, g):
        p=d/'artifacts/review/r2.md';p.write_text(p.read_text()+'\n2. repeated | Verdict: FIXED | Evidence: contradicted entry\n')
    case('duplicate_raw_issue', 1, 'CRITIC_RAW_DUPLICATE_ISSUE', setup=duplicate_raw)
    def revive(d,g):
        withdrawn(d,g)
        g['validations'].append({'id':'V2','kind':'sensitivity','outcome':'pass','paper_excerpt':'We withdraw claim C1 because the validation failed.'})
        g['claims'][0]['validation_ids'].append('V2')
    case('withdraw_plus_sensitivity', 1, 'WITHDRAWN_VALIDATION_SUPPORTS_ACTIVE_CLAIM',extra_text='We withdraw claim C1 because the validation failed.',setup=revive)
    case('valid_earlier_citation_and_final',0,setup=lambda d,g:write_critic(d,round3={i:'FIXED' for i in range(1,6)}))
    # --- normalizer unit checks (font-independent) ---
    sys.dont_write_bytecode = True; sys.path.insert(0, str(HERE)); import check_gate as cg
    eq = [('pre\u00ad\nregistered', 'pre-registered'), ('pre-\nregistered', 'pre-registered'), ('household\u2019s \u201cx\u201d', 'household\'s "x"'),
          ('2015\u20132016', '2015-2016'), ('**bold** _it_', 'bold it'), ('\ufb01nal', 'final'), ('8- layer', '8-layer'), ('2015\u2013 2016', '2015-2016')]
    ne = [('a \u22123.2 t', 'a 3.2 t'), ('rises 5%', 'falls 5%'), ('10-20', '1020'), ('x\u22123', 'x3'), ('a_b', 'ab')]
    bad = [x for x in eq if cg.norm(x[0]) != cg.norm(x[1])] + [x for x in ne if cg.norm(x[0]) == cg.norm(x[1])]
    C['norm_unit'] = (0, None, (1 if bad else 0, {'status': 'UNIT', 'fail': [repr(b) for b in bad], 'incomplete': [], 'warn': []}))
    # --- check_pdf: no hard-coded 25-page cap ---
    dp = w / 'fixture_checkpdf'; (dp / 'final').mkdir(parents=True, exist_ok=True); (dp / 'artifacts/review').mkdir(parents=True, exist_ok=True); (dp / 'data').mkdir(exist_ok=True)
    build_pdf(dp, pages=27); (dp / 'final/TEAM.pdf').rename(dp / 'final/T1.pdf')
    r = subprocess.run([sys.executable, str(HERE / 'check_pdf.py'), str(dp / 'final/T1.pdf'), '--team', 'T1', '--main-pages', '27', '--max-main-pages', '25'], capture_output=True, text=True)
    o = json.loads(r.stdout); C['checkpdf_no_hardcap'] = (0, 'OVER_YEAR_CAP', (r.returncode, {'status': o['status'], 'fail': o['errors'], 'incomplete': [], 'warn': [x['issue'] for x in o['review']]}))
    ok = True
    for k, (code, must, (got, out)) in C.items():
        msgs = ' '.join(map(str, out.get('fail', []) + out.get('incomplete', []) + out.get('warn', [])))
        good = got == code and (must is None or must in msgs)
        ok &= good
        print(('OK  ' if good else 'BAD ') + f'{k}: exit {got} (want {code})' + (f", needs '{must}'" if must else '') + ('' if good else f" | {out.get('status')} F={out.get('fail', [])[:2]} I={out.get('incomplete', [])[:2]} W={out.get('warn', [])[:2]}"))
    print(f'SELFTEST {"PASS" if ok else "FAIL"} ({sum(1 for _ in C)} cases)'); sys.exit(0 if ok else 1)

if __name__ == '__main__': main()
