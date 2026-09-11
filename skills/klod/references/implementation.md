# Implementation decisions

Use these patterns for retained work, asynchronous processing or external effects. Fit them
to the existing architecture and the failure being covered.

## Pick a path people can actually use

| Work | Fallback | Required behaviour |
|---|---|---|
| Optional summary or suggestion | Read and edit the original material | AI errors do not block opening, editing or exporting |
| Support reply or invoice processing | Saved work queue with human completion | Context, rules, permissions and delivery work without the provider |
| High-volume triage | People handle a priority subset; queue or suspend the rest | State selection rules, delay, ownership and capacity limits |
| Machine control | Approved manual mode or safe state | Independent controls, qualified operators and preserved interlocks |

An error message, second model or unstaffed queue is not a working manual path. State any
shortfall against required volume; do not invent measured capacity.

## Trace one work item end to end

Store the original input or authorised durable reference, rules, current state, accepted result
and reconciliation history separately from the model request. AI and human completion should
use the same business rules. Keep those rules readable outside the prompt.

```text
request -> durable work item -> AI proposal -> validation/review -> accepted result -> delivery
                           -> human completion ----------------^
```

If adding a queue changes a synchronous feature, define the new response and waiting behaviour.
Inputs and status must survive the covered outage; an export available only through the failed
supplier is not independent.

## Control changes at the place that accepts effects

Identify the boundary that saves a decision, sends a reply or dispatches a command. For
asynchronous work, an authority epoch or generation can invalidate obsolete attempts:

1. An authorised stop atomically disables AI and advances its generation in durable state.
2. Each job retains that generation and its input version.
3. Before accepting a result or dispatching an effect, check current mode, generation, input
   version, authority and whether the item was already completed.
4. Re-enabling AI never restores an old generation. Reconcile outstanding work before allowing
   deliberate new attempts; provider recovery and process restart do not grant authority.

Make the check and state change atomic through a transaction, conditional update or serialised
worker. State can change between a separate check and a later write. Multiple processes need
shared control state and enforcement at every consumer; an in-memory lock covers only its own process.

Define when the stop is acknowledged and which already-dispatched actions need reconciliation.
Cancelling a local task cannot recall an accepted external effect. For independent controls
and physical equipment, read the [human-control guide](human-control.md).

## Preserve human decisions and uncertain outcomes

Distinguish pending, proposed, accepted, delivered, cancelled and uncertain work where needed.
A human edit invalidates proposals based on older input. Retries must not overwrite that edit
or duplicate delivery.

Give external actions stable IDs. Use destination idempotency or a transactional outbox where
available. A timeout after dispatch leaves an unknown outcome; retain it and require authorised
reconciliation with recorded evidence before retrying. Do not relabel it “not sent.”

Use the application's real identity system and preserve account/tenant boundaries. Deny
unauthorised stop, enable and manual actions without changing state or effects. Client-supplied
roles are not authentication; identify simulated roles as test fixtures only.

## Fit deployment and operation

Control state must be accessible without the model. If it is missing or corrupt, use the agreed
safe state, never silently enable AI. Equipment may need a safe hold rather than a power cut.

Document how operators find work, stop AI, reconcile actions, finish manually and restart.
State process/concurrency limits, storage durability, access requirements and shared failures,
including any identity service the human path still needs.
