Verdict PASS_WITH_SCOPE_LIMITS

Fresh independent mechanical audit of frozen HiMCM candidate v8.3-r4. All **88 preregistered independent full-gate executions** match their original expected exits, physical/main/AI/counted/substance pages, effective-exemption flags, counting basis, required messages and input-integrity checks. All four retained current-contract suites also pass. The R3 ordinary-autolink finding is repaired in the tested bounded syntax, while known unfinished templates remain rejected. No product counterexample was found in this registered repair/regression audit.

This audit wrote only `work/v83-r4-independent-audit`, performed no source edits, author work, installation or subagent delegation, and read no author paper or old scientific-quality score. Requested agent settings were gpt-6.1-sol/high; backend execution settings are not independently exposed here. This audit context did not implement the repair or continue an earlier auditor's session.

## Frozen identity and protected code

- Runtime manifest SHA256: `91e221d644e49da09a7bce137ab75906b3daeb2bae55725292906db4b8d6c304`.
- Entry `SKILL.md`: `f8ca9547833880de63f918e9ae3c68dd5d87562f10d270963e956954330f7187`.
- Gate `scripts/check_gate.py`: `f98f3b960020cf7d176f353b00cd5967abec3f413c1c682c305399f73bf0b656`.

All 55 source runtime entries matched the manifest before and after all execution. The separate 55-entry runtime snapshot also matches after execution. The R3-to-R4 delta contains exactly `scripts/check_gate.py` and `scripts/selftest_page_cap.py`. All fourteen other top-level gate functions are AST-identical to R3; the entire gate module AST is identical after removing `policy_evidence_text`. Thus the observed scope is the policy-evidence helper, with the protected arithmetic, review/raw parsing and context code unchanged.

Evidence: `runtime-before.json`, `runtime-after.json`, `runtime-r3-r4-delta.json`, `protected-functions.json`, `protected-module.json`, `runtime-freeze-v83-r4.json` and `frozen-runtime/`. Two historical raw-suite fixture dependencies were separately copied and hashed before execution; they are not runtime-manifest entries.

## New independent controls

The expectations were written and hashed before any independent gate execution (`expectations-before-execution.json`, `execution-start.json`). The 63 genuinely new controls comprise 48 positive/negative citation-template cases, nine ordinary-wording positives and six strict-context controls. Each invokes the complete gate.

Eight citation/structure families are tested in each of `rules_source`, `ai_report_exclusion_rule_quote` and anchored reference `rule_quote`: HTTP angle autolinks with queries/fragments, a named uppercase-HTTPS link, a plain HTTPS query URL, a citation followed by a new-line blockquote and numbered/emphasized text, numbered blockquote structure around a named citation, successive angle/named citations, adjacent angle/plain citations, and task-list/blockquote/emphasis structure. Every family pairs supplied policy wording with a known unfinished marker or immediate missing-evidence target. Negative bodies include TBD, FIXME, TODO, fullwidth TODO, an adjacent non-URL angle prompt, and immediate replace/fill/insert targets. All pass their expected positive/negative dispositions.

The nine additional positives use ordinary supplied rules, report/reference placement instructions with a later evidence word, and a substantive rule followed by an explanatory TODO mention. These preserve useful supplied-evidence candidates without requiring a semantic-authentication classifier.

The six context controls combine ordinary URL citation forms with missing cutoff, mismatched cutoff year or a string-valued exemption flag. The missing-cutoff cases remain incomplete (exit 2); mismatched-year and invalid-flag cases fail (exit 1). Each keeps physical counting at 22 pages for an 18-page main report plus four AI pages, with effective exemption false. Citation syntax does not confer missing context or boolean authorization.

For normal source/AI field pairs, physical/main pages are 26/22: supplied evidence yields count 22 and effective exemption true; unfinished evidence yields count 26 and effective exemption false. For anchored-section pairs, physical/main pages are 29/25: supplied section evidence subtracts three reference pages, producing count/substance 22/22; unfinished section evidence refuses the subtraction, producing 25/25, while the separately valid AI exemption remains effective. All these fields and the counting basis are checked directly.

All statements and locators are synthetic audit inputs. An accepted candidate is not an authenticated or official rule.

## Exact historical replays

All three R3 main counterfixtures and all six syntax-only executions were copied byte for byte from the published input directories, including old output and hash metadata. Their original expectations remain unchanged: the three main autolinks and the three repeated autolinks now pass; the three plain-URL cases continue to pass. These are nine executions, including deliberate repeated configurations representing the same earlier finding.

The fourteen R2 product counterfixtures and two R1 counterfixtures are also copied byte for byte and replayed against their original dispositions. All nine former R2 wrapped-template false passes reject; all five former R2 substantive-placement false failures pass. Both R1 quotation-placeholder cases reject with physical/main/count 25/20/25 and ineffective AI exemption. Historical failing results and verdicts remain preserved in the published R1/R2/R3 evidence; a repaired candidate does not rewrite those earlier observations.

The independent batch therefore has 63 new controls plus 9 R3 and 16 R2/R1 replay executions, all 88 matching. Complete stdout, stderr, commands, expectations and checks are retained in `actual/` and `results.json`. Every copied/generated independent input is immutable; new hashes and outputs are stored outside each copied input directory.

## Retained bounded replays

| Suite | Actual result | Scope |
|---|---|---|
| Migrated current runner | 69/69, exit 0 | 67 full-gate, one normalizer, one standalone PDF case |
| Raw suite | 39 cases, exit 0 | 38 full-gate and one parser case |
| Scope suite | 191/191, exit 0 | Mixed parser, generated and frozen controls |
| Page suite | 169/169 full-gate, exit 0 | Retained 127, 33 implementation citation cases and 9 exact R3 replay executions |
| Unchanged old runner with R4 gate | exit 1; exactly one `BAD cap_refs_excluded` | Preserved old expectation/current contract difference |

The old69 mismatch is intentional fictional-policy-contract migration, not a new product regression. The separate current runner explicitly supplies the fictional exemption contract. No old assertion or expectation was silently changed. Page169 includes the same retained fourteen R2 and two R1 product counterfixtures checked independently above. Suite counts overlap each other and the independent batch; they are not independent quality samples.

Commands and expected outcomes were registered before the suite runs in `suite-expectations-before-execution.json`; direct actual exits and output hashes are in `suite-results.json`. Complete suite stdout/stderr and generated fixtures are retained.

## Harness handling and integrity

No audit-harness execution failed in this audit. Two earlier recorded harness issues were handled before execution: the R2 supplement expectation-schema mapping was applied from the preserved R3 correction, and the two raw39 fixture dependencies were copied and hashed separately from runtime55. Their original failed attempts and corrected reruns remain unchanged in the R3 evidence.

One deliberate harness-only deviation was preregistered before page169 execution. The stock page suite writes new `page-cap-result.json` files inside some copied historical input directories. A separate audit-owned derivative relocates those result destinations to `page169/case-output-records/`; its import path points to the unchanged frozen runtime. No test cases, setup, expectations, assertions, gate invocations or counting logic changed. The source/derived hashes, exact replacements and diff are retained in `page169-harness-deviation-before-execution.json`, `page169-output-relocation.py` and `.diff`. The runtime snapshot's original suite script remains unchanged.

All original allowed source/fixture trees retain exact before/after file-path-and-hash dictionaries. All 88 independent input directories remain unchanged and copied historical inputs match their sources byte for byte. All 29 unchanged copied page-suite inputs (four root, two R1, fourteen R2 and nine R3 executions) also match whole source dictionaries, with no new output files inside them. Scope fixture copies remain unchanged. Evidence: `source-hashes-before.json`, `source-hashes-after.json`, `all-input-integrity-final.json`, `page169-copied-input-integrity-final.json`, `scope-inputs-before.json` and `coverage-summary.json`.

## Scope limits

This is proportional verification of a bounded known-template grammar and common leading HTTP(S) citation/Markdown structure, strict exemption prerequisites, and the retained mechanical page/review/raw contracts. It does not certify arbitrary Markdown or languages, exhaustive natural-language classification, source existence/authenticity, applicable target-year primary-source policy, exact official quotations, actual reviewer independence, mathematics, baseline adequacy, originality, problem coverage, author-paper quality, installation, stability or award performance. Human verification of genuine applicable policy remains necessary.

There are zero whole v8.3 author attempts in this audit, no active author timer assessment and no scientific-quality score or award certification. No further broadening or repeated testing followed the clean registered checks. `audit-freeze.json` binds this report and all audit-owned evidence by SHA256.
