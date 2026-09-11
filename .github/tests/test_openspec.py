"""Preservation checks and optional compatibility checks against the released CLI."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
ADAPTER = ROOT / "integrations/openspec"
CLI = os.environ.get("KLOD_OPENSPEC") or shutil.which("openspec")
spec = importlib.util.spec_from_file_location("klod_openspec_installer", ADAPTER / "install.py")
assert spec and spec.loader
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="klod-openspec-test-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.source = self.base / "bundle"
        shutil.copytree(ADAPTER / "schema", self.source)
        self.project = self.base / "project"
        (self.project / "openspec/changes/existing").mkdir(parents=True)
        (self.project / "openspec/config.yaml").write_text("schema: spec-driven\ncontext: Preserve me\n")
        (self.project / "openspec/changes/existing/proposal.md").write_text("Owner's existing work\n")
        self.destination = self.project / "openspec/schemas/klod"

    def install(self, **kwargs):
        return installer.install(self.project, self.source, **kwargs)

    def test_install_and_repeat_preserve_project_and_bundle_resources(self):
        self.assertFalse(self.install(check=True))
        self.assertFalse(self.destination.exists())
        self.install()
        first = {p.relative_to(self.project): p.read_bytes() for p in self.project.rglob("*") if p.is_file()}
        self.install()
        self.assertTrue(self.install(check=True))
        self.assertEqual(first, {p.relative_to(self.project): p.read_bytes() for p in self.project.rglob("*") if p.is_file()})
        self.assertEqual((self.project / "openspec/config.yaml").read_text(), "schema: spec-driven\ncontext: Preserve me\n")
        self.assertEqual((self.project / "openspec/changes/existing/proposal.md").read_text(), "Owner's existing work\n")
        self.assertTrue((self.destination / "skills/klod-check/references/specification.md").is_file())

    def test_upgrade_preserves_unrelated_files_and_ignores_source_caches(self):
        (self.source / "retired.md").write_text("Old managed file")
        self.install()
        (self.destination / "operator-notes.md").write_text("Keep these notes")
        (self.source / "retired.md").unlink()
        (self.source / "verification.md").write_text("Updated verification\n")
        (self.source / "__pycache__").mkdir()
        (self.source / "__pycache__/local.pyc").write_bytes(b"local cache")
        (self.source / ".vscode").mkdir()
        (self.source / ".vscode/settings.json").write_text('{"local": "editor settings"}')
        self.assertFalse(self.install(check=True))
        self.install()
        self.assertFalse((self.destination / "retired.md").exists())
        self.assertEqual((self.destination / "operator-notes.md").read_text(), "Keep these notes")
        self.assertEqual((self.destination / "verification.md").read_text(), "Updated verification\n")
        self.assertFalse((self.destination / "__pycache__").exists())
        self.assertFalse((self.destination / ".vscode").exists())

    def test_local_edit_blocks_entire_upgrade(self):
        self.install()
        (self.destination / "templates/design.md").write_text("Local design instructions")
        original = (self.destination / "verification.md").read_bytes()
        (self.source / "verification.md").write_text("Upstream change")
        with self.assertRaisesRegex(installer.InstallError, "Locally changed"):
            self.install()
        self.assertEqual((self.destination / "verification.md").read_bytes(), original)
        self.assertEqual((self.destination / "templates/design.md").read_text(), "Local design instructions")

    def test_missing_managed_file_and_unmanaged_schema_are_not_overwritten(self):
        self.destination.mkdir(parents=True)
        (self.destination / "notes.md").write_text("Existing custom schema")
        with self.assertRaisesRegex(installer.InstallError, "not managed"):
            self.install()
        shutil.rmtree(self.destination)
        self.install()
        (self.destination / "schema.yaml").unlink()
        with self.assertRaisesRegex(installer.InstallError, "missing managed"):
            self.install()
        self.assertFalse((self.destination / "schema.yaml").exists())

    def test_update_refuses_unmanaged_collision_and_symlink_escape(self):
        self.install()
        (self.source / "new-file.md").write_text("Bundle file")
        (self.destination / "new-file.md").write_text("User file")
        with self.assertRaisesRegex(installer.InstallError, "Unmanaged file"):
            self.install()
        self.assertEqual((self.destination / "new-file.md").read_text(), "User file")
        (self.source / "new-file.md").unlink()
        outside = self.base / "outside"
        outside.mkdir()
        (self.source / "extra").mkdir()
        (self.source / "extra/note.md").write_text("Must not escape")
        (self.destination / "extra").symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(installer.InstallError, "symbolic link"):
            self.install()
        self.assertEqual(list(outside.iterdir()), [])

    def test_unmanaged_file_blocking_new_parent_is_preserved(self):
        self.install()
        (self.source / "extra").mkdir()
        (self.source / "extra/note.md").write_text("Bundle addition")
        (self.destination / "extra").write_text("User data")
        with self.assertRaisesRegex(installer.InstallError, "blocks a required directory"):
            self.install()
        self.assertEqual((self.destination / "extra").read_text(), "User data")

    def test_failed_upgrade_copy_keeps_original_installation(self):
        self.install()
        original = (self.destination / "verification.md").read_bytes()
        (self.source / "verification.md").write_text("New content")
        with patch.object(installer.shutil, "copytree", side_effect=OSError("Disk error")):
            with self.assertRaisesRegex(OSError, "Disk error"):
                self.install()
        self.assertEqual((self.destination / "verification.md").read_bytes(), original)
        self.assertTrue((self.destination / installer.MANIFEST).exists())

    def test_failed_final_rename_restores_original_installation(self):
        self.install()
        original = (self.destination / "verification.md").read_bytes()
        (self.source / "verification.md").write_text("New content")
        replace = installer.os.replace

        def fail_new_directory(source, target):
            if Path(source).name == "next":
                raise OSError("Rename failed")
            return replace(source, target)

        with patch.object(installer.os, "replace", side_effect=fail_new_directory):
            with self.assertRaisesRegex(OSError, "Rename failed"):
                self.install()
        self.assertEqual((self.destination / "verification.md").read_bytes(), original)

    def test_manifest_path_traversal_is_rejected(self):
        self.install()
        manifest = self.destination / installer.MANIFEST
        data = json.loads(manifest.read_text())
        data["files"]["../../config.yaml"] = "0" * 64
        manifest.write_text(json.dumps(data))
        with self.assertRaisesRegex(installer.InstallError, "Unsafe managed path"):
            self.install()
        self.assertEqual((self.project / "openspec/config.yaml").read_text(), "schema: spec-driven\ncontext: Preserve me\n")


@unittest.skipUnless(CLI, "Install openspec 1.13.0 or set KLOD_OPENSPEC for CLI checks")
class ReleasedCliTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="klod-openspec-cli-")
        self.addCleanup(self.temporary.cleanup)
        self.project = Path(self.temporary.name)
        self.cli = CLI
        self.environment = {**os.environ, "OPENSPEC_TELEMETRY": "0"}
        self.assertEqual(self.run_cli("--version").strip(), installer.TESTED_OPENSPEC)
        self.run_cli("init", "--tools", "none", "--no-animation")
        self.config = (self.project / "openspec/config.yaml").read_bytes()
        installer.install(self.project, ADAPTER / "schema")

    def run_cli(self, *arguments):
        result = subprocess.run([self.cli, *arguments], cwd=self.project, env=self.environment,
                                text=True, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 0, f"{' '.join(arguments)}\n{result.stdout}\n{result.stderr}")
        return result.stdout

    def status(self):
        return json.loads(self.run_cli("status", "--change", "support-recovery", "--json"))

    def test_schema_artifacts_instructions_and_archive_keep_standard_specs(self):
        self.run_cli("schema", "validate", "klod")
        self.run_cli("new", "change", "support-recovery", "--schema", "klod")
        self.assertEqual((self.project / "openspec/config.yaml").read_bytes(), self.config)
        state = self.status()
        statuses = {a["id"]: a["status"] for a in state["artifacts"]}
        self.assertEqual(statuses, {"proposal": "ready", "specs": "blocked", "design": "blocked", "tasks": "blocked"})
        change = self.project / "openspec/changes/support-recovery"
        instructions = json.loads(self.run_cli("instructions", "proposal", "--change", "support-recovery", "--json"))
        self.assertIn("openspec/schemas/klod/skills/klod/SKILL.md", instructions["instruction"])
        (change / "proposal.md").write_text("## Why\n\nSupport requests need a recoverable human path.\n\n## What Changes\n\nAdd manual completion.\n\n## Capabilities\n\n### New Capabilities\n\n- support-queue: Preserve and finish support requests.\n\n### Modified Capabilities\n\nNone.\n\n## Impact\n\nSupport queue.\n")
        statuses = {a["id"]: a["status"] for a in self.status()["artifacts"]}
        self.assertEqual(statuses["specs"], "ready")
        self.assertEqual(statuses["design"], "ready")
        self.assertEqual(statuses["tasks"], "blocked")
        spec_dir = change / "specs/support-queue"
        spec_dir.mkdir(parents=True)
        (spec_dir / "spec.md").write_text("## Purpose\n\nPreserve support requests so an authorised person can finish them when automated drafting is unavailable.\n\n## ADDED Requirements\n\n### Requirement: Manual completion\nThe system SHALL retain a pending request for authorised human completion.\n\n#### Scenario: Drafting unavailable\n- **WHEN** the drafting provider is unavailable\n- **THEN** an authorised operator can complete the saved request\n")
        (change / "design.md").write_text("## Approach\n\nUse a persisted queue and authorised operator view.\n")
        statuses = {a["id"]: a["status"] for a in self.status()["artifacts"]}
        self.assertEqual(statuses["tasks"], "ready")
        task_instructions = json.loads(self.run_cli("instructions", "tasks", "--change", "support-recovery", "--json"))
        self.assertIn("Tests and code inspection cannot establish L2 or L3", task_instructions["instruction"])
        task_text = "## 1. Compatibility fixture\n\n- [ ] 1.1 Create this spec fixture and validate its format; no application or human drill is being tested.\n"
        (change / "tasks.md").write_text(task_text)
        apply = json.loads(self.run_cli("instructions", "apply", "--change", "support-recovery", "--json"))
        self.assertIn("openspec/schemas/klod/verification.md", apply["instruction"])
        self.run_cli("validate", "support-recovery", "--strict")
        (change / "tasks.md").write_text(task_text.replace("- [ ]", "- [x]"))
        archived = json.loads(self.run_cli("archive", "support-recovery", "--json", "--yes"))
        self.assertTrue(archived)
        main_spec = self.project / "openspec/specs/support-queue/spec.md"
        self.assertTrue(main_spec.is_file())
        self.assertIn("Manual completion", main_spec.read_text())
        self.assertIn("authorised person can finish", main_spec.read_text())
        self.assertEqual((self.project / "openspec/config.yaml").read_bytes(), self.config)


if __name__ == "__main__":
    unittest.main()
