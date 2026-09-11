"""Exercise the KLOD extension with an installed Spec Kit CLI.

Install specify-cli==1.0.6 and run this file, or set KLOD_SPECIFY to that
version's executable. These tests do not invoke a coding agent or AI provider.
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from threading import Thread
import unittest


PUBLIC_ROOT = Path(__file__).resolve().parents[2]
EXTENSION = PUBLIC_ROOT / "integrations" / "spec-kit"
CLI = os.environ.get("KLOD_SPECIFY") or shutil.which("specify")
PACKAGE_VERSION = re.search(r"^version: (\S+)$", (PUBLIC_ROOT / "apm.yml").read_text(), re.M)[1]
sys.path.insert(0, str(PUBLIC_ROOT / ".github" / "scripts"))
from build_integrations import archive_bytes


@unittest.skipUnless(CLI, "Install specify-cli==1.0.6 or set KLOD_SPECIFY")
class SpecKitIntegrationTests(unittest.TestCase):
    def run_cli(self, project: Path, *arguments: str, input_text: str = "") -> str:
        result = subprocess.run(
            [str(CLI), *arguments],
            cwd=project,
            text=True,
            capture_output=True,
            timeout=60,
            input=input_text,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout

    def exercise_install(self, agent: str, script: str, skill_directory: str, prefix: str) -> None:
        with tempfile.TemporaryDirectory(prefix="klod-speckit-") as temporary:
            project = Path(temporary).resolve()
            self.run_cli(
                project, "init", "--here", "--integration", agent,
                "--script", script, "--ignore-agent-tools", "--non-interactive",
            )

            # Existing application and feature documents must survive installation/removal.
            feature = project / "specs" / "chosen-feature"
            feature.mkdir(parents=True)
            preserved = {
                project / "app.py": b"# existing application\n",
                feature / "spec.md": b"# Existing specification\n",
                feature / "plan.md": b"# Existing plan\n",
                feature / "tasks.md": b"- [x] T001 Existing completed task\n",
                project / "klod_report.md": b"# Existing audit with owner notes\n",
                project / ".specify" / "feature.json": json.dumps(
                    {"feature_directory": "specs/chosen-feature"}
                ).encode(),
            }
            for path, content in preserved.items():
                path.write_bytes(content)

            # A second feature ensures the command's resolver respects feature selection.
            (project / "specs" / "newer-feature").mkdir()
            self.run_cli(project, "extension", "add", "--dev", str(EXTENSION))
            installed = project / ".specify" / "extensions" / "klod"
            listing = self.run_cli(project, "extension", "list")
            self.assertIn("Commands: 2 | Hooks: 2", listing)
            registry = project / ".specify" / "extensions" / ".registry"
            entry = json.loads(registry.read_text())["extensions"]["klod"]
            self.assertTrue(entry["enabled"])
            self.assertEqual(entry["version"], PACKAGE_VERSION)
            self.assertEqual(
                entry["registered_commands"][agent],
                ["speckit.klod.plan", "speckit.klod.check"],
            )

            for skill in ("klod", "klod-check"):
                canonical = PUBLIC_ROOT / "skills" / skill
                for source in canonical.rglob("*"):
                    if source.is_file():
                        bundled = installed / "skills" / skill / source.relative_to(canonical)
                        self.assertEqual(bundled.read_bytes(), source.read_bytes(), str(bundled))

            plan_command = project / skill_directory / "speckit-klod-plan" / "SKILL.md"
            check_command = project / skill_directory / "speckit-klod-check" / "SKILL.md"
            plan_text = plan_command.read_text()
            check_text = check_command.read_text()
            for content in (plan_text, check_text):
                self.assertNotIn("{SCRIPT}", content)
                self.assertNotIn("__SPECKIT_COMMAND_", content)
                self.assertIn(".specify/extensions/klod/skills/", content)
                self.assertIn("--json --paths-only", content)
            self.assertIn(f"{prefix}speckit-tasks", plan_text)
            self.assertIn(f"{prefix}speckit-klod-check", plan_text)

            hooks = (project / ".specify" / "extensions.yml").read_text()
            self.assertIn("after_plan:", hooks)
            self.assertIn("after_implement:", hooks)
            self.assertEqual(hooks.count("optional: true"), 2)
            self.assertIn("command: speckit.klod.plan", hooks)
            self.assertIn("command: speckit.klod.check", hooks)

            if script == "sh":
                discovery = ["bash", ".specify/scripts/bash/check-prerequisites.sh"]
            else:
                discovery = ["python3", ".specify/scripts/python/check_prerequisites.py"]
            result = subprocess.run(
                [*discovery, "--json", "--paths-only"], cwd=project,
                text=True, capture_output=True, timeout=20, check=True,
            )
            resolved = json.loads(result.stdout)
            self.assertEqual(Path(resolved["FEATURE_DIR"]).resolve(), feature)
            self.assertEqual(Path(resolved["FEATURE_SPEC"]).resolve(), feature / "spec.md")
            self.assertEqual(Path(resolved["IMPL_PLAN"]).resolve(), feature / "plan.md")
            self.assertEqual(Path(resolved["TASKS"]).resolve(), feature / "tasks.md")

            for path, content in preserved.items():
                self.assertEqual(path.read_bytes(), content, str(path))

            self.run_cli(project, "extension", "remove", "klod", "--force")
            self.assertFalse(installed.exists())
            self.assertFalse(plan_command.exists())
            self.assertFalse(check_command.exists())
            self.run_cli(project, "extension", "list")
            remaining = json.loads(registry.read_text())["extensions"]
            self.assertNotIn("klod", remaining)
            hook_config = project / ".specify" / "extensions.yml"
            if hook_config.exists():
                self.assertNotIn("extension: klod", hook_config.read_text())
            for path, content in preserved.items():
                self.assertEqual(path.read_bytes(), content, str(path))

    def test_claude_shell_workflow(self) -> None:
        self.exercise_install("claude", "sh", ".claude/skills", "/")

    def test_codex_python_workflow(self) -> None:
        self.exercise_install("codex", "py", ".agents/skills", "$")

    def test_release_archive_installs_from_a_url(self) -> None:
        payload = archive_bytes(PUBLIC_ROOT, "spec-kit")

        class ArchiveHandler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:
                if self.path != "/klod-spec-kit.zip":
                    self.send_error(404)
                    return
                self.send_response(200)
                self.send_header("Content-Type", "application/zip")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

            def log_message(self, format: str, *arguments: object) -> None:
                pass

        with tempfile.TemporaryDirectory(prefix="klod-speckit-zip-") as temporary:
            project = Path(temporary).resolve()
            self.run_cli(
                project, "init", "--here", "--integration", "claude",
                "--script", "sh", "--ignore-agent-tools", "--non-interactive",
            )
            existing = project / "app.py"
            existing.write_text("# existing application\n")
            with HTTPServer(("127.0.0.1", 0), ArchiveHandler) as server:
                thread = Thread(
                    target=server.serve_forever, kwargs={"poll_interval": 0.02}, daemon=True,
                )
                thread.start()
                try:
                    url = f"http://127.0.0.1:{server.server_port}/klod-spec-kit.zip"
                    self.run_cli(
                        project, "extension", "add", "klod", "--from", url,
                        input_text="y\n",
                    )
                finally:
                    server.shutdown()
                    thread.join(timeout=5)
                self.assertFalse(thread.is_alive())

            installed = project / ".specify" / "extensions" / "klod"
            for skill in ("klod", "klod-check"):
                canonical = PUBLIC_ROOT / "skills" / skill
                for source in canonical.rglob("*"):
                    if source.is_file():
                        bundled = installed / "skills" / skill / source.relative_to(canonical)
                        self.assertEqual(bundled.read_bytes(), source.read_bytes(), str(bundled))
            for command in ("plan", "check"):
                registered = project / ".claude" / "skills" / f"speckit-klod-{command}" / "SKILL.md"
                self.assertTrue(registered.is_file())
                self.assertNotIn("{SCRIPT}", registered.read_text())
            self.assertIn("Commands: 2 | Hooks: 2", self.run_cli(project, "extension", "list"))
            self.run_cli(project, "extension", "remove", "klod", "--force")
            self.assertFalse(installed.exists())
            self.assertEqual(existing.read_text(), "# existing application\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
