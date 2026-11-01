# Current development workflow: structured-v1

For new projects, use references/structured-review.md. Write the full scientific report, then its bound structured record; assess original task completion separately from issue closure. Preserve all prior stable IDs and raw records. FULL reads all pages and required scientific support; SHORT checks changed pages, all issues and affected tasks without producing a new full Q. The author supplies only the allowed original packet and prior records. The following template is retained for LEGACY projects and does not replace structured-v1.

# Critic prompts (copy into a NEW session each round; Codex CLI `codex exec` in a fresh run is the default critic)

## Round 1 (full critique)
You are an independent critic of a HiMCM paper. Read ONLY the files in this folder: the problem statement and attachments, and paper.pdf. Do not read anything else.
First run `shasum -a 256 paper.pdf` (or `sha256sum`) and write the line `pdf_sha256: <hex>` at the top of critic_out.md.
After the top SHA line, put fresh_session: yes, inherited_parent_context: no and any custom metadata under an explicit `## Review metadata` heading. Use `Review verdict:` for the whole-review conclusion; never use bare `Verdict:` for that conclusion. Metadata must not contain Severity, Location, Minimal fix or per-issue Verdict fields.
Place actual issue entries under an explicit `## Issues` or `## Findings` heading. Keep numbered task-coverage, pages-read, references and recomputation lists in separate sections. Keep IDs stable; if a named ID differs from the numeric closure ID, preserve it and declare the mapping in the closure file, without editing this raw output.
List the actual issues most likely to overturn conclusions; do not invent a quota of issues (untested headline claims, hold-out reuse, cutoff violations, unused attachments, summary stronger than evidence, numbers inconsistent with tables). Format per issue:
N. Location: | Evidence: | Severity: high/medium/low | Minimal fix:
End with: "Length verdict: <padding or substance?>". Do not modify or delete other files.

## Round 2+ (NEW context for every round, including the short final verification; the LAST round must read the FINAL PDF)
Independent critic, round K. Read ONLY: the problem files, previous_issues.md (earlier issues) and paper.pdf.
First write `pdf_sha256: <hex>` (from shasum -a 256 paper.pdf) at the top of critic_roundK.md. Then write `## Review metadata`, `fresh_session: yes` and `inherited_parent_context: no`; put any custom metadata there. Use `Review verdict:` for the overall conclusion. Start the issue list with `## Issues`; metadata cannot contain issue control fields.
For every earlier stable issue ID, including previously FIXED issues, write exactly one live issue entry with its own Verdict. A short final review has the same requirement; a global conclusion cannot replace any per-issue verdict. For numeric issue N write:
N. <restatement> | Verdict: FIXED or NOT FIXED | Evidence: <page/quote> | Remaining fix
Carry all earlier issue IDs into this final-PDF review even if previously fixed. Then list any NEW high-severity issues (same format as round 1, numbered after the last old issue). Do not modify or delete other files.

In each full review, separately judge whether the original required outputs are substantively answered and whether earlier issues are fixed. A narrowed claim may be correct while leaving a required output unanswered; identify that gap from the original wording and its consequence. Where an original required output remains materially unanswered, retain an open issue for that missing output rather than closing it through a corrected overclaim or mentioning it only as a limitation. A justified conditional answer or an impossibility argument covering the original question can satisfy a task: do not add field trials, unconditional guarantees, a preferred algorithm or other requirements absent from the problem. A short final verification confirms its stated issue scope and does not replace a new full task-coverage review. Trace required conditional or preference-dependent functions into an operative rule and the reported outputs. A default-value numerical example does not establish a configurable function. Where an input could change the requested decision, inspect a discriminating change; an unchanged output may be valid because of a stated interval, inactive constraint or saturation. For a conceptual design task, an explicit operative rule or justified infeasibility may suffice; do not invent a software or field-trial requirement.

If no blocking issues exist, explicitly write `Review verdict: NO_BLOCKING_ISSUES`. Inspect all applicable tasks; the declaration is not proof of correctness. At most two full reviews plus one short final verification within the original budget. If a blocker remains, restrict/withdraw the affected claim and verify that disposition, or report PARTIAL.

A continuation of an earlier reviewer is not a fresh final verification. Start a new context and provide the bounded packet plus all earlier issues; retain failed/continuation review evidence.

Raw declaration contract (v8.2): put each issue field at the start of a line (optionally `- `), or at the start of a same-line pipe cell. `Verdict:` may have its FIXED/NOT FIXED value on the next live line. Fenced code, HTML comments, inline code and Markdown blockquotes are examples, not issue/field declarations. Keep live declarations outside them; put a blank line after a quote. Bare opaque `key: value` plus only `Verdict:` outside Issues/Findings is ambiguous and fails closed. Explicitly scoped existing numeric/opaque IDs remain supported. This contract governs newly generated raw output; never rewrite a frozen third-party raw report to make it pass.

For a zero-issue completion, both the closure summary and the final raw must contain exactly one live `Review verdict: NO_BLOCKING_ISSUES`. Code/comments/inline code/quotes/indented examples and ordinary prose mentions cannot authorize that result; duplicate or conflicting live Review verdict declarations fail.

Keep whole-review Review verdict declarations on rows containing no Severity, Location, Minimal fix or per-issue Verdict declaration cells. A live row mixing these scopes fails, including inside metadata or after an issue; an overall result cannot suppress adjacent issue controls. Global-only pipe rows remain supported.
