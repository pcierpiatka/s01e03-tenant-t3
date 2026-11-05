#!/usr/bin/env python3 -I
"""The only source of numbers for #4471.

Reads the kb's report export, dedupes it the way src/lib/kb/causes.ts does (one id, one report),
reads one id list per problem from analysis/ids/<problem>.txt, checks the invariants, and writes
analysis/counts.json plus src/lib/data/problems-4471.json (what the page's component renders).
Run: python3 -I tools/counts.py
"""
import hashlib, json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / 'src/lib/data/reports-4471.json'
TENANTS = ROOT / 'src/lib/data/tenants'
IDS = ROOT / 'analysis/ids'
OUT_JSON = ROOT / 'analysis/counts.json'
OUT_DATA = ROOT / 'src/lib/data/problems-4471.json'
TICKET = 4471

# Problems, in the order they are filed. Titles are the issue titles.
PROBLEMS = [
    ('parser', 'Shared date parser reads day-first dates month-first'),
    ('hint', 'booking-v3 form hint says MM/DD/YYYY, form reads the date day-first'),
    ('one-day', 'Bookings land one day off (timezone), no month change'),
]


def fail(msg):
    print('INVARIANT FAILED: ' + msg, file=sys.stderr)
    sys.exit(1)


def main():
    raw = REPORTS.read_bytes()
    rows = json.loads(raw)
    # uniqueById: new Map(reports.map(r => [r.id, r])) — last row wins per id, first-seen order.
    unique = list({r['id']: r for r in rows}.values())
    merged = [r for r in unique if r['mergedInto'] == TICKET]
    tenants = {}
    for f in sorted(TENANTS.glob('*.json')):
        t = json.loads(f.read_text())
        tenants[t['handle']] = t
    by_id = {r['id']: r for r in merged}

    lists = {}
    for key, _ in PROBLEMS:
        p = IDS / f'{key}.txt'
        if not p.exists():
            fail(f'missing id list {p}')
        ids = [l.strip() for l in p.read_text().splitlines() if l.strip() and not l.startswith('#')]
        if len(ids) != len(set(ids)):
            fail(f'{key}: duplicate ids in list')
        lists[key] = ids

    # Invariants: every id is a real merged report; lists are disjoint; together they cover all of them.
    seen = Counter()
    for key, ids in lists.items():
        for i in ids:
            if i not in by_id:
                fail(f'{key}: {i} is not a report merged into #{TICKET}')
            seen[i] += 1
    twice = [i for i, n in seen.items() if n > 1]
    if twice:
        fail(f'ids in more than one problem: {twice}')
    missing = sorted(set(by_id) - set(seen))
    if missing:
        fail(f'{len(missing)} merged reports in no problem: {missing[:10]}')
    if sum(len(v) for v in lists.values()) != len(merged):
        fail('sum of problem counts != merged count')

    problems = []
    for key, title in PROBLEMS:
        rs = [by_id[i] for i in lists[key]]
        days = sorted(r['receivedAt'][:10] for r in rs)
        problems.append({
            'key': key,
            'title': title,
            'reports': len(rs),
            'tenants': sorted({r['tenant'] for r in rs}),
            'channels': dict(sorted(Counter(r['channel'] for r in rs).items())),
            'intakeTag': dict(sorted(Counter(r['meta']['intakeTag'] for r in rs).items())),
            'firstSeen': days[0] if days else None,
            'lastSeen': days[-1] if days else None,
            'ids': sorted(lists[key]),
        })
    out = {
        'ticket': TICKET,
        'source': str(REPORTS.relative_to(ROOT)),
        'sha256': hashlib.sha256(raw).hexdigest(),
        'rows': len(rows),
        'unique': len(unique),
        'merged': len(merged),
        'duplicateRows': len(rows) - len(unique),
        'problems': problems,
    }
    OUT_JSON.write_text(json.dumps(out, indent=1) + '\n')
    OUT_DATA.write_text(json.dumps({'ticket': TICKET, 'sha256': out['sha256'], 'rows': out['rows'], 'merged': out['merged'],
                                    'problems': [{k: p[k] for k in ('key', 'title', 'reports', 'ids')} for p in problems]}, indent=1) + '\n')
    print(f'rows {out["rows"]}  unique {out["unique"]}  merged into #{TICKET} {out["merged"]}  (dup rows {out["duplicateRows"]})')
    for p in problems:
        print(f'  {p["key"]:8} {p["reports"]:4}  tenants {len(p["tenants"])}  {p["firstSeen"]} → {p["lastSeen"]}  {p["title"]}')
    print('invariants ok')


if __name__ == '__main__':
    main()
