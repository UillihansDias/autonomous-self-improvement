#!/usr/bin/env python3
"""Check package structure and, optionally, an experiment record; not outcomes."""
import argparse
import json
import re
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--root', required=True)
parser.add_argument('--record', type=Path, help='experiment JSON to check against the bundled schema')
args = parser.parse_args()
root = Path(args.root).resolve(strict=True)
skill = (root / 'SKILL.md').read_text()
assert skill.startswith('---\nname: autonomous-self-improvement\ndescription: '), 'Missing frontmatter'
for rel in ('references/workspace-audit.md', 'references/delegation.md', 'references/evaluation.md', 'scripts/audit_snapshot.py', 'scripts/validate_package.py', 'assets/improvement-record.schema.json'):
    assert rel in skill, f'Unreferenced support file: {rel}'
    assert (root / rel).is_file(), f'Missing support file: {rel}'
schema = json.loads((root / 'assets/improvement-record.schema.json').read_text())


def check(value, rule, location='$'):
    """Check the schema keywords used by this package without extra dependencies."""
    expected = rule.get('type')
    kinds = {'object': dict, 'array': list, 'string': str, 'boolean': bool}
    if expected and (expected not in kinds or not isinstance(value, kinds[expected])):
        raise ValueError(f'{location}: expected {expected}')
    if 'enum' in rule and value not in rule['enum']:
        raise ValueError(f'{location}: invalid value {value!r}')
    if expected == 'object':
        properties = rule.get('properties', {})
        for name in rule.get('required', []):
            if name not in value:
                raise ValueError(f'{location}: missing required field {name}')
        if rule.get('additionalProperties') is False:
            extra = set(value) - set(properties)
            if extra:
                raise ValueError(f'{location}: unknown field {sorted(extra)[0]}')
        for name, item in value.items():
            if name in properties:
                check(item, properties[name], f'{location}.{name}')
    if expected == 'array':
        for index, item in enumerate(value):
            check(item, rule['items'], f'{location}[{index}]')


if args.record:
    record = json.loads(args.record.read_text())
    check(record, schema)
    print('Package structure and record shape OK; outcome evidence and runtime untested')
else:
    print('Package structure and support references OK; record and runtime untested')
