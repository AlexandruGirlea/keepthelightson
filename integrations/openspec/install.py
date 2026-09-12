#!/usr/bin/env python3
"""Install the KLOD OpenSpec schema without changing the project's configuration."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import sys


VERSION = "0.1.1"
TESTED_OPENSPEC = "1.13.0"
MANIFEST = ".klod-install.json"
LOCAL_NAMES = {'.DS_Store', '.cache', '.git', '.idea', '.pytest_cache', '.ruff_cache', '.venv', '.vscode', '__pycache__'}


class InstallError(Exception):
    """A project needs attention before its schema can be updated."""


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_path(base: Path, relative: str) -> Path:
    parts = Path(relative).parts
    if not parts or Path(relative).is_absolute() or any(p in (".", "..") for p in parts):
        raise InstallError(f"Unsafe managed path: {relative!r}")
    current = base
    for part in parts:
        current = current / part
        if current.is_symlink():
            raise InstallError(f"Refusing symbolic link: {current}")
    return current


def source_files(source: Path) -> dict[str, str]:
    if not source.is_dir() or source.is_symlink():
        raise InstallError(f"Schema bundle not found: {source}")
    files = {}
    for path in sorted(source.rglob("*")):
        relative = path.relative_to(source)
        if any(part in LOCAL_NAMES for part in relative.parts) or path.suffix in (".pyc", ".pyo"):
            continue
        if path.is_symlink():
            raise InstallError(f"Bundle contains a symbolic link: {path}")
        if path.is_file():
            name = relative.as_posix()
            if name == MANIFEST:
                raise InstallError("A source bundle must not contain an installation manifest")
            files[name] = digest(path)
    required = ("schema.yaml", "verification.md", "skills/klod/SKILL.md", "skills/klod-check/SKILL.md")
    if any(name not in files for name in required):
        raise InstallError("Incomplete bundle: schema, verification and both bundled skills are required")
    return files


def previous_files(destination: Path) -> dict[str, str]:
    path = safe_path(destination, MANIFEST)
    if not path.exists():
        if destination.exists():
            raise InstallError(f"Existing schema is not managed by this installer: {destination}")
        return {}
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
        files = manifest["files"]
        if manifest.get("format") != 1 or not isinstance(files, dict) or not files:
            raise ValueError("invalid manifest structure")
        for name, value in files.items():
            if not isinstance(name, str) or not isinstance(value, str) or len(value) != 64:
                raise ValueError("invalid managed file entry")
            if name == MANIFEST or any(c not in "0123456789abcdef" for c in value):
                raise ValueError("invalid managed file entry")
            safe_path(destination, name)
        return files
    except (KeyError, ValueError, TypeError, OSError) as exc:
        raise InstallError(f"Cannot trust installation manifest {path}: {exc}") from exc


def atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".klod-", delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(content)
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def install(project: Path, source: Path, *, check: bool = False) -> bool:
    project = project.expanduser().resolve()
    if not project.is_dir():
        raise InstallError(f"Project directory does not exist: {project}")
    openspec = safe_path(project, "openspec")
    if not openspec.is_dir():
        raise InstallError("Initialize this project with openspec init before installing KLOD")
    destination = safe_path(project, "openspec/schemas/klod")
    wanted = source_files(source)
    previous = previous_files(destination)

    # Inspect every managed path before writing anything. Local edits and newly
    # colliding files need a user's merge; they are never silently overwritten.
    for name, recorded in previous.items():
        path = safe_path(destination, name)
        if not path.is_file() or digest(path) != recorded:
            raise InstallError(f"Locally changed or missing managed file; preserve and merge it first: {path}")
    for name in wanted:
        path = safe_path(destination, name)
        if name not in previous and path.exists():
            raise InstallError(f"Unmanaged file would be overwritten: {path}")
        for parent in path.parents:
            if parent == destination.parent:
                break
            if parent.exists() and not parent.is_dir():
                raise InstallError(f"A file blocks a required directory: {parent}")

    current = previous == wanted
    if check:
        return current
    if current:
        return True

    # Build the entire next copy first. A failed copy leaves the installation
    # untouched; a failed final rename restores the original directory.
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".klod-stage-", dir=destination.parent))
    replacement = staging / "next"
    backup = staging / "previous"
    keep_backup = False
    try:
        if destination.exists():
            shutil.copytree(destination, replacement, symlinks=True)
        else:
            replacement.mkdir()
        for name, expected in wanted.items():
            if previous.get(name) != expected:
                atomic_write(safe_path(replacement, name), (source / name).read_bytes())
        for name in previous.keys() - wanted.keys():
            safe_path(replacement, name).unlink()
        manifest = {"format": 1, "version": VERSION, "tested_openspec": TESTED_OPENSPEC, "files": wanted}
        atomic_write(replacement / MANIFEST, (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode())
        if destination.exists():
            os.replace(destination, backup)
        try:
            os.replace(replacement, destination)
        except OSError:
            if backup.exists():
                try:
                    os.replace(backup, destination)
                except OSError as exc:
                    keep_backup = True
                    raise InstallError(f"Restore the original schema from {backup}: {exc}") from exc
            raise
    finally:
        if not keep_backup:
            shutil.rmtree(staging)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path.cwd(), help="Existing initialized OpenSpec project (default: current directory)")
    parser.add_argument("--check", action="store_true", help="Check this bundle is installed without writing files")
    args = parser.parse_args()
    try:
        current = install(args.project, Path(__file__).resolve().parent / "schema", check=args.check)
    except (InstallError, OSError) as exc:
        print(f"KLOD installation stopped: {exc}", file=sys.stderr)
        return 1
    if args.check:
        print("KLOD schema matches this bundle." if current else "KLOD schema is not installed or needs an update.")
        return 0 if current else 1
    print(f"KLOD {VERSION} is installed in {args.project.expanduser().resolve() / 'openspec/schemas/klod'}")
    print("Project configuration and existing changes were preserved.")
    print("Next: openspec schema validate klod")
    print("Then: openspec new change <change-name> --schema klod")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
