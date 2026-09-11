# Regulatory context for findings

Use only when requested or when the project establishes a relevant sector or use case.
Keep applicability conditional and consult current linked primary texts before citing a duty.
These mappings were prepared on 10 September 2026.

State the applicable condition, the requirement and the repository evidence. Do not declare
compliance, breach or enforcement risk. A repository may not establish whether an organisation
is a financial entity, an essential or important entity, or a high-risk AI deployer.

For example:

> **Regulatory context.** If the organisation is an in-scope financial entity, DORA Art 28(8)
> requires an exit strategy identifying alternatives and transition plans. No such record was
> found in the inspected repository.

Include only relevant mappings. Read alongside [specification section 7](specification.md#7-relationship-to-law).

## No manual path or recorded alternative

- [DORA, Regulation (EU) 2022/2554, Art 28(8)](https://eur-lex.europa.eu/eli/reg/2022/2554/oj):
  financial entities' exit strategies, alternatives and transition plans, including the ability
  to bring functions in house.
- [NIS2, Directive (EU) 2022/2555, Art 21(2)(c)](https://eur-lex.europa.eu/eli/dir/2022/2555/oj):
  essential and important entities' business continuity, backups, disaster recovery and crisis management.

## Supplier concentration or unassessed common failure

- [DORA Art 29(1)(a)](https://eur-lex.europa.eu/eli/reg/2022/2554/oj): financial entities'
  concentration-risk assessment where providers are not easily substitutable.
- [DORA Art 30(3)(f)](https://eur-lex.europa.eu/eli/reg/2022/2554/oj): contractual exit strategies
  and a transition period for financial entities.
- [NIS2 Art 21(2)(d)](https://eur-lex.europa.eu/eli/dir/2022/2555/oj): essential and important
  entities' supply-chain security.

## Missing drills or testing

- [DORA Arts 11 and 12](https://eur-lex.europa.eu/eli/reg/2022/2554/oj): financial entities'
  ICT continuity, business-impact analysis, at least annual testing and crisis management;
  backups, segregated restoration, redundancy and recovery objectives.
- [ISO 22301:2019, clause 8.5, “Exercise programme”](https://www.iso.org/standard/75106.html):
  a certification requirement, not a legal obligation. “Exercising and testing” is the 2012 title.

## Competence supported only by training records

- [AI Act, Regulation (EU) 2024/1689, Art 26(2)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj):
  high-risk system deployers must assign oversight to people with competence, training,
  authority and support. The Regulation does not define those four terms.
- [GDPR Art 22](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng) and
  [WP251rev.01 guidance](https://ec.europa.eu/newsroom/article29/items/612053): human involvement
  must be meaningful; the reviewer needs authority and competence to change the decision.
  Token human involvement does not avoid Article 22.

KLOD clause 4.5 uses recent unaided performance in drills as competence evidence. Do not present
that proposed test as a legal definition.

## Knowledge held only inside the model

[AI Act Art 86](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) gives people affected by certain
high-risk decisions a right to an explanation of the system's role. The duty rests with the
deployer and does not disappear with the model vendor.

## Citation checks

| Reference | Check before use |
|---|---|
| [DORA Art 32](https://eur-lex.europa.eu/eli/reg/2022/2554/oj) | Covers the oversight framework. For continuity, use Arts 11, 12, 28(8) or 29(1)(a). |
| [AI Act Art 14](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) | Concerns high-risk systems' oversight during operation; it does not require a fallback after vendor withdrawal. |
| High-risk application dates | Check the current text, including [Regulation (EU) 2026/1744](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32026R1744). This reference records 2 December 2027 for Annex III and 2 August 2028 for Annex I, replacing 2 August 2026. |
| [ISO 22301:2019](https://www.iso.org/standard/75106.html) | Does not contain RPO. RTO and MTPD occur in notes to 8.2.2; notes are guidance, not requirements. |

[ESRB Warning ESRB/2026/3, 25 June 2026](https://www.esrb.europa.eu/pub/pdf/warnings/esrb.warning260625_on_systemic_cyber_risks_stemming_from_frontier_ai_models~ef424708cf.en.pdf)
identifies dependence on a limited number of AI providers as a resilience concern. Use this
context once in a relevant summary, rather than repeating it for each finding.
