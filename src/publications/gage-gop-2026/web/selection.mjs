export function restoreSelection(saved, records) {
  const selected = new Set(), counts = new Map();
  const allowed = new Set(Array.isArray(saved) ? saved : []);
  for (const row of records) {
    if (!allowed.has(row.id)) continue;
    const count = counts.get(row.contest) || 0;
    if (count < row.limit) { selected.add(row.id); counts.set(row.contest, count + 1); }
  }
  return selected;
}
export function canMark(selected, row, records) {
  return records.filter(r => r.contest === row.contest && selected.has(r.id)).length < row.limit;
}
