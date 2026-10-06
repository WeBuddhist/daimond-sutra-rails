#!/usr/bin/env python3
"""Check Claude's alignment of a Wikisource commentary against the Dzongsar team's human alignment of the
same commentary from the previous intake (git HEAD, 2026-10-02; other edition, old root numbering).
Read-only QA: nothing from the old alignment is written into the new files.
    python3 0-INBOX/temp/eval_alignment.py <id> <old file stem>"""
import sys, re, json, subprocess, collections, pathlib
sys.path.insert(0, "4-SYSTEM/Skills/aligned-corpus-intake/scripts")
from md_export import read_rows
from concordance import Concordance
from project import is_letter
oid, stem = sys.argv[1], sys.argv[2]
git = lambda p: subprocess.run(["git", "show", f"HEAD:{p}"], capture_output=True, text=True, check=True).stdout
ID = re.compile(r"\s\^([0-9-]+)\s*$")
def blocks(md):
    body = md.split("\n---\n", 1)[1]
    out, pend = [], []
    for para in re.split(r"\n\s*\n", body.strip()):
        lines = [l for l in para.split("\n") if l.strip()]
        txt = []
        for l in lines:
            m = re.match(r"^!\[\[.+?#\^([0-9-]+)\]\]$", l.strip())
            if m: pend.append(m.group(1))
            else: txt.append(l)
        if txt and not txt[0].startswith("#"):
            t = "\n".join(txt); m = ID.search(t)
            out.append((m.group(1) if m else None, t[:m.start()] if m else t, pend)); pend = []
        elif txt: pend = pend
    return out
old_root = [(b, t) for b, t, _ in blocks(git("1-SOURCES/Text/bo-vajracchedika.md")) if b]
disp = [(str(r["row"]), r["text"]) for r in read_rows("0-INBOX/raw-data/dorjeechoepa-root-bo(display).md") if any(is_letter(c) for c in r["text"])]
c1 = Concordance(disp, old_root)
old2disp = {b: [int(x) for x in c1.row(b)["targets"]] for b, _ in old_root}
new_rows = [(str(r["row"]), r["text"]) for r in read_rows(f"0-INBOX/raw-data/wikisource-{oid}/{oid}(root-comm).md")]
old_comm = blocks(git(f"1-SOURCES/Commentaries/{stem}.md"))
c2 = Concordance(new_rows, [(i, t) for i, (b, t, _) in enumerate(old_comm)])
print("edition concordance old commentary -> Wikisource rows:", c2.stats)
human = collections.defaultdict(set)            # display seg -> new rows where the humans place its comment
for i, (b, t, tr) in enumerate(old_comm):
    rows = {int(x) for x in c2.row(i)["targets"]}
    for n in tr:
        for d in old2disp.get(n, []):
            human[d] |= rows
mine = {}
for i, line in enumerate(open(f"0-INBOX/raw-data/wikisource-{oid}/{oid}-root(root-comm).md", encoding="utf-8").read().splitlines(), 1):
    pass
summ = json.load(open(f"0-INBOX/temp/align-{oid}/summary.json"))
tsv = [l.split("\t") for l in open(f"0-INBOX/temp/align-{oid}/alignment.tsv", encoding="utf-8").read().splitlines()[1:]]
for row, segs, *_ in tsv:
    for s in filter(None, segs.split(",")):
        mine[int(s)] = int(row)
both = [d for d in mine if d in human and human[d]]
exact = [d for d in both if mine[d] in human[d]]
near = [d for d in both if mine[d] not in human[d] and min(abs(mine[d] - r) for r in human[d]) <= 1]
far = [d for d in both if d not in exact and d not in near]
only_h = sorted(d for d in human if human[d] and d not in mine)
only_m = sorted(d for d in mine if d not in human or not human[d])
print(f"segments: mine {len(mine)}, human {sum(1 for d in human if human[d])}, both {len(both)}: "
      f"same row {len(exact)}, neighbouring row {len(near)}, elsewhere {len(far)}")
print("human-only (not aligned by me):", len(only_h), only_h[:60])
print("mine-only (humans did not align):", len(only_m), only_m[:40])
print("elsewhere:", [(d, mine[d], sorted(human[d])[:4]) for d in far][:40])
out = pathlib.Path(f"0-INBOX/temp/align-{oid}/eval-vs-dzongsar.json")
out.write_text(json.dumps({"human": {d: sorted(v) for d, v in human.items()}, "mine": mine, "exact": exact, "near": near,
                           "far": far, "human_only": only_h, "mine_only": only_m, "edition_concordance": c2.stats}, indent=0))
