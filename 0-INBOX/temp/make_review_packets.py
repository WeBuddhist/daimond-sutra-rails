#!/usr/bin/env python3
"""Review packets for the Claude alignment of a Wikisource commentary: chunks of ~45k characters of rows."""
import sys, json, pathlib
sys.path.insert(0, "4-SYSTEM/Skills/aligned-corpus-intake/scripts")
from md_export import read_rows
oid = sys.argv[1]
disp = {r["row"]: r["text"] for r in read_rows("0-INBOX/raw-data/dorjeechoepa-root-bo(display).md") if r["text"].strip()}
rows = {r["row"]: r["text"] for r in read_rows(f"0-INBOX/raw-data/wikisource-{oid}/{oid}(root-comm).md")}
tsv = [l.split("\t") for l in open(f"0-INBOX/temp/align-{oid}/alignment.tsv", encoding="utf-8").read().splitlines()[1:]]
assign, kind = {}, {}
for r, segs, q, _ in tsv:
    for x in q.split(" | "):
        if ":" in x:
            s = int(x.split(":")[0]); assign[s] = int(r); kind[s] = "inferred" if "(inferred)" in x else "quoted: " + x.split(":", 1)[1]
heads = {}
import re, yaml
ol = open(f"0-INBOX/temp/wiki-toc-{oid}/outline.placed.md", encoding="utf-8").read()
for n in yaml.safe_load(re.search(r"```yaml\n(.*?)```", ol, re.S).group(1))["nodes"]:
    heads.setdefault(int(n["start_row"]), []).append(f"{n['path']} {n['labels']['bo']}")
chunks, cur, size = [], [], 0
for r in sorted(rows):
    cur.append(r); size += len(rows[r])
    if size > 45000:
        chunks.append(cur); cur, size = [], 0
if cur:
    chunks.append(cur)
out = pathlib.Path(f"0-INBOX/temp/align-{oid}/review"); out.mkdir(parents=True, exist_ok=True)
segs_of = lambda rs: sorted(s for s, r in assign.items() if r in rs)
for k, ch in enumerate(chunks, 1):
    lo, hi = ch[0], ch[-1]
    mine = segs_of(set(ch))
    before = max([s for s, r in assign.items() if r < lo], default=0)
    after = min([s for s, r in assign.items() if r > hi], default=431)
    s_lo, s_hi = max(1, (mine[0] if mine else before) - 8), min(430, (mine[-1] if mine else after) + 8)
    L = [f"# Review packet {oid} chunk {k}: commentary rows {lo}–{hi}", "",
         f"Fixed context: root segments up to {before} are placed in rows before {lo}; segment {after} and later are placed in rows after {hi}.",
         f"So in this chunk only segments {before + 1}–{after - 1} may be placed, and each must stay in rows {lo}–{hi}.", "",
         "## Root segments in range (display Tibetan, segment number: text)", ""]
    for s in range(s_lo, s_hi + 1):
        if s in disp:
            L.append(f"- **{s}** [{('row ' + str(assign[s]) + ', ' + kind[s]) if s in assign else 'not placed'}] {disp[s]}")
    L += ["", "## Commentary rows", ""]
    for r in ch:
        if r in heads:
            L += [f"### heading before row {r}: {' / '.join(heads[r])}"]
        L += [f"**Row {r}** — placed segments: {', '.join(map(str, segs_of({r}))) or 'none'}", "", rows[r], ""]
    (out / f"chunk-{k}.md").write_text("\n".join(L), encoding="utf-8")
    print(f"chunk-{k}: rows {lo}-{hi}, segments {before+1}-{after-1}, {sum(len(rows[r]) for r in ch)} chars")
