# Identify every report

Start every generated Markdown scan, design or implementation report with the project name
and the block below, before the summary. Include it even in short reports about libraries or
projects with no AI dependencies. Skill references, runbooks and `LIGHTS.md` do not need this
header, and you do not need to create a separate report for a small implementation.

```markdown
# Example service · KLOD report

- **Project:** Example service
- **Git origin:** https://github.com/example/example-service.git
- **Revision:** 0123456789abcdef0123456789abcdef01234567
- **Model:** Unavailable (the host did not expose an exact active model identifier)
- **Report timestamp:** 2026-09-11T10:42:18+03:00 (Europe/Bucharest)

1 dependent capability found. Worst supported level: L0. Coverage: complete.
```

Replace the example values with facts about the project you inspected. Use `KLOD design report` or
`KLOD implementation report` for feature work; `KLOD report` follows the checker format.

## Required fields

- **Project:** use the name from the manifest, README or user, falling back to the directory
  name. Put it in the title too. For monorepos, name the repository and list the products you
  assessed in the scope.
- **Git origin:** use the actual origin, sanitised before display. Capture Git output privately; never
  print `git remote -v` or raw origin output. Remove URL userinfo/credentials, query parameters
  and fragments before printing or writing. Use `Unavailable (Git repository has no origin remote)`
  for missing origin, or `Not applicable (local project; not a Git repository)` for a non-Git
  project. If you cannot read the Git metadata, report it as unavailable and explain why;
  you cannot conclude that the project does not use Git.
- **Revision:** give the inspected commit, or mark it unavailable or not applicable with a reason.
  In the scope, identify any evidence affected by uncommitted changes, since a commit hash
  does not describe those changes.
- **Model:** give the exact active identifier exposed by the host or runtime, and say where
  it came from. A provider name, requested alias, configured preference or assistant brand
  does not identify the active model.
  If only the requested model is known, label it separately and keep the actual model unavailable
  with a reason. For delegated work, identify the coordinator and known worker models; state
  which identities were unavailable. Never guess or invent IDs.
- **Report timestamp:** use the actual completion time in ISO 8601 with a numeric UTC offset and timezone,
  such as `2026-09-11T10:42:18+03:00 (Europe/Bucharest)`. Use UTC if no local zone is established.
  If the clock is unavailable, write `Unavailable (reason)`. Keep report time separate from
  historical drill dates and specification versions.

## Collect local metadata

Each skill includes `scripts/report_metadata.py`, a helper that uses Python's standard library
to read Git metadata and the clock, remove credentials from the origin and print the header.
It makes no changes or network calls. Use the copy in the installed skill directory, for example:

```sh
python3 .agents/skills/klod-check/scripts/report_metadata.py --project . --name 'Example service'
```

For feature work use the `klod` copy with `--kind 'KLOD design report'` or
`--kind 'KLOD implementation report'`. Pass `--model` and `--model-source` only for a
host-confirmed active identity. `--timezone Europe/Bucharest` is optional; the default is UTC.
If Python or Git is unavailable, use reliable available facts and give a reason for each
missing field.

Place the block at the beginning of the report, where readers can see it, rather than in YAML,
comments or a footer. Check that it describes this run and contains no origin credentials.
For a rescan, use the current model identity and a new timestamp, and keep the existing finding
IDs and owner notes. Leave historical reports intact.
