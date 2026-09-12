#!/usr/bin/env python3
"""Check the portable KLOD package; --sync refreshes its bundled copies.

Uses only Python's standard library and the files in this repository.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
from build_integrations import BUNDLED_SKILLS, LOCAL_NAMES

ROOT = Path(__file__).resolve().parents[2]
REPO_URL = "https://github.com/AlexandruGirlea/keepthelightson"
SKILLS = ("klod", "klod-check")
ROOT_DIRECTORIES = {".github", "skills", "spec", "rfcs", "integrations"}
ROOT_FILES = {
    ".gitignore", "README.md", "CONTRIBUTING.md", "GOVERNANCE.md",
    "CODE_OF_CONDUCT.md", "CHANGELOG.md", "LICENSE-CODE.md", "LICENSE-SPEC.md",
    "CITATION.cff", "apm.yml",
}
PUBLIC_ASSETS = {
    Path(".github/assets/klod-mark.svg"),
    Path(".github/assets/klod-story.gif"),
}
VERSION = r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?"
LINK = re.compile(r"!?\[[^\]\n]*\]\(\s*(<[^>\n]+>|[^)\s]+)(?:\s+[\"'][^\n]*?[\"'])?\s*\)")


def read(path: str | Path) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def replace_once(pattern: str, replacement: str, text: str, name: str) -> str:
    updated, count = re.subn(pattern, lambda _: replacement, text, flags=re.M | re.S)
    if count != 1:
        raise ValueError(f"Expected one {name}; found {count}")
    return updated


def version_in(text: str, pattern: str, name: str) -> str:
    matches = re.findall(pattern, text, flags=re.M)
    if len(matches) != 1 or not re.fullmatch(VERSION, matches[0]):
        raise ValueError(f"Expected one semantic version in {name}")
    return matches[0]


def expected_outputs() -> dict[Path, str]:
    spec = read("spec/SPECIFICATION.md")
    spec_version = version_in(spec, r"^\*\*Version (\S+)\*\*", "the specification")
    package_version = version_in(read("apm.yml"), r"^version: *[\"']?([^\s\"']+)[\"']? *$", "apm.yml")
    principle_match = re.search(r"^## The six principles\n(.*?)(?=\n---\n)", spec, flags=re.M | re.S)
    if not principle_match:
        raise ValueError("The specification's six principles could not be found")
    principles = principle_match.group(0).strip()
    if len(re.findall(r"^\*\*[1-6]\. ", principles, flags=re.M)) != 6:
        raise ValueError("Expected six numbered principles in the specification")
    readme = replace_once(
        r"^## The six principles\n.*?(?=^## The two skills\n)",
        principles + "\n\n", read("README.md"), "README principles section",
    )
    blocks = {
        "release-line": f"**Specification {spec_version}** and **skills package {package_version}**. Release tag: `v{package_version}`.",
        "install-command": f"```sh\napm install AlexandruGirlea/keepthelightson#v{package_version}\n```",
    }
    for name, body in blocks.items():
        marker = f"<!-- generated:{name} -->"
        end = f"<!-- /generated:{name} -->"
        readme = replace_once(re.escape(marker) + r".*?" + re.escape(end),
                              marker + "\n" + body + "\n" + end, readme, name)
    licence = replace_once(
        r"<!-- generated:spec-version -->.*?<!-- /generated:spec-version -->",
        f"<!-- generated:spec-version -->{spec_version}<!-- /generated:spec-version -->",
        read("LICENSE-SPEC.md"), "licence version",
    )
    citation = replace_once(r"^version: [^\n]+$", f"version: {spec_version}",
                            read("CITATION.cff"), "citation version")
    outputs = {ROOT / "README.md": readme, ROOT / "LICENSE-SPEC.md": licence,
               ROOT / "CITATION.cff": citation}
    manifest = ROOT / "integrations/spec-kit/extension.yml"
    outputs[manifest] = replace_once(r"^  version: [^\n]+$", f'  version: "{package_version}"',
                                     read(manifest), "Spec Kit extension version")
    installer = ROOT / "integrations/openspec/install.py"
    outputs[installer] = replace_once(r"^VERSION = [^\n]+$", f'VERSION = "{package_version}"',
                                      read(installer), "OpenSpec integration version")
    exclusions = ", ".join(repr(name) for name in sorted(LOCAL_NAMES))
    outputs[installer] = replace_once(r"^LOCAL_NAMES = [^\n]+$", "LOCAL_NAMES = {" + exclusions + "}",
                                      outputs[installer], "OpenSpec local file exclusions")
    guide = ROOT / "integrations/openspec/README.md"
    outputs[guide] = replace_once(rf"^\*\*Version:\*\* {VERSION}\.", f"**Version:** {package_version}.",
                                  read(guide), "OpenSpec guide version")
    # Setup guides install from the tagged release, so their URLs follow the package version.
    for path in (ROOT / "README.md", ROOT / "integrations/spec-kit/README.md", guide):
        text = re.sub(re.escape(REPO_URL) + rf"/releases/download/v{VERSION}/",
                      f"{REPO_URL}/releases/download/v{package_version}/", outputs.get(path, read(path)))
        outputs[path] = re.sub(rf"--branch v{VERSION} ", f"--branch v{package_version} ", text)
    portable_licence = licence
    for name in ("LICENSE-CODE.md", "CONTRIBUTING.md"):
        portable_licence = portable_licence.replace(f"]({name})", f"]({REPO_URL}/blob/main/{name})")
    for skill in SKILLS:
        references = ROOT / "skills" / skill / "references"
        outputs[references / "specification.md"] = spec
        outputs[references / "LICENSE-SPEC.md"] = portable_licence
    for relative in ("references/human-control.md", "references/report-metadata.md", "scripts/report_metadata.py"):
        outputs[ROOT / "skills/klod-check" / relative] = read(Path("skills/klod") / relative)
    # Bundle the same canonical skills for both native workflow layouts. Use the
    # pending canonical outputs so one --sync refreshes every layer together.
    for integration, destination in BUNDLED_SKILLS.items():
        for skill in SKILLS:
            source = ROOT / "skills" / skill
            for path in sorted(source.rglob("*")):
                if not path.is_file() or path.suffix not in {".md", ".py"}:
                    continue
                if any(part in LOCAL_NAMES for part in path.relative_to(source).parts):
                    continue
                outputs[ROOT / destination / skill / path.relative_to(source)] = outputs.get(path, read(path))
        adapter = ROOT / "integrations" / integration
        outputs[adapter / "LICENSE-CODE.md"] = read("LICENSE-CODE.md")
        outputs[adapter / "LICENSE-SPEC.md"] = portable_licence
    return outputs


def package_files(errors: list[str]) -> list[Path]:
    for path in ROOT.iterdir():
        if path.name in LOCAL_NAMES:
            continue
        expected = ROOT_DIRECTORIES if path.is_dir() else ROOT_FILES
        if path.name not in expected:
            errors.append(f"Unexpected root entry: {path.name}")
    for name in sorted(ROOT_FILES | ROOT_DIRECTORIES):
        if not (ROOT / name).exists():
            errors.append(f"Missing package entry: {name}")
    for skill in SKILLS:
        if not (ROOT / "skills" / skill / "SKILL.md").is_file():
            errors.append(f"Missing skill instructions: skills/{skill}/SKILL.md")
    if (ROOT / "skills").is_dir():
        for path in (ROOT / "skills").iterdir():
            if path.name not in SKILLS and path.name not in LOCAL_NAMES:
                errors.append(f"Unexpected skill entry: {path.relative_to(ROOT)}")
    files = []
    for directory, dirs, names in os.walk(ROOT, followlinks=False):
        parent = Path(directory)
        for name in list(dirs):
            path = parent / name
            if path.is_symlink():
                errors.append(f"Symlink is not a portable package file: {path.relative_to(ROOT)}")
                dirs.remove(name)
            elif name in LOCAL_NAMES:
                dirs.remove(name)
        for name in names:
            path = parent / name
            relative = path.relative_to(ROOT)
            if name in LOCAL_NAMES or path.suffix == ".pyc":
                continue
            if path.is_symlink():
                errors.append(f"Symlink is not a portable package file: {path.relative_to(ROOT)}")
                continue
            if (path.suffix not in {".md", ".py", ".yml", ".yaml", ".cff"}
                    and path.name != ".gitignore" and relative not in PUBLIC_ASSETS):
                errors.append(f"Unexpected package file: {relative}")
                continue
            files.append(path)
    return files


def prose(text: str) -> str:
    """Ignore examples in fenced blocks and inline code when checking links."""
    lines = []
    fence = None
    for line in text.splitlines():
        match = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            lines.append("")
        elif fence is None:
            lines.append(line)
        else:
            lines.append("")
    return re.sub(r"(`+).*?\1", "", "\n".join(lines))


def heading_ids(text: str) -> set[str]:
    seen: dict[str, int] = {}
    result = set()
    for heading in re.findall(r"^ {0,3}#{1,6} +(.+?) *#* *$", prose(text), flags=re.M):
        heading = re.sub(r"!?\[([^]]+)\]\([^)]*\)", r"\1", heading)
        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        duplicate = seen.get(slug, 0)
        seen[slug] = duplicate + 1
        result.add(slug if duplicate == 0 else f"{slug}-{duplicate}")
    return result


def check_links(files: list[Path], errors: list[str]) -> int:
    count = 0
    headings = {path: heading_ids(path.read_text(encoding="utf-8"))
                for path in files if path.suffix == ".md"}
    for path in headings:
        relative = path.relative_to(ROOT)
        skill_root = ROOT / "skills" / relative.parts[1] if relative.parts[0] == "skills" else None
        for bundled in BUNDLED_SKILLS.values():
            base = ROOT / bundled
            if path.is_relative_to(base):
                skill_root = base / path.relative_to(base).parts[0]
        text = prose(path.read_text(encoding="utf-8"))
        destinations = [match.group(1) for match in LINK.finditer(text)]
        destinations.extend(re.findall(r"^ {0,3}\[[^]\n]+\]:\s*(<[^>\n]+>|\S+)", text, flags=re.M))
        for destination in destinations:
            href = re.sub(r"\\([()])", r"\1", destination.strip("<>"))
            url = urlsplit(href)
            if url.scheme in {"http", "https", "mailto"}:
                continue
            if url.scheme or url.netloc:
                errors.append(f"{relative}: unsupported local link {href}")
                continue
            count += 1
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if not target.is_relative_to(ROOT):
                errors.append(f"{relative}: link leaves this repository: {href}")
            elif skill_root and not target.is_relative_to(skill_root):
                errors.append(f"{relative}: link leaves its installed skill: {href}")
            elif not target.exists():
                errors.append(f"{relative}: missing link target: {href}")
            elif url.fragment and target in headings and unquote(url.fragment) not in headings[target]:
                errors.append(f"{relative}: missing heading in link: {href}")
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--sync", action="store_true", help="update bundled copies and release labels before checking")
    modes.add_argument("--check", action="store_true", help="check without writing files (the default)")
    args = parser.parse_args()
    errors: list[str] = []
    files = package_files(errors)
    # Validate the boundary before reading canonical files or changing a bundled copy.
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    try:
        outputs = expected_outputs()
        for bundled in BUNDLED_SKILLS.values():
            base = ROOT / bundled
            for path in base.rglob("*"):
                if path.is_file() and path.suffix in {".md", ".py"} and path not in outputs:
                    errors.append(f"Stale generated integration file: {path.relative_to(ROOT)}")
        for path, expected in outputs.items():
            if not path.exists() or path.read_text(encoding="utf-8") != expected:
                if args.sync:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(expected, encoding="utf-8")
                    print(f"Updated {path.relative_to(ROOT)}")
                else:
                    errors.append(f"Out of sync: {path.relative_to(ROOT)} (run with --sync)")
        files = package_files(errors)
        links = check_links(files, errors)
    except (OSError, ValueError) as error:
        errors.append(str(error))
        links = 0
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Package checks passed: {len(files)} files, {len(SKILLS)} portable skills, {links} local links.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
