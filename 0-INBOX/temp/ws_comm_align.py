#!/usr/bin/env python3
"""A Tibetan commentary that exists only on Wikisource -> a row pair aligned to the display root.

    python3 0-INBOX/temp/ws_comm_align.py <id> [--overrides 0-INBOX/temp/align-<id>/overrides.yaml]

Reads   0-INBOX/raw-data/wikisource-<id>/pages.json            (fetch_wikisource_text.py)
        0-INBOX/raw-data/dorjeechoepa-root-bo(display).md      (the stored Tibetan root)
Writes  0-INBOX/raw-data/wikisource-<id>/<id>(root-comm).md     commentary rows (numbered list): the text
                                                                of every proofread page, page markup and
                                                                pecha line breaks removed, letters verbatim
        0-INBOX/raw-data/wikisource-<id>/<id>-root(root-comm).md row N = the display segments row N comments
                                                                on, verbatim (empty = none)
        0-INBOX/temp/wiki-toc-<id>/outline.placed.md            the Index's inline headings at the rows they open
        0-INBOX/temp/align-<id>/alignment.tsv, summary.json     evidence: per row, its segments and the quoted
                                                                words that place them

How the alignment is made (Claude, on the vault owner's instruction of 2026-10-04):
1. Both texts are cut into syllables (letters only). Every 4-syllable sequence of the commentary that also
   occurs in the root (at most 12 times there) is a candidate match; the longest chain of matches that runs
   forward in both texts (LIS) keeps the commentary's quotations of the sūtra in their order and drops
   coincidences and look-ahead quotations.
2. A root segment is taken up where its first quotation of at least 5 consecutive syllables stands (a
   "lemma"); the commentary is cut at the sentence boundary (། ། or a final particle + །) before that lemma,
   if there is one after the previous cut. Rows are also cut at every Wikisource heading.
3. Each root segment with chain matches covering at least 3 of its syllables is assigned to the row holding
   its first match, so the assignment runs forward; segments the commentary does not quote get no row.
   overrides.yaml can add or move segments ({segment: row}) or drop them ({segment: null}), each with a
   reason — that is where a reviewer's judgement goes.
"""
import argparse, bisect, collections, hashlib, json, pathlib, re, sys, urllib.parse
import yaml

ap = argparse.ArgumentParser()
ap.add_argument("id")
ap.add_argument("--overrides")
ap.add_argument("--n", type=int, default=4)
a = ap.parse_args()
RAW = pathlib.Path("0-INBOX/raw-data")
src = RAW / f"wikisource-{a.id}"
d = json.loads((src / "pages.json").read_text(encoding="utf-8"))

# ── 1. the page stream, headings marked ─────────────────────────────────────
TOK = re.compile(r"<noinclude>.*?</noinclude>"
                 r"|(?P<eq>={2,})[ \t]*(?P<head>[^=\n]+?)[ \t]*(?P=eq)"
                 r"|\{\{[Hh]w[-/]bo\|(?P<hwa>[^|}]*)\|\|(?P<hwb>[^}]*)\}\}"
                 r"|\{\{[^{}]*\}\}|<[^>]+>", re.S)
stream, heads, title_cut = [], [], []
for p in d["pages"]:
    c, last = p["content"], 0
    for m in TOK.finditer(c):
        stream.append(c[last:m.start()])
        last = m.end()
        if m.group("head") is not None:
            lab = re.sub(r"<[^>]+>|\{\{[^{}]*\}\}|'''?", "", m.group("head")).strip().strip("﻿​ ")
            if not re.match(r"^\d", lab) and not heads:
                # the work's title, set as a heading on the page: the text's own title line -> a row of its own
                stream.append(lab)
                title_cut.append(sum(map(len, stream)))
                continue
            heads.append({"at": sum(map(len, stream)), "label": lab,
                          "page": p["title"].rsplit("/", 1)[1], "revid": p["revid"]})
        elif m.group("hwa") is not None:
            stream.append(m.group("hwa") + m.group("hwb"))
    stream.append(c[last:])
S = "".join(stream)
# pecha line breaks are not text breaks: drop them, keeping heading offsets
keep = [i for i, ch in enumerate(S) if ch != "\n"]
newpos = {old: new for new, old in enumerate(keep)}
def remap(i):
    j = bisect.bisect_left(keep, i)
    return j
S = "".join(S[i] for i in keep)
for h in heads:
    h["at"] = remap(h["at"])
title_cut = [remap(x) for x in title_cut]

# the first heading is the work's title (not a numbered node): its text is the text's own title line
nodes_raw = []
for h in heads:
    m = re.match(r"^(\d+(?:\.\d+)*)\.?\s+(.+)$", h["label"])
    if m:
        nodes_raw.append(dict(h, path=m.group(1), label=m.group(2).strip()))
    else:
        sys.exit(f"unnumbered heading after the title: {h['label']!r}")

# ── 2. syllables ────────────────────────────────────────────────────────────
sys.path.insert(0, "4-SYSTEM/Skills/aligned-corpus-intake/scripts")
from project import is_letter
from md_export import read_rows
SYL = re.compile(r"[^\s་།༎༏༐༑༔་༌༈།-༒༔༴༺-༽\d\[\]()]+")
def syllables(text, base=0):
    out = []
    for m in SYL.finditer(text):
        w = "".join(ch for ch in m.group(0) if is_letter(ch))
        if w:
            out.append((w, base + m.start(), base + m.end()))
    return out

root_rows = [(r["row"], r["text"]) for r in read_rows(RAW / "dorjeechoepa-root-bo(display).md") if any(is_letter(c) for c in r["text"])]
R, Rseg = [], []                                   # root syllables, their segment
for row, t in root_rows:
    for w, _, _ in syllables(t):
        R.append(w); Rseg.append(row)
seg_len = collections.Counter(Rseg)
C = syllables(S)                                   # commentary syllables with offsets in S
Cw = [w for w, _, _ in C]
N = a.n


def lis(pairs):
    """Longest chain of (i, j) strictly increasing in both."""
    pairs = sorted(pairs, key=lambda x: (x[0], -x[1]))
    tails, tidx, back = [], [], [-1] * len(pairs)
    for n, (i, j) in enumerate(pairs):
        p = bisect.bisect_left(tails, j)
        if p == len(tails):
            tails.append(j); tidx.append(n)
        else:
            tails[p], tidx[p] = j, n
        back[n] = tidx[p - 1] if p else -1
    out, n = [], tidx[-1] if tidx else -1
    while n != -1:
        out.append(pairs[n]); n = back[n]
    return out[::-1]


def gram_pairs(i0, i1, j0, j1, n, max_occ):
    """(i, j): n-syllable sequences shared by commentary [i0, i1) and root [j0, j1)."""
    g = collections.defaultdict(list)
    for j in range(j0, j1 - n + 1):
        g[tuple(R[j:j + n])].append(j)
    out = []
    for i in range(i0, i1 - n + 1):
        occ = g.get(tuple(Cw[i:i + n]))
        if occ and len(occ) <= max_occ:
            out += [(i, j) for j in occ]
    return out


def to_map(chain, n, cmap, used):
    for i, j in chain:
        for k in range(n):
            if i + k not in cmap and j + k not in used:
                cmap[i + k] = j + k
                used.add(j + k)


# pass 1: global, 4-syllable sequences that are not too common in the root
cmap, used = {}, set()
to_map(lis(gram_pairs(0, len(Cw), 0, len(R), N, 12)), N, cmap, used)
# pass 2: inside each gap between two anchored syllables, 3-syllable sequences of any frequency
anch = sorted(cmap.items())
bounds2 = [(-1, -1)] + anch + [(len(Cw), len(R))]
extra = {}
for (ia, ja), (ib, jb) in zip(bounds2, bounds2[1:]):
    if ib - ia > 3 and jb - ja > 3:
        to_map(lis(gram_pairs(ia + 1, ib, ja + 1, jb, 3, 10 ** 6)), 3, extra, used)
cmap.update(extra)
chain = sorted(cmap.items())
# runs of consecutive matches (lemmas)
runs, cur = [], None
for i in sorted(cmap):
    j = cmap[i]
    if cur and i == cur["i1"] + 1 and j == cur["j1"] + 1:
        cur["i1"], cur["j1"] = i, j
    else:
        cur = {"i0": i, "i1": i, "j0": j, "j1": j}
        runs.append(cur)

# ── 3. segments -> quotations ───────────────────────────────────────────────
# a run of consecutive matches is cut where it crosses from one root segment into the next
pieces = collections.defaultdict(list)             # segment -> [(i0, length)] in commentary order
for r in runs:
    i, j = r["i0"], r["j0"]
    while i <= r["i1"]:
        sg, i0 = Rseg[j], i
        while i <= r["i1"] and Rseg[j] == sg:
            i += 1; j += 1
        pieces[sg].append((i0, i - i0))
def quoted(s):
    """A segment counts as quoted when the commentary has ≥ 5 consecutive syllables of it (all but one
    syllable of a segment shorter than 6), or, for a segment of ≥ 7 syllables, pieces of ≥ 3 within 80
    commentary syllables that together cover ≥ 40 % of it (≥ 5 syllables). Returns the commentary syllable where it is first taken up
    (its first piece of ≥ 3 syllables) or None."""
    need = min(5, max(3, seg_len[s] - 1))
    ps = [(i0, n) for i0, n in pieces[s] if n >= 3]
    if any(n >= need for _, n in ps):
        return ps[0][0]
    if seg_len[s] >= 7:
        # woven quotation: pieces of ≥ 3 syllables within 80 syllables of each other covering ≥ 40 % of it
        want = max(5, round(0.4 * seg_len[s]))
        for k, (i0, _) in enumerate(ps):
            if sum(n for i, n in ps[k:] if i - i0 <= 80) >= want:
                return i0
    return None
first = {s: quoted(s) for s in pieces}
first = {s: i for s, i in first.items() if i is not None}
lemma = {}                                         # segment -> where its first ≥ 5-syllable quotation starts
for sg, ps in pieces.items():
    for i0, n in ps:
        if n >= 5:
            lemma.setdefault(sg, i0)
overrides = {}
if a.overrides and pathlib.Path(a.overrides).exists():
    overrides = yaml.safe_load(pathlib.Path(a.overrides).read_text(encoding="utf-8")) or {}

BOUND = re.compile(r"(?:ོ།(?:[ \t]*།)?|།[ \t]*།|༎)[ \t]*")
def sentence_start(pos, floor):
    """Start of the sentence holding character `pos`: just after the last boundary in (floor, pos]."""
    best = None
    for m in BOUND.finditer(S, floor, pos):
        best = m.end()
    return best

head_at = sorted({h["at"] for h in nodes_raw})
cuts = set(head_at) | set(title_cut)
aligned_segs = [s for s, _ in root_rows if s in first]
for s in sorted(lemma, key=lambda s: lemma[s]):
    if s not in aligned_segs:
        continue
    pos = C[lemma[s]][1]
    floor = max([c for c in cuts if c <= pos] + [0])
    st = sentence_start(pos, floor)
    if st is not None and st > floor:
        cuts.add(st)
cuts = sorted(c for c in cuts if 0 < c < len(S))
# a long stretch between two cuts is cut further at sentence boundaries, into pieces of about 1000-1500
# characters (the Dzongsar commentary docs are segmented by sentence), so no row is unwieldy
size_cuts = []
for x, y in zip([0] + cuts, cuts + [len(S)]):
    if y - x <= 2000:
        continue
    ends = [m.end() for m in BOUND.finditer(S, x, y) if x + 600 < m.end() < y - 600]
    last = x
    for e in ends:
        if e - last >= 1000:
            size_cuts.append(e)
            last = e
cuts = sorted(set(cuts) | set(size_cuts))
bounds = [0] + cuts + [len(S)]
rows = []                                          # (start, end) in S, lettered only
for x, y in zip(bounds, bounds[1:]):
    if any(is_letter(ch) for ch in S[x:y]):
        rows.append((x, y))
starts = [x for x, _ in rows]
def row_of_char(pos):
    return bisect.bisect_right(starts, pos)        # 1-based row number

assign = {}
for s in aligned_segs:
    assign[s] = row_of_char(C[first[s]][1])
# a row comments on the root from its lemma up to the next lemma: a segment the commentary does not quote,
# lying between two quoted ones, goes with the row of the quoted segment before it (inferred, listed in the
# evidence) — unless the gap is longer than 30 segments, where the commentary is taken to skip the passage
order = [s for s, _ in root_rows]
inferred, long_gaps = [], []
quoted_order = [s for s in order if s in assign]
for x, y in zip(quoted_order, quoted_order[1:]):
    gap = order[order.index(x) + 1:order.index(y)]
    if len(gap) > 30:
        long_gaps.append([gap[0], gap[-1]])
        continue
    for s in gap:
        assign[s] = assign[x]
        inferred.append(s)
for s, r in (overrides.get("segments") or {}).items():
    s = int(s)
    if r is None:
        assign.pop(s, None)
    else:
        assign[s] = int(r)
# the generated root copy must run forward: a segment never goes to an earlier row than the one before it
order = [s for s, _ in root_rows]
last, back_moves = 0, []
for s in order:
    if s in assign:
        if assign[s] < last:
            back_moves.append((s, assign[s], last))
            assign[s] = last
        last = assign[s]
if back_moves:
    print("segments moved forward to keep order:", back_moves[:20], file=sys.stderr)

# ── 4. outputs ──────────────────────────────────────────────────────────────
def clean(t):
    return re.sub(r"[ \t]+", " ", t).strip()
row_texts = [clean(S[x:y]) for x, y in rows]
for t in row_texts:
    if re.match(r"^\d+\.", t) or "[" in t or "]" in t:
        print("WARNING row needs a look:", t[:60], file=sys.stderr)
root_text = {r: t for r, t in root_rows}
per_row = collections.defaultdict(list)
for s in order:
    if s in assign:
        per_row[assign[s]].append(s)
comm_md = src / f"{a.id}(root-comm).md"
root_md = src / f"{a.id}-root(root-comm).md"
comm_md.write_text("".join(f"{i}. {t}\n" for i, t in enumerate(row_texts, 1)), encoding="utf-8")
root_md.write_text("".join(f"{i}. {' '.join(root_text[s] for s in per_row.get(i, []))}\n"
                           for i in range(1, len(row_texts) + 1)), encoding="utf-8")

# outline: each numbered heading at the row it opens
nodes = []
for h in nodes_raw:
    r = row_of_char(h["at"])
    if rows[r - 1][0] != h["at"]:
        r += 0
    nodes.append({"path": h["path"], "start_row": str(r), "labels": {"bo": h["label"]},
                  "page": h["page"], "page_revid": h["revid"], "clause": row_texts[r - 1][:60]})
out = pathlib.Path(f"0-INBOX/temp/wiki-toc-{a.id}")
out.mkdir(parents=True, exist_ok=True)
index_page = d["index_page"]
fm = {"outline_id": a.id, "source": "wikisource.org", "index_page": index_page,
      "index_url": "https://wikisource.org/wiki/" + urllib.parse.quote(index_page.replace(" ", "_")),
      "index_revid": d["index_revid"], "retrieved": d["retrieved"], "placed_on": None,
      "placed_on_text": f"0-INBOX/raw-data/wikisource-{a.id}/{comm_md.name}",
      "placed_on_sha1": hashlib.sha1(comm_md.read_bytes()).hexdigest(),
      "placement": "every row boundary of the text file falls at each of the Index's headings, so each heading stands at the start of the row it opens (ws_comm_align.py)"}
(out / "outline.placed.md").write_text(
    "---\n" + yaml.safe_dump(fm, allow_unicode=True, sort_keys=False) + "---\n\n```yaml\n"
    + yaml.safe_dump({"nodes": nodes}, allow_unicode=True, sort_keys=False) + "```\n", encoding="utf-8")

ev = pathlib.Path(f"0-INBOX/temp/align-{a.id}")
ev.mkdir(parents=True, exist_ok=True)
lines = ["row\tsegments\tquoted (first 5 syllables of each segment's first match)\trow start"]
for i, t in enumerate(row_texts, 1):
    segs = per_row.get(i, [])
    q = " | ".join((f"{s}:" + "་".join(Cw[first[s]:first[s] + 6])) if s in first else f"{s}:(inferred)" for s in segs)
    lines.append(f"{i}\t{','.join(map(str, segs))}\t{q}\t{t[:50]}")
(ev / "alignment.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")
unq = [s for s in order if s not in assign]
title_text = S[:title_cut[0]].strip() if title_cut else None
summary = {"rows": len(row_texts), "aligned_rows": sum(1 for i in range(1, len(row_texts) + 1) if per_row.get(i)),
           "segments_aligned": len(assign), "segments_not_aligned": unq,
           "chain_matches": len(chain), "matched_syllables": len(cmap), "commentary_syllables": len(Cw),
           "lemma_cuts": len(cuts) - len(head_at) - len(title_cut) - len(size_cuts), "length_cuts": len(size_cuts), "headings": len(nodes), "title_line": title_text,
           "moved_forward": back_moves, "inferred_between_quoted_neighbours": inferred, "gaps_left_unaligned": long_gaps,
           "method": ("Claude, ws_comm_align.py: the commentary's quotations of the sūtra found as 4-syllable sequences shared "
                      "with the display root, kept in order by a longest monotonic chain; a row starts at the sentence "
                      "boundary before each segment's first quotation of ≥ 5 syllables and at every Wikisource heading; "
                      "rows over 2000 characters are further cut at sentence boundaries into ~1000-1500-character pieces; "
                      "each segment quoted (≥ 5 consecutive syllables, or all but one of a shorter segment) is transcluded once, "
                      "from the row holding its first quotation; an unquoted segment between two quoted ones goes with "
                      "the row of the quoted segment before it (a row comments from its lemma to the next lemma; gaps "
                      "over 30 segments are left unaligned)" + ("; reviewed overrides in overrides.yaml" if overrides else "") + ".")}
(ev / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{a.id}: {summary['rows']} rows ({summary['aligned_rows']} aligned), {len(nodes)} headings, "
      f"{summary['segments_aligned']}/{len(order)} segments, {summary['matched_syllables']}/{len(Cw)} syllables matched")
