<script lang="ts">
  // The problems inside one merged ticket, counted at render time from the id lists in
  // src/lib/data/problems-<ticket>.json (written by tools/counts.py). Words stay in the page.
  import reports from '#lib/data/reports-4471.json';
  import problems from '#lib/data/problems-4471.json';
  import { uniqueById, type Report } from '#lib/kb/causes';

  let { ticket }: { ticket: number } = $props();

  const merged = $derived(uniqueById(reports as Report[]).filter((r) => r.mergedInto === ticket));
  const byId = $derived(new Map(merged.map((r) => [r.id, r])));
  const rows = $derived(
    problems.problems.map((p) => {
      const rs = p.ids.map((id) => byId.get(id)).filter((r): r is Report => !!r);
      const days = rs.map((r) => r.receivedAt.slice(0, 10)).sort();
      const channels = rs.reduce<Record<string, number>>((n, r) => ({ ...n, [r.channel]: (n[r.channel] ?? 0) + 1 }), {});
      return {
        ...p,
        count: rs.length,
        tenants: new Set(rs.map((r) => r.tenant)).size,
        channels: Object.entries(channels).sort((a, b) => b[1] - a[1]).map(([c, n]) => `${c} ×${n}`).join(' · '),
        firstSeen: days[0],
        lastSeen: days[days.length - 1],
        missing: p.ids.length - rs.length,
      };
    })
  );
  const placed = $derived(rows.reduce((n, r) => n + r.count, 0));
  const twice = $derived(problems.problems.flatMap((p) => p.ids).length - new Set(problems.problems.flatMap((p) => p.ids)).size);
  const ok = $derived(placed === merged.length && twice === 0 && rows.every((r) => r.missing === 0));
</script>

<p class="sum">
  <strong>{merged.length}</strong> reports merged into #{ticket} ·
  <strong>{rows.length}</strong> problems · {placed} placed, each once
</p>

<table>
  <thead>
    <tr><th>problem</th><th>reports</th><th>channels</th><th>tenants</th><th>seen</th></tr>
  </thead>
  <tbody>
    {#each rows as r (r.key)}
      <tr>
        <td><code>{r.key}</code> · {r.title}</td>
        <td>{r.count}</td>
        <td class="tags">{r.channels}</td>
        <td>{r.tenants}</td>
        <td>{r.firstSeen} → {r.lastSeen}</td>
      </tr>
    {/each}
  </tbody>
</table>

{#if !ok}
  <p class="warn">The id lists do not add up: {placed} placed of {merged.length}, {twice} ids placed twice. Re-run tools/counts.py.</p>
{/if}

<style>
  .sum { font-size: 1.1rem; }
  .tags { color: var(--muted); font-size: 0.85em; }
  .warn { color: var(--warn); font-weight: 600; }
</style>
