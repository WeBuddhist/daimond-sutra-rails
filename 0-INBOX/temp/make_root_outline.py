#!/usr/bin/env python3
"""Root outline (Wikisource Index inline headings) -> 2-RAILS/Sections/Raw/toc-wikisource/vajracchedika.md.
Reads the `place` output and applies the placement corrections read off the proofread pages (see CORR)."""
import json, re, pathlib, yaml
src = pathlib.Path("0-INBOX/temp/wiki-toc-vajracchedika/outline.placed.md").read_text(encoding="utf-8")
fm = yaml.safe_load(re.match(r"\A---\n(.*?)\n---\n", src, re.S).group(1))
nodes = yaml.safe_load(re.search(r"```yaml\n(.*?)```", src, re.S).group(1))["nodes"]
rows = {}
for l in pathlib.Path(fm["placed_on_text"]).read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(\d+)\. ?(.*)$", l)
    if m: rows[m.group(1)] = m.group(2).strip()
# The monotonic letter chain slipped on repeated formulas for five headings; on the proofread
# page each of them stands between two sentences that are also a row boundary of the display.
CORR = {"3": "20", "4": "29", "6": "44", "9": "293", "12": "398"}
SA = {"1": "निदानम्", "2": "आयुष्मतः सुभूतेः प्रश्नः", "3": "भगवतः प्रतिवचनम्", "4": "बोधिचित्तोत्पादः",
      "5": "षट्पारमिताचर्यायां शिक्षा", "6": "दानादिभ्यो रूपकायनिष्पत्तिनिर्देशः", "7": "अष्टौ प्रतिपन्नकफलस्थाः",
      "8": "लक्षणानुव्यञ्जनानि", "9": "तथागतस्य पञ्च विशिष्टानि चक्षूंषि", "10": "चित्तचैतसिकाः",
      "11": "फलं धर्मकायः", "12": "परमाणवः", "13": "उपसंहारः"}
out = []
for n in nodes:
    p = n["path"]
    sr = CORR.get(p, n["start_row"])
    clause = n["clause"] if "." in sr else rows[sr][:60]
    out.append({"path": p, "start_row": sr, "labels": {"bo": n["labels"]["bo"], "sa": SA[p]},
                "page": n["page"], "page_revid": n["page_revid"], "clause": clause})
pins = {}
for n in out:
    pins.setdefault(n["page"], {"page": f"Page:{fm['index_page'].split(':',1)[1]}/{n['page']}", "revid": n["page_revid"], "headings": []})["headings"].append(n["path"])
meta = {k: fm[k] for k in ("outline_id", "source", "index_page", "index_url", "index_revid")}
meta.update({
    "edition": "Derge Kangyur (སྡེ་དགེ་དཔར་ཁང་།, 1727; Index: པོད་34-ཤེས་རབ་སྣ་ཚོགས། ཀ ༡༢༡ན༡-༡༣༢བ༧; editor སི་ཏུ་ཆོས་ཀྱི་འབྱུང་གནས་)",
    "heading_pages": list(pins.values()),
    "retrieved": fm["retrieved"], "placed_on": fm["placed_on"], "placed_on_text": fm["placed_on_text"],
    "placed_on_sha1": fm["placed_on_sha1"], "applied_to": ["sa-root", "bo-display"],
    "labels": {"bo": "verbatim from the Index's inline headings (numbers and markup dropped)",
               "sa": "editorial Sanskrit renderings by Claude (2026-10-04), using the Sanskrit text's own vocabulary where it has it (सुभूति, बोधिसत्त्वयान… चित्तमुत्पादयितव्यम्, लक्षणसंपद्, मांसचक्षुः…, चित्तधारा, धर्मकाय, परमाणुसंचय) — for the text expert to check"},
    "placement": ("each heading found in the display rows by a monotonic chain of unique 12-letter anchors over the whole "
                  "proofread-page stream (fetch_wiki_outline.py place); five headings the chain placed a few letters "
                  "inside a row (3, 4, 6, 9, 12 — repeated formulas) were checked against the proofread pages by Claude "
                  "and set to the row they open (on the page each stands exactly at that row boundary). Headings 5 and 10 "
                  "stand inside rows 38 and 317, after དེ་ཅིའི་ཕྱིར་ཞེ་ན།, as on the page: those rows are split there (D7)."),
    "status": "complete"})
table = "\n".join(f"| {n['path']} | {n['labels']['bo']} | {n['labels']['sa']} | {n['start_row']} | {n['clause'][:40]} |" for n in out)
body = f"""# འཕགས་པ་ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པ་རྡོ་རྗེ་གཅོད་པ། — outline from the Wikisource Index

The thirteen inline headings of the Derge Kangyur text on its Wikisource Index page (revision {fm['index_revid']}). The Index's title heading is the work's title, not a node. Rows 1–4 of the display (title, Sanskrit and Tibetan titles, homage) precede node 1 and take ids `^0-n`.

The headings are numbered 1–13 on the page with no nesting by number (their `===`/`====` levels alternate without a pattern), so they are kept flat.

Rows 38 and 317 are split (D7): on the proofread page the heading stands after the question དེ་ཅིའི་ཕྱིར་ཞེ་ན། and before the answer. The row's Sanskrit segment is shown with part 2 (it renders the sentence the heading opens), so the Sanskrit heading stands before that segment.

| node | bo | sa (editorial) | row | text after the heading |
|---|---|---|---|---|
{table}

```yaml
{yaml.safe_dump({"nodes": out}, allow_unicode=True, sort_keys=False)}```
"""
pathlib.Path("2-RAILS/Sections/Raw/toc-wikisource/vajracchedika.md").write_text(
    "---\n" + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False, width=200) + "---\n\n" + body, encoding="utf-8")
splits = []
for n in out:
    if "." in n["start_row"]:
        r = n["start_row"].split(".")[0]
        splits.append({"row": int(r), "at": [n["clause"].split("།")[0].strip()],
                       "targets": [[], [0]],
                       "targets_note": ("The row's one Sanskrit segment (tat kasya hetoḥ? + the sentence the heading opens) is shown with part 2, "
                                        "which renders all of it but the question, so the Sanskrit section starts at the same passage as the "
                                        "Tibetan (Claude, 2026-10-04 — for the text expert to check; D7's default would show it with part 1)."),
                       "reason": f"Heading {n['path']} ({n['labels']['bo']}) stands inside this row on the Wikisource proofread page (page {n['page']}, revision {n['page_revid']}), after དེ་ཅིའི་ཕྱིར་ཞེ་ན།",
                       "decided_by": "vault owner — standing decision D7 carried over from heart-sutra-rails (2026-10-03)", "date": "2026-10-04"})
pathlib.Path("0-INBOX/temp/root-row-splits.yaml").write_text(yaml.safe_dump(splits, allow_unicode=True, sort_keys=False), encoding="utf-8")
print(table); print(splits)
