#!/usr/bin/env python3
"""Read-only metadata snapshot of canonical workspace documents and skill files."""
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--workspace', required=True)
parser.add_argument('--output', required=True)
args = parser.parse_args()
root = Path(args.workspace).expanduser().resolve(strict=True)
if not root.is_dir():
    parser.error('workspace must be a directory')
paths = [root / n for n in ('AGENTS.md', 'SOUL.md', 'TOOLS.md')]
if (root / 'skills').is_dir():
    paths.extend(sorted((root / 'skills').glob('*/SKILL.md')))
if (root / '.learnings').is_dir():
    paths.extend(sorted(p for p in (root / '.learnings').iterdir() if p.is_file()))
items = []
for p in paths:
    if p.is_file() and not p.is_symlink():
        s = p.stat()
        items.append({'path': str(p.relative_to(root)), 'bytes': s.st_size, 'mtime_epoch': s.st_mtime})
out = Path(args.output).expanduser().resolve()
if out.is_dir():
    parser.error('output must be a file path')
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps({'workspace': str(root), 'files': items}, indent=2) + '\n')
print(f'Inventoried {len(items)} files without modifying workspace content')
