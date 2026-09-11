# Governance

Decision rules, maintainer responsibilities and appeals.

This document describes project procedures, not requirements for KLOD implementations.
Words such as "must" and "should" carry their ordinary English meaning here.

Governance version 1.0, 10 September 2026. Changes to this document follow the process it
describes.

---

## 1. Current status

The project has one maintainer: Alex Girlea ([girlea.ro](https://girlea.ro)).

## 2. What this document covers

- `spec/SPECIFICATION.md`, the normative text
- `rfcs/`, proposals to change it
- `GOVERNANCE.md` and `CONTRIBUTING.md`, including the process described here
- `skills/`, the implementation and repository review instructions

## 3. Roles

Participation is open to anyone.

**Contributor.** Anyone who opens an issue, sends a pull request, reviews an RFC or reports a
drill result. An organisation contributes through a named person. Contributors keep the copyright
in what they write and license it to the project on the terms in `CONTRIBUTING.md`.

**Maintainer.** A contributor with commit rights and the duties that come with them: reviewing
proposals, determining whether consensus exists, running Final Comment Periods, preparing releases,
answering appeals in writing, and keeping the decision record public and legible. Editorial work
(clause numbering, the changelog, formatting) is a maintainer task and not a separate role.

Maintainers hold no authority over what the specification says beyond the process in section 5.

## 4. Maintainers

| Maintainer | Maintainer since | Scope |
|---|---|---|
| Alex Girlea | 2026-09-10 | All |

### 4.1 Becoming a maintainer

- A sustained record of contribution over at least three months, visible in the repository.
- Either one accepted RFC, or a comparable body of review work on other people's proposals.
- Demonstrated willingness to say no to a change, including their own.

The process: an existing maintainer nominates, or a contributor nominates themselves, in a public
issue. Comments stay open for 14 days. Appointment needs the approval of every sitting maintainer.
Objections raised during the 14 days are answered in writing on the issue, whether or not they
change the outcome.

Balance safeguard: where two or more maintainers are employed by the same organisation, that
organisation's approvals count once towards any quorum in section 5. This limits one employer's
influence over decisions.

### 4.2 Leaving

A maintainer may resign at any time by sending a pull request against the table above. A
maintainer inactive for 12 consecutive months is moved to emeritus by the others, and restored on
request without a new nomination. Removal against a maintainer's wishes needs every other
maintainer and a public record of the reason, and is available only for a breach of the code of
conduct or for acting deliberately against the project.

With one maintainer, use the continuity process in section 9.

## 5. How decisions are made

The default is consensus reached in public. Formal approvals confirm the decision after review.
[PEP 13](https://peps.python.org/pep-0013/) describes the approach:

> The council should look for ways to use these powers as little as possible. Instead of voting,
> it's better to seek consensus.

Consensus here takes the meaning it has in Annex II point 3(b) of [Regulation (EU) No 1025/2012](https://eur-lex.europa.eu/eli/reg/2012/1025/oj),
because that is the test a specification is eventually measured against:

> Consensus means a general agreement, characterised by the absence of sustained opposition to
> substantial issues by any important part of the concerned interests and by a process that
> involves seeking to take into account the views of all parties concerned and to reconcile any
> conflicting arguments. Consensus does not imply unanimity.

### 5.1 Ordinary changes

Typographical fixes, broken links, clarifications that do not alter what conforms, new informative
examples, and skill packaging changes are merged on one maintainer approval with no Final Comment Period. See
`CONTRIBUTING.md` for the full boundary.

While there is one maintainer, that person may merge their own editorial changes. Each such commit
is listed in the release notes.

### 5.2 Changes that need an RFC

Anything that changes what the specification requires, what a level means, how a measurement is
taken, what a declaration asserts, or how this project is governed. The list is in
`rfcs/README.md` and it is the operative one.

### 5.3 The quorum

An RFC is accepted when all of the following hold.

1. It has been in Final Comment Period for the full period set in 5.4, and that period has
   elapsed.
2. It carries approvals from at least two maintainers who are not the author, and who are not
   employed by the same organisation as each other or as the author.
3. Every objection has been answered in writing, and the maintainers judge that consensus exists
   in the sense set out at the head of this section. Consensus does not require unanimity, and it
   is not reached while substantial opposition is still standing.

**Transitional rule, in force while the project has fewer than three maintainers.** Condition 2 is
replaced by: approval from every sitting maintainer, plus written reviews posted in the pull
request from at least two contributors who are neither the author nor a maintainer, at least one
of whom has applied the specification to a capability they are responsible for. Final Comment
Periods are doubled. External reviews provide scrutiny until the ordinary quorum can be met.

### 5.4 Final Comment Period

A fixed window, announced in the RFC pull request and in a pinned issue on the tracker, during
which anyone may object.

| Kind of change | Period | While fewer than three maintainers |
|---|---|---|
| Governance, informative material, a new or changed SHOULD or MAY | 14 days | 28 days |
| Anything that changes what a published declaration means | 28 days | 56 days |

The second row covers adding, removing or tightening a MUST, redefining a level, changing how Time
to Manual or manual capacity is measured, changing the drill rules, and changing sections 5 or 6
of the specification.

If the normative text changes substantively during the period, the clock restarts. Editorial fixes
do not restart it. Any maintainer may extend the period once by the same length again; that is the
first step of section 6 and it is not a rejection.

### 5.5 Objections and appeals

An objection is sustained when it is written down, addresses the substance, and is restated after
being answered. A maintainer answers every sustained objection in writing before the RFC can be
accepted. Answering it is required. Agreeing with it is not.

Any decision may be appealed by opening an issue labelled `appeal`. Maintainers who did not take
the decision answer in writing within 30 days. Where every maintainer took the decision, they
answer anyway, and the answer is published. This mirrors clause 2.2 of the [Community Specification Governance Policy 1.0](https://raw.githubusercontent.com/CommunitySpecification/1.0/main/05-governance.md).

### 5.6 The record

Every decision happens in an issue or a pull request that anyone can read without an account.
Rejected RFCs are closed, never deleted, and stay readable with their reasoning intact. Nothing is
decided in a private channel; where a conversation starts somewhere else, it is summarised into
the relevant issue before it counts for anything.

## 6. Deadlock

Without consensus, the current text remains in place.

1. The Final Comment Period is extended once, by the same length again, at any maintainer's
   request.
2. If the objection still stands, the RFC returns to Review. The author may revise it, split it,
   or withdraw it.
3. An RFC that has sat in Review for 12 months with no route to consensus is closed as Rejected,
   with the reason recorded as "no consensus".
4. A rejected RFC can be reopened when there is new evidence: a drill result, a change in the law,
   an implementation report. Reopening on the same arguments is refused with a link to the
   original.

There is no casting vote and no individual who can break a tie. Without consensus, the proposal
must be revised or the current text remains in place.

## 7. Versioning the specification

Apply [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) to the document. Read "public API"
as "what a conformance declaration means".

**MAJOR.** Any change that could make a currently valid declaration invalid, or that changes what
it asserts. Adding a MUST. Tightening a threshold, for example moving the drill interval from 90
days to 60. Redefining a level. Changing how Time to Manual is measured. Removing a clause.

**MINOR.** New requirements that no existing declaration can fail against: a new SHOULD or MAY, a
new optional clause, a new informative section, a new worked example.

**PATCH.** No change in meaning. Typographical corrections, dead links, wording that clarifies
without altering what conforms, and fixes to the informative citations in section 7.

Where the choice between MINOR and MAJOR is arguable, use MAJOR.

**Before 1.0.0.** The current specification version is stated at the head of
`spec/SPECIFICATION.md`. The skills package is versioned separately in `apm.yml` and carries the
release tag, so a packaging fix can ship without the specification changing. Until the
specification reaches 1.0.0, a release may change anything, including normative requirements.
The rules above are followed as practice rather than offered as a promise, and section 8 says
what 1.0.0 would take.

**Clause identifiers.** Numbers such as 4.4.4 are the citation unit and are stable within a major
version. A clause removed in a major version has its number retired and never reused. 

**Immutability.** Each published version keeps a permanent location and is not edited after
release. Corrections go into the next version, with the changelog saying what moved.

**Declarations name a version.** Clause 5.2 of the specification already requires this. A new
release does not retroactively invalidate a declaration made against an earlier one.

## 8. What "stable" would mean

Release 1.0.0 requires:

- Three or more maintainers, not all employed by the same organisation.
- At least five published declarations from organisations unconnected to the maintainers,
  covering more than one sector, each reporting a Time to Manual figure taken from a drill rather
  than estimated.
- At least one failed drill written up in public.
- No change to any normative clause for 180 days.
- Every citation in section 7 of the specification re-verified against the primary text within the
  preceding 90 days.
- The process in section 5 exercised at least once on an RFC that was genuinely contested.

After 1.0.0, major versions should be rare and each one ships with a migration note saying plainly
what a declaration holder has to redo. Two major versions inside twelve months would be a failure
of this process and would be explained in public as one.

## 9. Continuity

- The specification is one markdown file in a git repository. Every clone is a complete copy with
  full history. Reading or maintaining the Markdown does not require a running service.
  Each skill includes the references and helper it needs. The package check and synchronisation
  command use Python's standard library and do not depend on a hosted service.
- The text is licensed CC BY 4.0. Anyone may fork it, revise it and publish the result, with
  attribution, without asking permission.

**Dormancy.** If no maintainer responds to an open issue or pull request for 180 consecutive days,
the project is dormant. Any contributor may say so, in an issue. If there is still no response 30
days after that, contributors may continue the work in a fork.

## 10. The long path towards a standards body

A standards-body submission requires an accepted RFC. Relevant routes include public
consultations, a national mirror committee or a liaison with
[CEN-CENELEC JTC 21](https://www.cencenelec.eu/areas-of-work/cen-cenelec-topics/artificial-intelligence/).

**Rights for a later submission.** Contributions are accepted on the basis that the project may one
day submit the specification, or parts of it, to a standards development organisation, and that
contributors grant the copyright rights needed to make that submission. This mirrors clause 4.5 of
the [Community Specification Governance Policy 1.0](https://raw.githubusercontent.com/CommunitySpecification/1.0/main/05-governance.md). No submission will be made without an
accepted RFC.

**Licensing.** The specification text is CC BY 4.0. CC BY says nothing about patents, and Annex II
point 4(c) expects intellectual property essential to implementation to be licensed on (fair)
reasonable and non-discriminatory terms, with royalty-free licensing expressly permitted. If the
project ever pursues identification under Article 13 of [Regulation (EU) No 1025/2012](https://eur-lex.europa.eu/eli/reg/2012/1025/oj) or a CEN
Workshop Agreement, moving to a licence with an express patent grant, such as the [Community Specification License 1.0](https://spdx.org/licenses/Community-Spec-1.0.html), is likely to be necessary. That would be an RFC, and a major version.

## 11. Changing this document

Through the same RFC process. Final Comment Period of 14 days, doubled while there are fewer than
three maintainers, and the quorum in 5.3. No maintainer may amend it alone.

The transitional quorum in section 5.3 also applies to governance changes.
