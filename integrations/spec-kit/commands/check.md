---
description: Audit the implementation's AI dependencies and human takeover evidence using KLOD.
scripts:
  sh: ../../scripts/bash/check-prerequisites.sh --json --paths-only
  ps: ../../scripts/powershell/check-prerequisites.ps1 -Json -PathsOnly
  py: ../../scripts/python/check_prerequisites.py --json --paths-only
---

# Check the implementation and its evidence

## User input

$ARGUMENTS

## Load the assessment rules

Read `.specify/extensions/klod/skills/klod-check/SKILL.md`. Resolve its references and scripts
relative to that installed directory. Follow the complete skill, including classification,
coverage, runtime dependency tracing, evidence gates, report identity and required report
format. Its bundled specification is authoritative.

This is a repository assessment with the active Spec Kit feature as additional context. Do not
report a whole-repository conclusion from a feature-only inspection. If access or scope limits
inspection, mark coverage **Partial** and identify the uninspected areas.

## Relate the feature to the implementation

1. Run `{SCRIPT}` from the project root once to resolve the active feature's paths. Read any
   existing specification, plan, tasks and `klod-plan.md` from that feature directory. Do not
   infer the active feature from the newest directory. If paths cannot be resolved, disclose
   the missing feature context and continue the repository audit when its root is known.
2. Use the feature documents to identify intended behaviour and relevant changes. Plans,
   checked task boxes and declared levels are claims to verify, not evidence that the runtime
   path works. Inspect the implementation, test assertions, existing results and operating
   records. Distinguish a test present in source from a test actually run at an identified
   revision, and distinguish both from a dated human drill on real work.
3. Follow runtime dependencies through the delivered business outcome and inspect adjacent
   workflows. Development-only AI does not make a product AI-dependent. Self-run runtime AI
   needs a human-control review but receives no hosted supplier-dependence level. Apply the
   prescribed short-report rules to libraries, demos and samples.
4. Check the planned human path, usable state, permissions, shared failure exposure and AI-off
   controls against actual evidence. Preserve the distinction between L0–L3 gates and
   informative principle 6 observations. Missing drill records are missing evidence, not proof
   that no drill ever happened. Never invent an operator, date, capacity or Time to Manual.

## Report without changing the product

Write `klod_report.md` at the repository root using the bundled report format. Preserve
existing finding IDs and owner notes and reconcile previous findings. Reference the feature's
planning artifacts where useful without replacing the required report sections. Cite actual
code and evidence paths and check them before saving.

The check does not change application code, planning artifacts or `LIGHTS.md`; install
dependencies; call AI providers; run tests, services or drills; or operate an AI stop control.
Report existing test results precisely. If runtime checks or real-work evidence are missing,
identify the next checks for the implementation workflow or an authorised drill and leave the
assessment limited to what the evidence supports.

Finish with the report path, confirmed findings, missing evidence and the next actions.
Do not claim certification, legal compliance or successful human takeover from this scan.
