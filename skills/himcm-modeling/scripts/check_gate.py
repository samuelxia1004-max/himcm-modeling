#!/usr/bin/env python3
"""HiMCM v8.3 candidate delivery gate (one entry point). Reads only; writes nothing unless --output.

Exit 0 = GATE_PASS (mechanical checks pass; math/originality still need human/critic review)
Exit 1 = GATE_FAIL (hard problem: fix before calling the paper done)
Exit 2 = GATE_INCOMPLETE (required fields missing or unknown)
A paper may be DELIVERED as PARTIAL with exit 1/2 only if the failures are listed in
PROJECT_CONTEXT.md under "Known gaps" and in the AI-use report; it may never be called DONE.

Inputs (project-relative):
  artifacts/gate.json        one manifest: rules, pdf anchors, requirements, validations, attachments
  data/source_log.md         markdown table with a Class column (observed/attachment/external/estimated/assumed)
                             and optionally a Use column (input/calibration/validation/context)
  artifacts/review/critic.md independent critic pass, issues closed with Status: FIXED (verified round K) | WONTFIX <reason>
                             plus one 'Round:' line per critic round (see assets/critic_template.md)
  the final PDF (--pdf)
Thresholds are generic and problem-independent. Template: assets/gate_template.json
"""
import argparse, hashlib, json, re, sys, unicodedata
from pathlib import Path
sys.dont_write_bytecode = True
from _exact_io import strict_pairs

VAL_KINDS = {"external_holdout", "external_check", "development_holdout", "in_sample_replay",
             "reference_law", "implementation", "feasibility", "analytical", "consistency", "sensitivity"}
INDEPENDENT = {"external_holdout", "external_check"}
CLAIM_TYPES = {"prediction", "empirical_effect", "optimization", "mechanistic", "normative", "descriptive", "proof"}

DASHES = dict.fromkeys(map(ord, '\u2010\u2011\u2012\u2013\u2014\u2015\u2212\ufe63\uff0d'), '-')
QUOTES = {ord(c): "'" for c in '\u2018\u2019\u201a\u201b\u2032\u00b4`'}
QUOTES.update({ord(c): '"' for c in '\u201c\u201d\u201e\u201f\u2033\u00ab\u00bb'})

def norm(t):
    """Canonical text for excerpt matching: NFKC (ligatures, nbsp), straight quotes, ASCII hyphens,
    paired markdown emphasis removed, hyphens between letters dropped ('pre- registered' == 'pre-registered'),
    other line-break hyphens rejoined ('8- layer' -> '8-layer'); numeric ranges, minus signs and identifiers are preserved,
    whitespace collapsed. Case and digits are kept."""
    t = unicodedata.normalize('NFKC', str(t)).translate(DASHES).translate(QUOTES)
    t = t.replace('\u00ad', '-').replace('\u200b', '')   # some fonts extract a line-end hyphen as a soft hyphen
    for pat in (r'\*\*(.+?)\*\*', r'__(.+?)__', r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'(?<!\w)_(?!\s)(.+?)(?<!\s)_(?!\w)'):
        t = re.sub(pat, r'\1', t)                       # paired Markdown emphasis only; identifiers like a_b are kept
    t = re.sub(r'\s+', ' ', t)
    t = re.sub(r'(?<=[^\W\d_])- ?(?=[^\W\d_])', '', t)   # hyphen between LETTERS (word-internal or line break) dropped on both sides
    t = re.sub(r'(?<=\w)- (?=\w)', '-', t)                # other line-break hyphens ('8- layer', '2015- 2016') rejoined, hyphen kept
    return t.strip()


def policy_evidence_text(value, minimum):
    """Reject known unfilled policy templates, without authenticating a source.

    Normalize wrappers only for instruction detection; citation brackets and
    ordinary substantive rule quotations remain evidence candidates.
    """
    if not isinstance(value, str) or len(value.strip()) < minimum:
        return False
    text = norm(value).casefold()
    control = text
    url = r'https?://[^/\s<>][^\s<>]*'
    citation = r'(?:<' + url + r'>|\[[^\]\r\n]+\]\(https?://[^/\s<>)][^\s<>)]*\)|' + url + r')'
    previous = None
    while control != previous:
        previous = control
        control = re.sub(r'^[\s`*_\'"{}()]+', '', control)
        control = re.sub(r'^(?:>\s*|#{1,6}\s+|[-+*]\s+|\d+[.)]\s+)', '', control)
        # A citation is supplied evidence syntax, not an unfinished angle
        # prompt. Inspect what follows it so a URL cannot hide a known TODO.
        link = re.match(citation, control)
        if link:
            control = control[link.end():].lstrip()
        else:
            control = re.sub(r'^[\[\]]+', '', control)
    control = re.sub(r'[`*_]', '', control)
    if control.startswith('<') or re.match(r'(?:todo|tbd|fixme)\b', control):
        return False
    # Match the insertion/replacement target, not an evidence word in a later
    # clause describing where to put a report, references or other content.
    determiner = r'(?:(?:the|an?|your|this)\s+)?'
    modifiers = r'(?:(?:exact|actual|official|applicable|relevant|target\s*year|ai(?:\s*use)?|exemption|exclusion|policy|missing|unfilled|following)\s+)*'
    evidence_target = r'(?:quote|quotation|sentence|rule|source|citation|locator|placeholder)\b'
    if re.match(r'(?:please\s+)?(?:paste|insert|replace|fill(?:\s*in)?)\s+' + determiner + modifiers + evidence_target, control):
        return False
    return True



def markdown_live_text(text, protect_examples=False):
    """Remove HTML comments and fenced examples before reading declarations.
    Keep line breaks so comment/example contents cannot become authorization.
    """
    live = []; fence = None; comment = False
    for line in text.splitlines():
        if fence:
            m = re.match(r'^\s{0,3}(`{3,}|~{3,})(.*)$', line)
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= fence[1] and not m.group(2).strip(): fence = None
            live.append(''); continue
        if protect_examples and not comment and re.match(r'^\s*>', line):
            live.append(line); continue  # quoted comment delimiters are examples
        pos = 0; pieces = []
        while pos < len(line):
            if comment:
                end = line.find('-->', pos)
                if end < 0: break
                comment = False; pos = end + 3
            else:
                start = line.find('<!--', pos)
                if protect_examples:
                    tick = re.search(r'`+', line[pos:])
                    if tick and (start < 0 or pos + tick.start() < start):
                        a = pos + tick.start(); b = pos + tick.end()
                        close = re.search(r'(?<!`)`{' + str(b - a) + r'}(?!`)', line[b:])
                        if not close: pieces.append(line[pos:]); break
                        end = b + close.end()
                        pieces.append(line[pos:end]); pos = end; continue
                if start < 0: pieces.append(line[pos:]); break
                pieces.append(line[pos:start]); comment = True; pos = start + 4
        clean = ''.join(pieces)
        m = re.match(r'^\s{0,3}(`{3,}|~{3,})(.*)$', clean)
        if m:
            fence = (m.group(1)[0], len(m.group(1))); live.append(''); continue
        live.append(clean)
    return '\n'.join(live)

RAW_ISSUE_NAMED = r'(?:[A-Za-z][A-Za-z0-9]*(?:[-_][A-Za-z0-9]+)+|[A-Za-z]+[0-9]+)'
RAW_ISSUE_MARKER = re.compile(r'^\s*(?:#{1,6}\s+)?(?:[-+*]\s+)?(?:'
                        r'(\d+)[.)](?:\s+|$)|(' + RAW_ISSUE_NAMED + r')'
                        r'(?:[.):](?:\s+|$)|\s+[—–-]\s*|\s+|$))(.*)$')
REVIEW_HEADING = re.compile(r'^\s*(#{1,6})\s+(.+)$')
REVIEW_VERDICT_DECLARATION = re.compile(r'^Review\s+verdict\s*:\s*(.*)$', re.I)
ISSUE_CONTROL_DECLARATION = re.compile(r'^(Issue ID|Severity|Location|Minimal fix|Verdict)\s*:\s*(.*)$', re.I)

def review_live_rows(text, errors=None):
    """Shared live declaration text for raw issues and raw/closure review results."""
    errors = [] if errors is None else errors
    marker, heading = RAW_ISSUE_MARKER, REVIEW_HEADING
    # Fences/comments and inline spans are inert for *both* ID and field reads.
    # An unclosed inline span is ambiguous; never let it eat later live lines.
    rows = []; quoted = False
    for i, line in enumerate(markdown_live_text(text, protect_examples=True).splitlines()):
        if not line.strip(): quoted = False; rows.append(''); continue
        if re.match(r'^\s*>', line): quoted = True; rows.append(''); continue
        if re.match(r'^(?: {4}|\t)', line): rows.append(''); continue
        if quoted:
            if heading.match(line) or marker.match(line) or re.match(r'^[-+*]\s+', line): quoted = False
            else:
                errors.append(f'CRITIC_RAW_AMBIGUOUS_SCOPE: line {i + 1} may continue a Markdown quote; use a blank line before live declarations')
                rows.append(''); continue
        clean = []; pos = 0
        while pos < len(line):
            tick = re.search(r'`+', line[pos:])
            if not tick: clean.append(line[pos:]); break
            a = pos + tick.start(); b = pos + tick.end()
            clean.append(line[pos:a])
            close = re.search(r'(?<!`)`{' + str(b - a) + r'}(?!`)', line[b:])
            if not close:
                errors.append(f'CRITIC_RAW_AMBIGUOUS_SCOPE: line {i + 1} has an unclosed inline code span')
                break
            pos = b + close.end(); clean.append(' ' * (pos - a))
        line = ''.join(clean)
        for pat in (r'\*\*(.+?)\*\*', r'__(.+?)__'):
            line = re.sub(pat, r'\1', line)
        rows.append(line)

    # A global result does not own neighboring issue-control cells. Reject
    # mixed live rows in every scope, including raw/closure metadata and a
    # completed issue's following global row, before any row is classified.
    for i, line in enumerate(rows):
        marker = RAW_ISSUE_MARKER.match(line)
        if REVIEW_HEADING.match(line) and not marker: continue
        body = marker.group(3) if marker else line
        cells = review_field_cells(body)
        if (any(REVIEW_VERDICT_DECLARATION.match(cell) for cell in cells)
                and any(ISSUE_CONTROL_DECLARATION.match(cell) for cell in cells)):
            errors.append(f'CRITIC_REVIEW_MIXED_FIELDS: line {i + 1} combines Review verdict with issue control fields; put the overall result and issue fields on separately scoped rows')
    return rows


def review_field_cells(line):
    """A field starts a live line (optional bullet) or a pipe-delimited cell."""
    line = re.sub(r'^[-+*]\s+', '', line.strip())
    return [cell.strip() for cell in line.split('|')]


def review_verdict_fields(line):
    # An issue row cannot also serve as the whole-review declaration.
    if RAW_ISSUE_MARKER.match(line): return []
    h = REVIEW_HEADING.match(line)
    if h:
        title = h.group(2).strip().rstrip('#').strip()
        if re.fullmatch(r'Review\s+verdict', title, re.I): return ['']
        m = REVIEW_VERDICT_DECLARATION.fullmatch(title)
        return [m.group(1)] if m else []
    return [m.group(1) for cell in review_field_cells(line) if (m := REVIEW_VERDICT_DECLARATION.match(cell))]


def review_declarations(rows):
    result = []
    for i, line in enumerate(rows):
        for value in review_verdict_fields(line):
            value_row = i
            if not value.strip():
                for k in range(i + 1, len(rows)):
                    if rows[k].strip(): value = rows[k].strip(); value_row = k; break
            result.append((i, value, value_row))
    return result


def parse_review_verdict(text, errors=None):
    """One live whole-review declaration; examples/prose never supply authority.

    Duplicate or conflicting declarations fail even if one says NO_BLOCKING_ISSUES.
    A missing/unrecognized result has no authority. Legacy standalone spelling
    remains supported, with the same bullet/pipe/multiline grammar as issue fields.
    """
    errors = [] if errors is None else errors
    rows = review_live_rows(text, errors)
    if any(message.startswith('CRITIC_REVIEW_MIXED_FIELDS:') for message in errors): return None
    labels = review_declarations(rows)
    if len(labels) > 1:
        errors.append(f'CRITIC_REVIEW_VERDICT_COUNT: {len(labels)} live Review verdict declarations; require exactly one overall result')
        return None
    if not labels: return None
    i, value, _ = labels[0]
    return value if re.fullmatch(r'NO_BLOCKING_ISSUES|NOT FIXED|FIXED', value) else None


def parse_raw_issues(text, errors=None):
    """Read live issue/field declarations, with explicit review metadata scope.

    Legacy numeric/opaque heading, list and bare IDs remain supported. A bare
    opaque key: value with only a Verdict has indistinguishable metadata/issue
    readings: retain its ID, withhold its verdict and fail closed. New reviews
    should use Review metadata / Review verdict / Issues boundaries.
    """
    errors = [] if errors is None else errors
    named, marker, heading = RAW_ISSUE_NAMED, RAW_ISSUE_MARKER, REVIEW_HEADING
    declaration = ISSUE_CONTROL_DECLARATION

    rows = review_live_rows(text, errors)

    stack = []; candidates = []; in_container = []; metadata = []
    globals_ = {i for i, _, _ in review_declarations(rows)}
    globals_.update(k for _, value, k in review_declarations(rows) if value in ('FIXED','NOT FIXED','NO_BLOCKING_ISSUES'))
    for i, line in enumerate(rows):
        h = heading.match(line)
        if h:
            level = len(h.group(1))
            while stack and stack[-1][0] >= level: stack.pop()
            title = h.group(2).strip().rstrip('#').strip()
            is_metadata = bool(re.fullmatch(r'(?:Review\s+)?metadata', title, re.I))
            # Issue titles and titles ending in Findings grant implicit
            # identity. Findings followed by a narrative subject do not.
            # Keep arbitrary modifiers (e.g. Critical findings), rather
            # than silently dropping incomplete legacy issue listings.
            is_issues = bool(re.search(r'\bissues?\b', title, re.I) or re.search(r'\bfindings?(?:\s*\([^)]*\))?$', title, re.I))
            guard_fields = bool(re.search(r'\b(?:issues?|findings?)\b', title, re.I))
            stack.append((level, is_issues, is_metadata, guard_fields))
        meta = any(v for _, _, v, _ in stack)
        active = any(v for _, v, _, _ in stack) and not meta
        guard = any(v for _, _, _, v in stack) and not meta
        metadata.append(meta); in_container.append(guard)
        if i in globals_: continue
        m = marker.match(line)
        if m and not meta:
            # A multiword emphasized label ending in a colon inside an
            # explicitly headed issue is prose belonging to that issue.
            # Keep its following fields in the parent's block, so a late
            # verdict retains identity and duplicate/negative fields cannot
            # disappear behind an evidence caption.
            original_line = text.splitlines()[i].strip()
            label = bool(re.match(r'^(?:\*\*[^*]+:\*\*|__[^_]+:__)(?:\s|$)', original_line))
            bare_title = not h and bool(re.match(r'^\s*' + re.escape(m.group(1) or m.group(2)) + r'\s+\S', line))
            previous = candidates[-1] if candidates else None
            same_block = previous is not None and not any(
                k in globals_ or metadata[k] or (heading.match(rows[k]) and len(heading.match(rows[k]).group(1)) <= previous[3])
                for k in range(previous[0] + 1, i))
            label_match = re.match(r'^(?:\*\*([^*]+):\*\*|__([^_]+):__)(?:\s|$)', original_line)
            multiword_label = bool(label_match and len((label_match.group(1) or label_match.group(2)).split()) >= 2)
            caption = bool(label and multiword_label and bare_title and same_block)
            if caption: continue
            level = len(h.group(1)) if h else (stack[-1][0] if stack else 2)
            # key: value alone is not enough to distinguish an opaque issue
            # from arbitrary legacy header metadata. Issue fields disambiguate.
            bare_key = not h and bool(re.match(r'^\s*' + named + r':(?:\s|$)', line))
            candidates.append((i, m.group(1) or m.group(2), active, level, bare_key))

    def fields_at(i, first=False):
        if i in globals_: return []
        line = rows[i].strip()
        if first:
            m = marker.match(line)
            if m: line = m.group(3).strip()
        else:
            # Child headings bound structure but never supply inline fields.
            if heading.match(line): return []
        result = []
        for cell in review_field_cells(line):
            m = declaration.match(cell)
            if m: result.append((m.group(1).lower(), m.group(2)))
        return result

    issues = []; covered = set()
    for j, (i, ident, in_issues, level, bare_key) in enumerate(candidates):
        end = candidates[j + 1][0] if j + 1 < len(candidates) else len(rows)
        for k in range(i + 1, end):
            h = heading.match(rows[k])
            if k in globals_ or metadata[k] or (h and len(h.group(1)) <= level): end = k; break
        fields = [(k, label, value) for k in range(i, end) for label, value in fields_at(k, k == i)]
        explicit_ids = [(k, value.strip()) for k, label, value in fields if label == 'issue id']
        if explicit_ids:
            if len(explicit_ids) != 1:
                errors.append(f'CRITIC_RAW_ID_COUNT: issue at line {i + 1} has {len(explicit_ids)} explicit Issue ID fields')
            elif not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', explicit_ids[0][1]):
                errors.append(f'CRITIC_RAW_ID_VALUE: issue at line {i + 1} has an invalid or missing explicit Issue ID')
            else:
                declared = explicit_ids[0][1]
                if not ident.isdigit() and ident != declared:
                    errors.append(f'CRITIC_RAW_ID_CONFLICT: heading ID {ident} differs from explicit Issue ID {declared}')
                # A numeric list position may be an ordinal, not identity.
                # Preserve the declared stable ID; closure aliases must be
                # explicit rather than guessed from that ordinal or suffix.
                ident = declared
        if not in_issues and not fields: continue
        covered.update(range(i, end))
        labels = [(k, value) for k, label, value in fields if label == 'verdict']
        ambiguous = bare_key and not in_issues and labels and not any(label != 'verdict' for _, label, _ in fields)
        verdict = None
        if ambiguous:
            errors.append(f'CRITIC_RAW_AMBIGUOUS_SCOPE: issue/key {ident} at line {i + 1} has only Verdict outside Issues/Findings; declare Review metadata or an explicit issue container')
        if len(labels) > 1:
            errors.append(f'CRITIC_RAW_VERDICT_COUNT: issue {ident} has {len(labels)} verdict declarations; require exactly one when reviewing a disposition')
        elif labels and not ambiguous:
            k, value = labels[0]
            if not value.strip():
                # The previous parser supported a Verdict label and value on
                # separate lines. Only the next live nonblank value can supply it.
                for n in range(k + 1, end):
                    if rows[n].strip(): value = rows[n].strip(); break
            vd = re.fullmatch(r'NOT FIXED|FIXED', value.strip())
            if vd: verdict = vd.group(0)
        issues.append((ident, verdict))
    for i in range(len(rows)):
        fields = fields_at(i, first=bool(marker.match(rows[i]))) if metadata[i] else fields_at(i)
        if metadata[i] and fields:
            errors.append(f'CRITIC_RAW_AMBIGUOUS_SCOPE: line {i + 1} has issue control fields in Review metadata')
        elif i not in covered and fields and (in_container[i] or any(label == 'issue id' or (label == 'verdict' and value.strip() in ('FIXED', 'NOT FIXED', '')) for label, value in fields)):
            errors.append(f'CRITIC_RAW_UNASSIGNED_ISSUE_FIELDS: line {i + 1} has issue fields without a recognized stable ID')
    return issues

def found(excerpt, haystack_norm):
    e = norm(excerpt) if isinstance(excerpt, str) else ''
    return len(e) >= 10 and e in haystack_norm

def miss_hint(excerpt, haystack_norm):
    e = norm(excerpt); n = len(e)
    while n > 12 and e[:n] not in haystack_norm: n -= 1
    return f" (first {n} of {len(e)} chars match; check the text after: '{e[n:n + 30]}')" if n > 12 else ''

def page_coverage(page):
    """Fraction of the usable page height (header/footer bands excluded) covered by text, images or drawings."""
    H = page.rect.height; top, bot = H * 0.07, H * 0.93; iv = []
    for b in page.get_text('dict')['blocks']:
        x0, y0, x1, y1 = b['bbox']
        if b.get('type') == 0 and not ''.join(s['text'] for l in b.get('lines', []) for s in l['spans']).strip(): continue
        iv.append((y0, y1))
    try: iv += [(r.y0, r.y1) for r in (d['rect'] for d in page.get_drawings()) if r.height < H * 0.9]
    except Exception: pass
    iv = sorted((max(a, top), min(b, bot)) for a, b in iv if min(b, bot) > max(a, top))
    cov, cur = 0.0, None
    for a, b in iv:
        if cur and a <= cur[1] + 6: cur = (cur[0], max(cur[1], b))
        else:
            if cur: cov += cur[1] - cur[0]
            cur = (a, b)
    if cur: cov += cur[1] - cur[0]
    return cov / (bot - top)

def md_rows(text):
    rows, header = [], None
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith('|'):
            header = None; continue
        cells = [c.strip() for c in s.strip('|').split('|')]
        if all(re.fullmatch(r':?-{2,}:?', c) for c in cells if c): continue
        if header is None: header = [c.lower() for c in cells]; continue
        rows.append(dict(zip(header, cells)))
    return rows

def cls(v):
    v = v.lower()
    for k, out in [('observ', 'observed'), ('attach', 'attachment'), ('given', 'attachment'), ('provided', 'attachment'),
                   ('external', 'external'), ('estimat', 'estimated'), ('assum', 'assumed')]:
        if k in v: return out
    return 'unknown'

def sniff(p):
    b = p.read_bytes()[:512]
    low = b.lower()
    if b'<html' in low or b'<!doctype html' in low: return 'html'
    if b.startswith(b'%PDF'): return 'pdf'
    if b.startswith(b'PK'): return 'zip'          # xlsx/docx/zip
    if b.startswith(b'\xd0\xcf\x11\xe0'): return 'ole'  # xls
    if b.startswith(b'\x89PNG') or b.startswith(b'\xff\xd8'): return 'image'
    return 'text_or_other'

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('project'); ap.add_argument('--pdf', required=True); ap.add_argument('--output')
    ap.add_argument('--review-format', choices=['legacy', 'structured-v1'])
    a = ap.parse_args()
    root = Path(a.project).resolve(); fail, inc, warn, info = [], [], [], {}
    doc = None
    F = fail.append; I = inc.append; W = warn.append
    def finish():
        status = 'GATE_FAIL' if fail else 'GATE_INCOMPLETE' if inc else 'GATE_PASS'
        out = {'status': status, 'fail': fail, 'incomplete': inc, 'warn': warn, 'info': info,
               'not_checked': 'mathematical correctness, originality, source authenticity, actual reviewer independence, official award level; GATE_PASS establishes only registered evidence consistency'}
        txt = json.dumps(out, ensure_ascii=False, indent=2)
        if doc is not None: doc.close()
        if a.output: Path(a.output).write_text(txt + '\n', encoding='utf-8')
        print(txt)
        sys.exit(1 if fail else 2 if inc else 0)

    gp = root / 'artifacts/gate.json'
    try: g = json.loads(gp.read_text(encoding='utf-8'), object_pairs_hook=strict_pairs, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
    except Exception as e: g = {}; I(f'GATE_JSON_MISSING_OR_INVALID: {e}')
    if not isinstance(g, dict):
        F('GATE_JSON_NOT_OBJECT'); finish()
    declared_format = g.get('review_format')
    if declared_format not in (None, 'legacy', 'structured-v1'): F('REVIEW_FORMAT_INVALID')
    if a.review_format and declared_format and a.review_format != declared_format: F('REVIEW_FORMAT_CONFLICT')
    review_format = a.review_format or declared_format or ('structured-v1' if (root / 'artifacts/review/review_index.json').exists() else 'legacy')
    info['review_format'] = review_format
    if review_format == 'legacy': W('LEGACY_REVIEW_FORMAT: historical compatibility; not structured-v1 acceptance')
    rules = g.get('rules', {}); pdfm = g.get('pdf', {})
    if not isinstance(rules, dict) or not isinstance(pdfm, dict):
        F('GATE_RULES_OR_PDF_NOT_OBJECT'); finish()
    # Reject malformed collection structures before consumers iterate or hash IDs.
    # Missing content is diagnosed later as incomplete; an explicitly wrong JSON type is a failure.
    for group in ('requirements', 'validations', 'claims', 'attachments'):
        entries = g.get(group, [])
        if not isinstance(entries, list) or any(not isinstance(x, dict) for x in entries):
            F('GATE_COLLECTION_INVALID: ' + group + ' must be a list of objects')
            continue
        for i, entry in enumerate(entries):
            where = f'{group}[{i}]'
            for field in ('id', 'kind', 'type', 'no_independent_data_reason', 'path'):
                if field in entry and entry[field] is not None and not isinstance(entry[field], str):
                    F('GATE_FIELD_TYPE_INVALID: ' + where + '.' + field + ' must be text')
            for field in ('exhibits', 'validation_ids', 'used_in'):
                if field in entry and (not isinstance(entry[field], list) or any(not isinstance(x, str) for x in entry[field])):
                    F('GATE_FIELD_TYPE_INVALID: ' + where + '.' + field + ' must be a list of text')
            if 'failure_action' in entry and not isinstance(entry['failure_action'], dict):
                F('GATE_FIELD_TYPE_INVALID: ' + where + '.failure_action must be an object')
    if pdfm.get('short_page_reasons') is not None and not isinstance(pdfm['short_page_reasons'], dict):
        F('GATE_FIELD_TYPE_INVALID: pdf.short_page_reasons must be an object')
    if rules.get('excluded_from_cap') is not None and not isinstance(rules['excluded_from_cap'], list):
        F('GATE_FIELD_TYPE_INVALID: rules.excluded_from_cap must be a list')
    if fail: finish()

    # ---------- PDF ----------
    try:
        import pymupdf as fitz
    except ImportError:
        try: import fitz
        except ImportError:
            I('PYMUPDF_UNAVAILABLE'); finish()
    pdf = Path(a.pdf); pdf = pdf if pdf.is_absolute() else root / pdf
    if not pdf.is_file():
        I('PDF_MISSING: ' + str(pdf)); finish()
    try:
        doc = fitz.open(pdf)
        total = len(doc); pages = [p.get_text() for p in doc]
        if total == 0: raise ValueError('zero pages')
    except (OSError, RuntimeError, ValueError) as exc:
        F('PDF_UNREADABLE: ' + str(exc)); finish()
    npages = [norm(p) for p in pages]
    pdf_sha = hashlib.sha256(pdf.read_bytes()).hexdigest()
    def anchor(key, required=True):
        t = pdfm.get(key)
        if not isinstance(t, str) or len(t.strip()) < 15:
            if required: I(f'PDF_ANCHOR_MISSING: pdf.{key} (paste >=15 chars of exact text)')
            return None
        hits = [i + 1 for i, p in enumerate(npages) if norm(t) in p]
        if len(hits) != 1: I(f'PDF_ANCHOR_NOT_FOUND_OR_NOT_UNIQUE: pdf.{key} -> pages {hits}'); return None
        return hits[0]
    # main pages: declared value is checked against the AI-report anchor; never silently fall back to the total
    ai_auto = next((i + 1 for i, p in enumerate(npages) if re.search(r'Report on (the )?Use of AI', p[:200], re.I)), None)
    ai_pg = anchor('ai_report_first_text', required=False) or ai_auto
    declared = pdfm.get('main_pages'); main_ok = True
    if type(declared) is int and 1 <= declared <= total:
        main_n = declared
        if ai_pg is not None and ai_pg != main_n + 1: F(f'MAIN_PAGES_MISMATCH: pdf.main_pages={main_n} but the AI-use report starts on page {ai_pg} (expected {main_n + 1})')
        if ai_pg is None and total > main_n: F(f'AI_REPORT_NOT_FOUND: {total - main_n} pages after the main report but no "Report on Use of AI" heading')
    elif ai_pg is not None and ai_pg > 1:
        main_n = ai_pg - 1; W(f'MAIN_PAGES_AUTODETECTED: {main_n} (AI-use report starts on page {ai_pg}); set pdf.main_pages to confirm')
    else:
        main_n = total; main_ok = False
        I('PDF_MAIN_PAGES_UNKNOWN: set pdf.main_pages or start the AI-use report with "Report on Use of AI". Page-length checks were NOT run.')
    if g.get('rules', {}).get('ai_report_required', True) and ai_pg is None:
        I('AI_REPORT_REQUIRED_MISSING: this AI-assisted workflow needs an actual appended AI-use report; declaring all pages main is not an exemption')
    full = '\n'.join(pages[:main_n]); flat = norm(full)
    # year-aware page rules: pages excluded from the cap (e.g. references) are located by anchors
    cap = rules.get('max_main_pages'); target = rules.get('target_min_pages', 18)
    ry = rules.get('rules_year'); cy = str(rules.get('contest_cutoff_date', ''))[:4]
    if type(ry) is not int: I('RULES_YEAR_MISSING: set rules.rules_year = the contest year whose instructions you followed')
    elif cy.isdigit() and ry != int(cy): F(f'RULES_YEAR_MISMATCH: rules.rules_year={ry} but contest_cutoff_date is in {cy}; use that year\'s page rules')
    source_ok = policy_evidence_text(rules.get('rules_source'), 10)
    if not source_ok:
        I('RULES_SOURCE_MISSING: quote where the page rule comes from (problem statement / official instructions of that year)')
    # The AI anchor partitions report content; it does not authorize a page-cap
    # exemption. Unknown policy counts every submitted page conservatively.
    ai_exempt = False
    exemption = rules.get('ai_report_excluded_from_main_limit', False)
    if type(exemption) is not bool:
        F('AI_REPORT_EXEMPTION_FLAG_INVALID: rules.ai_report_excluded_from_main_limit must be a JSON boolean')
    elif exemption:
        quote = rules.get('ai_report_exclusion_rule_quote')
        if not policy_evidence_text(quote, 15):
            F('AI_REPORT_EXEMPTION_WITHOUT_RULE: quote the target-year official sentence excluding the AI-use report in rules.ai_report_exclusion_rule_quote')
        elif type(ry) is not int or not cy.isdigit() or ry != int(cy) or not source_ok:
            I('AI_REPORT_EXEMPTION_YEAR_UNVERIFIED: require target-year rules_year, matching contest_cutoff_date, and rules_source before excluding AI pages')
        else:
            ai_exempt = True
    excluded = set()
    for ex in rules.get('excluded_from_cap', []) or []:
        nm = ex.get('name', '?')
        if not policy_evidence_text(ex.get('rule_quote'), 15):
            F(f'EXCLUDED_FROM_CAP_WITHOUT_RULE: {nm}: quote the sentence of that year\'s rules that excludes it (rule_quote)'); continue
        def where(key):
            t = ex.get(key)
            if not isinstance(t, str) or len(t.strip()) < 10: return None
            return [i + 1 for i, p in enumerate(npages[:main_n]) if norm(t) in p]
        a0 = where('first_text')
        if not a0 or len(a0) != 1: I(f'EXCLUDED_SECTION_ANCHOR: {nm} first_text found on pages {a0} (need exactly one)'); continue
        if ex.get('last_text'):
            a1 = where('last_text')
            if not a1 or len(a1) != 1: I(f'EXCLUDED_SECTION_ANCHOR: {nm} last_text found on pages {a1} (need exactly one)'); continue
            end = a1[0]
        elif ex.get('to_end') is True: end = main_n
        else: I(f'EXCLUDED_SECTION_END: {nm}: give last_text, or "to_end": true if the section runs to the end of the main report'); continue
        if end < a0[0]: F(f'EXCLUDED_SECTION_REVERSED: {nm} ends (p{end}) before it starts (p{a0[0]})'); continue
        excluded |= set(range(a0[0], end + 1))
    report_counted = main_n - len(excluded)
    counted = (main_n if ai_exempt else total) - len(excluded)
    info['pdf'] = {'total_pages': total, 'main_pages': main_n, 'ai_report_pages': total - main_n,
                   'ai_report_excluded_from_main_limit': ai_exempt,
                   'page_cap_basis': 'main_report_excluding_ai' if ai_exempt else 'all_submitted_pages',
                   'excluded_from_cap': sorted(excluded), 'main_report_counted_pages': report_counted,
                   'counted_pages': counted, 'sha256': pdf_sha}
    if type(cap) is not int: I('RULES_MAX_MAIN_PAGES_UNKNOWN (read the target-year official instructions)')
    elif main_ok and counted > cap: F(f'PAGE_CAP_EXCEEDED: {counted} counted pages > {cap}')
    critic_raw_txt = (root / 'artifacts/review/critic.md').read_text(encoding='utf-8') if (root / 'artifacts/review/critic.md').exists() else ''
    closure_scope_errors = []
    # Every closure field uses the same live Markdown scope as raw verdicts.
    # Comments, examples and quoted instructions supply no closure authority.
    critic_txt = '\n'.join(review_live_rows(critic_raw_txt, closure_scope_errors))
    short_ok = re.search(r'^SHORT_EXCEPTION_APPROVED:\s*\S.{20,}', critic_txt, re.M)
    if main_ok and report_counted < target:
        if short_ok: W(f'BELOW_TARGET_WITH_CRITIC_EXCEPTION: {report_counted} < {target}')
        else: W(f'BELOW_INTERNAL_TARGET: {report_counted} counted main-report pages < {target}. Review substantive task coverage; page count alone does not establish quality. Never pad.')
    s_end = anchor('summary_last_text')
    if s_end is not None and s_end != 1: F(f'SUMMARY_SPILLS_TO_PAGE_{s_end}: the Summary Sheet must fit on page 1 at >=12 pt (cut words, do not shrink font)')
    small = [i + 1 for i, p in enumerate(doc) if any(s['size'] < 11.9 and s['text'].strip()
             for b in p.get_text('dict')['blocks'] if 'lines' in b for l in b['lines'] for s in l['spans'])]
    if small: W(f'TEXT_BELOW_12PT_ON_PAGES {small} (body text and summary must be >=12 pt; check captions/tables against current rules)')
    # half-empty pages, images included (a big figure pushed to the next page leaves a half-blank page)
    allowed = {str(k): v for k, v in (pdfm.get('short_page_reasons') or {}).items() if isinstance(v, str) and len(v.strip()) >= 10}
    cov = {i + 1: round(page_coverage(doc[i]), 2) for i in range(1, main_n)} if main_ok else {}
    half = [pg for pg, c in cov.items() if c < 0.6]
    unexcused = [pg for pg in half if str(pg) not in allowed and pg not in excluded]
    info['pdf']['half_empty_pages'] = {pg: cov[pg] for pg in half}
    if [pg for pg in half if str(pg) in allowed]: W(f'EXCUSED_SHORT_PAGES {[pg for pg in half if str(pg) in allowed]}: reasons given in pdf.short_page_reasons (reviewer: check them)')
    if len(unexcused) >= 3: W(f'HALF_EMPTY_PAGES {unexcused}: content covers <60% of the page height (figures/tables included). Fix layout (smaller figures, float text) or justify each page in pdf.short_page_reasons.')
    elif unexcused: W(f'HALF_EMPTY_PAGES {unexcused}: content covers <60% of the page height; check layout or add pdf.short_page_reasons')
    s1 = pages[0] if pages else ''
    nums = len(re.findall(r'(?<![A-Za-z])\d+(?:[.,]\d+)?\s*(?:%|[A-Za-z$]+)?', s1))
    info['summary'] = {'words': len(re.findall(r'[A-Za-z]{2,}', s1)), 'number_tokens': nums}
    if not re.search(r'valid|back-?test|hold-?out|out-of-sample|hindcast|cross-?valid|verif', s1, re.I):
        W('SUMMARY_NO_VALIDATION_STATEMENT: say what was checked and the outcome (including failures)')

    # ---------- requirements ----------
    reqs = g.get('requirements', [])
    if not reqs: I('NO_REQUIREMENTS: list every sub-question / deliverable of the problem statement')
    for r in reqs:
        rid = r.get('id', '?')
        if 'status' in r and r['status'] != 'ANSWERED':
            I(f'REQUIREMENT_INCOMPLETE: {rid} is explicitly {r["status"]!r}; a fixed review issue does not answer a required task')
        for k in ('result_excerpt', 'interpretation_excerpt'):
            t = r.get(k)
            if not isinstance(t, str) or len(t.strip()) < 15: I(f'REQ {rid}: missing {k}')
            elif not found(t, flat): F(f'REQ {rid}: {k} not found in the main report' + miss_hint(t, flat))
        if r.get('quantitative', True):
            if not re.search(r'\d', str(r.get('result_excerpt', ''))): F(f'REQ {rid}: quantitative deliverable but result_excerpt has no number')
        if not r.get('exhibits') and not r.get('exhibit_not_applicable_reason'): I(f'REQ {rid}: no figure/table listed and no reason')
        for ex in r.get('exhibits', []):
            m = re.match(r'(Figure|Fig\.|Table)\s*(\d+)', str(ex))
            if m and not re.search(r'\b%s\s*%s\b' % (re.escape(m.group(1)), m.group(2)), full): F(f'REQ {rid}: {ex} not found in the main report')
    info['exhibits'] = {'figures': len(set(re.findall(r'\b(?:Figure|Fig\.)\s*(\d+)', full))),
                        'tables': len(set(re.findall(r'\bTable\s*(\d+)', full)))}

    # ---------- validations ----------
    for group in ('requirements', 'validations', 'claims'):
        ids = [x.get('id') for x in g.get(group, [])]
        if any(not isinstance(x, str) or not x.strip() for x in ids): I(f'INVALID_IDS: {group} requires nonempty string IDs')
        if len(ids) != len(set(map(str, ids))): F(f'DUPLICATE_IDS: {group}')
    vals = {v.get('id', f'v{i}'): v for i, v in enumerate(g.get('validations', []))}
    if not vals: I('NO_VALIDATIONS registered')
    indep_pass_or_fail = set(); validation_sources = []
    for vid, v in vals.items():
        k = v.get('kind')
        if k not in VAL_KINDS: I(f'VAL {vid}: kind must be one of {sorted(VAL_KINDS)}'); continue
        if v.get('outcome') not in ('pass', 'fail', 'mixed'): I(f'VAL {vid}: outcome must be pass/fail/mixed')
        ex = v.get('paper_excerpt')
        if not isinstance(ex, str) or len(ex.strip()) < 15: I(f'VAL {vid}: missing paper_excerpt')
        elif not found(ex, flat): F(f'VAL {vid}: paper_excerpt not found in the main report' + miss_hint(ex, flat))
        if k in ('external_holdout', 'development_holdout', 'external_check'):
            for f in ('data_source', 'metric', 'model_value', 'baseline_name', 'baseline_value'):
                if v.get(f) in (None, ''): I(f'VAL {vid}: missing {f} (compare against a naive baseline)')
            if v.get('pre_cutoff') is not True: F(f'VAL {vid}: test data not confirmed pre-cutoff (pre_cutoff must be true)')
            mv, bv, d = v.get('model_value'), v.get('baseline_value'), v.get('metric_direction')
            num = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool) and x == x and abs(x) != float('inf')
            if d not in ('lower_is_better', 'higher_is_better'): I(f'VAL {vid}: set metric_direction = lower_is_better | higher_is_better')
            if mv not in (None, '') and bv not in (None, '') and not (num(mv) and num(bv)):
                I(f'VAL {vid}: model_value and baseline_value must be finite numbers (got {mv!r}, {bv!r})')
            elif num(mv) and num(bv) and d in ('lower_is_better', 'higher_is_better'):
                if (mv > bv) if d == 'lower_is_better' else (mv < bv):
                    said = found(v.get('baseline_loss_excerpt'), flat)
                    W(f'MODEL_LOSES_TO_BASELINE: VAL {vid} model {mv} vs {bv} ({v.get("baseline_name", "baseline")}, {d})'
                      + ('; the paper states it' if said else '; the paper must say so (add baseline_loss_excerpt)'))
                    if not said: F(f'BASELINE_LOSS_UNDISCLOSED: VAL {vid}: model loses to baseline but no matching disclosure in the paper')
            validation_sources.append((vid, k, v))
        if k == 'external_holdout':
            if v.get('planned_before_results') is not True: I(f'VAL {vid}: planned_before_results must be true for an external hold-out')
            if v.get('used_for_model_selection') is not False:
                F(f'VAL {vid}: hold-out was used to choose/tune the model -> relabel kind=development_holdout, or test on fresh data')
            else: indep_pass_or_fail.add(vid)
        if k == 'external_check':
            if v.get('planned_before_results') is not True: I(f'VAL {vid}: external_check requires planned_before_results=true; otherwise relabel development_holdout')
            if v.get('used_for_model_selection') is not False:
                F(f'VAL {vid}: external_check was used to choose/tune the model; changing its kind does not restore independence')
            elif v.get('planned_before_results') is True: indep_pass_or_fail.add(vid)
        if v.get('outcome') in ('fail', 'mixed'):
            act = v.get('failure_action', {})
            if act.get('kind') not in ('repair', 'restrict_scope', 'withdraw'):
                F(f'VAL {vid}: failed test has no disposition (repair / restrict_scope / withdraw the claim)')
            elif not isinstance(act.get('paper_excerpt'), str) or not found(act['paper_excerpt'], flat):
                F(f'VAL {vid}: failure disposition is not stated in the paper')
    claims = g.get('claims', [])
    if not claims: I('NO_CLAIMS: list the 3-6 headline claims made in the Summary')
    for c in claims:
        cid = c.get('id', '?'); t = c.get('type')
        if t not in CLAIM_TYPES: I(f'CLAIM {cid}: type must be one of {sorted(CLAIM_TYPES)}'); continue
        ex = c.get('summary_excerpt')
        if not isinstance(ex, str) or not found(ex, norm(s1)): F(f'CLAIM {cid}: summary_excerpt not found on page 1' + (miss_hint(ex, norm(s1)) if isinstance(ex, str) else ''))
        unknown = [x for x in c.get('validation_ids', []) if x not in vals]
        if unknown: F(f'CLAIM {cid}: unknown validation IDs {unknown}')
        tied = [x for x in c.get('validation_ids', []) if x in vals]
        if not tied: I(f'CLAIM {cid}: no validation linked (choose a check that could refute it)')
        withdrawn = [x for x in tied if vals[x].get('outcome') in ('fail', 'mixed') and vals[x].get('failure_action', {}).get('kind') == 'withdraw']
        if withdrawn:
            if c.get('status') != 'withdrawn' or not found(c.get('withdrawal_excerpt'), norm(s1)):
                F(f'WITHDRAWN_VALIDATION_SUPPORTS_ACTIVE_CLAIM: {cid}; remove the unsupported headline claim or explicitly withdraw it in the Summary')
        if t in ('prediction', 'empirical_effect') and not set(tied) & indep_pass_or_fail:
            if c.get('no_independent_data_reason'):
                if not found(c.get('unvalidated_excerpt'), flat): I(f'CLAIM {cid}: provide unvalidated_excerpt explicitly limiting the empirical claim in the main report')
                W(f'CLAIM {cid}: empirical claim without independent real-data test ({c["no_independent_data_reason"][:80]}); the paper must label it unvalidated')
            else: F(f'CLAIM {cid}: prediction/empirical claim has no untouched real-data test and no stated reason')
    if not indep_pass_or_fail:
        W('NO_INDEPENDENT_REAL_DATA_TEST: in the forward test, papers with a real pre-cutoff check beat those without. Look for a proxy outcome, a sub-component, or an analogous historical case before giving up.')

    # ---------- attachments ----------
    for at in g.get('attachments', []):
        aid = at.get('id', '?'); p = at.get('path')
        if p:
            fp = (root / p) if not Path(p).is_absolute() else Path(p)
            if not fp.exists(): F(f'ATTACHMENT {aid}: file not found {p}')
            else:
                kind = sniff(fp); info.setdefault('attachments', {})[aid] = kind
                if kind == 'html' and not str(p).lower().endswith(('.html', '.htm')): F(f'ATTACHMENT {aid}: file is an HTML page (failed download?), not real data')
        if not at.get('used_in') and not at.get('not_applicable_reason'): I(f'ATTACHMENT {aid}: say which requirement uses it, or why it is not needed')
        if at.get('used_in') and not at.get('conversion_notes'): I(f'ATTACHMENT {aid}: document how it was converted into model input')

    # ---------- source log ----------
    sl = root / 'data/source_log.md'
    if not sl.exists(): I('SOURCE_LOG_MISSING: data/source_log.md')
    else:
        rows = md_rows(sl.read_text(encoding='utf-8'))
        ck = next((k for k in (rows[0] if rows else {}) if k in ('class', 'type', 'category', 'kind')), None)
        uk = next((k for k in (rows[0] if rows else {}) if k in ('use', 'uses', 'used for', 'role')), None)
        if ck is None: I('SOURCE_LOG_NO_CLASS_COLUMN')
        cl = [cls(r.get(ck, '')) for r in rows] if ck else []
        info['source_log'] = {'rows': len(rows), **{k: cl.count(k) for k in set(cl)}}
        if cl.count('unknown'): W(f'SOURCE_LOG: {cl.count("unknown")} rows without a recognised class')
        for r in rows:
            line = ' '.join(r.values()).lower()
            use = r.get(uk, '').lower() if uk else line
            if 'post-contest' in line and re.search(r'calibrat|validat|input', use):
                F(f'SOURCE_LOG: post-contest source used for model input/calibration/validation: {line[:90]}')
            if 'from memory' in line and 'not used' not in line: W(f'SOURCE_LOG: value from memory: {line[:90]}')
            if ck and cls(r.get(ck, '')) in ('assumed', 'estimated') and not re.search(r'range|\d\s*[-–~]\s*\d|±|x\s*\d|\bto\b', line):
                I(f'SOURCE_LOG: assumption without a range for sensitivity: {line[:90]}')

        if validation_sources and uk is None: I('SOURCE_LOG_NO_USE_COLUMN: add a Use column (input/calibration/validation/context)')
        source_rows = {}
        for row in rows:
            sid = row.get('id', '').strip()
            if sid:
                if sid in source_rows: F(f'SOURCE_ID_DUPLICATE: {sid}')
                source_rows[sid] = row
        for vid, k, v in validation_sources:
            source_ids = v.get('source_ids')
            if not isinstance(source_ids, list) or not source_ids or any(not isinstance(x, str) or not x.strip() for x in source_ids):
                I(f'VAL {vid}: source_ids must list the exact ID column values in source_log; text overlap cannot establish dataset identity')
                continue
            if len(source_ids) != len(set(source_ids)): F(f'VAL {vid}: duplicate source_ids')
            unknown_ids = [x for x in source_ids if x not in source_rows]
            if unknown_ids: F(f'VAL {vid}: unknown source_ids {unknown_ids}'); continue
            expected_names = [source_rows[x].get('dataset', '').strip() for x in source_ids]
            if any(not x for x in expected_names): I(f'VAL {vid}: each source ID needs a nonempty Dataset column')
            actual_names = v.get('data_source', [])
            actual_names = [actual_names] if isinstance(actual_names, str) else actual_names
            if not isinstance(actual_names, list) or any(not isinstance(x, str) for x in actual_names):
                I(f'VAL {vid}: data_source must be a dataset name or list of names')
            elif sorted(norm(x).casefold() for x in actual_names) != sorted(norm(x).casefold() for x in expected_names):
                F(f'VALIDATION_DATASET_MISMATCH: VAL {vid}: data_source differs from the Dataset names of source_ids {source_ids}')
            for sid in source_ids:
                row=source_rows[sid]; use=norm(row.get(uk, '')).lower() if uk else ''
                if use not in (('validation','calibration') if k == 'development_holdout' else ('validation',)):
                    F(f'VAL {vid}: source_id {sid} has inappropriate Use {use!r}')
                if k in INDEPENDENT and ck and cls(row.get(ck, '')) == 'assumed':
                    F(f'INDEPENDENT_SOURCE_IS_ASSUMED: VAL {vid} source_id {sid}')
        STOP = {'data', 'from', 'with', 'hourly', 'daily', 'table', 'file', 'public', 'report', 'source'}
        for vid, k, v in validation_sources:
            keys = v.get('source_log_match'); keys = [keys] if isinstance(keys, str) else keys
            if not isinstance(keys, list) or not keys or any(not isinstance(x, str) or len(x.strip()) < 8 for x in keys):
                I(f'VAL {vid}: set source_log_match = a >=8-char phrase (or a list, one per dataset) from the source_log row(s) for its data ({str(v.get("data_source", ""))[:50]})'); continue
            rows_hit = []
            for key in keys:
                k_n = norm(key.replace('|', ' ')).lower()
                hit = [r for r in rows if k_n in norm(' '.join(r.values())).lower()]
                if not hit: F(f'VAL {vid}: no data/source_log.md row matches source_log_match "{key[:50]}" (log every validation data source)'); continue
                if len(hit) > 1: I(f'VAL {vid}: source_log_match "{key[:40]}" matches {len(hit)} rows; make it identify one dataset'); continue
                r = hit[0]; rows_hit.append(r)
                if k in INDEPENDENT and ck and cls(r.get(ck, '')) == 'assumed':
                    F(f'INDEPENDENT_SOURCE_IS_ASSUMED: VAL {vid} uses assumed data as independent real-data evidence')
                elif k in INDEPENDENT and ck and cls(r.get(ck, '')) == 'unknown':
                    I(f'INDEPENDENT_SOURCE_CLASS_UNKNOWN: VAL {vid}')
                use = norm(r.get(uk, '')).lower() if uk else ''
                ok_use = ('validation', 'calibration') if k == 'development_holdout' else ('validation',)
                if uk and use not in ok_use:
                    F(f'VAL {vid}: its source_log row has Use "{r.get(uk, "")[:30]}", expected {" or ".join(ok_use)}')
            toks = {t for t in re.findall(r'[a-z0-9]{4,}', norm(str(v.get('data_source', ''))).lower()) if t not in STOP}
            if rows_hit and toks and not any(t in norm(' '.join(r.values())).lower() for r in rows_hit for t in toks):
                I(f'VAL {vid}: data_source "{str(v.get("data_source"))[:50]}" shares no word with its source_log row(s); check the match')

    # A separately registered task contract cannot be silently superseded
    # by result excerpts in gate.json. Legacy projects without it remain
    # supported; this checks declared status, not natural-language truth.
    contract_path = root / 'artifacts/problem_contract.json'
    if contract_path.exists():
        try:
            contract = json.loads(contract_path.read_text(encoding='utf-8'))
            if not isinstance(contract, dict) or not isinstance(contract.get('requirements', []), list):
                raise ValueError('requirements must be a list')
            for requirement in contract.get('requirements', []):
                if not isinstance(requirement, dict) or requirement.get('status') != 'ANSWERED':
                    ident = requirement.get('id', '?') if isinstance(requirement, dict) else '?'
                    I(f'REQUIREMENT_INCOMPLETE: problem_contract {ident} has no ANSWERED status')
        except (ValueError, TypeError):
            I('REQUIREMENT_CONTRACT_UNVERIFIED: problem_contract.json is not a valid registered contract')

    # ---------- ideation ----------
    ip = root / 'artifacts/independent_ideas.md'
    if not ip.exists(): I('IDEAS_MISSING: artifacts/independent_ideas.md (baseline + >=3 candidates, written before reading solutions)')
    else:
        it = ip.read_text(encoding='utf-8')
        cands = [l for l in re.findall(r'^\s*\d+[.)]\s*(.*)$', it, re.M) if len(l.strip()) >= 10]
        natural = re.search(r'^Single natural structure reason:\s*(.{30,})$', it, re.M)
        if len(cands) < 3 and not natural: I(f'IDEAS: {len(cands)} filled candidates (need >= 3 or a substantive Single natural structure reason)')
        m = re.search(r'^[#>*\s-]*Chosen[^:\n]*:(.*)', it, re.I | re.M | re.S)   # first colon on the Chosen line, then the rest
        rest = m.group(1).lstrip(' \t') if m else ''
        rest = rest[1:] if rest.startswith('\n') else rest          # content may start on the next line, but not after a blank line
        body = '' if re.match(r'\s*\n', rest) else re.split(r'\n\s*\n|\n\s*#', rest)[0].strip()
        if len(re.sub(r'[^A-Za-z0-9]', '', body)) < 15: I('IDEAS: chosen core contribution and reason missing')

    # ---------- critic ----------
    if review_format == 'structured-v1':
        from check_reviews import verify
        reviewed = verify(root, pdf, reqs)
        for message in reviewed['errors']: F('STRUCTURED_REVIEW: ' + message)
        for message in reviewed['incomplete']: I('STRUCTURED_REVIEW: ' + message)
        info['critic'] = reviewed
    elif not critic_txt: I('CRITIC_MISSING: artifacts/review/critic.md (independent critic pass is mandatory)')
    else:
        closure_errors = list(closure_scope_errors)
        closure_review_verdict = parse_review_verdict(critic_txt, closure_errors)
        for message in dict.fromkeys(closure_errors): F(f'CRITIC_CLOSURE: {message}')
        if closure_review_verdict == 'NOT FIXED': F('CRITIC_CLOSURE_REVIEW_NOT_FIXED: the live closure reports an overall unresolved review')
        if closure_review_verdict is None and any(review_verdict_fields(row) for row in critic_txt.splitlines()):
            I('CRITIC_CLOSURE_REVIEW_UNRECOGNIZED: use one complete live overall verdict value')
        issues = re.findall(r'^#{0,4}\s*\d+[.)]\s+\S', critic_txt, re.M)
        st = re.findall(r'^\s*Status:\s*(FIXED_UNREVIEWED|FIXED|WONTFIX|OPEN)\b([^\n]*)', critic_txt, re.M)
        statuses = [x[0] for x in st]
        if not statuses and closure_review_verdict != 'NO_BLOCKING_ISSUES': I('CRITIC: list actual issues with Status lines or an evidenced Review verdict: NO_BLOCKING_ISSUES; do not invent issues')
        if len(statuses) < len(issues): I(f'CRITIC: {len(issues)} issues but only {len(statuses)} Status lines (close every issue)')
        if not re.search(r'^Critic:\s*\S+', critic_txt, re.M): I('CRITIC: add a "Critic: <who / which fresh context>" line (the author cannot be the only reviewer)')
        if re.search(r'Status:\s*WONTFIX\s*$', critic_txt, re.M): F('CRITIC: WONTFIX without a reason')
        if 'OPEN' in statuses: F('CRITIC: issues still OPEN')
        if re.search(r'Severity:\s*high[^\n]*\n(?:(?!Status:).*\n){0,6}Status:\s*WONTFIX\s*$', critic_txt, re.I | re.M):
            F('CRITIC: a high-severity issue closed as WONTFIX without a reason')
        # rounds: "Round: 2 | critic: <name> | fresh_session: yes | pdf_sha256: <hex> | raw: <path>"
        rounds = {}
        for m in re.finditer(r'^Round:\s*(\d+)\s*\|(.*)$', critic_txt, re.M):
            kv = dict((a.strip().lower(), b.strip()) for a, b in (x.split(':', 1) for x in m.group(2).split('|') if ':' in x))
            if int(m.group(1)) in rounds: F(f'CRITIC_ROUND_{m.group(1)}: duplicate Round line')
            rounds[int(m.group(1))] = kv
        if not rounds: I('CRITIC_ROUNDS_MISSING: add one "Round: N | critic: ... | fresh_session: yes | pdf_sha256: ... | raw: ..." line per critic round')
        # Round-local aliases are declarations, not guesses from an ID suffix.
        aliases = {}; alias_targets = {}
        alias_txt = markdown_live_text(critic_txt)
        for m in re.finditer(r'^Issue alias:\s*round\s+(\d+)\s*\|\s*raw_id:\s*(\S+)\s*\|\s*issue:\s*(\d+)\s*$', alias_txt, re.M):
            rn, rid, cid = int(m.group(1)), m.group(2), m.group(3)
            if (rn, rid) in aliases or (rn, cid) in alias_targets:
                F(f'CRITIC_ALIAS_DUPLICATE: round {rn}, raw_id {rid}, issue {cid}')
            if rid.isdigit() and rid != cid: F(f'CRITIC_ALIAS_NUMERIC_REMAP: {rid} -> {cid}')
            if rn not in rounds: F(f'CRITIC_ALIAS_UNKNOWN_ROUND: {rn}')
            aliases[rn, rid] = cid; alias_targets[rn, cid] = rid
        used_aliases = set()
        raw, verdicts, raw_issues = {}, {}, set()
        round_verdicts = {}; review_verdicts = {}; opaque_targets = {}; canonical_opaque_ids = {}; raw_context_metadata = {}
        for n in sorted(rounds):
            kv = rounds[n]; rp = root / kv.get('raw', '#none#')
            if not kv.get('raw') or not rp.is_file() or rp.stat().st_size < 90: F(f'CRITIC_ROUND_{n}: raw critic output missing or empty ({kv.get("raw")})'); continue
            raw[n] = rp.read_text(encoding='utf-8', errors='replace')
            metadata_values = {}
            for row in review_live_rows(raw[n]):
                for cell in review_field_cells(row):
                    field = re.fullmatch(r'(fresh_session|inherited_parent_context)\s*:\s*(.*)', cell, re.I)
                    if field: metadata_values.setdefault(field.group(1).lower(), []).append(field.group(2).strip().lower())
            raw_context_metadata[n] = metadata_values
            for field, values in metadata_values.items():
                if len(values) != 1 or values[0] not in ('yes','no','true','false'):
                    I(f'CRITIC_RAW_CONTEXT_UNVERIFIED: round {n} has ambiguous {field} declarations')
                elif (field == 'fresh_session' and values[0] in ('no','false')) or (field == 'inherited_parent_context' and values[0] in ('yes','true')):
                    F(f'CRITIC_RAW_CONTEXT_CONTRADICTION: round {n} raw declares {field}: {values[0]}')
            if kv.get('fresh_session', '').lower() not in ('yes', 'true'): F(f'CRITIC_ROUND_{n}: fresh_session must be yes (a new session that saw only the problem, attachments and PDF)')
            hdr = re.search(r'^\s*pdf_sha256:\s*([0-9a-fA-F]{64})\s*$', '\n'.join(raw[n].splitlines()[:5]), re.M)
            if not hdr: F(f'CRITIC_ROUND_{n}: raw output must start with the line "pdf_sha256: <hex>" written by the critic (SHA_NOT_IN_RAW)')
            elif hdr.group(1).lower() != kv.get('pdf_sha256', '').lower(): F(f'CRITIC_ROUND_{n}: pdf_sha256 in critic.md differs from the one in the raw output')
            round_verdicts[n] = {}; raw_seen = set(); canonical_seen = set()
            parse_errors = []
            parsed_issues = parse_raw_issues(raw[n], parse_errors)
            review_verdicts[n] = parse_review_verdict(raw[n], parse_errors)
            for message in dict.fromkeys(parse_errors): F(f'CRITIC_ROUND_{n}: {message}')
            for rid, vd in parsed_issues:
                if rid in raw_seen: F(f'CRITIC_RAW_DUPLICATE_ISSUE: round {n} repeats issue {rid}; one issue/verdict per round')
                raw_seen.add(rid)
                num_ = aliases.get((n, rid), rid)
                if not rid.isdigit():
                    if rid in opaque_targets and opaque_targets[rid] != num_:
                        F(f'CRITIC_ALIAS_CROSS_ROUND_RETARGET: stable ID {rid} maps to different closure issues')
                    opaque_targets[rid] = num_
                    canonical_opaque_ids.setdefault(num_, set()).add(rid)
                if (n, rid) in aliases: used_aliases.add((n, rid))
                if num_ in canonical_seen:
                    F(f'CRITIC_RAW_DUPLICATE_ISSUE: round {n} aliases collide at issue {num_}')
                canonical_seen.add(num_)
                raw_issues.add(num_)
                if vd: round_verdicts[n][num_] = vd; verdicts[num_] = (n, vd)
        for key in set(aliases) - used_aliases:
            F(f'CRITIC_ALIAS_UNKNOWN_RAW_ID: round {key[0]} raw_id {key[1]}')
        for num_, stable_ids in canonical_opaque_ids.items():
            if len(stable_ids) > 1:
                F(f'CRITIC_ALIAS_CROSS_ROUND_ID_REPLACEMENT: closure issue {num_} merges distinct stable IDs {sorted(stable_ids)}; retain the original stable ID in independent rechecks')
        if rounds:
            last = max(rounds); kv = rounds[last]
            if review_verdicts.get(last) == 'NOT FIXED':
                F(f'CRITIC_FINAL_REVIEW_NOT_FIXED: final round {last} reports an overall unresolved review')
            if last in raw and review_verdicts.get(last) is None:
                live = review_live_rows(raw[last])
                if any(review_verdict_fields(row) for row in live):
                    I(f'CRITIC_FINAL_REVIEW_UNRECOGNIZED: final round {last} has no recognized complete overall verdict')
            if kv.get('pdf_sha256', '').lower() != pdf_sha:
                F(f'FINAL_CRITIC_ROUND_NOT_ON_FINAL_PDF: round {last} reviewed sha256 {kv.get("pdf_sha256", "?")[:12]}..., final PDF is {pdf_sha[:12]}... Run a fresh critic session on the final PDF.')
        blocks = re.split(r'(?m)^(?=#{0,4}\s*\d+[.)]\s)', critic_txt)
        nums, unrev, contra = [], [], []
        orphan = len(re.findall(r'(?m)^\s*Status:', blocks[0])) if blocks else 0
        for b in blocks:
            mnum = re.match(r'#{0,4}\s*(\d+)[.)]\s', b)
            if not mnum: continue
            num = mnum.group(1); nums.append(num)
            nstatus = len(re.findall(r'^\s*Status:', b, re.M))
            if nstatus != 1: F(f'CRITIC_ISSUE_STATUS_COUNT: issue {num} has {nstatus} status lines; require exactly one')
            ms = re.search(r'^\s*Status:\s*(FIXED_UNREVIEWED|FIXED)\b([^\n]*)', b, re.M)
            severity = re.search(r'Severity:\s*(high|medium|low)\b', b, re.I)
            if not severity: I(f'CRITIC_ISSUE_{num}: missing Severity: high/medium/low')
            wont = re.search(r'^\s*Status:\s*WONTFIX\b', b, re.M)
            if wont and severity and severity.group(1).lower() == 'high': F(f'CRITIC_HIGH_WONTFIX: issue {num}; repair, restrict or withdraw the claim and obtain a final-PDF FIXED verdict')
            if wont and rounds and round_verdicts.get(max(rounds), {}).get(num) != 'FIXED': I(f'CRITIC_WONTFIX_UNVERIFIED: issue {num} needs a final-PDF verdict accepting its limited disposition')
            if not ms: continue
            if rounds and round_verdicts.get(max(rounds), {}).get(num) != 'FIXED': I(f'CRITIC_FINAL_ISSUE_UNVERIFIED: issue {num} has no FIXED verdict on the final PDF')
            if ms.group(1) == 'FIXED_UNREVIEWED': unrev.append(num); continue
            mv = re.search(r'verified round\s*(\d+)', ms.group(2), re.I); vd = verdicts.get(num)
            if not mv or not vd: unrev.append(num)
            elif vd[1] == 'NOT FIXED': contra.append(f'{num} (latest verdict: round {vd[0]})')
            elif round_verdicts.get(int(mv.group(1)), {}).get(num) != 'FIXED': unrev.append(num)
        if orphan: F(f'CRITIC: {orphan} Status lines are not under a numbered issue ("N. ..."); number every issue')
        dup = sorted({x for x in nums if nums.count(x) > 1}, key=int)
        if dup: F(f'CRITIC: duplicate issue numbers {dup}')
        missing = sorted(raw_issues - set(nums), key=lambda x: (not x.isdigit(), int(x) if x.isdigit() else x))
        if missing: F(f'CRITIC_RAW_ISSUES_NOT_CLOSED: issues {missing} raised in critic raw output have no block in critic.md')
        if contra: F(f'CRITIC_CONTRADICTION: Status FIXED but the latest critic verdict is NOT FIXED for issues {contra}')
        if unrev: I(f'FIXED_UNREVIEWED: issues {unrev} are closed without a critic re-review verdict (cite "verified round K" whose raw output says Verdict: FIXED)')
        if not statuses and rounds:
            if review_verdicts.get(max(rounds)) != 'NO_BLOCKING_ISSUES': I('CRITIC_NO_ISSUE_VERDICT_NOT_IN_RAW: final critic must explicitly report NO_BLOCKING_ISSUES')
        info['critic'] = {'issues': len(issues), 'statuses': {x: statuses.count(x) for x in set(statuses)}, 'rounds': sorted(rounds), 'unreviewed': unrev,
                          'closure_review_verdict': closure_review_verdict, 'raw_review_verdicts': review_verdicts}
        info['critic']['raw_context_metadata'] = raw_context_metadata

    finish()

if __name__ == '__main__': main()
