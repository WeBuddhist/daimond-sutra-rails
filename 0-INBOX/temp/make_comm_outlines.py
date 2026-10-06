#!/usr/bin/env python3
"""Commentary outlines (Wikisource Index inline headings) -> 2-RAILS/Sections/Raw/toc-wikisource/<id>.md."""
import re, json, pathlib, yaml
WORK = {"vasubandhu-saptartha": "bo-vasubandhu-saptartha-tika", "chone-drakpa-shedrub": "bo-chone-drakpa-shedrub",
        "kamalasila-tika": "bo-kamalasila-tika"}
for oid, key in WORK.items():
    src = pathlib.Path(f"0-INBOX/temp/wiki-toc-{oid}/outline.placed.md").read_text(encoding="utf-8")
    fm = yaml.safe_load(re.match(r"\A---\n(.*?)\n---\n", src, re.S).group(1))
    nodes = yaml.safe_load(re.search(r"```yaml\n(.*?)```", src, re.S).group(1))["nodes"]
    d = json.loads(pathlib.Path(f"0-INBOX/raw-data/wikisource-{oid}/pages.json").read_text(encoding="utf-8"))
    f = {}
    for part in d["index_content"].split("\n|"):
        if "=" in part:
            k, v = part.split("=", 1); f[k.strip()] = v.strip()
    pins = {}
    for n in nodes:
        pins.setdefault(n["page"], {"page": f"Page:{d['index_page'].split(':', 1)[1]}/{n['page']}", "revid": n["page_revid"], "headings": []})["headings"].append(n["path"])
    meta = {"outline_id": oid, "registered_id": oid, "source": "wikisource.org", "index_page": fm["index_page"],
            "index_url": fm["index_url"], "index_revid": fm["index_revid"],
            "edition": ", ".join(x for x in (f.get("Publisher"), f.get("Year"), f.get("Volumes")) if x) or None,
            "heading_pages": list(pins.values()), "retrieved": fm["retrieved"],
            "placed_on": key, "placed_on_text": fm["placed_on_text"], "placed_on_sha1": fm["placed_on_sha1"],
            "applied_to": [key],
            "labels": {"bo": "verbatim from the Index's inline headings (decimal numbers, which give the path, and markup dropped)"},
            "placement": ("the commentary's rows were cut at every heading of the proofread pages (ws_comm_align.py), so each "
                          "heading stands exactly at the start of the row it opens; no row split needed"),
            "status": "complete"}
    table = "\n".join(f"| {n['path']} | {n['labels']['bo']} | {n['start_row']} | {n['clause'][:40]} |" for n in nodes)
    body = (f"# {d['index_page'].split(':',1)[1].removesuffix('.pdf')} — outline from the Wikisource Index\n\n"
            f"The {len(nodes)} numbered inline headings of the commentary's proofread pages (Index revision {fm['index_revid']}). "
            "The heading numbers are decimal paths; nesting follows them. The page's title heading is the text's own title "
            "line and stays in the text (row 1), not a node.\n\n| node | bo | row | text after the heading |\n|---|---|---|---|\n"
            + table + "\n\n```yaml\n" + yaml.safe_dump({"nodes": [{k: n[k] for k in ("path", "start_row", "labels", "page", "page_revid", "clause")} for n in nodes]},
                                                     allow_unicode=True, sort_keys=False) + "```\n")
    out = pathlib.Path(f"2-RAILS/Sections/Raw/toc-wikisource/{oid}.md")
    out.write_text("---\n" + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False, width=200) + "---\n\n" + body, encoding="utf-8")
    print(out, len(nodes))
