"""Portable release bundles must contain current guidance and reproducible bytes."""
from io import BytesIO
from pathlib import Path
import re
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".github/scripts"))
from build_integrations import BUNDLED_SKILLS, INTEGRATIONS, archive_bytes


class IntegrationPackageTests(unittest.TestCase):
    def test_archives_contain_the_current_self_contained_skills(self):
        for name in INTEGRATIONS:
            with self.subTest(integration=name):
                payload = archive_bytes(ROOT, name)
                self.assertEqual(payload, archive_bytes(ROOT, name))
                with ZipFile(BytesIO(payload)) as archive:
                    prefix = f"klod-{name}/"
                    bundled = BUNDLED_SKILLS[name].relative_to(Path("integrations") / name)
                    for path in (ROOT / "skills").rglob("*"):
                        if path.is_file() and path.suffix in {".md", ".py"}:
                            exported = prefix + (bundled / path.relative_to(ROOT / "skills")).as_posix()
                            self.assertEqual(archive.read(exported), path.read_bytes(), exported)
                    self.assertIn(prefix + "README.md", archive.namelist())
                    self.assertIn(prefix + "LICENSE-CODE.md", archive.namelist())
                    self.assertTrue(all(item.startswith(prefix) for item in archive.namelist()))
                    self.assertFalse(any("/.github/" in item or "/private/" in item or "/.git/" in item
                                         for item in archive.namelist()))

    def test_sync_updates_all_bundles_and_rejects_drift(self):
        with TemporaryDirectory(prefix="klod-sync-") as temporary:
            root = Path(temporary) / "package"
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", ".cache", "__pycache__"))
            canonical = root / "skills/klod/references/human-control.md"
            canonical.write_text(canonical.read_text() + "\nA test clarification.\n")
            manifest = root / "apm.yml"
            manifest.write_text(re.sub(r"^version: .+$", "version: 7.8.9", manifest.read_text(), flags=re.M))
            command = [sys.executable, str(root / ".github/scripts/check_package.py")]
            failed = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(failed.returncode, 0)
            synced = subprocess.run([*command, "--sync"], capture_output=True, text=True)
            self.assertEqual(synced.returncode, 0, synced.stdout + synced.stderr)
            self.assertIn('version: "7.8.9"', (root / "integrations/spec-kit/extension.yml").read_text())
            self.assertIn('VERSION = "7.8.9"', (root / "integrations/openspec/install.py").read_text())
            self.assertIn('**Version:** 7.8.9.', (root / "integrations/openspec/README.md").read_text())
            for base in BUNDLED_SKILLS.values():
                for skill in ("klod", "klod-check"):
                    self.assertEqual((root / base / skill / "references/human-control.md").read_bytes(),
                                     canonical.read_bytes())
            modified = root / BUNDLED_SKILLS["spec-kit"] / "klod/SKILL.md"
            modified.write_text("Instructions that are no longer the canonical skill.\n")
            failed = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("Out of sync", failed.stderr)

    def test_ignored_editor_and_cache_files_never_enter_an_archive(self):
        with TemporaryDirectory(prefix="klod-local-files-") as temporary:
            root = Path(temporary)
            shutil.copytree(ROOT / "integrations", root / "integrations")
            for name in INTEGRATIONS:
                before = archive_bytes(root, name)
                for directory in (".vscode", ".idea", ".ruff_cache", ".cache", "__pycache__"):
                    path = root / "integrations" / name / directory / "private.json"
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text('{"local": "not for distribution"}')
                self.assertEqual(archive_bytes(root, name), before)

    def test_archive_rejects_symlinks(self):
        with TemporaryDirectory(prefix="klod-archive-") as temporary:
            root = Path(temporary)
            shutil.copytree(ROOT / "integrations", root / "integrations")
            external = root / "private-note.md"
            external.write_text("Not public.\n")
            (root / "integrations/spec-kit/leak.md").symlink_to(external)
            with self.assertRaisesRegex(ValueError, "symlink"):
                archive_bytes(root, "spec-kit")


if __name__ == "__main__":
    unittest.main()
