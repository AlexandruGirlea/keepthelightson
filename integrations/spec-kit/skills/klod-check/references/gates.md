# Evidence gates

A gate is one condition a capability must meet, with evidence, before a level can be supported.
Apply every gate per capability against the [specification](specification.md). Record
**satisfied**, **failed**, **evidence missing** or **not applicable**. Continue after a failed
gate; apply the strictest limit when deciding the supported level.

## A usable path: L0 or L1

All five rows must hold for L1. An unregistered capability is L0. Missing evidence leaves L1
unestablished; it does not prove no external process exists.

| Evidence | Clauses |
|---|---|
| Supplier, capability, declared level, accountable person | 4.1.1, 4.1.2, 4.1.3 |
| Followable instructions and explicit capacity limits | 4.2.1, 4.2.2 |
| Manual path works without the AI being replaced | 4.2.3 |
| Inputs, outputs and reference data accessible without the supplier | 4.6.1 |
| Manual operators identified by role | 4.5.1 |

An overdue register review (4.1.4) is a separate finding; an existing entry does not disappear.

Supplier failover alone establishes no human path. If a documented human procedure uses a
substitute supplier, all L1 gates still apply. State what people can do independently and what
still requires the substitute; 4.2.4 adds the common-mode assessment for higher levels.

## Requirements shared by L2 and L3

| Evidence | Clauses |
|---|---|
| Common-mode assessment when substituting a second AI supplier | 4.2.4 |
| No necessary knowledge held only inside AI | 4.6.2 |
| Dated TTM and capacity measured from a drill, within twelve months | 4.3.1–4.3.4 |
| AI unavailable; real work; at least one in four drills unannounced | 4.4.2–4.4.4 |
| Drill records include measurements and failures | 4.4.5 |
| A failed drill followed by a successful drill | 4.4.6 |
| Two people demonstrate unsupervised performance, beyond training records | 4.5.2, 4.5.5 |
| Re-drill if the people who last performed the work have left | 4.5.3 |

L3 does not waive measurements, competence, independence or failed-drill recovery. Report
SHOULD recommendations, such as rotating participants, separately from mandatory gates.

## L2: exercised fallback

Require all shared gates and a successful drill within 90 days. At 91–119 days, the 90-day
requirement is unmet even if the existing declaration has not expired. At 120 days, L2 expires
to L1. Correct published claims within 30 days of expiry (4.4.1, 6.1, 6.2).

## L3: routine human performance

Require independent human performance during ordinary work, a review confirming it within
twelve months, and all shared gates. Reviewing AI output alone does not qualify. L3 does not
use L2's 90-day schedule, but still requires current drill measurements and competence evidence.
An expired routine-performance review reverts the declaration to L1 until renewed; do not
substitute L2 automatically.

## Missing evidence and accepted risk

Keep **declared**, **supported by records** and **not established** distinct. Mark unavailable
records `EVIDENCE-NOT-IN-REPO` and name what to obtain. Treat dated records as evidence of a
claim, not independent observation of the event. Accepted risk stays unresolved and never
raises a level.
