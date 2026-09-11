---
description: Add human takeover requirements and acceptance checks to the active Spec Kit feature.
scripts:
  sh: ../../scripts/bash/check-prerequisites.sh --json --paths-only
  ps: ../../scripts/powershell/check-prerequisites.ps1 -Json -PathsOnly
  py: ../../scripts/python/check_prerequisites.py --json --paths-only
---

# Plan a feature people can take over

## User input

$ARGUMENTS

## Scope

This command prepares the active feature before implementation. It does not implement the
feature, run a drill, assign a readiness level or audit the whole repository. Preserve existing
requirements, accepted decisions, owner notes and unrelated work.

## Locate the feature and load KLOD

1. Run `{SCRIPT}` from the project root once. Read `REPO_ROOT`, `FEATURE_DIR`, `FEATURE_SPEC`,
   `IMPL_PLAN` and `TASKS` from its JSON output. Use these resolved paths; do not guess a feature
   from a branch name or choose the newest directory. If resolution fails or the active feature
   is ambiguous, report that and request the feature selection before editing anything.
2. Read the resolved specification and implementation plan, the project's constitution and
   relevant application code. If the specification or plan is missing, explain which prerequisite
   is missing and direct the user to `__SPECKIT_COMMAND_SPECIFY__` or
   `__SPECKIT_COMMAND_PLAN__` as appropriate. Stop without creating a substitute feature.
3. Read `.specify/extensions/klod/skills/klod/SKILL.md` and resolve its referenced files relative
   to that skill directory. Apply its boundary, acceptance, implementation-decision and
   verification guidance to **planning only**. Its implementation and handover steps describe
   future work; do not execute them during this command.
4. Establish whether this feature uses hosted or self-run AI at runtime. Development-only use
   of a coding agent does not make the product dependent on AI. If there is no runtime AI,
   report that KLOD runtime takeover planning is not applicable and leave the feature unchanged.

## Prepare the human path

1. Identify the essential work, dependency, failure being covered and authorised operators.
   Trace existing inputs, state, effects and access controls. Mark unknown owners, tolerable
   delays and capacity targets as unresolved; do not invent business decisions.
2. Specify normal, AI-unavailable and operator-stopped behaviour. Include a person completing
   the essential work through an actual interface, with the required information and permissions.
   Explain any reduced service or intentionally suspended optional work.
3. Plan the changes needed to preserve usable inputs and work state, protect the human path
   from shared failures, isolate the provider and model behind a configurable adapter, and
   enforce an authorised AI stop at the point where results and actions are accepted.
   Account for in-flight work, late results, restarts and human edits where applicable.
4. Define observable acceptance checks using isolated data and deterministic provider failures.
   Include the normal path, provider outage, denied actions, authorised stop and human
   completion; add concurrency and external-effect checks when the feature needs them.
   Separate these software checks from a future authorised human drill on real work.
   Tests and demonstrations cannot establish L2 or L3. Self-run AI receives human-control
   consideration but no hosted supplier-dependence level.

## Update the planning artifacts

1. Create or update `klod-plan.md` within the resolved `FEATURE_DIR`. Begin with the report
   identity block required by the bundled KLOD skill, using its metadata helper for local
   facts and a reliable host source for the active model. Include the feature scope, decisions,
   required changes, acceptance checks, unknowns and evidence still needed.
2. Add a concise `KLOD human takeover` section to the resolved specification and plan, linking
   to `klod-plan.md`. Put essential user-visible failure requirements and acceptance scenarios
   in the specification; put implementation choices and test work in the plan. Preserve the
   existing structure and reconcile any conflicts explicitly.
3. If `TASKS` already exists, add or update the corresponding incomplete tasks in its existing
   format, preserving task IDs and completion states. Otherwise, leave task generation to
   `__SPECKIT_COMMAND_TASKS__`; the updated specification and plan must contain enough detail
   for it to include the KLOD work. Repeat runs update the same sections rather than duplicating
   requirements or tasks.
4. Summarise changed paths, required implementation work and unresolved decisions. Recommend
   `__SPECKIT_COMMAND_TASKS__` next if tasks have not been generated. After implementation,
   use `__SPECKIT_COMMAND_KLOD_CHECK__` to review the code and available evidence.
