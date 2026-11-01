#!/usr/bin/env python3
"""Create a resumable HiMCM v8 workspace. Existing files are never overwritten or deleted."""
import argparse, json, shutil
from pathlib import Path
HERE = Path(__file__).resolve().parent

def write_new(path, value):
    if path.exists(): return
    path.write_text(value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf8')

def main():
    p = argparse.ArgumentParser(); p.add_argument('project'); p.add_argument('--year', type=int, required=True); p.add_argument('--problem', choices=['A', 'B']); a = p.parse_args()
    root = Path(a.project).resolve(); root.mkdir(parents=True, exist_ok=True)
    for d in ['inputs', 'data', 'code', 'scratch', 'artifacts/results', 'artifacts/review', 'paper', 'figures', 'final']: (root / d).mkdir(parents=True, exist_ok=True)
    write_new(root / 'PROJECT_CONTEXT.md', f'# HiMCM {a.year} {a.problem or ""}\n\nStage: intake\nContest cutoff date: TODO\nTime budget: TODO (see SKILL.md table)\n\n## Checklist (mechanical status from check_gate.py; scientific completion also requires substantive review)\n\n## Known gaps (copy every GATE_FAIL / GATE_INCOMPLETE item here if delivering PARTIAL)\n\n## Scratch\nUse ./scratch only. Never use /tmp. Never delete files.\n')
    tpl = HERE.parent / 'assets/gate_template.json'
    if not (root / 'artifacts/gate.json').exists():
        g = json.loads(tpl.read_text(encoding='utf8')); g['rules']['rules_year'] = a.year
        (root / 'artifacts/gate.json').write_text(json.dumps(g, ensure_ascii=False, indent=1) + '\n', encoding='utf8')
    write_new(root / 'data/source_log.md', '# Source log. Contest cutoff: TODO\n\n| Parameter | Value | Class | Use | Source / URL / accessed | Note | ID | Dataset |\n|---|---|---|---|---|---|---|---|\n')
    write_new(root / 'data/attachments_log.md', '# Attachments log (file, real type, rows/cols, units, conversion, error)\n')
    write_new(root / 'artifacts/independent_ideas.md', '# Independent ideas (write BEFORE reading any solution of this problem)\n\nBaseline:\n\nCandidates (>=3 when there is a real route choice; justify a unique natural structure):\n1.\n2.\n3.\n\nChosen core contribution and why (testable? changes the decision?):\n')
    write_new(root / 'artifacts/plausibility.md', '# Plausibility checks (conservation, units, monotonicity, extremes, historical range)\n')
    write_new(root / 'artifacts/review/critic.md', (HERE.parent / 'assets/critic_template.md').read_text(encoding='utf8'))
    review_format = json.loads((root / 'artifacts/gate.json').read_text()).get('review_format', 'legacy')
    if review_format == 'structured-v1':
        write_new(root / 'artifacts/task_contract.v1.json', (HERE.parent / 'assets/task_contract_v1.json').read_text())
        write_new(root / 'artifacts/review/review_index.json', (HERE.parent / 'assets/review_index_v1.json').read_text())
    print(json.dumps({'project': str(root), 'status': 'INITIALIZED', 'existing_files': 'preserved', 'review_format': review_format, 'next': ('complete immutable task contract and structured reviews; run check_gate.py --review-format structured-v1 at 75% time' if review_format == 'structured-v1' else 'existing legacy review format retained; run check_gate.py at 75% time')}))

if __name__ == '__main__': main()
