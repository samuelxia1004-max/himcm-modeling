# Structured review v1: complete tasks and closed issues are separate

This is a development interface. A mechanical pass proves registered consistency, not scientific truth, originality, actual reading, reviewer independence or an award level. Keep the original problem and every attachment; full human-readable reviews remain required. An independent reviewer must check the original wording against the task decomposition and inspect the complete scientific packet. A JSON declaration cannot override contradictory evidence in the report.

## Author: prepare once, then preserve each round

1. Put all original input files under `inputs/`. Fill `artifacts/task_contract.v1.json`: all input path/hash bindings and each required output with stable ID, original request, source paths and locator. Freeze it before review. Do not rewrite required outputs to suit the current solution. `gate.json.requirements` must contain exactly these IDs. A conditional answer or a justified impossibility proof can satisfy the original request; withdrawing a required output cannot.
2. Give each fresh reviewer the full original inputs, this contract, the current immutable PDF and necessary scientific code/data/appendices, plus all earlier original reviews and issue records. No old quality scores, desired verdicts or parent science hints. The author must start and wait for reviewers within the original budget. At most two FULL and one final SHORT; a continuation is not a fresh context.
3. The reviewer writes a full readable report first, then its own JSON record binding that report, the exact reviewed PDF and contract hashes. Preserve both unchanged. Add the record's path/hash to `artifacts/review/review_index.json`. No author-written substitute verdict and no repair of a historical raw report. If a record is malformed, preserve it and treat the attempt honestly; a new review still consumes the original limits. Current limitation: a syntactically malformed or structurally invalid record in the indexed history blocks this interface; no rejected-attempt ledger has yet been validated. Do not delete it, repair it in place, or omit it to obtain a pass. Preserve the unsuccessful attempt and use a separately preregistered fair attempt when authorized by the experiment protocol. Ordinary valid PARTIAL records can be resolved by a later permitted FULL.
4. Run `scripts/check_gate.py PROJECT --pdf final/TEAM.pdf --review-format structured-v1`. This integrates the review check with existing source, task, validation, PDF and attachment checks. `scripts/check_reviews.py` can diagnose review consistency alone. Legacy Markdown parsing remains for old projects; a legacy pass is not acceptance of this interface.

All paths in bindings are relative to the project and remain inside it. An ordinary binding is exactly `{"path":"...","sha256":"64 lowercase hex characters"}`. No extra JSON keys, duplicate keys, NaN, Boolean integers, duplicate IDs or guessed ID aliases. `--output` for the standalone review checker only creates a new file.

## Task contract and index

The task contract has exactly:

```json
{
  "schema": "himcm-task-contract/v1",
  "inputs": [{"path": "inputs/problem.txt", "sha256": "ACTUAL_SHA256"}],
  "tasks": [{
    "id": "R1",
    "request": "The original required output, preserving its qualifications.",
    "source_paths": ["inputs/problem.txt"],
    "source_locator": "Question 1, paragraph 2"
  }]
}
```

The index has exactly `schema: "himcm-review-index/v1"`, `task_contract` (binding), and `rounds` (ordered list of JSON-record bindings). It has no verdicts to override the original reviewer. Empty initializer templates are unfilled work, never completion evidence.

## Reviewer record

Write exactly these top-level fields:

- `schema`: `"himcm-review/v1"`; `round`: consecutive integer starting at 1; `mode`: `"FULL"` or `"SHORT"`.
- `reviewer`: `session_id` (actual identifiable session), `fresh_context: true`, `inherited_parent_context: false`. These are declarations; retain actual tool provenance separately. Never claim them for a continued or context-inheriting reviewer.
- `task_contract_sha256`: actual frozen contract hash.
- `paper`, `report`: path/hash bindings to the immutable PDF and completed readable report.
- `supporting_files`: list of bindings exactly `{"path":"...","sha256":"...","role":"code/model.py"}`. A role is the unique canonical relative delivery path; it stays the same when the immutable snapshot path changes. These bind for every scientific code/data/editable source/figure/result file supplied with this PDF. Before each review, preserve immutable copies of that round's scientific packet and bind those copies; do not mutate an earlier round's files or rewrite its record. The final record must cover every file under `code/`, `data/`, `paper/`, `figures/`, `artifacts/results/` and `final/` except the already-bound final PDF. Include other necessary scientific files explicitly too. Keep administrative reviews outside these output roots. Put the final delivery ZIP outside `final/` and the scientific roots, e.g. `delivery.zip`, to avoid recursive packaging and a circular review requirement. A missing or changed supporting file blocks acceptance.
- `previous_review_sha256`: the ordered hashes of **all** earlier records, or `[]` for the first. Include earlier failures.
- `overall`: `"COMPLETE"` only if every task is ANSWERED and no issue is OPEN; otherwise `"PARTIAL"`.
- `coverage` and `issues`: structures below. Do not add Q to a SHORT record.

`coverage` has exactly:

```json
{
  "contract_complete": true,
  "pages_read": [1, 2],
  "rechecked_tasks": ["R1"],
  "base_full_sha256": null,
  "tasks": [{
    "id": "R1",
    "status": "ANSWERED",
    "paper_evidence": [{"page": 2, "quote": "An actual passage in this PDF, at least ten characters."}],
    "report_quote": "An actual passage in this readable review, at least fifteen characters."
  }]
}
```

The example page count is illustrative, not a two-page limit. FULL requires every PDF page and every task in `rechecked_tasks`, with `base_full_sha256: null`. `contract_complete` means the reviewer compared the decomposition with the complete original problem; false requires PARTIAL. A valid negative record is retained in the history and a later independent FULL can resolve the uncertainty without rewriting it, if the frozen task contract was already correct. If original tasks were actually omitted, stop this acceptance attempt: a new contract requires a separately recorded fair attempt, preserving all earlier files and clocks; do not silently reset the cap or timer. Task status is exactly ANSWERED, PARTIAL or UNANSWERED. ANSWERED needs paper evidence; the other states may have empty evidence when the output is absent. Every record lists every contract task exactly once. Quotes are location bindings, not proof that the answer is correct. Inspect figures and calculations as well as the quoted text.

Each `issues` item has exactly `id`, `summary`, `severity`, `status`, `task_ids`, `paper_evidence`, `report_quote`. Preserve a stable ID, summary, severity and task association in later rounds; a different defect gets a new ID. Severity is high/medium/low. Status is OPEN, FIXED or ACCEPTED_LIMITATION. A newly discovered issue starts OPEN. Later FIXED means the independent reviewer verified its disposition on this PDF; high-severity issues cannot be closed as ACCEPTED_LIMITATION. A legitimate limitation may be accepted for a lesser issue, with the reason in the linked report. It cannot make an unanswered task ANSWERED. Carry every previous issue into each later record, even if already fixed; an empty list is valid when there were genuinely no issues.

## SHORT and revised PDFs

A SHORT cannot upgrade an unconfirmed task contract to confirmed; that requires a remaining FULL. A SHORT is the last review and refers to the nearest preceding FULL via `base_full_sha256`. It rechecks every old issue and any new issue, every changed page, and every affected task. A newly recorded issue or any changed issue disposition/evidence must include all its linked task IDs in rechecked_tasks. Merely reading the quoted page does not declare that task rechecked. An unchanged previously closed issue can be carried forward subject to the other scope rules. List the task IDs actually rechecked. Unchecked task records must be exactly equal to the preceding record, including their report quote; include that explicitly labelled carried-forward passage in the new report and verify the carry-forward is justified. Their supporting pages must be unchanged.

If the mapping from scientific file role to content hash changes between the preceding FULL and SHORT, every original task must be explicitly rechecked. Swapping filenames or import roles matters even if the content-hash multiset is unchanged. The final record may bind an immutable snapshot path while naming the canonical current delivery path in its role. The checker verifies both the original bound copy and the current role file against the same hash, including explicitly supplied files outside the standard roots. Missing or changed current support requires an actual later permitted review; do not rewrite the original record. This is a conservative scope rule, not a new full Q. If that review cannot fit the original budget, report PARTIAL. The checker cannot prove that an omitted file outside the standard output roots was unnecessary: the reviewer must inspect the complete scientific packet.

The checker compares extracted text and rendered pixels between the preceding and current PDF. Changed page count requires a new FULL because positional evidence no longer establishes safe carry-forward. Unchanged cited pages do **not** establish independence from changes elsewhere: the reviewer must inspect changed assumptions, formulas, data and code dependencies and add every affected task to `rechecked_tasks`. Inspect the full scientific packet to decide the affected scope. If that scope cannot be bounded, use the remaining FULL opportunity or report PARTIAL. A SHORT never supplies a fresh complete-paper Q.

The machine cannot detect every semantic contradiction, omitted original request, forged session declaration or scientific dependency. Full reports, raw inputs and tool evidence remain visible to independent scientific review and parent audit. Do not turn this interface into an automatic mathematical or award certificate.
