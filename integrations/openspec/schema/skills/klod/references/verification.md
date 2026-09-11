# Verification and handoff

Select the checks relevant to the feature. Record any omitted check that limits the result.

## Acceptance evidence

| Situation | Evidence to inspect |
|---|---|
| AI operating normally | Acceptable result through the feature's actual entry point |
| Timeout, refusal or provider unavailable | Original work remains accessible and manual/reduced service can complete |
| Authorised stop | New AI work is rejected; human work remains usable |
| Late result after stop | No AI decision, overwrite or effect is accepted |
| Re-enable | Invalidated work stays invalid; only eligible new attempts run |
| Human edit during inference | The saved human decision survives late AI output |
| Duplicate or uncertain delivery | One intended effect, or an explicit unresolved state requiring reconciliation |
| Process restart | Saved work and disabled mode survive |
| Unauthorised request | Denial leaves mode, work and effects unchanged |

For external effects, inspect the destination record or local journal, not only the returned
status. Reopen storage in a fresh process when testing persistence. Queued dispatch may not
apply to a synchronous read-only feature.

## Run checks that can fail for the right reason

Use the project's tooling and deterministic provider adapters. Control delayed results with a
barrier or deferred response. Stub effects at the integration boundary while retaining the
application's authorisation and state transitions.

Check that at least one relevant negative test fails when its protection is removed, such as
the generation check for late results. Assertions about comments, filenames or success messages
do not establish the behaviour.

Use isolated data and effect sinks. Inspect changed interfaces running with representative
data, including errors and manual actions. If a dependency or runtime is unavailable, name the
unverified behaviour and the narrower checks completed. Follow a task's published evaluation
contract; leave private answer keys untouched.

## Keep three kinds of evidence separate

| Evidence | Supports | Does not establish |
|---|---|---|
| Repository inspection | A control or defect at a cited location | Deployment state or human performance |
| Isolated executable test | Observed behaviour under tested conditions | Live provider quality, hardware safety or sustained human capacity |
| Authorised operational drill | Handover and throughput on recorded real work | Performance beyond the conditions exercised |

Record commands, pass/fail results and environment limits. Do not invent dates, participants,
capacity or Time to Manual. Apply the [specification](specification.md) when declaring levels.

## Handoff

Use a short response for a small change. For a substantial change, record the following in the
project's existing documentation or a concise handoff. A generated Markdown report starts with
the [report identity block](report-metadata.md).

- **Delivered:** feature, capability and changed call sites.
- **Human operation:** control location, authorised operators, completion, reconciliation and
  restart instructions. Link the implemented interface and runbook.
- **Verified:** commands and observed results; distinguish simulation from live integration.
- **Limits:** deployment constraints, lost functionality, missing owners/capacity and each
  important part still unverified or deferred. Show unresolved failures prominently.
- **Register:** the `LIGHTS.md` entry and evidence needed for a higher level.

Plan real-work drills within agreed authorisation, scope and recovery controls. State which
records the exercise must produce; a skipped check or accepted debt remains unresolved.
