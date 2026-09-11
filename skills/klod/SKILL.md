---
name: klod
license: CC-BY-4.0, see references/LICENSE-SPEC.md
metadata:
  author: Alex Girlea
  homepage: https://keepthelightson.eu
description: Build or change AI features with a usable human path and an authorised AI-off control. Use for AI integrations, manual work queues, emergency takeover and LIGHTS.md entries. Human-control guidance applies to hosted and self-run runtime AI; supplier-dependence levels apply only to hosted AI. Use klod-check for repository audits.
---

# Build AI features people can take over

Deliver the requested feature with an answer to: **if AI becomes unavailable or unsafe,
how does a person stop it and finish the essential work?** Use the existing stack and keep
the change within the requested feature. An accepted L0 prototype is a valid outcome when
its dependency and next improvement are explicit.

The [specification](references/specification.md) governs supplier-dependence levels.
Self-run AI needs human-control consideration but has no supplier-dependence level.
Development-only AI does not make the product dependent.

## 1. Establish the work and its boundary

Trace the feature's entry points, provider adapters, workers, stored inputs and downstream
effects through to the delivered result. Follow wrappers to their suppliers and inspect
adjacent call sites the change could affect.

Identify the business capability, essential outcome, failure being covered, authorised
operators, required information and permissions. Record tolerable delay and minimum capacity
only when the user or existing records establish them. Leave unknown owners and targets
explicit; keep consequential actions inactive until authority and operating state are agreed.

## 2. Choose the fallback and define acceptance

Describe normal, AI-unavailable and operator-stopped behaviour before coding, including work
already in flight. Specify an observable outcome, such as an operator editing and sending a
saved reply with the provider blocked.

Choose a usable manual path, slower service, priority subset or explicit suspension of optional
work. State lost functionality and capacity limits. A second provider alone does not establish
human capability; a safe shutdown does not mean the business continues.

For stateful work, retries or external effects, read
[implementation decisions](references/implementation.md). For an AI-off switch or consequential
actions, read the [human-control guide](references/human-control.md). Preserve independent safety
interlocks and approved safe states for equipment; do not invent domain operating procedures.

## 3. Implement both paths through to completion

Retain the inputs, rules and state people need without the supplier. The manual interface must
show pending, completed and uncertain work and let an authorised person finish it. Preserve
existing access controls, tenant boundaries and retention rules; do not expose credentials or
keep unnecessary sensitive data.

Put AI behind one replaceable adapter, with the provider and model chosen by configuration,
so that a switch of supplier is a setting and not a rewrite; read
[keep the model replaceable](references/provider-portability.md) for what does not travel
between providers. Enforce the adapter's mode where results and effects are accepted:
an authorised stop blocks new AI work and obsolete queued or late output. Keep the human path
usable, persist the stop across restarts and require deliberate human re-enablement. Protect
human edits and reconcile uncertain delivery before retrying.

Use concurrency controls appropriate to the deployment. Identify adjacent workflows that
remain dependent after this change.

## 4. Exercise failure behaviour and inspect the result

Read [verification and handoff](references/verification.md). Exercise the normal path, provider
failure, authorised stop and human completion through the application's entry points. For
asynchronous work or external effects, include late results, restart, conflicting edits and
duplicate delivery. Denied actions must leave state and effects unchanged.

Use isolated data, deterministic provider adapters and local effect sinks. Inspect saved
results and effects; inspect a changed interface running with representative data. Fix observed
failures and rerun the affected checks. Record precisely which runtime or integration checks
could not run.

Small tasks stay sequential. Larger changes may use at most four agents: one coordinator and
up to three workers with explicit areas and no nested delegation. The coordinator verifies
the integrated implementation and tests.

## 5. Record and hand over

Update the affected `LIGHTS.md` entry, preserving owner notes and unrelated entries. Record
supplier, capability, accountable person, supported level, manual path, limits and missing
evidence. If no register exists, create one using specification section 4.1.

Unit tests and demonstrations do not establish L2. It requires a drill on real work with AI
unavailable; L3 requires current routine human-performance evidence and its other gates. Live
drills need the user's authorisation, agreed scope and recovery controls. Never invent drill
dates, people, capacity or Time to Manual.

Finish with the delivered feature, human operating instructions, checks and results, and
remaining limits. Use the [handoff format](references/verification.md#handoff) for substantial
changes. Whole-repository assessments and `klod_report.md` belong to `klod-check`.

Every Markdown design or implementation report starts with the
[report identity block](references/report-metadata.md): project name, sanitised Git origin or
local-project status, revision, exact runtime model or unavailable reason, and timestamp with
timezone. Use the [metadata helper](scripts/report_metadata.py) for local facts; obtain the
active model identity from the host.
