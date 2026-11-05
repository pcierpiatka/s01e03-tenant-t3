# s01e03-tenant-t3 — #4471 split into the problems it holds

The support desk merged 412 reports about wrong booking dates into ticket #4471 on subject lines alone.
This repo reads every body, splits the ticket into the problems it really holds, files one issue per
problem with the number of reports it covers, and adds a signed page to the desk's knowledge base (kb).

- **Issues**: one per problem, generated from `analysis/counts.json` by `tools/issues.py`.
- **Page**: `src/routes/kb/incidents/4471-what-it-shows/+page.svx`; rendered copy in
  `build/kb/incidents/4471-what-it-shows/index.html` (as the desk will see it).
- **Numbers**: `tools/counts.py` is the only source. It dedupes the export the way the kb's own
  `uniqueById` does, reads one id list per problem from `analysis/ids/`, and checks that every merged
  report is in exactly one list. The page's `ProblemTable` computes the same numbers at render time.
- **kb export**: `src/` is the desk's export (see `KB-README.md`), untouched except for the new page,
  the `ProblemTable` component and `src/lib/data/problems-4471.json`, which `counts.py` writes.

Build: `bun install && bun run build` (SvelteKit + mdsvex, static adapter).
Count: `python3 -I tools/counts.py && python3 -I tools/issues.py`.
