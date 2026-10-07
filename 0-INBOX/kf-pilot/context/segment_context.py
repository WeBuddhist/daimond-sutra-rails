#!/usr/bin/env python3
"""Per-segment context for the root text: Tibetan, aligned Sanskrit, aligned commentary passages.

Library:
    from segment_context import build_context
    ctx = build_context()          # {root_id: {"bo", "sa": [{"id","text"}], "commentaries": {cid: [{"id","text"}]}}}

CLI:
    python3 segment_context.py [--root bo-vajracchedika] [--out context.json] [--show 7-28]

Joins follow the alignment recorded in 1-SOURCES/Annotations/*.annotations.json,
never identical block numbers (Tibetan and Sanskrit ids differ in this vault).
- Sanskrit: the root's blocks[id].targets -> ids in the Sanskrit file.
- Commentary: a commentary block whose `targets` name root ids opens a passage;
  the following untargeted blocks continue it until the next targeted block.
  Every root id the opening block targets receives the whole passage.
"""
import argparse
import json
import pathlib

VAULT = pathlib.Path(__file__).resolve().parents[3]
ANN = VAULT / "1-SOURCES/Annotations"


def load(name):
    return json.loads((ANN / f"{name}.annotations.json").read_text(encoding="utf-8"))


def commentary_passages(ann, root_file):
    """{root_id: [ {id: first block id, text: passage} ]} for one commentary."""
    if not (ann.get("target_file") or "").endswith(root_file):
        return {}
    out, cur_targets, cur = {}, None, None
    for bid, b in ann["blocks"].items():
        targets = b.get("targets") or []
        if targets:
            cur = {"id": bid, "text": b.get("text", "")}
            cur_targets = targets
            for t in targets:
                out.setdefault(t, []).append(cur)
        elif cur is not None:
            cur["text"] += " " + b.get("text", "")
    return out


def build_context(root="bo-vajracchedika"):
    rann = load(root)
    sa_name = pathlib.Path(rann["target_file"]).stem
    sa = load(sa_name)["blocks"]
    root_file = f"1-SOURCES/Translations/{root}.md"
    comms = {}
    for f in sorted(ANN.glob("bo-*.annotations.json")):
        cid = f.name.replace(".annotations.json", "")
        if cid == root:
            continue
        p = commentary_passages(json.loads(f.read_text(encoding="utf-8")), root_file)
        if p:
            comms[cid] = p
    ctx = {}
    for rid, b in rann["blocks"].items():
        ctx[rid] = {
            "bo": b.get("text", ""),
            "sa": [{"id": t, "text": sa[t]["text"]} for t in (b.get("targets") or []) if t in sa],
            "commentaries": {cid: p[rid] for cid, p in comms.items() if rid in p},
        }
    return ctx


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="bo-vajracchedika")
    ap.add_argument("--out")
    ap.add_argument("--show")
    a = ap.parse_args()
    ctx = build_context(a.root)
    if a.out:
        pathlib.Path(a.out).write_text(json.dumps(ctx, ensure_ascii=False, indent=1), encoding="utf-8")
    n_sa = sum(1 for c in ctx.values() if c["sa"])
    per_c = {}
    for c in ctx.values():
        for cid in c["commentaries"]:
            per_c[cid] = per_c.get(cid, 0) + 1
    print(f"root blocks={len(ctx)} with_sanskrit={n_sa} with_commentary={per_c}")
    if a.show:
        print(json.dumps(ctx[a.show], ensure_ascii=False, indent=1)[:3000])


if __name__ == "__main__":
    main()
