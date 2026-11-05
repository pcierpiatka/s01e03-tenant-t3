#!/usr/bin/env python3 -I
"""Render one issue per problem from analysis/counts.json (never from anywhere else).
Writes analysis/issues/<key>.md with the title on line 1 and the body after a blank line.
Run: python3 -I tools/issues.py   (after tools/counts.py)
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
counts = json.loads((ROOT / 'analysis/counts.json').read_text())
OUT = ROOT / 'analysis/issues'
OUT.mkdir(exist_ok=True)

WHAT = {
    'parser': ("The shared parser reads every date month first. Every tenant on file writes the day first, "
               "so a booking for 7 April goes out as 4 July. This is the bug #4471 was opened for.",
               "Make the parser read dates in the tenant's locale order (`dayFirst(locale)` in `src/lib/kb/causes.ts` already asks the platform)."),
    'hint': ("booking-v3 prints `MM/DD/YYYY` under its date field. People at the three booking-v3 tenants type what the hint says, "
             "month first, and the form reads it day first. Same symptom as the parser bug, different code, different fix. "
             "The kb's own `causeOf` already separates it; the old #4471 page rendered it as 'no ticket of its own'.",
             "Change the booking-v3 hint to the tenant's order, or make the form read what the hint says."),
    'one-day': ("These bodies show no day/month swap. The booking lands one day off, or two people in different places see different days "
                "for the same meeting, or an invite arrives the day before the booking. The desk's notes read them as a one-day move "
                "but filed them under the parser by tenant. A parser fix will not touch them; this looks like a timezone or day-boundary bug.",
                "Reproduce with a tenant and a client in different timezones; check how the invite's date is derived from the booking's instant."),
}

for p in counts['problems']:
    what, fix = WHAT[p['key']]
    ids = p['ids']
    body = f"""**Reports covered: {p['reports']}** of the {counts['merged']} merged into #{counts['ticket']} (export sha256 `{counts['sha256'][:12]}…`, {counts['rows']} rows, {counts['duplicateRows']} duplicate rows dropped by id).

## What it is

{what}

## Where it shows

- Tenants: {len(p['tenants'])} ({', '.join(p['tenants'])})
- Channels: {', '.join(f'{c} ×{n}' for c, n in p['channels'].items())}
- Intake tagged them: {', '.join(f'{c} ×{n}' for c, n in p['intakeTag'].items())}
- First seen {p['firstSeen']}, last seen {p['lastSeen']}

## Suggested fix

{fix}

## How the count was made

Every body was read blind (no intake tag, no desk note) and classified by what it says; where the body and the kb's rule disagreed, an adjudicator and a second reader placed it. `tools/counts.py` in this repo is the only source of these numbers and checks that each of the {counts['merged']} reports is in exactly one problem. Page: `src/routes/kb/incidents/4471-what-it-shows/+page.svx`.

<details><summary>Report ids ({len(ids)})</summary>

{' '.join(ids)}

</details>
"""
    title = f"[#4471 split] {p['title']} ({p['reports']} reports)"
    (OUT / f"{p['key']}.md").write_text(title + '\n\n' + body)
    print(title)
