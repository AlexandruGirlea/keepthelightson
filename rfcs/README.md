# RFCs

Substantial changes to the Keep The Lights On specification go through a written proposal, in
public, with a fixed comment period and a stated decision rule. Small changes do not.

RFC means Request for Comments. The proposal records the problem, the proposed wording,
alternatives and effects on existing declarations. 

[GOVERNANCE.md](../GOVERNANCE.md) defines the decision rule, quorum, comment periods and appeals.
This file explains how to submit and revise a proposal.

---

## When you need an RFC

An RFC is required for any change that alters what the specification requires or what a declaration
made against it means:

- adding, removing or altering a normative requirement (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY)
- redefining a level, adding one, or changing the condition attached to one
- changing the definition or the measurement of Time to Manual, manual capacity, a drill, a
  dependent capability, a manual path or a common-mode failure
- changing the declaration rules in section 5, or the expiry rules in section 6
- changing the scope in section 1, so that the specification starts or stops applying to somebody
- changes to `GOVERNANCE.md`, to this process, or to the RFC template

## When you do not

Send an ordinary pull request for:

- typographical fixes, grammar, dead links, formatting
- wording that clarifies an existing requirement without changing what conforms to it
- new examples, worked cases and translations
- corrections to the informative citations in section 7 of the specification
- informative material in the top-level README and skill references, subject to the meaning test below

The boundary is meaning. If the set of things that conform is the same before and after your
change, it is not an RFC. If you are unsure, open an issue to establish the scope before writing
the proposal.

## Numbering

While a proposal is open, its file is `rfcs/0000-short-hyphenated-title.md` and its Number field
reads `0000`.

When an RFC is accepted, the maintainer merging it renames the file to the number of its pull
request, zero-padded to four digits, and sets the Number field to match. For example, a proposal
accepted from pull request 42 could become `rfcs/0042-unannounced-drill-ratio.md`.

Numbers are never reused. A rejected or withdrawn proposal keeps the number of its pull request
even though no file is ever merged for it, so "RFC 39 was rejected" always points somewhere real.

## Lifecycle

| Status | What it means | Who moves it |
|---|---|---|
| **Draft** | Being written. The pull request may be open as a draft, or not exist yet. | Author |
| **Review** | Open for comment. Maintainers and anybody else read it, argue with it, and the author revises. There is no time limit on this stage and no obligation on anyone to respond. | Author opens, anyone comments |
| **Final Comment Period** | The text is settled enough to decide on. A fixed window during which anybody may object, announced in the pull request and in a pinned issue. Lengths are in section 5.4 of `GOVERNANCE.md`. | A maintainer |
| **Accepted** | The period elapsed, the quorum in section 5.3 of `GOVERNANCE.md` was met, and no sustained objection was left unanswered. The RFC is merged. | Maintainers |
| **Rejected** | Not proceeding. The pull request is closed with the reason written down, and stays readable. Record the decision reason. | Maintainers |
| **Withdrawn** | The author has stopped pursuing it. Closed, still readable.  | Author |
| **Final** | The specification change has been merged and released in a numbered version. The status line records it, for example `Final (0.4.0)`. | Maintainer cutting the release |
| **Superseded** | A later RFC replaced it. Both headers are updated: this one gains a Superseded-by, the new one gains a Supersedes. | Maintainers |

### How the states work

**Review has no deadline.** An RFC can sit in Review indefinitely while it is being improved. It
does not expire quietly. After 12 months with no route to consensus a maintainer closes it as
Rejected with the reason "no consensus", per section 6 of `GOVERNANCE.md`.

**The Final Comment Period is for objections, not for discovery.** Substantive revision belongs in
Review. If the normative text changes substantively during the period, the clock restarts.
Editorial fixes do not restart it.

**Accepted is agreement in principle, not a change to the specification.** Merging the RFC records
that the proposal has been agreed. A separate pull request carries the text into
`spec/SPECIFICATION.md`, with clause numbers assigned and the changelog updated. That pull request
can raise problems the RFC missed, in which case it goes back.

**Implementation.** Acceptance assigns no implementer, deadline or priority. An unimplemented
proposal remains Accepted.

**Rejected is not deleted.** Closed proposals stay public with their reasoning. A rejected RFC can be reopened
when there is new evidence: a drill result, a change in the law, an implementation report. New
arguments about the same evidence are not new evidence.

## How to file one

1. Optionally open an issue to discuss the idea before writing a full proposal.
2. Copy `rfcs/0000-template.md` to `rfcs/0000-short-hyphenated-title.md` and fill it in. Every
   section, including Drawbacks. Delete the guidance text.
3. Open a pull request. Its number becomes the RFC number if it is accepted.
4. Respond to comments. 
5. When the text is settled, ask a maintainer to move it to Final Comment Period. They may decline
   and say why.
6. Wait out the period. Answer objections. Silence at the end of a Final Comment Period is a valid
   outcome and it means acceptance, provided the quorum is met.

Keep the proposal specific about the change, the evidence behind it and the cost to implementers.
