[#4471 split] Bookings land one day off (timezone), no month change (5 reports)

**Reports covered: 5** of the 412 merged into #4471 (export sha256 `2bd8489da70d…`, 427 rows, 15 duplicate rows dropped by id).

## What it is

These bodies show no day/month swap. The booking lands one day off, or two people in different places see different days for the same meeting, or an invite arrives before the booking it belongs to. The desk's notes read them as a one-day move but filed them under the parser by tenant. A parser fix will not touch them; this looks like a timezone or day-boundary bug.

## Where it shows

- Tenants: 5 (alder.physio, kettle.books, lantern.row, nine.lanterns, pale.harbour)
- Channels: app ×2, email ×3
- Intake tagged them: parser ×5
- First seen 2026-04-02, last seen 2026-10-04

## Suggested fix

Reproduce with a tenant and a client in different timezones; check how the invite's date is derived from the booking's instant.

## How the count was made

Every body was read blind (no intake tag, no desk note) and classified by what it says; where the body and the kb's rule disagreed, an adjudicator and a second reader placed it. `tools/counts.py` in this repo is the only source of these numbers and checks that each of the 412 reports is in exactly one problem. Page: `src/routes/kb/incidents/4471-what-it-shows/+page.svx`.

<details><summary>Report ids (5)</summary>

R-41202 R-41209 R-41236 R-41344 R-41620

</details>
