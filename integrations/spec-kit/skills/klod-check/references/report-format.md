# The report

Write `klod_report.md` at the repository root. The report is read by busy people: keep it to
one screen for a product with no hosted AI, and never longer than the template allows. Every
number, level and gap must carry file or record evidence. Copy the template below and fill
in the placeholders; do not add sections, and drop only the sections the template marks
optional.

## The result line

The line after the identity block states the outcome. Use exactly one of these forms.

| Result | Use when |
|---|---|
| `**Result: PASS.** No dependence on an external AI provider.` | Coverage is complete and no hosted runtime AI was traced. Self-run models and development-time AI do not change this. |
| `**Result: L0.**`, `**Result: L1.**`, `**Result: L2.**` or `**Result: L3.**` | Hosted runtime AI was traced. Give the worst supported level across capabilities. |
| `**Result: NOT ESTABLISHED.**` | A project-owned area could not be inspected and no hosted dependence was traced. |
| `**Result: NOT GRADED.** Library, SDK, demo or sample.` | The repository is not a product or service. |

Follow the result with one sentence: the count of dependent capabilities, the worst
supported level when there is one, and coverage. For example:
`**Result: L1.** 2 dependent capabilities. Worst supported level: L1. Coverage: complete.`
For a pass: `**Result: PASS.** No dependence on an external AI provider. 0 dependent capabilities. Coverage: complete.`

PASS is a scan outcome, not a KLOD level or a conformance claim. Levels belong to
capabilities, never to a product or an organisation (specification 5.5).

## Length limits

| Section | Limit |
|---|---|
| Summary | 3 to 5 bullets, one sentence each |
| AI inventory | One row per AI use; 12 rows at most, group the rest |
| Capabilities | One row per capability |
| Gate results | One table per capability; 6 rows for L0 or L1, 15 rows only for a declared L2 or L3 |
| Findings | One block of 5 bullets per finding; nothing else |
| Human control | One table, 5 rows, or 6 for physical equipment |
| Coverage | One row per project area |
| Evidence to obtain | 3 bullets at most |
| Scope and limits | 4 bullets |

Write in short plain sentences. No introductions, no repeated definitions, no advice that is
not tied to a row or a finding.

## Words with fixed meanings

- Gate result: **Satisfied**, **Failed**, **Missing** (record not in the repository,
  `EVIDENCE-NOT-IN-REPO`) or **N/A**.
- Inventory type: **Hosted runtime**, **Self-run**, **Installation-time** (weights or an
  engine downloaded once, then held), **Development-time**, **Unused** or **Sample**.
  Only Hosted runtime counts toward a level.
- Human-control status: **In place**, **Gap**, **Not checked**.
- Severity: **High** (the capability stops or its data becomes inaccessible), **Medium**
  (a path exists but readiness is unproven, expired or under-staffed), **Low** (record-keeping
  or a SHOULD gap without an operational consequence).
- Confidence: **High** (traced and demonstrated, no counterevidence), **Medium** (dependency
  traced, gap relies on records absent from the repository).
- Finding IDs: `KLOD-<clause>-<capability-slug>`, stable across rescans. Status: new,
  unchanged, accepted and unresolved, or resolved.

## Template

```markdown
# <Project> · KLOD report

- **Project:** <name and version>
- **Git origin:** <sanitised origin, or Not applicable / Unavailable with a reason>
- **Revision:** <commit, or Not applicable / Unavailable with a reason>
- **Model:** <exact active model (source: where it was read), or Unavailable with a reason>
- **Report timestamp:** <ISO 8601 with offset (timezone)>

**Result: <PASS / L0 / L1 / L2 / L3 / NOT ESTABLISHED / NOT GRADED>.** <one sentence: count, worst level, coverage>

## Summary

- Classification: <product / service / library / demo>, <one clause of evidence>.
- <What depends on AI, in business terms, or "No business work depends on a hosted model.">
- <The most important gap, with its finding ID, or "No gap against the numbered clauses.">
- <The first action and who owns it.>
- Assessed against specification <version from references/specification.md>.

## AI inventory

| AI use | Where | Workflow | Type | Counts toward a level |
|---|---|---|---|---|
| <supplier and model or engine> | <path:lines> | <business work it serves, or None> | <Hosted runtime / Self-run / Installation-time / Development-time / Unused / Sample> | <Yes / No> |

## Capabilities

| Capability | Supplier | Declared | Supported | Blocking gap |
|---|---|---|---|---|
| <business work> | <supplier> | <level or None> | <level> | <finding ID or "None"> |

Portability: <per capability, one sentence: where the provider is wired, chosen by configuration or hard-coded, provider-specific features, and whether a switch was ever run>.

## Gate results

<Omit this section when there are no capabilities. One table per capability. Keep the bold line and the table together, with no blank line between them.>
**<Capability>**
| Gate | Result | Evidence |
|---|---|---|
| Register: supplier, capability, level, owner (4.1.1–4.1.3) | <Satisfied / Failed / Missing / N/A> | <path:lines or record, or what was searched> |
| Instructions and capacity limits (4.2.1–4.2.2) | | |
| Manual path independent of the AI (4.2.3) | | |
| Data accessible without the supplier (4.6.1) | | |
| Operators identified by role (4.5.1) | | |
| L2 and L3 gates (4.2.4, 4.3.1–4.3.4, 4.4.1–4.4.6, 4.5.2–4.5.5, 4.6.2) | <N/A when nothing above L1 is declared; otherwise replace this row with one row per gate from references/gates.md> | |

## Findings

<One block per finding against a numbered clause. Write "No findings against the numbered clauses." when there are none.>
### KLOD-<clause>-<capability-slug>
- **Capability:** <business work>, on <supplier>. <What stops if the supplier stops.>
- **Gap:** <requirement, linked as [<clause>](https://keepthelightson.dev/standard.html#c-<clause with dashes>)>. Evidence: <path:lines or dated record>. Counterevidence: <or "none">.
- **Severity and confidence:** <High / Medium / Low>, <High / Medium>. Status: <new / unchanged / accepted and unresolved / resolved>.
- **Consequence:** supported <level>; <remaining uncertainty>.
- **Next action:** <action>. Owner: <role or "to assign">. Closure: <the record that closes it>.

### Human control (principle 6)

<One table for all runtime AI, hosted or self-run. Informative: it changes no level.>
| Control | Status | Evidence | Next action |
|---|---|---|---|
| AI-off switch that works without the supplier, with the mode visible | <In place / Gap / Not checked> | <path:lines> | <action or "None"> |
| Mode enforced where actions are accepted, kept across restarts | | | |
| Late results and queued AI actions rejected after switch-off | | | |
| Manual work usable: inputs, status, permissions, controls | | | |
| Restart needs a recorded human decision | | | |
| Safe state and qualified operators for physical equipment (only when equipment is involved) | | | |

## Coverage

| Area | Status | Note |
|---|---|---|
| <directory or file group> | <Inspected / Partially inspected / Excluded / Inaccessible> | <AI use found, exclusion reason or untraced lead> |

## Evidence to obtain

- <Record, who holds it, and which finding or result it would change. Or "None.">

## Scope and limits

- Repository review, not a drill. No service was interrupted and no provider was called.
- <What was read but not run, such as tests, and what was not inspected, such as model weights.>
- <Uncommitted changes, if any, and what they could affect. Or "Working tree clean.">
- Previous scan: <none (first scan) / date, with IDs new, resolved, unchanged or regrouped>.
```

## Example: a pass

```markdown
# Ledger desk · KLOD report

- **Project:** Ledger desk 2.4.0
- **Git origin:** https://example.invalid/team/ledger-desk.git
- **Revision:** 0123456789abcdef0123456789abcdef01234567
- **Model:** example-model-2026-06 (source: host system prompt)
- **Report timestamp:** 2026-09-12T14:00:42+03:00 (Europe/Bucharest)

**Result: PASS.** No dependence on an external AI provider. 0 dependent capabilities. Coverage: complete.

## Summary

- Classification: product, a web service with a worker (Dockerfile:1; src/main.py:1).
- No business work depends on a hosted model. Receipt matching runs on a classifier the team trains and hosts itself (src/match/model.py:12).
- No gap against the numbered clauses. One human-control gap: matches are applied without a way to stop the classifier (see Human control).
- First action: add an operator switch that holds new matches for manual review. Owner: platform lead.
- Assessed against specification 0.1.0.

## AI inventory

| AI use | Where | Workflow | Type | Counts toward a level |
|---|---|---|---|---|
| Self-trained receipt classifier served by the worker | src/match/model.py:12; worker/run.py:40 | Receipt matching | Self-run | No |
| Code review assistant in CI | .github/workflows/review.yml:8 | None, pull request review | Development-time | No |
| Sample chat client in docs/examples | docs/examples/chat.py:3 | None | Sample | No |

## Capabilities

| Capability | Supplier | Declared | Supported | Blocking gap |
|---|---|---|---|---|
| None | No hosted AI supplier | None | No level applies | None |

Portability: not applicable.

## Findings

No findings against the numbered clauses.

### Human control (principle 6)

| Control | Status | Evidence | Next action |
|---|---|---|---|
| AI-off switch that works without the supplier, with the mode visible | Gap | No switch found; worker/run.py:40 applies every match | Add a hold mode checked by the worker |
| Mode enforced where actions are accepted, kept across restarts | Gap | Depends on the switch above | Same |
| Late results and queued AI actions rejected after switch-off | Not checked | Queue in worker/queue.py:1 not traced to a mode check | Trace after the switch exists |
| Manual work usable: inputs, status, permissions, controls | In place | src/ui/match.py:22 lets a clerk match by hand | None |
| Restart needs a recorded human decision | Gap | No restart record | Log who resumes and why |

## Coverage

| Area | Status | Note |
|---|---|---|
| src/, worker/ | Inspected | Self-run classifier only |
| infra/, Dockerfile | Inspected | No AI endpoints |
| tests/ | Inspected | Read, not run |
| docs/ | Inspected | Sample client only |

## Evidence to obtain

- None.

## Scope and limits

- Repository review, not a drill. No service was interrupted and no provider was called.
- Tests were read, not run. Model weights were not inspected.
- Working tree clean.
- Previous scan: none (first scan).
```

## Example: one hosted capability

```markdown
# Support desk · KLOD report

- **Project:** Support desk 1.8.2
- **Git origin:** https://example.invalid/team/support-desk.git
- **Revision:** 89abcdef0123456789abcdef0123456789abcdef
- **Model:** Unavailable (the host did not expose an exact active model identifier)
- **Report timestamp:** 2026-09-12T09:15:00+00:00 (UTC)

**Result: L1.** 1 dependent capability. Worst supported level: L1. Coverage: complete.

## Summary

- Classification: product, a deployed service (Dockerfile:1; src/main.py:1).
- Support reply drafting depends on Provider A; staff can reply by hand from the ticket queue.
- Biggest gap: the L2 declaration rests on a drill 102 days old (KLOD-4.4.1-support-drafting).
- First action: run an authorised real-work drill with AI unavailable. Owner: head of support.
- Assessed against specification 0.1.0.

## AI inventory

| AI use | Where | Workflow | Type | Counts toward a level |
|---|---|---|---|---|
| Provider A chat completions | src/drafting.py:12 | Support reply drafting | Hosted runtime | Yes |
| Provider A SDK in requirements, no other call site | requirements.txt:7 | None | Unused | No |

## Capabilities

| Capability | Supplier | Declared | Supported | Blocking gap |
|---|---|---|---|---|
| Support reply drafting | Provider A | L2 | L1 | KLOD-4.4.1-support-drafting |

Portability: one adapter (src/llm/adapter.py:1), provider chosen by configuration (src/settings.py:14), no provider-specific features, no switch recorded.

## Gate results

**Support reply drafting**
| Gate | Result | Evidence |
|---|---|---|
| Register: supplier, capability, level, owner (4.1.1–4.1.3) | Satisfied | LIGHTS.md:12 |
| Instructions and capacity limits (4.2.1–4.2.2) | Satisfied | docs/support-runbook.md:8 |
| Manual path independent of the AI (4.2.3) | Satisfied | src/manual_reply.py:18 |
| Data accessible without the supplier (4.6.1) | Satisfied | src/tickets.py:20 reads the local store |
| Operators identified by role (4.5.1) | Satisfied | docs/support-runbook.md:4 |
| Common-mode assessment for a substitute supplier (4.2.4) | N/A | No substitute supplier |
| No knowledge held only inside AI (4.6.2) | Satisfied | docs/reply-rules.md:1 |
| TTM and capacity measured in a drill within 12 months (4.3.1–4.3.4) | Satisfied | docs/drills/2026-06-01.md:12 |
| AI unavailable, real work, one in four unannounced (4.4.2–4.4.4) | Satisfied | docs/drills/index.md:3 |
| Measurements and failures recorded (4.4.5) | Satisfied | docs/drills/2026-06-01.md:12 |
| Failed drill followed by a successful one (4.4.6) | N/A | No failed drill recorded |
| Two people perform unaided (4.5.2, 4.5.5) | Satisfied | docs/drills/2026-06-01.md:6 |
| Re-drill after departures (4.5.3) | N/A | LIGHTS.md:18, both operators remain |
| Drill within 90 days for L2 (4.4.1) | Failed | KLOD-4.4.1-support-drafting |
| Routine human performance and annual review for L3 | N/A | No L3 claim |

## Findings

### KLOD-4.4.1-support-drafting
- **Capability:** support reply drafting, on Provider A. Staff can reply by hand; the automated draft stops.
- **Gap:** [4.4.1](https://keepthelightson.dev/standard.html#c-4-4-1). Evidence: LIGHTS.md:18 names docs/drills/2026-06-01.md as the last successful drill, 102 days before this report. Counterevidence: none.
- **Severity and confidence:** Medium, High. Status: new.
- **Consequence:** supported L1; the L2 declaration has not yet reached its 120-day expiry. Current manual capacity was not observed.
- **Next action:** arrange an authorised real-work drill with AI unavailable. Owner: head of support. Closure: a dated successful drill record meeting the shared gates.

### Human control (principle 6)

| Control | Status | Evidence | Next action |
|---|---|---|---|
| AI-off switch that works without the supplier, with the mode visible | In place | src/control.py:22 | None |
| Mode enforced where actions are accepted, kept across restarts | In place | src/drafting.py:48 rejects old-generation results | None |
| Late results and queued AI actions rejected after switch-off | In place | tests/test_stop.py:10, read not run | Verify in the deployment test environment |
| Manual work usable: inputs, status, permissions, controls | In place | src/manual_reply.py:18 | None |
| Restart needs a recorded human decision | In place | src/control.py:31 logs who resumed | None |

## Coverage

| Area | Status | Note |
|---|---|---|
| src/ | Inspected | Support drafting |
| deploy/, Dockerfile, requirements.txt | Inspected | Provider A endpoint |
| tests/ | Inspected | Read, not run |
| .github/ | Inspected | No AI |
| docs/, LIGHTS.md | Inspected | Runbook and drill records read; events not independently observed |

## Evidence to obtain

- A new drill record from the head of support would resolve KLOD-4.4.1-support-drafting.

## Scope and limits

- Repository review, not a drill. No service was interrupted and no provider was called.
- Tests were read, not run. Drill records were read; the drills were not observed.
- Working tree clean.
- Previous scan: none (first scan).
```

## After the report

Check the citations, supply missing records and give each finding an owner and a date.
Use `klod` for implementation changes, arrange authorised drills, update `LIGHTS.md` and
rescan. Accepted risks keep their reason, owner and review date but stay unresolved until
evidence closes the gap.
