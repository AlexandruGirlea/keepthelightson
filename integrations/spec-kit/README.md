# KLOD for Spec Kit

Add human takeover requirements to a Spec Kit feature, then review the implementation with
KLOD. The extension bundles the same open-source `klod` and `klod-check` skills used on their
own. No separate APM installation is needed for this extension.

For an AI invoice feature, for example, KLOD adds the work needed for an authorised person
to find unfinished invoices, inspect the saved information and finish processing them when
AI is unavailable. It also plans the stop controls and failure checks that make that path usable.

## Install

Use a project already initialised with Spec Kit. Compatibility was checked with
[Spec Kit v1.0.6](https://github.com/github/spec-kit/releases/tag/v1.0.6); the extension accepts
versions `>=1.0.6,<2.0.0`. Other versions in that range have not been tested.

If you are starting a new Spec Kit project, install the tested CLI and initialise it first:

```bash
uv tool install specify-cli==1.0.6
specify init my-project --integration claude
cd my-project
```

Choose your actual coding agent instead of `claude` when initialising. Skip these commands
for a project that already uses Spec Kit.

Install the extension archive from your project root:

```bash
specify extension add klod --from https://keepthelightson.eu/downloads/integrations/klod-spec-kit.zip
specify extension list
```

Spec Kit asks you to confirm installation from the URL. The archive contains the manifest,
commands and all KLOD references. This direct installation does not need a catalog listing.

To install from a local checkout, use the extension directory:

```bash
specify extension add --dev /path/to/keepthelightson/integrations/spec-kit
specify extension list
```

Run these commands from your **application's Spec Kit project**, not from the KLOD source
repository. Restart your coding agent if its new commands do not appear.

## Use it in your workflow

1. Create the feature specification and implementation plan with Spec Kit as usual.
2. Run KLOD planning before generating tasks. It updates the active feature's specification
   and plan and writes `klod-plan.md` beside them. It adds acceptance checks and makes missing
   decisions explicit; it does not implement the feature.
3. Generate tasks and implement the feature with your usual Spec Kit workflow. Run the
   planned software checks during implementation and retain their results.
4. Run the KLOD check. It writes `klod_report.md` at the project root, reviewing the code,
   coverage and available evidence. It does not run tests or drills, change the application
   or award a level based on a plan or checked task box.

The command spelling depends on your agent's Spec Kit integration:

| Agent setup | Plan before tasks | Check after implementation |
| --- | --- | --- |
| Claude Code, default skills | `/speckit-klod-plan` | `/speckit-klod-check` |
| Codex, default skills | `$speckit-klod-plan` | `$speckit-klod-check` |
| Command integrations using dots | `/speckit.klod.plan` | `/speckit.klod.check` |

Use the commands your agent displays. The registered command IDs are `speckit.klod.plan` and
`speckit.klod.check`; Spec Kit renders the appropriate invocation for each integration.

The extension also registers two optional prompts: one after `plan`, before task generation,
and one after `implement`. You can skip either and invoke KLOD yourself later. These hooks
are instructions surfaced by Spec Kit's agent workflow, not background jobs or a CI gate.
Set a hook's `enabled` value to `false` in `.specify/extensions.yml` to hide its prompt.

Only runtime AI creates a need for this takeover workflow. Using a coding agent during
development does not make the resulting application AI-dependent. Self-run AI needs human
controls but does not receive a hosted supplier-dependence level. Software tests alone do not
establish L2 or L3; those levels retain KLOD's real-work evidence requirements.

## Update or remove

For an archive update, rerun the archive installation command with `--force`. For a local
update, rerun the local installation command with `--force`. Review the new source first;
installation copies the bundled guidance into your project.

```bash
specify extension remove klod
```

Removal unregisters KLOD's commands and hooks and removes its installed resources. Feature
plans and `klod_report.md` are project documents and remain in place.

## Compatibility and maintenance

The compatibility checks use the real v1.0.6 CLI to initialise disposable Claude and Codex
projects, install the extension, inspect rendered commands and bundled resources, resolve a
selected feature and remove the extension while preserving existing project files. Archive
installation is checked separately. These checks verify packaging and CLI integration; they
do not establish model performance or a successful human takeover.

The source for this adapter is `integrations/spec-kit/`. Its `skills/` copies are generated
from the canonical skills so their instructions stay identical. Edit the canonical skills
when changing shared guidance.

KLOD is an independently maintained community extension. It is not an official GitHub
product, endorsed extension or accepted catalog entry. To propose discovery through Spec
Kit, first publish a versioned archive, then follow its
[extension publishing guide](https://github.com/github/spec-kit/blob/main/extensions/EXTENSION-PUBLISHING-GUIDE.md).

The instructions and specification are [CC BY 4.0](LICENSE-SPEC.md). The bundled helper
scripts are [MIT licensed](LICENSE-CODE.md).
