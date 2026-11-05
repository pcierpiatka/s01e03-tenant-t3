[#4471 split] booking-v3 form hint says MM/DD/YYYY, form reads the date day-first (33 reports)

**Reports covered: 33** of the 412 merged into #4471 (export sha256 `2bd8489da70d…`, 427 rows, 15 duplicate rows dropped by id).

## What it is

booking-v3 prints `MM/DD/YYYY` under its date field. People at the three booking-v3 tenants type what the hint says, month first, and the form reads it day first. Same symptom as the parser bug, different code, different fix. The kb's own `causeOf` already separates it; the old #4471 page rendered it as 'no ticket of its own'.

## Where it shows

- Tenants: 3 (alder.physio, copper.studio, pale.harbour)
- Channels: form ×33
- Intake tagged them: hint ×18, parser ×15
- First seen 2026-04-17, last seen 2026-09-22

## Suggested fix

Change the booking-v3 hint to the tenant's order, or make the form read what the hint says.

## How the count was made

Every body was read blind (no intake tag, no desk note) and classified by what it says; where the body and the kb's rule disagreed, an adjudicator and a second reader placed it. `tools/counts.py` in this repo is the only source of these numbers and checks that `parser` and `hint` together cover each of the 412 reports exactly once, and that `one-day` is counted where the desk files it. Page: `src/routes/kb/incidents/4471-what-it-shows/+page.svx`.

<details><summary>Report ids (33)</summary>

R-41230 R-41241 R-41251 R-41259 R-41262 R-41275 R-41294 R-41305 R-41308 R-41366 R-41372 R-41384 R-41387 R-41396 R-41400 R-41406 R-41415 R-41416 R-41418 R-41428 R-41439 R-41441 R-41449 R-41453 R-41456 R-41460 R-41472 R-41485 R-41493 R-41539 R-41572 R-41582 R-41584

</details>
