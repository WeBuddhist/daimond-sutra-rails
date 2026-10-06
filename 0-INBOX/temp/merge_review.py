#!/usr/bin/env python3
"""Fold the reviewers' chunk corrections into 0-INBOX/temp/align-<id>/overrides.yaml (read by ws_comm_align.py)
and check the result keeps segment order. python3 0-INBOX/temp/merge_review.py <id>"""
import sys, pathlib, yaml
oid = sys.argv[1]
ev = pathlib.Path(f"0-INBOX/temp/align-{oid}")
segs, notes = {}, []
for f in sorted((ev / "review").glob("chunk-*.corrections.yaml")):
    for c in (yaml.safe_load(f.read_text(encoding="utf-8")) or {}).get("corrections") or []:
        s = int(c["segment"])
        segs[s] = None if c.get("row") in (None, "null") else int(c["row"])
        notes.append({"segment": s, "row": segs[s], "evidence": c.get("evidence"), "from": f.name})
assign = {}
for l in (ev / "alignment.tsv").read_text(encoding="utf-8").splitlines()[1:]:
    r, ss = l.split("\t")[:2]
    for s in filter(None, ss.split(",")):
        assign[int(s)] = int(r)
for s, r in segs.items():
    if r is None: assign.pop(s, None)
    else: assign[s] = r
bad, last = [], 0
for s in sorted(assign):
    if assign[s] < last: bad.append((s, assign[s], last))
    last = max(last, assign[s])
(ev / "overrides.yaml").write_text(
    "# Reviewed corrections to the mechanical alignment (Claude reviewers, 2026-10-04), one per segment, with evidence.\n"
    + yaml.safe_dump({"segments": dict(sorted(segs.items())), "evidence": notes}, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
print(oid, len(segs), "corrections;", "order violations:", bad[:20] or "none")
