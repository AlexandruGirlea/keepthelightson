# Check the implemented change

Read [the klod skill](skills/klod/SKILL.md) and its
[verification and handoff guide](skills/klod/references/verification.md).

1. Run the isolated checks specified in the change. Exercise application entry points,
   inspect saved state and effects, and record the exact commands and actual results.
   Include normal operation, unavailable AI, authorised stop and human completion for
   applicable features. Cover restarts, queued/late output and conflicting edits when
   those behaviours exist. Inspect changed interfaces with representative data.
2. Fix observed failures and repeat affected checks. Leave skipped or blocked work
   explicit. Update the affected `LIGHTS.md` entry without overwriting owner notes.
3. When a repository audit is requested, read
   [the klod-check skill](skills/klod-check/SKILL.md) and follow its coverage, metadata
   and evidence requirements. The audit writes `klod_report.md` at the project root.
   It does not execute tests, call providers, change application code or run drills.
   A review limited to this change must not claim complete repository coverage.
4. Compare the delivered behaviour with the specs and tasks. OpenSpec's optional
   verification workflow can assist, but its report is not proof of successful
   execution. Keep test output and human evidence available to the reviewer.
5. Follow the normal OpenSpec completion/archive process with the unresolved work
   visible. The schema preserves the standard `specs` artifact for spec syncing.

Schema dependencies check whether files exist. They do not enforce their contents or
run tests. An automated check cannot establish that a person completed real work.
L2 needs a real-work drill with AI unavailable; L3 needs current routine human evidence
and its other gates. Do not invent dates, people, Time to Manual, capacity or levels.
Live drills need an agreed scope, authorisation and recovery controls. Keep them as
outstanding follow-ups when those conditions are missing.
