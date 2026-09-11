#!/usr/bin/env python3
"""Build reproducible integration archives using only the public package."""
from __future__ import annotations

import argparse
from io import BytesIO
from pathlib import Path
import subprocess
import sys
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[2]
INTEGRATIONS = ("spec-kit", "openspec")
BUNDLED_SKILLS = {
    "spec-kit": Path("integrations/spec-kit/skills"),
    "openspec": Path("integrations/openspec/schema/skills"),
}
LOCAL_NAMES = {
    ".git", ".DS_Store", ".idea", ".vscode", "__pycache__", ".venv",
    ".pytest_cache", ".ruff_cache", ".cache",
}


def archive_bytes(root: Path, integration: str) -> bytes:
    """Give each archive one predictable directory, timestamps and file permissions."""
    if integration not in INTEGRATIONS:
        raise ValueError(f"Unknown integration: {integration}")
    source = root / "integrations" / integration
    if source.is_symlink() or not source.is_dir():
        raise ValueError(f"Missing integration directory: {integration}")
    required = ("extension.yml", "commands/plan.md", "commands/check.md") if integration == "spec-kit" else (
        "install.py", "schema/schema.yaml")
    for name in (*required, "README.md", "LICENSE-CODE.md", "LICENSE-SPEC.md"):
        if not (source / name).is_file():
            raise ValueError(f"Missing integration file: {integration}/{name}")
    for skill in ("klod", "klod-check"):
        if not (root / BUNDLED_SKILLS[integration] / skill / "SKILL.md").is_file():
            raise ValueError("Bundled skills are missing; run check_package.py --sync")
    buffer = BytesIO()
    with ZipFile(buffer, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(source.rglob("*")):
            relative = path.relative_to(source)
            if any(part in LOCAL_NAMES for part in relative.parts) or path.suffix == ".pyc":
                continue
            if path.is_symlink():
                raise ValueError(f"Integration archives cannot contain symlinks: {relative}")
            if not path.is_file():
                continue
            if path.suffix not in {".md", ".py", ".yml", ".yaml", ".json"}:
                raise ValueError(f"Unexpected integration file: {relative}")
            info = ZipInfo(f"klod-{integration}/{relative.as_posix()}", date_time=(2026, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = ZIP_DEFLATED
            archive.writestr(info, path.read_bytes(), compresslevel=9)
    return buffer.getvalue()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="Directory for the two ZIP files")
    args = parser.parse_args()
    checked = subprocess.run([sys.executable, str(ROOT / ".github/scripts/check_package.py")], cwd=ROOT)
    if checked.returncode:
        return checked.returncode
    try:
        payloads = {f"klod-{name}.zip": archive_bytes(ROOT, name) for name in INTEGRATIONS}
        args.output.mkdir(parents=True, exist_ok=True)
        for name, payload in payloads.items():
            destination = args.output / name
            if destination.is_symlink():
                raise ValueError(f"Refusing to write through a symlink: {destination}")
            destination.write_bytes(payload)
            print(f"Built {destination} ({len(payload)} bytes)")
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
