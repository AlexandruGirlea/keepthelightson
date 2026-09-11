# The report

Write `klod_report.md` at the repository root. Use these section titles and order so reports
can be compared across projects and rescans.

## Structure

1. **Identity and headline.** Start with `# <Project name> · KLOD report` and the visible
   [identity block](report-metadata.md): project, sanitised Git origin or local-project status,
   revision, exact active model or unavailable reason, timestamp and timezone. Then state the
   dependent-capability count, worst supported level and coverage. Short reports use the same block.
2. **Assessment.** Inspected scope, repository classification with evidence, and specification
   version from `references/specification.md`, not the skill package version.
3. **Coverage.** Every project area, with status (Inspected, Partially inspected, Excluded or
   Inaccessible), AI use and uncertainty. Any project-owned area not fully inspected makes
   overall coverage Partial.
4. **AI inventory.** Every AI use: file/line, workflow, category (hosted runtime, self-run,
   development-time, unused or sample) and whether gated. Only hosted runtime dependence enters
   capability counts and levels; self-run runtime AI still receives a human-control review.
5. **Capabilities.** Capability, supplier, declared level, supported level and evidence limit.
   Use stable business names. Reconcile supplier relationships and counts with the inventory.
6. **Gate results.** Every gate group in the gate guide, per capability: satisfied, failed,
   evidence missing or not applicable, with evidence or a finding reference. Continue after failure.
7. **Portability.** Per hosted capability, how the provider is wired (one adapter or gateway,
   several places, everywhere), whether the provider and model are chosen by configuration,
   provider-specific features and embeddings in use, and whether a switch has been run. Reported
   with file evidence; it changes no level.
8. **Findings.** Confirmed clause gaps in the format below. For runtime AI, include the separate
   `### Human-control observations (principle 6)` subsection.
9. **Evidence to obtain.** External records that could change a result, tied to findings or uncertainties.
10. **Changes since the previous scan.** IDs new, resolved, unchanged or regrouped; otherwise
   “First scan”. Preserve owner notes and accepted risks.
11. **Scope and limits.** Inspection exclusions and uncertainty. State that this was a repository
    review, not a drill; no service was interrupted and no provider called.

## Findings

A finding requires a traced runtime dependency and a clause gap supported by evidence.
Untraced imports, provider names and suspected call paths remain leads in Coverage.

Each finding contains:

- Stable ID `KLOD-<clause>-<capability-slug>` and status: new, unchanged, accepted and unresolved, or resolved.
- Severity and confidence as defined below.
- Capability, supplier dependency and what stops if the supplier stops.
- Linked clause; file/line or dated-record evidence; counterevidence.
- Supported-level consequence and remaining uncertainty.
- Next action, owner (or “to assign”) and evidence needed for closure.

Severity reflects the consequences of supplier loss that the evidence supports:

| Severity | Basis |
|---|---|
| High | No usable path: the capability stops, fallback depends on the unavailable supplier, or required data becomes inaccessible. |
| Medium | A path exists but readiness is unproven, expired or under-staffed: missing drills, stale measurements, one operator, model-only knowledge or no common-mode assessment. |
| Low | Record-keeping or SHOULD gap without an evidenced operational consequence, such as an overdue register review. |

A missing register entry caps the level at L0 (4.1.3) but does not itself establish High severity.
State uncertainty where consequences depend on unavailable records; “not found here” does not
mean “does not exist”.

Confidence is **High** for a traced capability and demonstrated gap with no counterevidence;
**Medium** when the dependency is established but the gap relies on records absent from the
repository (`EVIDENCE-NOT-IN-REPO`). Low-confidence leads belong in Coverage, not Findings.

## Human-control observations

Use the Findings subsection `### Human-control observations (principle 6)` for runtime AI.
State whether controls are evidenced, a gap is demonstrated or evidence is missing. Cite operator
authority, the action boundary, queued and late work, human operation, restart controls and
inspected tests or records.

Give each distinct observation a stable `KLOD-P6-<capability-slug>-<control-slug>` ID. Include
status, consequence, evidence and counterevidence, owner, next action and closure evidence.
Mark its basis **Principle 6 (informative)** and level consequence **None by itself**. Describe
the exposure without applying supplier-outage severity or inferring danger from the sector.
When no gap is found, record inspected controls and verification limits.

Self-run AI can have observations while the headline reports zero dependent capabilities and
no level.

## Example

Illustrative project and evidence; replace all values and citations with inspected facts.

```markdown
# Example helpdesk · KLOD report

- **Project:** Example helpdesk
- **Git origin:** Not applicable (local project; not a Git repository)
- **Revision:** Not applicable (local project; no Git revision)
- **Model:** Unavailable (the host did not expose an exact active model identifier)
- **Report timestamp:** 2026-09-11T07:42:18+00:00 (UTC)

1 dependent capability found. Worst supported level: L1. Coverage: complete.

## Assessment

Scope: example-helpdesk, a deployed service (Dockerfile; src/main.py:1).
Assessed against specification 0.1.0 at the timestamp above.

## Coverage

| Area | Status | AI use found | Remaining uncertainty |
|---|---|---|---|
| src/ | Inspected | Support drafting | None |
| deploy/, Dockerfile, requirements.txt | Inspected | Provider A endpoint | None |
| tests/ | Inspected | Provider stub and takeover checks | Tests inspected, not executed |
| .github/ | Inspected | Development-time AI review | None |
| docs/, LIGHTS.md | Inspected | Manual runbook and drill records | Events not independently observed |

## AI inventory

| Use | Location | Workflow | Category | Gated |
|---|---|---|---|---|
| Provider A chat completions | src/drafting.py:12 | Support drafting | Hosted runtime | Yes |
| AI review action | .github/workflows/review.yml:14 | Pull request review | Development-time | No |
| Unused AI SDK | requirements.txt:7 | No call site or configuration use found | Unused | No |

## Capabilities

| Capability | Supplier | Declared | Supported | Evidence limit |
|---|---|---|---|---|
| Support drafting | Provider A | L2 | L1 | Last successful drill was 102 days ago |

## Gate results

All rows concern support drafting.

| Gate | Result | Evidence |
|---|---|---|
| Register, 4.1.1–4.1.3 | Satisfied | LIGHTS.md:12 identifies supplier, work, level and owner |
| Instructions and capacity, 4.2.1–4.2.2 | Satisfied | docs/support-runbook.md:8 |
| Independent path, 4.2.3 | Satisfied | src/manual_reply.py:18; docs/support-runbook.md:8 |
| Accessible data, 4.6.1 | Satisfied | src/tickets.py:20 reads the local ticket store |
| Operator roles, 4.5.1 | Satisfied | docs/support-runbook.md:4 |
| Supplier common-mode assessment, 4.2.4 | Not applicable | No substitute AI supplier |
| Independent knowledge, 4.6.2 | Satisfied | docs/reply-rules.md:1 contains the decision rules |
| Measured TTM and capacity, 4.3.1–4.3.4 | Satisfied | docs/drills/2026-06-01.md:12 |
| AI-off, real work, unannounced frequency, 4.4.2–4.4.4 | Satisfied | docs/drills/index.md:3; latest drill was unannounced |
| Measurements and failures recorded, 4.4.5 | Satisfied | docs/drills/2026-06-01.md:12 |
| Failed-drill recovery, 4.4.6 | Not applicable | docs/drills/index.md:3 records no failed drills |
| Two competent operators, 4.5.2 and 4.5.5 | Satisfied | docs/drills/2026-06-01.md:6 records unaided performance |
| Departure re-drill, 4.5.3 | Not applicable | LIGHTS.md:18 confirms both operators remain |
| L2 recency, 4.4.1 | Failed | KLOD-4.4.1-support-drafting |
| L3 routine performance and annual review | Not applicable | No routine-performance claim; people use the path during drills |

## Portability

| Capability | Provider wiring | Chosen by configuration | Provider-specific use | Switch ever run |
|---|---|---|---|---|
| Support drafting | One adapter, src/llm/adapter.py:1 | Yes, settings.LLM_PROVIDER (src/settings.py:14) | None found | No comparison recorded |

One place to change. A switch to another supplier or a self-run model is a configuration
change plus an untested prompt; no level consequence.

## Findings

### KLOD-4.4.1-support-drafting

Status: unchanged. Severity: medium. Confidence: high.
Capability: support drafting, on Provider A. Staff can reply manually after supplier loss,
but the most recent recorded successful drill was 102 days ago.
Requirement: [4.4.1](https://keepthelightson.eu/standard.html#c-4-4-1).
Evidence: LIGHTS.md:18 identifies docs/drills/2026-06-01.md as the last successful drill.
Counterevidence: the runbook and independent manual path remain available.
Consequence: supported L1; the 90-day requirement is unmet. The existing L2 declaration has
not yet reached its 120-day expiry. Actual current manual capacity was not observed.
Next action: arrange an authorised real-work drill with AI unavailable.
Owner: Head of Support. Closure evidence: a dated successful drill meeting the shared gates.

### Human-control observations (principle 6)

KLOD-P6-support-drafting-stop. Status: unchanged. Basis: Principle 6 (informative).
Level consequence: None by itself.
Evidence: src/control.py:22 persists operator-only stop; src/drafting.py:48 rejects old-generation
results; src/manual_reply.py:18 permits manual replies. tests/test_stop.py:10 covers late results
and deliberate restart. No control gap found in these paths; no counterevidence found.
Limit: tests were inspected, not run; deployed enforcement was not observed.
Owner: Service operator. Next action: verify these cases in the deployment test environment.
Closure evidence: recorded results for stop, late outputs, manual replies and restart.

## Evidence to obtain

A new drill record would resolve KLOD-4.4.1-support-drafting. No external record is currently
needed to establish the repository coverage.

## Changes since the previous scan

Unchanged: KLOD-4.4.1-support-drafting; KLOD-P6-support-drafting-stop.
New, resolved and regrouped: none. Owner notes retained.

## Scope and limits

All project areas listed above were inspected. This was a repository review, not a drill;
no service was interrupted and no provider called. Operating records were read; the events
and deployment behaviour were not independently observed.
```

## Acting on the report

Verify citations and supply missing records. Assign unresolved findings an owner and target date;
prioritise work whose loss stops essential operations. Use `klod` for specific implementation
changes, arrange authorised drills, update `LIGHTS.md`, then rescan. Accepted risks retain their
reason, owner and review date but stay unresolved until evidence closes the gap. Review supported
levels before publishing declarations; levels belong to capabilities, not the organisation.
