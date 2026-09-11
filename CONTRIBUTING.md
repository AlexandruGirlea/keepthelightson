# Contribute to Keep The Lights On

Share what happens when people try to keep work running without an AI supplier.

[Star the project](https://github.com/AlexandruGirlea/keepthelightson) to support
its visibility. For changes, read the [specification](spec/SPECIFICATION.md) and
[governance](GOVERNANCE.md), then choose the route below.

## Bring evidence from real work

- Share a manual path that another team can adapt.
- Record a drill: the capability, date, participants, measured Time to Manual, capacity
  and what went wrong. Remove confidential information before publishing it.
- Show where a clause is ambiguous, impractical or missing a relevant case.
- Correct a citation using the primary text and the applicable version.
- Review the skills and their installation instructions.

## Open an issue

Use the [issue templates](https://github.com/AlexandruGirlea/keepthelightson/issues/new/choose)
for a specification question, citation correction or adoption report.

For an ambiguous clause, link its number, explain both readings and describe the
work affected. For a citation correction, provide the instrument, article, paragraph
and a direct primary-source link. For a technical bug, include the steps to reproduce
it and the expected result.

## Send a small correction

Typos, broken links, informative examples, skill packaging changes and clarifications that
leave the requirements unchanged can go directly to a pull request. They need one
maintainer approval and do not require an RFC or Final Comment Period.

Keep each change focused. Explain the concrete problem, the resulting behaviour
and how you checked it. Edit the canonical source and update its bundled copies.

## Propose a requirement change

Use the [RFC process](rfcs/README.md) for changes to normative requirements,
level definitions, measurements, declaration or expiry rules, governance or the
RFC process itself. Copy the [proposal template](rfcs/0000-template.md).

## Write clearly and link the evidence

Use concrete capabilities, actions and measurements. Explain unfamiliar terms.
Prefer a dated fact and a source over a broad claim. Do not invent citations,
results, drill dates or statistics.

Use British English for project prose. Keep quotations in their original form,
identify the source and distinguish a quotation from your interpretation.

Write percentages with numerals and `%`, such as `50%`. Use everyday words and
complete thoughts. Contractions such as "doesn't" and "you'll" are welcome in guides
and explanatory prose. Explain what someone needs to do, with examples they can recognise.
Avoid slogans, strings of sentence fragments and vague phrases such as "retained
capability" when you mean what a team can still do. Keep requirements precise, and
preserve the wording of direct quotations.

The [BCP 14 keywords](https://www.rfc-editor.org/info/bcp14/) carry requirement
force in the normative text. Their meaning is defined by
[RFC 2119](https://www.rfc-editor.org/info/rfc2119/) and
[RFC 8174](https://www.rfc-editor.org/info/rfc8174/). Keep the explanatory definition
in [section 2 of the specification](spec/SPECIFICATION.md#2-definitions).

For legal references, read the primary text, including amendments, and state the
scope and reference date. [Section 7](spec/SPECIFICATION.md#7-relationship-to-law)
records the legal context and its sources.

## Check a change

Use Python 3.10+ from the repository root. The package check uses only the standard library:

```sh
python3 .github/scripts/check_package.py --sync
python3 .github/scripts/check_package.py
```

The first command synchronises bundled references, licence copies and release labels. The
second checks the repository layout, local Markdown links, skill portability and agreement
between source files and their copies. GitHub Actions runs the same check. These checks do
not execute an AI assistant, assess model quality or establish operational readiness.

Edit these canonical sources:

| Content | Source |
|---|---|
| Specification and six principles | `spec/SPECIFICATION.md` |
| Shared human-control guidance | `skills/klod/references/human-control.md` |
| Shared report identity guidance | `skills/klod/references/report-metadata.md` |
| Shared report metadata helper | `skills/klod/scripts/report_metadata.py` |
| Prose licence | `LICENSE-SPEC.md` |
| Skill-specific instructions and references | The relevant file under `skills/klod/` or `skills/klod-check/` |
| Spec Kit commands and workflow hooks | `integrations/spec-kit/` (excluding generated `skills/` and licence copies) |
| OpenSpec schema, templates and installer | `integrations/openspec/` (excluding generated `schema/skills/` and licence copies) |

Each skill's `specification.md` and `LICENSE-SPEC.md` are bundled copies. The three shared
skill files above are copied from `klod` to `klod-check`. The README's six principles come
from the specification. Commit source changes and updated copies together.

The integration packages also bundle both skills. Edit the canonical skill files and run
`check_package.py --sync` to refresh every copy. Their READMEs are also the website setup
guides, so update setup instructions there. Build reproducible ZIP files with
`python3 .github/scripts/build_integrations.py --output .cache/integrations`.
The same synchronisation command updates both adapter versions from `apm.yml`.

Run the public integration tests with `python3 -m unittest discover -s .github/tests`.
For upstream CLI compatibility checks, use the versions and commands recorded in each
integration's README. A new integration can be distributed before a community catalog
accepts it. Follow the upstream submission process after testing; describe it as
independently maintained and do not imply endorsement.

For a helper change, run it against a temporary repository and record the command and result.
For instruction changes, describe a representative task, the observed behaviour and any
limits. Do not present a package check as evidence of live assistant performance. Reports
start with the [report identity block](skills/klod/references/report-metadata.md).

## Release versions

The specification version is the `**Version x.y.z**` line in `spec/SPECIFICATION.md`.
The skills package version is `version:` in `apm.yml`. Change the relevant version, record
the change in `CHANGELOG.md`, and run the two commands above. Specification changes also
belong in the specification's changelog. Keep `date-released` in `CITATION.cff` accurate for
the specification release.

A release tag uses the package version, for example `v0.1.0`. Installation commands pin that
tag. Follow [governance](GOVERNANCE.md#7-versioning-the-specification) when deciding what kind
of specification change is being made.

## Sign off and retain the licences

Every commit needs a [Developer Certificate of Origin 1.1](https://developercertificate.org/)
sign-off:

```sh
git commit -s
```

The sign-off confirms your right to submit under the project licence.

Specification, skill and documentation contributions use [CC BY 4.0](LICENSE-SPEC.md).
Original scripts use [MIT](LICENSE-CODE.md). Retain third-party
notices. The possible standards-submission terms are in
[section 10 of governance](GOVERNANCE.md#10-the-long-path-towards-a-standards-body);
a submission requires an accepted RFC.

The [Code of Conduct](CODE_OF_CONDUCT.md) applies to contributors and maintainers.
