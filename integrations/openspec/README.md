# KLOD for OpenSpec

Plan AI features with a human path, then check the implemented behaviour. This
independent custom schema adds KLOD to OpenSpec's proposal, specs, design and tasks.
It includes the portable `klod` and `klod-check` guidance and their references.

**Version:** 0.1.2. **Compatibility tested:** OpenSpec 1.13.0, using its released CLI.
This is a custom schema, not an official OpenSpec plugin or an accepted catalog entry.

## Install

You need Python 3.10 or later for the installer and Node.js 20.19 or later for this
OpenSpec release. In your project, install OpenSpec and initialise it if needed:

```sh
npm install -g @fission-ai/openspec@1.13.0 && openspec init
```

Choose your coding assistant during OpenSpec setup. If the project is already
initialised, keep its current setup.

OpenSpec has no command for fetching a schema from a repository, so the schema ships with
a small installer. Clone the KLOD repository at the release tag next to your project, which
keeps the checkout out of your own repository, then run the installer from your project
directory:

```sh
git clone --depth 1 --branch v0.1.2 https://github.com/AlexandruGirlea/keepthelightson.git ../keepthelightson &&
python3 ../keepthelightson/integrations/openspec/install.py --project . &&
openspec schema validate klod
```

The same files are attached to each entry on the
[releases page](https://github.com/AlexandruGirlea/keepthelightson/releases) as
`klod-openspec.zip`. Extract it and run its `install.py` the same way if you prefer a download.

The installer puts the complete bundle in `openspec/schemas/klod/`. It leaves
`openspec/config.yaml`, other schemas, assistant configuration and existing changes
alone. Commit the installed schema with your project so your team has the same version.

## Use it on a change

In your coding assistant, ask:

```text
Use OpenSpec to propose add-support-drafting with the klod schema.
Include the human path when AI is unavailable or stopped.
```

Review the generated proposal, requirements, design and tasks. Then ask:

```text
Apply the add-support-drafting change.
```

These are ordinary assistant prompts, not new slash commands. Use your installed
OpenSpec workflows; they read the schema's instructions and bundled KLOD guidance.
Installation alone does not generate a plan or change application code.

For a CLI-created scaffold, the equivalent schema selection is:

```sh
openspec new change add-support-drafting --schema klod
```

Then ask your assistant to continue that existing change using its `klod` schema.
Do not run both creation paths for the same name. If you want KLOD on every new
change, change the existing `schema:` value in `openspec/config.yaml` to `klod`;
preserve the rest of that file. Existing changes keep their selected schemas.

## What the schema adds

- **Proposal:** identifies runtime AI, the work it serves and the people who need
  to complete the essential outcome. Unknown owners and operating targets stay explicit.
- **Specs:** describes observable unavailable-provider, operator-stop and human
  completion behaviour alongside the feature's normal behaviour.
- **Design:** traces usable data, permissions, controls, in-flight work and shared
  dependencies through both AI and human operation.
- **Tasks and implementation:** includes isolated execution checks and an honest
  handover, with operating instructions and an updated `LIGHTS.md` entry where relevant.

The standard `specs` artifact and delta format remain in place for OpenSpec's sync
and archive workflows. Changes without runtime AI record that scope and continue
normally; using an AI coding assistant alone does not create a supplier-dependence level.

This version is tested with ordinary project-local OpenSpec changes. Standalone
stores, worksets and multi-repository planning are not yet supported by this adapter.
Use it from the project where `openspec/schemas/klod/` is installed.

## Check the implementation

The apply instructions point to the bundled
[verification guide](schema/verification.md). Run the change's authorised isolated
tests and inspect actual state and effects. Record failures, unrun checks and the
remaining limits. A document describing a test is not a test result.

For a separate repository audit, ask:

```text
Read openspec/schemas/klod/skills/klod-check/SKILL.md and follow it to audit
this project. Write klod_report.md with file evidence and missing evidence.
```

That audit is read-only apart from its report. It does not run application tests,
call providers or perform a live drill. It assesses the repository; a change-only
inspection cannot claim complete coverage.

OpenSpec schema dependencies check file existence. They do not enforce successful
tests or prove that people can operate the business. L2 requires a real-work drill
with AI unavailable; L3 has further evidence gates. Live drills need authorisation,
an agreed scope and recovery controls. Never invent participants, dates or measurements.

## Update or customise

Check out the new release tag and run its installer against the same project. An unchanged
installation can be updated repeatedly. Only previously managed, unchanged files may
be replaced or removed; unrelated files stay in place. The installer refuses local
edits, missing managed files, file collisions and symbolic links before making changes.
It records managed hashes in `.klod-install.json` inside the installed schema.

To check whether a bundle matches the installation without writing:

```sh
python3 ../keepthelightson/integrations/openspec/install.py --project . --check
```

If you customise the installed schema, keep those changes in version control. Compare
the new bundle with your copy and merge deliberately; the installer does not have a
force-overwrite option. To maintain a separate custom workflow, copy the installed
folder under a different schema name and update its `name` and internal
`openspec/schemas/klod/` references to match. Keep `klod` unchanged for managed updates.

OpenSpec's own `openspec update` does not update custom schema folders. To stop using
KLOD, select a different schema for new changes. Keep the installed folder while any
existing change still references it. Remove it only after preserving your own changes
and confirming it is no longer needed.

## Verification and contribution

Compatibility checks cover installation, preservation and updates, schema validation,
change creation, artifact dependencies, instruction generation and standard spec
validation/archive behaviour with OpenSpec 1.13.0. They do not measure model quality,
production readiness or real human takeover.

OpenSpec maintains a
[community schema catalog](https://github.com/Fission-AI/OpenSpec/blob/main/docs/customization.md#community-schemas)
and invites repository links or documentation pull requests. A future KLOD submission
can link this adapter, its example and compatibility results. No submission or acceptance
is implied here. For upstream mechanics, see
[OpenSpec's schema documentation](https://openspec.dev/docs/customize-schemas).

KLOD guidance and templates use [CC BY 4.0](LICENSE-SPEC.md); the installer uses
[MIT](LICENSE-CODE.md). The bundled skill copies come from KLOD's canonical skills and
are checked for drift. Edit the canonical guidance when changing shared rules.
