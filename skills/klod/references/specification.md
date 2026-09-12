# Keep The Lights On

**Version 0.1.0** · Alex Girlea · Specification text licensed CC BY 4.0 · keepthelightson.dev

---

### Don't build a business that only a model can run.

---

## Summary

For every business capability that depends on a third-party AI system, maintain a path by which
people deliver that capability without it. Document the path. Measure how long it takes to reach
first correct output. Practise it on real work under the drill conditions in section 4.4.

---

## The six principles

Design AI-powered software so people can keep essential work going when a supplier stops
serving you, or when the model itself has to be switched off.

**1. Know what stops when AI stops.**
List the work that depends on your AI supplier, such as answering customers or processing
invoices. Name who is responsible and decide what must keep running.

**2. Keep your data usable without AI.**
Save the requests, results and business rules people need in a form they can read without
your supplier. Show what is finished and what still needs doing.

**3. Build human takeover into the software.**
Provide the screens, tools and permissions people need to finish the job without AI.
Name and train the people responsible, and write instructions someone else can follow.

**4. Protect the backup from the same failure.**
Check what could stop AI and human work together: a shared login, cloud service or access
restriction. The backup needs to work through the failure you are preparing for.

**5. Prove it works with AI switched off.**
Regularly have people complete real work with AI unavailable. Measure time to the first
correct result, how much work they can handle, and for how long. Fix what fails and repeat.

**6. Keep an off switch, and the authority to use it.**
Give authorised people an independent way to stop AI from acting when its supplier fails or
its behaviour becomes unsafe. Keep the controls and information people need to take over.
For devices, machines and infrastructure, define a safe state when human operation is not
possible, and preserve safety interlocks. Practise the switch and the handover under an agreed
exercise plan.

---

## 1. Scope

1.1 This specification applies to any organisation that operates a business capability which,
in normal running, depends on an AI system it does not control.

1.2 It is written for capabilities rather than systems. The unit of analysis is the work that
has to happen, not the software that currently happens to do it.

1.3 It is deliberately narrower than business continuity management and deliberately wider than
disaster recovery. It concerns one failure mode: the supplier of an AI capability ceases to
serve you, at any notice, for any reason, and your people have to carry on.

1.4 Nothing here removes an obligation arising under law. Where this specification and a legal
duty differ, the legal duty governs. Section 7 records where the two overlap.

## 2. Definitions

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY
and OPTIONAL in this document are to be interpreted as described in [BCP 14](https://www.rfc-editor.org/info/bcp14/) ([RFC 2119](https://www.rfc-editor.org/info/rfc2119/), [RFC 8174](https://www.rfc-editor.org/info/rfc8174/))
when, and only when, they appear in all capitals.

BCP means Best Current Practice. In plain language, MUST is a requirement, SHOULD is a
recommendation that needs a stated reason to depart from, and MAY is optional. The six
principles above use none of these words and can be read without them.

The principles are design guidance. Principle 6 also addresses unsafe behaviour by a self-run
model; the numbered clauses and L0 to L3 declarations remain about supplier dependence.
An off switch or a continuity level does not establish that a system is safe to operate.
See the [human-control guide](https://keepthelightson.dev/human-control.html) for implementation
and review guidance, including systems that control physical equipment.

**Dependent capability.** A business capability whose normal operation requires an AI system
supplied by a party other than the implementer.

**Manual path.** The documented, resourced and practised means by which people deliver a
dependent capability without the AI system it normally uses.

**Time to Manual (TTM).** Elapsed time from the decision to revert until the manual path produces
its first output at the quality the business accepts.

**Manual capacity.** The share of normal volume the manual path sustains, and the period it
sustains it for. Written as a pair, for example 40% for 30 days.

**Drill.** An exercise in which the AI system is made genuinely unavailable and the manual path
is used to perform real work.

**Common-mode failure.** A single cause that disables the primary path and the fallback together.

## 3. Levels

An implementer declares a level per dependent capability, not per organisation.

| Level | Name | Condition |
|---|---|---|
| **L0** | Dark | No manual path. If the supplier stops, the capability stops. |
| **L1** | Torchlight | A manual path is documented. It has not been exercised. |
| **L2** | Generator | The manual path is exercised on a schedule against real work, and TTM and manual capacity are measured. |
| **L3** | Mains | People perform the work as a matter of routine, keeping the manual capability in regular use. |

L1 is not a safe resting place. Section 6 exists because documents rot faster than people expect.

## 4. Requirements

### 4.1 Inventory

4.1.1 An implementer MUST maintain a register of its dependent capabilities.

4.1.2 Each entry MUST record the supplier, the capability affected, the declared level, and the
name of the accountable person.

4.1.3 A capability absent from the register MUST be treated as L0.

4.1.4 The register SHOULD be reviewed whenever a new supplier is introduced, and MUST be
reviewed at least annually.

### 4.2 The manual path

4.2.1 For any capability declared L1 or above, a manual path MUST be documented in enough detail
that a competent person who did not write it can follow it.

4.2.2 The documentation MUST state what the path cannot do, and the volume at which it fails.

4.2.3 The manual path MUST NOT require the AI system it exists to replace.

4.2.4 A manual path that substitutes one third-party AI supplier for another MUST NOT be declared
above L1 unless the implementer has assessed the two for common-mode failure and recorded the
result. Suppliers sharing a jurisdiction, a compute provider, a regulator or an export-control
regime are not independent of each other for this purpose.

### 4.3 Measurement

4.3.1 For any capability declared L2 or above, the implementer MUST measure TTM and manual
capacity.

4.3.2 Both figures MUST be obtained from a drill and MUST NOT be estimated.

4.3.3 Measured figures MUST be recorded with the date of the drill that produced them.

4.3.4 A figure older than twelve months MUST NOT be relied upon in a declaration.

### 4.4 Drills

4.4.1 A capability declared L2 MUST be drilled at least once every 90 days.

> NOTE. The retention literature supports the premise of this clause strongly and the specific
> interval weakly. No study identifies 90 days as a threshold or an optimum, and this
> specification does not claim one does.
>
> What ninety days has is regulatory precedent for exactly this problem. It is the recency of
> experience interval in [14 CFR 61.57(a)(1)](https://www.ecfr.gov/current/title-14/chapter-I/subchapter-D/part-61/subpart-A/section-61.57) and in [FCL.060(b)(1)](https://www.easa.europa.eu/en/document-library/easy-access-rules/easy-access-rules-aircrew-regulation-eu-no-11782011): a pilot who has not performed
> the manoeuvre within the preceding 90 days may not carry passengers. Aviation regulators on
> both sides of the Atlantic converged on the same figure for the same question, which is
> whether somebody has done this recently enough to still be able to do it. No published
> derivation of the aviation figure was found either, so this is convergent practice rather
> than a measured result.
>
> For scale rather than for justification, [Tatel and Ackerman (2025)](https://doi.org/10.1037/bul0000481), *Psychological Bulletin*,
> pooling 1,344 effect sizes from 457 reports, estimate decay at 0.08 standard deviations per
> month for accuracy-based performance and find half of initial acquisition gains lost after
> 6.5 months of intermittent or non-use. That work covers procedural skills with a significant
> motor component. It supports the need for practice but does not establish a decay rate for
> every cognitive task covered by this specification.
>
> Note also that both aviation regulations pair the 90 day interval with **three** repetitions,
> not one. Whether this specification should follow them is an open question and a candidate for
> an early [RFC proposal](https://github.com/AlexandruGirlea/keepthelightson/tree/main/rfcs).
>
> Sectors with evidence for a different interval are invited to propose one through the [RFC process](https://github.com/AlexandruGirlea/keepthelightson/tree/main/rfcs). Notes in this specification are guidance and carry no obligation.

4.4.2 During a drill the AI system MUST be genuinely unavailable to the people performing the
work. Simulating unavailability while access remains MUST NOT be counted.

4.4.3 A drill MUST use real work, not rehearsal material.

4.4.4 At least one drill in every four MUST be unannounced.

4.4.5 A drill MUST record TTM, manual capacity, and what went wrong.

4.4.6 A drill that fails MUST be recorded as a failed drill. The capability reverts to L1 until
a subsequent drill succeeds.

4.4.7 Drills SHOULD be scheduled so that no single person is present for all of them.

### 4.5 People

4.5.1 The implementer MUST identify, by role, the people who would perform the manual path.

4.5.2 For a capability declared L2 or above, at least two people MUST be able to perform the
manual path without supervision.

4.5.3 Where the people who last performed the work unaided have left the organisation, the
capability MUST be re-drilled before its level is reasserted.

4.5.4 An implementer SHOULD record when each named person last performed the work unaided.

4.5.5 Training material MUST NOT be the only evidence offered for 4.5.2. Performance in a drill
is the evidence.

### 4.6 Retention

4.6.1 The inputs, outputs and reference data a person needs to perform the manual path MUST
remain accessible to the implementer without the AI supplier's cooperation.

4.6.2 Where an AI system holds knowledge that exists nowhere else in retrievable form, that
condition MUST be recorded as a finding against the capability, and the capability MUST NOT be
declared above L1 until it is resolved.

## 5. Declaration

5.1 An implementer MAY publish a declaration. A declaration is self-issued. There is no
certifying body and this specification does not create one.

5.2 A declaration MUST state the version of this specification, the date, the capabilities
covered, and the level claimed for each.

5.3 A declaration MUST NOT claim a level for a capability that is not in the register.

5.4 A declaration SHOULD state the date of the most recent drill for each capability at L2 or
above.

5.5 An implementer MUST NOT describe itself as conformant without qualification. Conformance
attaches to capabilities. "L2 for claims triage" is a valid statement. "KLOD conformant" is not.

## 6. Decay

6.1 A declared level expires. L2 expires 120 days after the most recent successful drill. L3
expires 12 months after the most recent review confirming routine human performance.

6.2 On expiry the capability reverts to L1 and the implementer MUST correct any published
declaration within 30 days.

6.3 Expiry is a normal event and not a failure. It exists because the property being claimed is
a live one, and live properties lapse.

## 7. Relationship to law

EU rules already require continuity measures in some sectors. High-risk AI rules also address
human oversight and safe stopping. KLOD is voluntary; the legal duties depend on the organisation,
system and jurisdiction. Applying the pattern does not by itself establish compliance.

Informative legal context, reviewed on 11 September 2026.

### 7.1 Why supplier dependence matters

The European Systemic Risk Board's [Warning of 25 June 2026, ESRB/2026/3](https://www.esrb.europa.eu/pub/pdf/warnings/esrb.warning260625_on_systemic_cyber_risks_stemming_from_frontier_ai_models~ef424708cf.en.pdf)
identifies dependence on a small number of AI and cloud providers as a resilience risk. Its
warning is a reason to examine dependencies, not a requirement to use KLOD.

### 7.2 Existing continuity requirements

These duties apply to organisations within each law's scope. NIS2 covers qualifying entities
in sectors including energy, transport, healthcare, digital infrastructure and public
administration. Check its scope and the applicable national law; sector membership alone
does not determine coverage.

| Rule | Requirement | Who is covered |
|---|---|---|
| [DORA Art 28(8)](https://eur-lex.europa.eu/eli/reg/2022/2554/oj) | Documented, tested exit plans for ICT services supporting critical or important functions, with alternatives and transition arrangements | Financial entities within DORA's scope |
| [Regulation (EU) 2022/2554](https://eur-lex.europa.eu/eli/reg/2022/2554/oj) Art 29(1)(a) | Assessment of concentration risk where a provider is "not easily substitutable" | Financial entities |
| [Regulation (EU) 2022/2554](https://eur-lex.europa.eu/eli/reg/2022/2554/oj) Art 11, Art 12 | ICT continuity policy, business impact analysis, yearly testing, backup and restoration, RTO and RPO | Financial entities |
| [Directive (EU) 2022/2555](https://eur-lex.europa.eu/eli/dir/2022/2555/oj) (NIS2) Art 21(2)(c) | Business continuity, backup management, disaster recovery, crisis management | Essential and important entities |
| [Directive (EU) 2022/2555](https://eur-lex.europa.eu/eli/dir/2022/2555/oj) Art 21(2)(d) | Supply chain security | Essential and important entities |

These laws address continuity and supplier risk. They do not prescribe KLOD or require every
AI task to have a manual equivalent.

### 7.3 Human oversight and safe stopping

[AI Act Article 14](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) requires high-risk systems to
support effective human oversight. As appropriate and proportionate, people must be able to
override outputs and interrupt operation through a stop button or similar procedure that
brings the system to a safe state. Article 26(2) requires deployers to assign oversight to
people with competence, training, authority and support.

High-risk classification follows Article 6: specified products or safety components subject
to third-party conformity assessment, and listed Annex III uses subject to the Article 6(3)
exceptions. A medical, industrial or public-sector use is not automatically high-risk.

Under Article 113 as amended by [Regulation (EU) 2026/1744](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32026R1744),
the relevant Chapter III requirements apply from **2 December 2027 for Annex III systems**
and **2 August 2028 for Annex I systems**. Check the applicable exclusions and transitional
rules for an existing system.

Oversight during operation does not establish continuity after supplier withdrawal.
Article 15(4) permits backup or fail-safe arrangements; it does not impose a universal manual path.

### 7.4 Use this in a design review

1. Identify the affected work, its users and the rules that apply to the organisation.
2. Design the required continuity and control measures: retained data, independent access,
   operator permissions, safe stopping and a usable human workflow where appropriate.
3. Test those measures and keep the results. Use the legally required procedures and intervals
   alongside the evidence needed for any KLOD declaration.

For decisions about people, also check [GDPR Article 22](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng).
It restricts solely automated decisions with legal or similarly significant effects, subject
to its exceptions and safeguards. The [Article 29 Working Party guidance](https://ec.europa.eu/newsroom/article29/items/612053)
requires meaningful human involvement by someone able to change the decision. KLOD's drill
evidence can inform a review of competence; it is not a legal definition of competence.

---

## Appendix A. Questions

This appendix is informative. Nothing in it creates an obligation.

**Is this not just disaster recovery?**

Disaster recovery restores the system. KLOD keeps the work possible while AI is unavailable,
including when supplier access is permanently withdrawn.

**Is this not just human-in-the-loop?**

Human-in-the-loop reviews a running model's output. KLOD also requires a path people can
operate independently when AI is unavailable or stopped. Reviewing AI output alone does not
demonstrate that capability (clause 4.5.5).

**We use two providers. Does that not cover us?**

Read clause 4.2.4. Two suppliers sharing a jurisdiction, a compute provider, a regulator or an
export-control regime fail together under the causes that matter most here. On 18 November 2025
a [configuration change at a single infrastructure provider](https://blog.cloudflare.com/18-november-2025-outage/) took down a large part of the web,
including services from more than one AI company. Second-sourcing can reduce exposure to one
supplier. By itself it does not establish a manual path. Clause 4.2.4 covers a documented human
operating procedure that uses a substitute; it does not waive the need for people, usable
information, a followable procedure or the remaining evidence gates. State what people can do
independently and what still relies on AI.

**We self-host an open-weights model. Does that count?**

A model you run yourself, from weights you hold, on infrastructure you control, is not an AI
system supplied by another party. A capability that runs entirely on such a model is not a
dependent capability under clause 1.1, and the numbered requirements do not grade it. The
informative human-control principle still applies to runtime AI. The same scope distinction goes
for a classifier you trained. The failure mode here is a supplier who can stop serving you, and
a model you can run has no such supplier.

Where the capability normally runs on a hosted model and a self-run model is the fallback, the
capability is dependent in normal running and section 4 applies. The self-run model can be the
manual path on the same terms as any other: documented, drilled with the hosted model genuinely
cut, measured, and staffed by people who have done it. What self-hosting does not do is keep the
skill alive in people. Record honestly what nobody could do by hand any more.

**Our provider offers an availability guarantee. Is that not enough?**

An availability guarantee covers availability. It does not cover deprecation, repricing, a
change of acceptable use policy, an export control, an acquisition, or a quality regression that
never registers as downtime. Between 5 August and 18 September 2025 [one provider's output quality degraded through three overlapping infrastructure faults](https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues) while its status page stayed
green throughout.

**Does this mean we should not automate?**

No. L3 is not the goal for every capability, and plenty of work can be automated. Identify what people could still perform and verify it before an incident.

**We are five people. Is this realistic?**

Start with a register of dependent work and responsible people (clause 4.1). Clause 4.5.2 requires two people for L2,
which is a real constraint on a very small team, and a small team may reasonably sit at L1 with
that recorded as a known finding rather than pretend otherwise.

**Who certifies this?**

Declarations are self-issued and self-published under clause 5.1. KLOD has no certifying body.

**Then is a self-declaration not worthless?**

Check the named capability, claimed level, measurements and dated drill records. An
unqualified "KLOD conformant" claim is not permitted under clause 5.5.

**We are not in the EU. Does this apply?**

KLOD can be adopted in any jurisdiction. Section 7 provides EU legal context.

**What if the manual path is far slower and far more expensive?**

Then record that. Clause 4.2.2 requires the documentation to state what the path cannot do and
the volume at which it fails, and manual capacity is written as a pair for exactly this reason.
"12% of normal volume for 60 days, at four times the unit cost" is a useful sentence. It lets
somebody decide, in advance and calmly, whether that is survivable.

**Will better and cheaper models not make this unnecessary?**

Improving capability does not address any risk in this document. A model that is better and
cheaper can still be deprecated, repriced, restricted by policy, made unavailable in your
country, or withdrawn because your company was acquired by the wrong buyer. Those are commercial
and political events, and they do not become less likely as the technology improves. If
anything, deeper integration raises the cost of each one.

---

## Changelog

### 0.1.0, 10 September 2026
- First release.
