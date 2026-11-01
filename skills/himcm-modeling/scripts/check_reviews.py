#!/usr/bin/env python3
"""Verify bound review declarations; does not certify scientific truth or independence."""
import argparse
import hashlib
import re
from pathlib import Path
import sys
sys.dont_write_bytecode = True
from _exact_io import keys, read, emit


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text(value, minimum=1):
    require(isinstance(value, str) and len(value.strip()) >= minimum, 'TEXT_MISSING_OR_INVALID')
    return value


def identifier(value):
    require(isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', value), 'INVALID_STABLE_ID')
    return value


def distinct(values, label):
    require(isinstance(values, list), label + ': expected list')
    require(all(isinstance(x, str) for x in values) and len(set(values)) == len(values), label + ': duplicate/invalid value')
    return set(values)


def bound(root, binding):
    keys(binding, ['path', 'sha256'])
    relative = text(binding['path'])
    path = (root / relative).resolve()
    require(not Path(relative).is_absolute() and '..' not in Path(relative).parts
            and path.is_relative_to(root), 'PATH_OUTSIDE_PROJECT:' + relative)
    require(isinstance(binding['sha256'], str) and re.fullmatch('[0-9a-f]{64}', binding['sha256']), 'INVALID_SHA256')
    if not path.is_file():
        raise FileNotFoundError('MISSING_BOUND_FILE:' + relative)
    require(digest(path) == binding['sha256'], 'STALE_BOUND_FILE:' + relative)
    return path


def compact(value):
    return ' '.join(value.split())


def report_quote(value, report):
    require(compact(text(value, 15)) in compact(report), 'REPORT_QUOTE_NOT_FOUND')


def page_evidence(items, pages, required=True):
    require(isinstance(items, list) and (items or not required), 'PAPER_EVIDENCE_MISSING')
    result = set()
    for item in items:
        keys(item, ['page', 'quote'])
        page = item['page']
        require(type(page) is int and 1 <= page <= len(pages), 'PAPER_PAGE_INVALID')
        require(compact(text(item['quote'], 10)) in compact(pages[page - 1]), 'PAPER_QUOTE_NOT_FOUND')
        result.add(page)
    return result


def pdf_state(path):
    try:
        import pymupdf as fitz
    except ImportError:
        import fitz
    with fitz.open(path) as doc:
        require(len(doc) > 0, 'EMPTY_PDF')
        texts, fingerprints = [], []
        for page in doc:
            content = page.get_text()
            pixels = page.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)
            payload = str((pixels.width, pixels.height, pixels.n)).encode() + b'\0' + content.encode() + b'\0' + pixels.samples
            texts.append(content)
            fingerprints.append(hashlib.sha256(payload).hexdigest())
        return texts, fingerprints


def _verify(root, final_pdf, gate_requirements=None):
    root = Path(root).resolve()
    final_pdf = Path(final_pdf).resolve()
    index, index_sha = read(root / 'artifacts/review/review_index.json')
    keys(index, ['schema', 'task_contract', 'rounds'])
    require(index['schema'] == 'himcm-review-index/v1', 'INDEX_SCHEMA')
    contract_path = bound(root, index['task_contract'])
    contract, contract_sha = read(contract_path)
    keys(contract, ['schema', 'inputs', 'tasks'])
    require(contract['schema'] == 'himcm-task-contract/v1', 'CONTRACT_SCHEMA')
    require(isinstance(contract['inputs'], list) and contract['inputs'], 'NO_ORIGINAL_INPUTS')
    input_paths = []
    for binding in contract['inputs']:
        bound(root, binding)
        input_paths.append(binding['path'])
    require(len(input_paths) == len(set(input_paths)), 'DUPLICATE_INPUT')
    inventory = {str(p.relative_to(root)) for p in (root / 'inputs').rglob('*') if p.is_file()}
    require(set(input_paths) == inventory and inventory, 'INPUT_INVENTORY_MISMATCH: bind all files under inputs/')
    require(isinstance(contract['tasks'], list) and contract['tasks'], 'NO_CONTRACT_TASKS')
    task_ids = set()
    for item in contract['tasks']:
        keys(item, ['id', 'request', 'source_paths', 'source_locator'])
        ident = identifier(item['id'])
        require(ident not in task_ids, 'DUPLICATE_TASK:' + ident)
        task_ids.add(ident)
        text(item['request'], 15)
        text(item['source_locator'])
        cited = distinct(item['source_paths'], 'TASK_SOURCE_PATHS')
        require(cited and cited <= set(input_paths), 'UNKNOWN_TASK_SOURCE')
    if gate_requirements is not None:
        require(isinstance(gate_requirements, list) and all(isinstance(x, dict) for x in gate_requirements), 'GATE_REQUIREMENTS_INVALID')
        ids = [x.get('id') for x in gate_requirements]
        require(len(ids) == len(task_ids) and set(ids) == task_ids, 'GATE_CONTRACT_TASK_MISMATCH')

    rounds = index['rounds']
    if rounds == []:
        return {'status': 'REVIEW_INCOMPLETE', 'errors': [], 'incomplete': ['NO_REVIEW_ROUNDS'],
                'index_sha256': index_sha, 'task_contract_sha256': contract_sha, 'history': [],
                'declared_task_count': len(task_ids), 'mode': 'structured-v1'}
    require(isinstance(rounds, list) and 1 <= len(rounds) <= 3, 'REVIEW_ROUND_COUNT')
    history, hashes, sessions, seen_issues, documents = [], [], set(), {}, {}
    prior_tasks = prior_fingerprints = None
    last_full = None
    full_count = short_count = 0
    for position, binding in enumerate(rounds, 1):
        path = bound(root, binding)
        record, record_sha = read(path)
        require(record_sha not in hashes, 'DUPLICATE_REVIEW_RECORD')
        keys(record, ['schema', 'round', 'mode', 'reviewer', 'task_contract_sha256', 'paper', 'report',
                      'previous_review_sha256', 'overall', 'coverage', 'issues', 'supporting_files'])
        require(record['schema'] == 'himcm-review/v1', 'REVIEW_SCHEMA')
        require(type(record['round']) is int and record['round'] == position, 'REVIEW_ROUND_ORDER')
        require(record['task_contract_sha256'] == contract_sha, 'REVIEW_CONTRACT_CHANGED')
        require(record['previous_review_sha256'] == hashes, 'REVIEW_HISTORY_MISMATCH')
        reviewer = record['reviewer']
        keys(reviewer, ['session_id', 'fresh_context', 'inherited_parent_context'])
        session = text(reviewer['session_id'])
        require(session not in sessions, 'REUSED_REVIEWER_SESSION')
        sessions.add(session)
        require(reviewer['fresh_context'] is True and reviewer['inherited_parent_context'] is False,
                'REVIEW_CONTEXT_CONTRADICTION')
        require(isinstance(record['supporting_files'], list), 'SUPPORTING_FILES_INVALID')
        support_bindings, support_roles = {}, {}
        for support in record['supporting_files']:
            keys(support, ['path', 'sha256', 'role'])
            bound(root, {key: support[key] for key in ['path', 'sha256']})
            role = text(support['role'])
            require(not Path(role).is_absolute() and '..' not in Path(role).parts
                    and str(Path(role)) == role and role != '.', 'INVALID_SUPPORTING_ROLE')
            require(support['path'] not in support_bindings, 'DUPLICATE_SUPPORTING_FILE')
            require(role not in support_roles, 'DUPLICATE_SUPPORTING_ROLE')
            support_bindings[support['path']] = support['sha256']
            support_roles[role] = support['sha256']
        if position == len(rounds):
            # These are the standard scientific output roots created by init_project.
            # Review/administrative records are outside them; original inputs have their own contract.
            delivered = {str(p.relative_to(root)) for folder in ['code', 'data', 'paper', 'figures', 'artifacts/results', 'final']
                         for p in (root / folder).rglob('*') if p.is_file() and p.resolve() != final_pdf}
            # The immutable reviewed copy and its canonical delivery role must both
            # exist and match the same hash. Do not require identical path strings.
            require(delivered <= set(support_roles), 'DELIVERED_SCIENTIFIC_FILE_UNREVIEWED:' + ','.join(sorted(delivered - set(support_roles))))
            # Include explicitly reviewed support outside standard roots as well:
            # e.g. an idea/assumption note changing must not pass under an old hash.
            for role, expected_sha in support_roles.items():
                bound(root, {'path': role, 'sha256': expected_sha})
        paper = bound(root, record['paper'])
        report = bound(root, record['report']).read_text(encoding='utf-8')
        text(report, 30)
        paper_sha = record['paper']['sha256']
        if paper_sha not in documents:
            documents[paper_sha] = pdf_state(paper)
        pages, fingerprints = documents[paper_sha]
        coverage = record['coverage']
        keys(coverage, ['contract_complete', 'tasks', 'pages_read', 'rechecked_tasks', 'base_full_sha256'])
        require(type(coverage['contract_complete']) is bool, 'CONTRACT_COMPLETE_NOT_BOOLEAN')
        read_pages = coverage['pages_read']
        require(isinstance(read_pages, list) and all(type(p) is int and 1 <= p <= len(pages) for p in read_pages)
                and len(set(read_pages)) == len(read_pages), 'PAGES_READ_INVALID')
        read_pages = set(read_pages)
        rechecked = distinct(coverage['rechecked_tasks'], 'RECHECKED_TASKS')
        require(rechecked <= task_ids, 'UNKNOWN_RECHECKED_TASK')
        if record['mode'] == 'FULL':
            full_count += 1
            require(short_count == 0 and full_count <= 2, 'FULL_AFTER_SHORT_OR_CAP_EXCEEDED')
            require(read_pages == set(range(1, len(pages) + 1)), 'FULL_PAGE_COVERAGE_INCOMPLETE')
            require(rechecked == task_ids and coverage['base_full_sha256'] is None, 'FULL_TASK_COVERAGE_INCOMPLETE')
            last_full = record_sha
        elif record['mode'] == 'SHORT':
            short_count += 1
            require(last_full is not None and short_count == 1 and position == len(rounds), 'SHORT_WITHOUT_FULL_OR_NOT_FINAL')
            require(history[-1]['contract_complete'] or not coverage['contract_complete'],
                    'SHORT_CONTRACT_CONFIRMATION_REQUIRES_FULL')
            require(coverage['base_full_sha256'] == last_full, 'SHORT_FULL_BASE_MISMATCH')
            # Pagination changes invalidate positional carry-forward. Require another FULL.
            require(len(prior_fingerprints) == len(fingerprints), 'SHORT_PAGE_COUNT_CHANGED_REQUIRES_FULL')
            changed = {p + 1 for p, (a, b) in enumerate(zip(prior_fingerprints, fingerprints)) if a != b}
            require(changed <= read_pages, 'SHORT_CHANGED_PAGE_NOT_CHECKED')
            previous_support = history[-1]['supporting_roles']
            if support_roles != previous_support:
                require(rechecked == task_ids, 'SHORT_CHANGED_SCIENCE_REQUIRES_ALL_TASK_RECHECK')
        else:
            raise ValueError('REVIEW_MODE_INVALID')
        tasks = {}
        require(isinstance(coverage['tasks'], list), 'TASK_COVERAGE_INVALID')
        for task in coverage['tasks']:
            keys(task, ['id', 'status', 'paper_evidence', 'report_quote'])
            ident = identifier(task['id'])
            require(ident in task_ids and ident not in tasks, 'UNKNOWN_OR_DUPLICATE_COVERAGE_TASK')
            require(task['status'] in ['ANSWERED', 'PARTIAL', 'UNANSWERED'], 'TASK_STATUS_INVALID')
            report_quote(task['report_quote'], report)
            support = page_evidence(task['paper_evidence'], pages, task['status'] == 'ANSWERED')
            if ident in rechecked:
                require(support <= read_pages, 'TASK_EVIDENCE_PAGE_NOT_CHECKED')
            else:
                require(record['mode'] == 'SHORT' and task == prior_tasks[ident], 'SHORT_UNCHECKED_TASK_CHANGED')
                require(not support.intersection(changed), 'SHORT_CHANGED_TASK_NOT_RECHECKED')
            tasks[ident] = task
        require(set(tasks) == task_ids, 'TASK_COVERAGE_MISSING')
        require(isinstance(record['issues'], list), 'ISSUES_INVALID')
        current = {}
        for issue in record['issues']:
            keys(issue, ['id', 'summary', 'severity', 'status', 'task_ids', 'paper_evidence', 'report_quote'])
            ident = identifier(issue['id'])
            require(ident not in current, 'DUPLICATE_ISSUE:' + ident)
            text(issue['summary'], 10)
            require(issue['severity'] in ['high', 'medium', 'low'], 'ISSUE_SEVERITY_INVALID')
            require(issue['status'] in ['OPEN', 'FIXED', 'ACCEPTED_LIMITATION'], 'ISSUE_STATUS_INVALID')
            require(distinct(issue['task_ids'], 'ISSUE_TASK_IDS') <= task_ids, 'UNKNOWN_ISSUE_TASK')
            if record['mode'] == 'SHORT' and (ident not in seen_issues or issue != seen_issues[ident]):
                require(set(issue['task_ids']) <= rechecked, 'SHORT_ISSUE_TASK_NOT_RECHECKED:' + ident)
            if ident in seen_issues:
                for field in ['summary', 'severity', 'task_ids']:
                    require(issue[field] == seen_issues[ident][field], 'ISSUE_IDENTITY_CHANGED:' + ident)
            else:
                require(issue['status'] == 'OPEN', 'NEW_ISSUE_ALREADY_CLOSED:' + ident)
            report_quote(issue['report_quote'], report)
            support = page_evidence(issue['paper_evidence'], pages)
            require(support <= read_pages, 'ISSUE_EVIDENCE_PAGE_NOT_CHECKED')
            require(not (issue['severity'] == 'high' and issue['status'] == 'ACCEPTED_LIMITATION'), 'HIGH_ISSUE_LIMITATION_NOT_FIXED')
            current[ident] = issue
        require(set(seen_issues) <= set(current), 'PRIOR_ISSUE_MISSING')
        complete = coverage['contract_complete'] and all(t['status'] == 'ANSWERED' for t in tasks.values()) and all(i['status'] != 'OPEN' for i in current.values())
        require(record['overall'] == ('COMPLETE' if complete else 'PARTIAL'), 'OVERALL_CONTRADICTS_TASKS_OR_ISSUES')
        history.append({'round': position, 'sha256': record_sha, 'mode': record['mode'], 'paper_sha256': paper_sha,
                        'overall': record['overall'], 'contract_complete': coverage['contract_complete'], 'tasks': len(tasks), 'issues': len(current),
                        'pages_declared_read': sorted(read_pages), 'rechecked_tasks': sorted(rechecked),
                        'supporting_files': len(support_bindings), 'supporting_roles': dict(sorted(support_roles.items()))})
        hashes.append(record_sha)
        seen_issues = current
        prior_tasks, prior_fingerprints = tasks, fingerprints
    require(history[-1]['paper_sha256'] == digest(final_pdf), 'FINAL_REVIEW_NOT_ON_FINAL_PDF')
    return {'status': 'REVIEW_PASS' if history[-1]['overall'] == 'COMPLETE' else 'REVIEW_INCOMPLETE',
            'errors': [], 'incomplete': [] if history[-1]['overall'] == 'COMPLETE' else ['FINAL_REVIEW_PARTIAL'],
            'index_sha256': index_sha, 'task_contract_sha256': contract_sha, 'history': history,
            'declared_task_count': len(task_ids), 'mode': 'structured-v1'}


def verify(root, final_pdf, gate_requirements=None):
    try:
        result = _verify(root, final_pdf, gate_requirements)
    except FileNotFoundError as exc:
        result = {'status': 'REVIEW_INCOMPLETE', 'errors': [], 'incomplete': [str(exc)]}
    except (ValueError, TypeError, KeyError, OSError, RuntimeError) as exc:
        result = {'status': 'REVIEW_FAIL', 'errors': [str(exc)], 'incomplete': []}
    result['not_checked'] = ('Mathematical truth, semantic agreement of narrative with declarations, completeness of original task decomposition, '
                             'authenticity/independence of reviewer sessions, actual reading or cross-page dependencies; '
                             'independent scientific review and external frozen provenance remain required. SHORT is not a new full Q.')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    parser.add_argument('--pdf', required=True, type=Path)
    parser.add_argument('--output')
    args = parser.parse_args()
    pdf = args.pdf if args.pdf.is_absolute() else args.project / args.pdf
    result = verify(args.project, pdf)
    emit(result, args.output)
    return 1 if result['errors'] else 2 if result['incomplete'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
