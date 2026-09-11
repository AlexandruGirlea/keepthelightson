#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Print a report header from Git and the clock, with credentials stripped from the origin URL.

Pass --model and --model-source only when the runtime exposes the exact model identity.
"""
import argparse
from datetime import datetime
from pathlib import Path
import re
import subprocess
from urllib.parse import urlsplit, urlunsplit
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def one_line(value):
    if not isinstance(value, str) or not value.strip() or any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise ValueError('Metadata values must be nonempty single-line text')
    return value.strip()


def sanitise_origin(raw):
    """Strip userinfo, query and fragment from a Git origin."""
    raw = one_line(raw)
    if '://' not in raw:
        scp = re.fullmatch(r'(?:[^/@\s]+@)?(?P<host>[A-Za-z0-9.-]+):(?P<path>[^\s]+)', raw)
        if scp and not re.match(r'^[A-Za-z]:[/\\]', raw):
            raw = f"ssh://{scp['host']}/{scp['path']}"
        elif raw.startswith(('/', './', '../', '~')) or re.match(r'^[A-Za-z]:[/\\]', raw):
            return raw.split('?', 1)[0].split('#', 1)[0]
        else:
            raise ValueError('Origin format cannot be safely displayed')
    if any(char.isspace() for char in raw):
        raise ValueError('Origin URL contains unencoded whitespace')
    url = urlsplit(raw)
    if url.scheme not in ('https', 'http', 'ssh', 'git', 'file'):
        raise ValueError('Origin scheme cannot be safely displayed')
    if url.scheme == 'file':
        if url.username or url.password:
            raise ValueError('Credential-bearing local origin cannot be safely displayed')
        return urlunsplit(('file', url.hostname or '', url.path, '', ''))
    host = url.hostname
    if not host or not re.fullmatch(r'[A-Za-z0-9.:-]+', host):
        raise ValueError('Origin hostname cannot be safely displayed')
    authority = f'[{host}]' if ':' in host else host
    if url.port is not None:
        authority += f':{url.port}'
    return urlunsplit((url.scheme, authority, url.path, '', ''))


def git_read(project, *arguments):
    """Capture output privately; callers never print raw Git output or errors."""
    try:
        result = subprocess.run(['git', '-C', str(project), *arguments], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True, timeout=5, check=False)
    except FileNotFoundError:
        return None, 'Git executable is unavailable'
    except (OSError, subprocess.TimeoutExpired):
        return None, 'Git metadata could not be read within the local check'
    if result.returncode == 0:
        return result.stdout.strip(), None
    if 'not a git repository' in result.stderr.lower():
        return None, 'Not a Git repository'
    return None, 'Git did not provide the requested metadata'


def collect(project, *, name=None, model=None, model_source=None, timezone='UTC'):
    project = Path(project).resolve(strict=True)
    if not project.is_dir():
        raise ValueError('Project must be a directory')
    if bool(model) != bool(model_source):
        raise ValueError('Provide both the exact model and its runtime identity source, or neither')
    if model and (any(char.isspace() for char in model) or model.lower() in {'codex', 'claude', 'openai', 'chatgpt', 'unknown', 'auto'}):
        raise ValueError('Use an exact active model identifier, not an assistant brand or requested preference')
    metadata = {'project': one_line(name or project.name)}
    inside, error = git_read(project, 'rev-parse', '--is-inside-work-tree')
    if inside == 'true':
        origin, _ = git_read(project, 'remote', 'get-url', 'origin')
        if origin:
            try:
                metadata['git_origin'] = sanitise_origin(origin)
            except ValueError:
                metadata['git_origin'] = 'Unavailable (origin format could not be safely redacted)'
        else:
            metadata['git_origin'] = 'Unavailable (Git repository has no origin remote)'
        revision, _ = git_read(project, 'rev-parse', '--verify', 'HEAD')
        metadata['revision'] = revision if revision and re.fullmatch(r'[0-9a-fA-F]{40,64}', revision) else 'Unavailable (Git repository has no readable commit)'
    elif error == 'Not a Git repository' and not any((parent / '.git').exists() for parent in (project, *project.parents)):
        metadata['git_origin'] = 'Not applicable (local project; not a Git repository)'
        metadata['revision'] = 'Not applicable (local project; no Git revision)'
    else:
        metadata['git_origin'] = f'Unavailable ({error or "Git work-tree status could not be established"})'
        metadata['revision'] = 'Unavailable (Git work-tree status could not be established)'
    metadata['model'] = (f'{one_line(model)} (source: {one_line(model_source)})' if model else
                         'Unavailable (the host did not expose an exact active model identifier)')
    zone = ZoneInfo(timezone)
    metadata['report_timestamp'] = datetime.now(zone).isoformat(timespec='seconds')
    metadata['timezone'] = timezone
    return metadata


def markdown_text(value):
    return re.sub(r'([\\`*_{}\[\]<>])', r'\\\1', value)


def render(metadata, *, kind='KLOD report'):
    title = f"# {markdown_text(metadata['project'])} · {markdown_text(one_line(kind))}"
    fields = [
        ('Project', metadata['project']), ('Git origin', metadata['git_origin']),
        ('Revision', metadata['revision']), ('Model', metadata['model']),
        ('Report timestamp', f"{metadata['report_timestamp']} ({metadata['timezone']})"),
    ]
    return title + '\n\n' + '\n'.join(f'- **{key}:** {markdown_text(value)}' for key, value in fields) + '\n'


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, default=Path.cwd())
    parser.add_argument('--name', help='verified product/project name; otherwise use the directory name')
    parser.add_argument('--kind', default='KLOD report', help='for example KLOD report or KLOD implementation report')
    parser.add_argument('--model', help='exact active model identifier, only if exposed by the runtime')
    parser.add_argument('--model-source', help='where the active runtime identity was observed')
    parser.add_argument('--timezone', default='UTC', help='IANA timezone such as Europe/Bucharest; UTC is the explicit default')
    args = parser.parse_args(argv)
    try:
        value = collect(args.project, name=args.name, model=args.model, model_source=args.model_source, timezone=args.timezone)
        print(render(value, kind=args.kind), end='')
    except (ValueError, OSError, ZoneInfoNotFoundError) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
