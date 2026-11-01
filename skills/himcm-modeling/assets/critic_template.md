# Independent critic pass (fresh session; reads only the problem, attachments and PDF)

Critic: <who: e.g. Codex CLI, fresh session, on machine X; never the author's own context>

<!-- one line per round; raw = the critic's own output file, unedited; pdf_sha256 = sha256 of the PDF it read -->
Round: 1 | critic: <name> | fresh_session: yes | pdf_sha256: <hex> | raw: artifacts/review/critic_round1_raw.md
Round: 2 | critic: <name> | fresh_session: yes | pdf_sha256: <sha256 of final PDF> | raw: artifacts/review/critic_round2_raw.md

<!-- one block per issue (actual issues, no minimum). FIXED needs "verified round K": round K's raw output must contain "K-th issue number. ... Verdict: FIXED".
     Without it write FIXED_UNREVIEWED (gate returns INCOMPLETE). The LAST round must review the final PDF (gate compares sha256). -->
1. Location: | Evidence: | Severity: high/medium/low | Minimal fix:
Status: OPEN

<!-- optional diagnostic for a concise paper below the internal page target: -->
<!-- SHORT_EXCEPTION_APPROVED: <reason> -->

<!-- If a genuine complete review finds no issues, use Review verdict: NO_BLOCKING_ISSUES here AND in the final raw critic output. Never manufacture five issues. High WONTFIX cannot complete. Every earlier stable issue ID, including previously closed issues, needs its own exactly-once final-PDF Verdict, even in a short final verification. The overall Review verdict cannot replace it. -->

<!-- Every round, including a short final verification, must use an actually NEW context.
     For opaque raw IDs, declare each round-local mapping explicitly (no suffix inference):
Issue alias: round 1 | raw_id: C1-01 | issue: 1
     Put the actual declarations outside comments. The raw output stays unedited.
     One raw ID maps to one numeric issue per round; unknown/duplicate declarations fail.
     Plain numeric IDs need no alias. The gate recognizes issue fields and explicit
     Issues/Findings containers; numbering a coverage/read/reference checklist is not an issue.
     The parser is structural: arbitrary prose/unnumbered complaints need review and a
     structured issue entry, not a claim that mechanical detection is exhaustive. -->

<!-- Raw-output scope contract (v8.2): retain the top pdf_sha256 line. Put fresh_session, inherited_parent_context and arbitrary custom keys under ## Review metadata; put all actual entries under ## Issues or ## Findings. Use Review verdict: for the overall conclusion. Do not put Severity/Location/Minimal fix/Verdict controls in metadata. Fields begin a live line (optional list bullet) or a pipe cell; the Verdict value may be on the next live line. Code/comments/inline-code/quotes cannot authorize a verdict or ID. Legacy numeric/opaque heading/list/bare formats remain, but an unscoped opaque key:value with only Verdict fails as CRITIC_RAW_AMBIGUOUS_SCOPE. Keep frozen raw unedited; obtain a new independent review with explicit scope if clarification is needed. -->

<!-- For a zero-issue completion, both this closure summary and the final raw must contain exactly one live `Review verdict: NO_BLOCKING_ISSUES`. Code/comments/inline code/quotes/indented examples and ordinary prose mentions cannot authorize that result; duplicate or conflicting live Review verdict declarations fail. -->

<!-- Keep whole-review Review verdict declarations on rows containing no Severity, Location, Minimal fix or per-issue Verdict declaration cells. A live row mixing these scopes fails, including inside metadata or after an issue; an overall result cannot suppress adjacent issue controls. Global-only pipe rows remain supported. -->
