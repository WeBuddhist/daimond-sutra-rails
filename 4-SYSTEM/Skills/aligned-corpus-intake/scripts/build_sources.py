#!/usr/bin/env python3
"""Build vault source files from human-made raw data, driven by a manifest.

    python3 build_sources.py <manifest.yaml> [--only key,key] [--dry-run]

The manifest (see ../templates/manifest.example.yaml) lists every *work* to
produce, the raw files that supply its text, segmentation, headings and
alignment, the adapter that reads them, and its frontmatter. Works are built
in manifest order; a work may name an earlier work as its alignment target.

Every work produces:
  * the vault markdown file (frontmatter, '# title ^0', headings, transclusions,
    blocks with ids) — the shape the publication linter/parser reads;
  * a sidecar JSON with everything the markdown cannot carry: provenance of
    every block (raw file, paragraph, line), every formatted run (colour,
    bold, italic, highlight, …) with its offsets, reviewer comments, typed
    reference prefixes, variant notes, the raw alignment rows;
  * an entry in the intake report (counts, unmapped rows, warnings).

Adapters never alter wording. They may only: split on paragraph/line
boundaries the source already has, trim outer whitespace of a line, and
remove a typed alignment prefix (recorded in the sidecar).
"""
import argparse
import datetime
import json
import pathlib
import re
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import docx_model                                  # noqa: E402
import openpecha_model                             # noqa: E402
from common import LetterIndex, letters_only, parse_ref_prefix, sha1   # noqa: E402
from project import Projector                      # noqa: E402
import vault_writer                                # noqa: E402

NEUTRAL = docx_model.NEUTRAL_COLOURS


# --------------------------------------------------------------------------
# context shared across works
# --------------------------------------------------------------------------

class Ctx:
    def __init__(self, manifest, vault):
        self.m = manifest
        self.vault = pathlib.Path(vault)
        self.raw = self.vault / manifest.get("raw_root", "0-INBOX/raw-data")
        self.works = {}          # key -> {"path", "blocks": [(id, text)], "index"}
        self._docx = {}
        self.report = []

    def docx(self, rel):
        if rel not in self._docx:
            p = self.raw / rel
            if not p.exists():
                raise FileNotFoundError(p)
            self._docx[rel] = docx_model.read(p)
        return self._docx[rel]

    def op(self, text_id):
        return openpecha_model.load(self.raw / self.m.get("openpecha_root", "openpecha-api"), text_id)

    def index(self, key):
        w = self.works[key]
        if "index" not in w:
            w["index"] = LetterIndex(w["blocks"])
        return w["index"]


def formatted_runs(para, legend=None):
    """Runs that carry any non-neutral formatting, with offsets into the
    paragraph text, labelled by the document legend when one is given."""
    out, pos = [], 0
    legend = legend or {}
    for r in para["runs"]:
        n = len(r["text"])
        attrs = {k: r[k] for k in ("color", "highlight", "shading", "bold", "italic",
                                   "underline", "strike", "vert_align")
                 if r[k] and not (k == "color" and r[k] in NEUTRAL)
                 and not (k == "highlight" and r[k] == "white")}
        if attrs and r["text"].strip():
            label = legend.get(attrs.get("color")) if attrs.get("color") else None
            out.append({"start": pos, "end": pos + n, "text": r["text"],
                        **attrs, **({"meaning": label} if label else {})})
        pos += n
    return out


def para_colour(para):
    """Dominant non-neutral colour of a paragraph's visible letters."""
    weights = {}
    total = 0
    for r in para["runs"]:
        n = len(letters_only(r["text"]))
        total += n
        c = r["color"] if r["color"] not in NEUTRAL else None
        weights[c] = weights.get(c, 0) + n
    if not total:
        return None, False
    c = max(weights, key=weights.get)
    bold = sum(len(letters_only(r["text"])) for r in para["runs"] if r["bold"]) * 2 > total
    return (c if weights[c] * 2 > total else None), bold


def provenance(ctx, rels):
    out = []
    for rel in rels:
        p = ctx.raw / rel
        if p.exists():
            out.append({"file": f"{ctx.m.get('raw_root', '0-INBOX/raw-data')}/{rel}", "sha1": sha1(p)})
    return out


# --------------------------------------------------------------------------
# adapters
# --------------------------------------------------------------------------

def adapt_rows(ctx, spec, rep):
    """One block per non-empty paragraph; id = row number (paragraph index+1).
    Used for a human sentence/segment split whose rows ARE the segmentation."""
    doc = ctx.docx(spec["text"])
    items = []
    comments = doc["comments"]
    for p in doc["paragraphs"]:
        if not p["text"].strip():
            continue
        items.append({"kind": "block", "text": p["text"], "id": str(p["index"] + 1),
                      "source": {"doc": spec["text"], "paragraph": p["index"]},
                      "annotations": formatted_runs(p, spec.get("legend")),
                      **({"comments": [comments[c] for c in p["comment_ids"] if c in comments]}
                         if p["comment_ids"] else {})})
    rep["blocks"] = len(items)
    return items, {}


def adapt_numbered(ctx, spec, rep):
    """Blocks are the auto-numbered paragraphs; id = the number Word renders.
    An unnumbered paragraph before the first number is the title; any other
    unnumbered text is reported (it has no human id)."""
    doc = ctx.docx(spec["text"])
    items, unnumbered = [], []
    for p in doc["paragraphs"]:
        if not p["text"].strip():
            continue
        n = p["numbering"]
        if n and n.get("value"):
            items.append({"kind": "block", "text": p["text"], "id": str(n["value"]),
                          "source": {"doc": spec["text"], "paragraph": p["index"], "rendered": n.get("rendered")},
                          "annotations": formatted_runs(p, spec.get("legend"))})
        else:
            unnumbered.append({"paragraph": p["index"], "text": p["text"]})
    rep["blocks"] = len(items)
    if unnumbered:
        rep["unnumbered_paragraphs"] = unnumbered
    extra = {}
    if spec.get("align_via"):
        extra["raw_alignment"] = _align_via(ctx, spec, items, rep)
    return items, extra


def _align_via(ctx, spec, items, rep):
    """Derive this work's transclusions from a separate line-parallel pair in
    which the same text was re-split (and possibly reordered) against the
    target's rows: each `other` row is located in this work's blocks, each
    `root_rows` row in the target, and the two id sets are linked."""
    own = LetterIndex([(it["id"], it["text"]) for it in items])
    tgt = ctx.index(spec["target"])
    rows_r = _row_lines(ctx, spec["align_via"]["root_rows"])
    rows_o = _row_lines(ctx, spec["align_via"]["other"])
    by_id = {it["id"]: it for it in items}
    raw, unmapped, hr, ho = [], [], 0, 0
    for i in range(max(len(rows_r), len(rows_o))):
        rt = rows_r[i]["text"] if i < len(rows_r) else ""
        ot = rows_o[i]["text"] if i < len(rows_o) else ""
        if not (rt.strip() and ot.strip()):
            continue
        tids, hr = tgt.find(rt, hr)
        oids, ho = own.find(ot, ho)
        raw.append({"row": i + 1, "target_ids": tids or [], "own_ids": oids or [], "text": ot})
        if not tids or not oids:
            unmapped.append({"row": i + 1, "text": ot})
            continue
        for oid in oids:
            t = by_id[oid].setdefault("targets", [])
            t += [x for x in tids if x not in t]
    for it in items:
        if it.get("targets"):
            it["targets"].sort(key=lambda x: int(x) if x.isdigit() else x)
    rep["aligned_rows"] = len(raw) - len(unmapped)
    rep["unmapped_rows"] = unmapped
    return raw


def _row_lines(ctx, rel):
    """Rows of a line-parallel (Tsadrel) doc: one row per paragraph."""
    return ctx.docx(rel)["paragraphs"]


def adapt_parallel(ctx, spec, rep):
    """A translation laid out row-for-row against a root split.

    spec.pair = {root_rows: <docx>, other: <docx>}; row i of one is row i of
    the other, a blank row has no counterpart. Each `root_rows` row is located
    in the target work's blocks by its letters, so the root split may differ
    from the target's segmentation. Block id = first target id (identity when
    the splits agree); rows sharing a first target are kept as lines of one
    block; every target is transcluded."""
    tgt = spec["target"]
    idx = ctx.index(tgt)
    rows_r = _row_lines(ctx, spec["pair"]["root_rows"])
    rows_o = _row_lines(ctx, spec["pair"]["other"])
    comments = ctx.docx(spec["pair"]["other"])["comments"]
    n = max(len(rows_r), len(rows_o))
    blocks, order, hint = {}, [], 0
    unmapped, root_only, raw_pairs = [], [], []
    for i in range(n):
        r = rows_r[i] if i < len(rows_r) else None
        o = rows_o[i] if i < len(rows_o) else None
        rt = r["text"] if r else ""
        ot = o["text"] if o else ""
        if not ot.strip():
            if rt.strip():
                root_only.append(i + 1)
            continue
        ids = []
        if rt.strip():
            ids, hint = idx.find(rt, hint)
            ids = ids or []
        raw_pairs.append({"row": i + 1, "root_row_text": rt, "targets": ids})
        if not ids:
            unmapped.append({"row": i + 1, "text": ot})
            continue
        key = ids[0]
        if key not in blocks:
            blocks[key] = {"kind": "block", "text": "", "id": key, "targets": [], "lines": [],
                           "source": {"doc": spec["pair"]["other"], "rows": []}, "annotations": [],
                           "comments": []}
            order.append(key)
        b = blocks[key]
        off = sum(len(x) + 1 for x in b["lines"])
        b["lines"].append(ot.strip())
        b["source"]["rows"].append(i + 1)
        for t in ids:
            if t not in b["targets"]:
                b["targets"].append(t)
        for a in formatted_runs(o, spec.get("legend")):
            a = dict(a, row=i + 1, start=a["start"] + off, end=a["end"] + off)
            b["annotations"].append(a)
        b["comments"] += [comments[c] for c in o["comment_ids"] if c in comments]
    items = []
    for key in sorted(order, key=lambda k: [int(x) if x.isdigit() else x for x in re.split(r"[-]", k)]):
        b = blocks[key]
        b["text"] = "\n".join(b.pop("lines"))
        if not b["comments"]:
            b.pop("comments")
        items.append(b)
    identity = all(b["targets"] == [b["id"]] for b in items)
    rep.update({"blocks": len(items), "rows": n, "identity_alignment": identity,
                "rows_without_counterpart": root_only, "unmapped_rows": unmapped})
    return items, {"raw_alignment": raw_pairs}


def explode_lines(para):
    """Split a paragraph at its internal line breaks into pseudo-paragraphs
    (same index, a "line" number), each keeping its own runs."""
    out, cur = [], {"runs": []}
    def push():
        cur["text"] = "".join(r["text"] for r in cur["runs"])
        out.append(cur)
    for r in para["runs"]:
        parts = r["text"].split("\n")
        for k, part in enumerate(parts):
            if k:
                push()
                cur = {"runs": []}
            if part:
                cur["runs"].append(dict(r, text=part))
    push()
    return [dict(para, runs=q["runs"], text=q["text"], line=i, numbering=para["numbering"] if i == 0 else None)
            for i, q in enumerate(out)]


def _heading_level(spec, para):
    """Heading level by the document legend: {colour: level} plus optional
    {"<colour>+bold": level} and {"style:<name>": level}."""
    hl = spec.get("headings") or {}
    for pat in spec.get("heading_patterns") or []:
        if re.match(pat["regex"], para["text"].strip()):
            return pat["level"]
    if para["style"] and f"style:{para['style']}" in hl:
        return hl[f"style:{para['style']}"]
    c, bold = para_colour(para)
    if c and bold and f"{c}+bold" in hl:
        return hl[f"{c}+bold"]
    if c and c in hl:
        return hl[c]
    return None


def adapt_ref_commentary(ctx, spec, rep):
    """Commentary whose paragraphs carry typed (or auto-numbered) references
    to the target's numbered segments (Pecha convention: '12.', '4-12.',
    '1-3,5.'). Headings come from the colour/style legend. A paragraph is
    split where an internal line starts with a reference."""
    doc = ctx.docx(spec["text"])
    refs_mode = spec.get("refs", "align")          # align | candidate | none
    legend = spec.get("legend")
    lemma = set(spec.get("lemma_colours") or [])
    items, heads = [], [0, 0]
    n_refs = n_auto = 0
    candidates = []
    title_para = spec.get("title_paragraph")
    paras = doc["paragraphs"]
    if spec.get("split_lines"):
        paras = [q for p in paras for q in explode_lines(p)]
    for p in paras:
        if not p["text"].strip():
            continue
        if title_para is not None and p["index"] == title_para:
            continue
        lvl = _heading_level(spec, p)
        if lvl:
            if lvl == 1 or heads[0] == 0:
                heads = [heads[0] + 1, 0]
                path = str(heads[0])
            else:
                heads[1] += 1
                path = f"{heads[0]}.{heads[1]}"
            items.append({"kind": "heading", "path": path, "title": p["text"],
                          "source": {"doc": spec["text"], "paragraph": p["index"], "line": p.get("line"),
                                     "annotations": formatted_runs(p, legend)}})
            continue
        colour, _ = para_colour(p)
        role = "lemma" if colour in lemma else "body"
        runs = formatted_runs(p, legend)
        # split into segments at internal lines that begin with a reference
        lines = p["text"].split("\n")
        segs, cur, off = [], None, 0
        for li, line in enumerate(lines):
            refs, prefix, rest = parse_ref_prefix(line) if refs_mode != "none" else (None, "", line)
            if cur is None or refs:
                cur = {"lines": [], "refs": refs, "prefix": prefix, "start": off, "line": li}
                segs.append(cur)
                cur["lines"].append(rest if refs else line)
                cur["prefix_len"] = len(prefix) if refs else 0
            else:
                cur["lines"].append(line)
            off += len(line) + 1
        auto = (p["numbering"] or {}).get("value")
        for k, s in enumerate(segs):
            refs = s["refs"]
            if k == 0 and auto and refs_mode != "none":
                refs = [auto] + [r for r in (refs or []) if r != auto]
                n_auto += 1
            text = "\n".join(s["lines"])
            if not letters_only(text):
                continue
            end = s["start"] + len("\n".join(lines[s["line"]:s["line"] + len(s["lines"])]))
            ann = [dict(a, start=a["start"] - s["start"] - s["prefix_len"],
                        end=a["end"] - s["start"] - s["prefix_len"])
                   for a in runs if a["start"] >= s["start"] and a["end"] <= end]
            item = {"kind": "block", "text": text, "role": role,
                    "source": {"doc": spec["text"], "paragraph": p["index"], "line": p.get("line", s["line"]),
                               **({"typed_prefix": s["prefix"]} if s["prefix"] else {}),
                               **({"auto_number": auto} if k == 0 and auto else {})},
                    "annotations": ann}
            if refs:
                if refs_mode == "align":
                    item["targets"] = [str(r) for r in refs]
                    n_refs += 1
                else:
                    item["source"]["candidate_refs"] = refs
                    candidates.append(refs)
                    if s["prefix"]:      # keep the number in the text: it is not confirmed markup
                        item["text"] = s["prefix"] + text
                        item["source"].pop("typed_prefix")
            items.append(item)
    known = {bid for bid, _ in ctx.works[spec["target"]]["blocks"]} if spec.get("target") else set()
    bad = sorted({t for it in items for t in it.get("targets", []) if t not in known})
    if bad:
        rep["warnings"] = rep.get("warnings", []) + [f"references to unknown target ids: {bad}"]
        for it in items:
            if "targets" in it:
                it["targets"] = [t for t in it["targets"] if t in known]
    rep.update({"blocks": sum(1 for i in items if i["kind"] == "block"),
                "headings": sum(1 for i in items if i["kind"] == "heading"),
                "blocks_with_refs": n_refs, "auto_numbered_refs": n_auto,
                "candidate_refs": len(candidates),
                "lemma_blocks": sum(1 for i in items if i.get("role") == "lemma")})
    extra = {}
    if spec.get("tsadrel"):
        extra["tsadrel"] = tsadrel_crosscheck(ctx, spec, items, rep)
    return items, extra


def tsadrel_crosscheck(ctx, spec, items, rep):
    """Read a commentary's line-parallel Tsadrel pair (its own root split
    against its own commentary rows), locate every root row in the target
    and every commentary row in the built blocks, and record the row-level
    alignment. Agreement with the typed references is reported."""
    tgt_idx = ctx.index(spec["target"])
    blk = [(str(i), it["text"]) for i, it in enumerate(items) if it["kind"] == "block"]
    blk_idx = LetterIndex(blk)
    rows_r = _row_lines(ctx, spec["tsadrel"]["root_rows"])
    rows_c = _row_lines(ctx, spec["tsadrel"]["other"])
    out, hint_r, hint_c, agree, total = [], 0, 0, 0, 0
    for i in range(max(len(rows_r), len(rows_c))):
        rt = rows_r[i]["text"] if i < len(rows_r) else ""
        ct = rows_c[i]["text"] if i < len(rows_c) else ""
        if not rt.strip():
            continue
        tids, hint_r = tgt_idx.find(re.sub(r"_+", "", rt), hint_r)
        ct_clean = re.sub(r"_+|(?<=\S)-(?=\S)", "", ct)
        bids, hint_c = blk_idx.find(ct_clean, hint_c) if ct.strip() else (None, hint_c)
        row = {"row": i + 1, "root_text": rt, "target_ids": tids or [],
               "commentary_text": ct, "commentary_blocks": bids or []}
        out.append(row)
        if tids and bids:
            total += 1
            typed = {t for b in bids for t in (items_by_pos(items, int(b)).get("targets") or [])}
            if typed & set(tids):
                agree += 1
    rep["tsadrel_rows_with_root"] = len(out)
    rep["tsadrel_agreement_with_typed_refs"] = f"{agree}/{total}"
    return out


def items_by_pos(items, k):
    return items[k]


def adapt_op_translation(ctx, spec, rep):
    """A translation whose text, segmentation and alignment come from the
    OpenPecha API, aligned to an OpenPecha parent that is the same text as an
    already-built target work. Parent spans are located in the target by
    letter projection."""
    m = ctx.op(spec["openpecha_text"])
    parent = ctx.op(m["alignment"]["parent_text"])
    tgt = ctx.works[spec["target"]]
    tgt_text = "\n".join(t for _, t in tgt["blocks"])
    proj = Projector(parent["content"], tgt_text)
    # target block offsets in tgt_text
    offs, pos = [], 0
    for bid, t in tgt["blocks"]:
        offs.append((bid, pos, pos + len(t)))
        pos += len(t) + 1
    by_seg = {}
    for pr in m["alignment"]["pairs"]:
        sp = proj.span(pr["target_start"], pr["target_end"])
        ids = [b for b, s, e in offs if sp and s < sp[1] and e > sp[0]]
        by_seg.setdefault((pr["start"], pr["end"]), []).extend(x for x in ids if x not in by_seg.get((pr["start"], pr["end"]), []))
    blocks, order, unmapped = {}, [], []
    for sgm in m["segments"]:
        text = m["content"][sgm["start"]:sgm["end"]]
        if not text.strip():
            continue
        ids = by_seg.get((sgm["start"], sgm["end"]), [])
        if not ids:
            unmapped.append({"segment": sgm["id"], "text": text})
            continue
        key = ids[0]
        if key not in blocks:
            blocks[key] = {"kind": "block", "id": key, "lines": [], "targets": [],
                           "source": {"openpecha_segments": []}}
            order.append(key)
        b = blocks[key]
        b["lines"].append(text.strip())
        b["source"]["openpecha_segments"].append({"id": sgm["id"], "start": sgm["start"], "end": sgm["end"]})
        b["targets"] += [i for i in ids if i not in b["targets"]]
    items = []
    for key in sorted(order, key=lambda k: int(k) if k.isdigit() else k):
        b = blocks[key]
        b["text"] = "\n".join(b.pop("lines"))
        items.append(b)
    rep.update({"blocks": len(items), "openpecha_segments": len(m["segments"]),
                "unmapped_segments": unmapped, "projection": proj.stats})
    return items, {"openpecha": {"text_id": m["text_id"], "instance_id": m["instance_id"],
                                 "alignment_annotation": m["alignment"]["annotation_id"]}}


ADAPTERS = {
    "rows": adapt_rows,
    "numbered": adapt_numbered,
    "parallel": adapt_parallel,
    "ref_commentary": adapt_ref_commentary,
    "op_translation": adapt_op_translation,
}


def register_adapter(name, fn):
    ADAPTERS[name] = fn


# --------------------------------------------------------------------------
# driver
# --------------------------------------------------------------------------

def raw_files(spec):
    out = []
    for k in ("text", "toc", "segmentation", "citations"):
        if isinstance(spec.get(k), str):
            out.append(spec[k])
    for k in ("pair", "tsadrel"):
        if spec.get(k):
            out += [v for v in spec[k].values() if isinstance(v, str)]
    out += spec.get("extra_raw") or []
    return out


def build(manifest_path, vault, only=None, dry=False, out=None):
    manifest = yaml.safe_load(pathlib.Path(manifest_path).read_text(encoding="utf-8"))
    ctx = Ctx(manifest, vault)
    sidecar_dir = manifest.get("sidecar_dir", "1-SOURCES/Annotations")
    for spec in manifest["works"]:
        key = spec["key"]
        rep = {"key": key, "path": spec["path"], "adapter": spec["adapter"]}
        items, extra = ADAPTERS[spec["adapter"]](ctx, spec, rep)
        fm = dict(spec.get("frontmatter") or {})
        fm["raw_sources"] = provenance(ctx, raw_files(spec))
        if spec.get("openpecha_text"):
            fm.setdefault("openpecha_text_id", spec["openpecha_text"])
        fm["intake"] = {"skill": "aligned-corpus-intake", "adapter": spec["adapter"],
                        "date": datetime.date.today().isoformat(),
                        "annotations": f"{sidecar_dir}/{pathlib.Path(spec['path']).stem}.annotations.json"}
        target_path = ctx.works[spec["target"]]["path"] if spec.get("target") else None
        work = {"path": spec["path"], "frontmatter": fm, "title": spec["title"],
                "id_scheme": spec.get("id_scheme", "flat"), "target_file": target_path,
                "sidecar": f"{sidecar_dir}/{pathlib.Path(spec['path']).stem}.annotations.json",
                "items": items,
                "extra": {"legend": spec.get("legend"), "notes": spec.get("notes"), **extra}}
        ids = []
        if not dry:
            vault_writer.render(work, out or vault)
        # remember the rendered block ids for later works
        blocks = _rendered_blocks(work)
        ctx.works[key] = {"path": spec["path"], "blocks": blocks}
        rep["ids"] = f"{blocks[0][0]}..{blocks[-1][0]}" if blocks else "-"
        rep["transclusions"] = sum(len(i.get("targets") or []) for i in items if i["kind"] == "block")
        ctx.report.append(rep)
        print(f"{key:28s} {spec['adapter']:15s} blocks={rep.get('blocks')} "
              f"transclusions={rep['transclusions']} -> {spec['path']}", file=sys.stderr)
    return ctx


def _rendered_blocks(work):
    """Recompute the ids the writer assigns, in document order."""
    out, h2, counters, nxt = [], "0", {}, 1
    for it in work["items"]:
        if it["kind"] == "heading":
            if len(str(it["path"]).split(".")) == 1:
                h2 = str(it["path"])
            continue
        if not vault_writer.clean_lines(it["text"]):
            continue
        if work["id_scheme"] == "flat":
            bid = str(it.get("id") or nxt)
            if bid.isdigit():
                nxt = int(bid) + 1
        else:
            counters[h2] = counters.get(h2, 0) + 1
            bid = f"{h2}-{counters[h2]}"
        out.append((bid, "\n".join(vault_writer.clean_lines(it["text"]))))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest")
    ap.add_argument("--vault", default=".")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--out", help="write outputs under this root instead of the vault (for a test build)")
    ap.add_argument("--report", help="write the JSON intake report here")
    a = ap.parse_args()
    import adapters_tibetan                      # noqa: F401  (registers Tibetan adapters)
    ctx = build(a.manifest, a.vault, dry=a.dry_run, out=a.out)
    if a.report:
        pathlib.Path(a.report).write_text(json.dumps(ctx.report, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
