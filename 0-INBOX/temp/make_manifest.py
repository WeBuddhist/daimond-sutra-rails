#!/usr/bin/env python3
"""Write 0-INBOX/raw-data/intake-manifest.yaml for the Diamond Sūtra (dorjeechoepa) intake of 2026-10-04.

Re-run this instead of hand-editing the manifest. Decisions live here (and in the
files under 0-INBOX/temp/ it reads), each with reason, who decided and when.
Run from the vault root:  python3 0-INBOX/temp/make_manifest.py
"""
import csv, json, pathlib, urllib.parse
import yaml

V = pathlib.Path(".")
RAW = V / "0-INBOX/raw-data"
TEMP = V / "0-INBOX/temp"
TODAY = "2026-10-04"
STANDING = "vault owner — standing decision carried over from heart-sutra-rails (2026-10-03)"
OWNER_0410 = "vault owner (2026-10-04, this intake)"
CLAUDE = 'Claude (standing instruction "read it and fix if it really makes sense", carried over from heart-sutra-rails 2026-10-03) — for the text expert to check'


def meta(name):
    """A Dzongsar metadata sheet (Entries,BO,EN[,…]) -> {entry: [cells]}."""
    out = {}
    for r in csv.reader(open(RAW / name, encoding="utf-8")):
        if r and r[0] and r[0] not in ("Entries", "Detail"):
            out[r[0].strip()] = [c.strip() for c in r[1:]]
    return out


def sheet_index(n):
    for r in csv.reader(open(RAW / "dorjeechoepa.csv", encoding="utf-8")):
        if r and r[0] == str(n):
            return next(c for c in r if "Index:" in c)


def ws_meta(oid):
    d = json.loads((RAW / f"wikisource-{oid}/pages.json").read_text(encoding="utf-8"))
    f = {}
    for part in d["index_content"].split("\n|"):
        if "=" in part:
            k, v = part.split("=", 1)
            f[k.strip()] = v.strip()
    url = "https://wikisource.org/wiki/" + urllib.parse.quote(d["index_page"].replace(" ", "_"))
    return d, f, url


# ── Upload metadata (2026-10-04, for the WeBuddhist library; mirrors heart-sutra-rails) ──
UPLOAD = "upload preparation of 2026-10-04 (Claude, on the vault owner's instruction; values mirror heart-sutra-rails)"
CATEGORY = "uGpinx0GZlvU1uw44RyYS"          # Prajñāpāramitā — as heart-sutra-rails and summary-of-the-perfection-of-wisdom-rails
ROOT_TAGS = ["FZ5STsdU0eLvo7Nb2CpvH", "ZPcgMZgVJxAMQ7rpfW72a"]   # on the root only, as both sister roots carry; the backend
                                                                # cascades tags, and heart-sutra's Tibetan upload failed on tags
# Dzongsar Google Docs the raw exports came from: links_manifest.csv of the Dzongsar Drive export (raw data of the
# 2026-10-02 intake, removed from 0-INBOX/raw-data since; in git at 866538d:
# 0-INBOX/raw-data/dzongsar-drive/Dzongsar_corpus/Dzongsar/links_manifest.csv). Each export below was checked on
# 2026-10-04 to be letter-identical to the 2026-10-02 .docx download of that doc (project.Projector: 0 skipped letters).
DOC_SA = "https://docs.google.com/document/d/1EqG6xuFzFJasTMMovafuzLMgFpNQV9nAT3zbYDo6rxE/edit"     # row 7, I: 'M42AE7A72 རྡོ་རྗེ་གཅོད་པ་རྩ་བ། Sanskrit- Tibetan' = root-sa(sa-bo).md (26,967 letters)
DOC_TSADEL = "https://docs.google.com/document/d/1uISaW2HYeS3vCPeAhiDTn-RmwDkM1B7kvhMGTEPyfp0/edit" # row 9, G: 'M42AE7A72 རྡོ་རྗེ་གཅོད་པ་རྩ་བ། Tsadel' = root-bo(display).md (29,185 letters)
DOC_ZH = "https://docs.google.com/document/d/12wVNIm5bhbjJIB87uEHXEux9xv0qjXhKfFqyPkZUCQU/edit"     # row 8, I: 'M42AE7A72 金剛般若波羅蜜經 - Chinese-Tibetan Tsawa' = root-zh(bo-zh).md (5,172 letters)
# Author BDRC ids, verified 2026-10-04 in the BDRC work record of each commentary's bdrc_work_id
# (ldspdi.bdrc.io/resource/<work>.ttl: AgentAsCreator, role R0ER0019 "main author").
AUTHOR_BDRC = {"vasubandhu-saptartha": ("WA0RT3161", "P6119"),     # P6119 slob dpon dbyig gnyen
               "chone-drakpa-shedrub": ("WA3CN22739", "P1629"),    # P1629 co ne grags pa bshad sgrub
               "kamalasila-tika": ("WA0RT3162", "P7641")}          # P7641 ka ma la shI la

ROOT_OUTLINE = "2-RAILS/Sections/Raw/toc-wikisource/vajracchedika.md"
ROOT_TOC_NOTE = ("The root's TOC is the thirteen inline headings of the Derge Kangyur text on its Wikisource Index page "
                 "(Index:འཕགས་པ་ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པ་རྡོ་རྗེ་གཅོད་པ་ཞེས་བྱ་བ་ཐེག་པ་ཆེན་པོའི་མདོ།.pdf, revision 1197220), "
                 "each placed where the Index's proofread pages put it, found by letters in the display Tibetan and carried "
                 "onto the Sanskrit through the row pairing, with headings in each file's own language (Tibetan verbatim; "
                 "Sanskrit editorial). D4/D5, " + STANDING + ".")

bo = meta("dorjeechoepa-root-bo.csv")
works = []

# ── Sanskrit root ───────────────────────────────────────────────────────────
sa_pairs = yaml.safe_load((TEMP / "pair-review/sa-bo-corrections.yaml").read_text(encoding="utf-8")) \
    if (TEMP / "pair-review/sa-bo-corrections.yaml").exists() else {}
works.append({
    "key": "sa-root",
    "path": "1-SOURCES/Text/sa-vajracchedika.md",
    "adapter": "md_rows", "id_scheme": "h2",
    "text": "dorjeechoepa-root-sa(sa-bo).md",
    "text_corrections": [{
        "row": 273, "find": "\n000. ", "replace": " ",
        "reason": ("Markdown-export artifact: the row's second sentence was an indented continuation line in the Google Doc, "
                   "exported as a list item numbered 000; the marker and the line break are removed, the words kept."),
        "decided_by": CLAUDE, "date": TODAY}],
    "title": "वज्रच्छेदिका नाम त्रिशतिका प्रज्ञापारमिता",
    "notes": ("The Sanskrit is the root of this vault (D1); the Tibetan is its translation. Rows are the Dzongsar team's "
              "segmentation of the Sanskrit-Tibetan pair (434 rows). The edition's section numbers (॥१॥ … ॥३२॥) are "
              "part of the doc's text and are kept."),
    "meta": "dorjeechoepa-root-bo.csv",
    "frontmatter": {
        "title": "वज्रच्छेदिका नाम त्रिशतिका प्रज्ञापारमिता",
        "alt_titles": ["आर्यवज्रच्छेदिका भगवती प्रज्ञापारमिता"],
        "author": bo["author"][2],
        "language": "Sanskrit", "lang_tag": "sa", "file_type": "root-text",
        "verse_id_format": "section-paragraph",
        "category_id": CATEGORY, "tag_ids": ROOT_TAGS,
        "license": "unknown",            # nothing recorded upstream (also 'unknown' at the 2026-10-02 intake)
        "source": DOC_SA,
        "edition_type": "critical",
        "other_ids": ["Dzongsar: M42AE7A72 (Sanskrit- Tibetan)", "GRETIL: bsu051 (listed in Dzongsar metadata, 2026-10-02 intake)"],
        "source_description": ("Dzongsar Google Doc 'M42AE7A72 རྡོ་རྗེ་གཅོད་པ་རྩ་བ། Sanskrit- Tibetan' (the Sanskrit side of the "
                               "Sanskrit-Tibetan row alignment), exported as dorjeechoepa-root-sa(sa-bo).md, letter-identical to "
                               "the 2026-10-02 download of that doc; source URL from the Dzongsar Drive's links_manifest.csv "
                               "(2026-10-02 raw data). Title and author from the Sanskrit column of dorjeechoepa-root-bo.csv "
                               "(which records no edition; its composition_date cell reads 2004); the alternative title from the "
                               "text's closing line (row 433). No licence recorded upstream. One block per row."),
        "text_id": None, "edition_id": None, "toc_id": None,
    },
    "toc": {"kind": "outline", "file": ROOT_OUTLINE, "note": ROOT_TOC_NOTE},
})

# ── Tibetan display (translation of the Sanskrit) ───────────────────────────
bo_display = {
    "key": "bo-display",
    "path": "1-SOURCES/Translations/bo-vajracchedika.md",
    "adapter": "md_rows", "id_scheme": "h2",
    "text": "dorjeechoepa-root-bo(display).md",
    "pair": {"own_side": "dorjeechoepa-root-bo(sa-bo).md", "target_side": "dorjeechoepa-root-sa(sa-bo).md"},
    "target": "sa-root",
    **({"pair_corrections": sa_pairs["pair_corrections"]} if sa_pairs.get("pair_corrections") else {}),
    "title": "འཕགས་པ་ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པ་རྡོ་རྗེ་གཅོད་པ་ཞེས་བྱ་བ་ཐེག་པ་ཆེན་པོའི་མདོ།",
    "notes": ("The display segmentation (430 rows): the one Tibetan text the library stores (D2). The Tibetan side of the "
              "Sanskrit pair (dorjeechoepa-root-bo(sa-bo).md, 434 rows) is the same text cut differently; it is carried "
              "onto these blocks by letters. Every commentary points at these blocks."),
    "meta": "dorjeechoepa-root-bo.csv",
    "frontmatter": {
        "title": "འཕགས་པ་ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པ་རྡོ་རྗེ་གཅོད་པ་ཞེས་བྱ་བ་ཐེག་པ་ཆེན་པོའི་མདོ།",
        "alt_titles": ["འཕགས་པ་ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པ་རྡོ་རྗེ་གཅོད་པ་ཞེས་བྱ་བ།",
                       bo["title_short"][0].strip(), "རྡོ་རྗེ་གཅོད་པ།"],
        "title_in_english": "The Diamond Sūtra (Vajracchedikā Prajñāpāramitā Sūtra)",
        "author": bo["author"][0], "author_in_english": bo["author"][1],
        "language": "Tibetan", "lang_tag": "bo", "file_type": "translation",
        "root_text": "1-SOURCES/Text/sa-vajracchedika.md",
        "verse_id_format": "section-paragraph",
        "category_id": CATEGORY,
        "license": "public",             # as recorded for this text at the 2026-10-02 intake, as heart-sutra-rails did for its Tibetan
        "source": DOC_TSADEL,
        "edition_type": "critical",
        "other_ids": ["Dzongsar: M42AE7A72 (རྡོ་རྗེ་གཅོད་པ་རྩ་བ། Tsadel)"],
        "source_description": ("Dzongsar Google Doc 'M42AE7A72 རྡོ་རྗེ་གཅོད་པ་རྩ་བ། Tsadel' (the display segmentation), exported "
                               "as dorjeechoepa-root-bo(display).md, letter-identical to the 2026-10-02 download of that doc; "
                               "source URL from the Dzongsar Drive's links_manifest.csv (2026-10-02 raw data). Title from the "
                               "sheet's title_long_clean (dorjeechoepa-root-bo.csv) with འཕགས་པ་ as in the text's own row 3; "
                               "author from the sheet; licence as recorded for this text at the 2026-10-02 intake. A translation "
                               "of the Sanskrit root, aligned by the Dzongsar team's row pairing."),
        "text_id": None, "edition_id": None, "toc_id": None,
    },
    "toc": {"kind": "outline", "file": ROOT_OUTLINE, "note": ROOT_TOC_NOTE},
}
splits = TEMP / "root-row-splits.yaml"
if splits.exists():
    bo_display["row_splits"] = yaml.safe_load(splits.read_text(encoding="utf-8"))
works.append(bo_display)

# ── Chinese (Kumārajīva), translation of the Tibetan, added 2026-10-04 ──────
zh_meta = meta("dorjeechoepa-root-zh.csv")
zh_pairs = yaml.safe_load((TEMP / "pair-review/zh-bo-corrections.yaml").read_text(encoding="utf-8"))
ZH_D7 = ("vault owner — standing decision D7 carried over from heart-sutra-rails (2026-10-03); cut position and "
         "targets by Claude (2026-10-04), for the text expert to check")
works.append({
    "key": "lzh-translation",
    "path": "1-SOURCES/Translations/lzh-vajracchedika.md",
    "adapter": "md_rows", "id_scheme": "h2",
    "text": "dorjeechoepa-root-zh(bo-zh).md",
    # The Chinese doc's 430 rows are paired one for one with the 430 rows of the display doc (the Dzongsar 'Tsadel'),
    # as at the 2026-10-02 intake ("aligned row for row to the Tibetan Tsadel"); see 0-INBOX/temp/pair-review/zh-bo.md.
    "pair": {"own_side": "dorjeechoepa-root-zh(bo-zh).md", "target_side": "dorjeechoepa-root-bo(display).md"},
    "target": "bo-display",
    "pair_corrections": zh_pairs["pair_corrections"],
    "row_splits": [
        {"row": 38, "at": ["若菩薩不住相布施"], "targets": [[0], [1]],
         "reason": ("Heading 5 (ཕར་ཕྱིན་དྲུག་གི་སྤྱོད་པ་ལ་སློབ་ཚུལ།) stands inside the paired Tibetan row 38, after the "
                    "question དེ་ཅིའི་ཕྱིར་ཞེ་ན། (Wikisource page 3, revision 1239138), where that row is split (D7). The Chinese "
                    "row holds the same question and answer (何以故？ / 若菩薩不住相布施，其福德不可思量。) and is cut at the "
                    "same place; part 1 shows the Tibetan part 1, part 2 the Tibetan part 2."),
         "decided_by": ZH_D7, "date": TODAY},
        {"row": 317, "at": ["須菩提！過去心不可得"], "targets": [[0], [1]],
         "reason": ("Heading 10 (སེམས་སེམས་བྱུང་།) stands inside the paired Tibetan row 317, after the question "
                    "དེ་ཅིའི་ཕྱིར་ཞེ་ན། (Wikisource page 18, revision 1239152), where that row is split (D7). The Chinese row "
                    "holds the same question and answer (所以者何？ / 須菩提！過去心不可得，現在心不可得，) and is cut at the "
                    "same place; part 1 shows the Tibetan part 1, part 2 the Tibetan part 2."),
         "decided_by": ZH_D7, "date": TODAY},
    ],
    "title": "金剛般若波羅蜜經",
    "meta": "dorjeechoepa-root-zh.csv",
    "pair_side_not_used": {
        "file": "dorjeechoepa-root-bo(bo-zh).md",
        "reason": ("The Dzongsar doc 'M42AE7A72 རྡོ་རྗེ་གཅོད་པ་རྩ་བ། Tibetan - Chinese' (348 rows; letter-identical to its "
                   "2026-10-02 download), an older state of the Tibetan root with no partner (2026-10-02 report). Its rows do "
                   "not line up with the Chinese doc's 430 rows (they diverge from row 14); the Chinese doc's rows line up with "
                   "the display doc's 430 rows, which is therefore pair.target_side."),
        "decided_by": "Claude (2026-10-04), from the row comparison and the 2026-10-02 intake records — for the text expert to check"},
    "notes": ("Kumārajīva's translation as the Dzongsar team cut it into the 430 rows of the Tibetan display doc (61 rows "
              "empty where Kumārajīva has no counterpart). In a few places the team rearranged his wording to follow the "
              "Tibetan (rows 15, 132, 311-313, 372-373; see 0-INBOX/temp/pair-review/zh-bo.md), so the file is not in "
              "T0235 order everywhere. The older Chinese file 1-SOURCES/Translations/lzh-kumarajiva.md (2026-10-02, the 127 "
              "numbered segments the Chinese commentaries cite) is left untouched."),
    "frontmatter": {
        "title": "金剛般若波羅蜜經",
        "alt_titles": [zh_meta["title_short"][0]],
        "translator": "鳩摩羅什",
        "translator_in_english": "Kumārajīva",
        "language": "Classical Chinese", "lang_tag": "lzh", "file_type": "translation",
        "root_text": "1-SOURCES/Translations/bo-vajracchedika.md",
        "verse_id_format": "section-paragraph",
        "category_id": CATEGORY,
        "license": "public",         # as recorded for this doc at the 2026-10-02 intake (lzh-kumarajiva-tibetan-order.md)
        "source": zh_meta["source"][0],
        "edition_type": "critical",
        "cbeta_id": "T0235",
        "other_ids": ["Dzongsar: M42AE7A72 (金剛般若波羅蜜經 - Chinese-Tibetan Tsawa)", "CBETA: T0235"],
        "source_description": ("Dzongsar Google Doc 'M42AE7A72 金剛般若波羅蜜經 - Chinese-Tibetan Tsawa' (" + DOC_ZH + "), "
                               "exported as dorjeechoepa-root-zh(bo-zh).md, letter-identical to the 2026-10-02 download of "
                               "that doc: Kumārajīva's translation, cut by the Dzongsar team into the 430 rows of the Tibetan "
                               "display doc and paired with them row for row (19 pairings corrected, see the sidecar). Source "
                               "URL (CBETA T0235) and short title from dorjeechoepa-root-zh.csv; title from the doc's first row "
                               "and the Dzongsar metadata sheet MFF4994FD (2026-10-02 raw data: 金剛般若波羅蜜經, 後秦 鳩摩羅什譯), "
                               "which also names the translator; licence as recorded for this doc at the 2026-10-02 intake. A "
                               "translation of the Tibetan; a few passages follow the Tibetan order (see the manifest notes)."),
        "text_id": None, "edition_id": None, "toc_id": None,
    },
    "toc": {"kind": "outline", "file": ROOT_OUTLINE,
            "note": ROOT_TOC_NOTE.replace("(Tibetan verbatim; Sanskrit editorial)",
                                          "(Tibetan verbatim; Sanskrit and Chinese editorial)")
                    + " Chinese labels and the D7 splits of Chinese rows 38 and 317 added 2026-10-04 (Claude)."},
})

# ── Tibetan commentaries from Wikisource, aligned by Claude ─────────────────
COMM = [
    # (outline/raw id, registered_id, file stem, sheet row, metadata csv)
    ("vasubandhu-saptartha", "vasubandhu-saptartha", "bo-vasubandhu-saptartha-tika", 2, "dorjeechoepa-comm-2.csv"),
    ("chone-drakpa-shedrub", "chone-drakpa-shedrub", "bo-chone-drakpa-shedrub", 3, "dorjeechoepa-comm-3.csv"),
    ("kamalasila-tika", "kamalasila-tika", "bo-kamalasila-tika", 4, "dorjeechoepa-comm-4.csv"),
]
for oid, rid, stem, row, csvname in COMM:
    pair_dir = RAW / f"wikisource-{oid}"
    comm_rows, root_rows = f"{oid}(root-comm).md", f"{oid}-root(root-comm).md"
    if not (pair_dir / comm_rows).exists():
        continue
    m = meta(csvname)
    d, f, url = ws_meta(oid)
    align = json.loads((TEMP / f"align-{oid}/summary.json").read_text(encoding="utf-8"))
    title = m["title_long_clean"][0].rstrip("། ").replace("་ཞེས་བྱ་བ་བཞུགས་སོ", "") + "།"
    work, pid = AUTHOR_BDRC[rid]
    assert "bdrc" in m["source"][0] and m["source"][0].rsplit("/", 1)[1] == work, (rid, m["source"][0])
    assert urllib.parse.unquote(sheet_index(row).split("/wiki/", 1)[1]).replace("_", " ") == d["index_page"], rid
    edition = ", ".join(x for x in (f.get("Publisher"), f.get("Year"), f.get("Volumes")) if x)
    fm = {
        "title": title,
        "alt_titles": [t for t in [m["title_long_clean"][0], m["title_short"][0]] + [m.get(f"title_alt_{i}", [""])[0] for i in range(1, 6)] if t and t != title],
        # The sheet's English title for comm-4 lacks its closing quote (“The Perfection of Wisdom") — balanced here,
        # wording unchanged; it becomes the library's English title of the text. Claude, 2026-10-04, for the text expert.
        "title_in_english": (m["title_long_clean"][1].replace('Wisdom"', "Wisdom”") if m["title_long_clean"][1] else None),
        "author": f'{m["author"][0]} [bdrc:{pid}]', "author_in_english": f'{m["author"][1]} [bdrc:{pid}]',
        **({"translator": f["Translator"]} if f.get("Translator") else {}),
        "registered_id": rid,
        "language": "Tibetan", "lang_tag": "bo", "file_type": "commentary",
        "root_text": "1-SOURCES/Translations/bo-vajracchedika.md",
        "verse_id_format": "section-paragraph",
        "category_id": CATEGORY,
        "license": "public",         # Wikisource Derge/pecha text; as recorded for this work at the 2026-10-02 intake (heart-sutra: public)
        "source": sheet_index(row),  # the sheet's Wikisource Index link, verbatim (same page as pages.json)
        "edition_type": "critical",
        "bdrc_work_id": work,
        "other_ids": [f"Wikisource: {d['index_page']} (revision {d['index_revid']})"],
        "alignment_status": "needs-review",
        "source_description": (f"Wikisource, {d['index_page']} (revision {d['index_revid']}){'; ' + edition if edition else ''}; "
                               f"text of every Page: page (proofread, quality 3; revisions pinned in "
                               f"0-INBOX/raw-data/wikisource-{oid}/pages.json) retrieved {d['retrieved']}. Title, author and "
                               f"BDRC work from {csvname} and the text sheet dorjeechoepa.csv (row {row}); translator and edition "
                               f"from the Index page; source URL = the sheet's Index link; the author's BDRC id verified in the "
                               f"BDRC work record ({work}); licence as recorded for this work at the 2026-10-02 intake. No human "
                               f"alignment to the root exists in the raw data: the "
                               f"alignment to the Tibetan root was made by Claude from the commentary's quotations of the "
                               f"sūtra (see the manifest), for the text expert to review."),
        "text_id": None, "edition_id": None, "toc_id": None,
    }
    works.append({
        "key": stem,
        "path": f"1-SOURCES/Commentaries/{stem}.md",
        "adapter": "md_rows", "id_scheme": "h2",
        "text": f"wikisource-{oid}/{comm_rows}",
        "pair": {"own_side": f"wikisource-{oid}/{comm_rows}", "target_side": f"wikisource-{oid}/{root_rows}"},
        "target": "bo-display",
        "min_overlap": 12,   # the generated root side is whole segments (shortest: 15 letters); stops 3-4-letter diff slivers
        "title": title,
        "meta": csvname,
        "toc": {"kind": "outline", "file": f"2-RAILS/Sections/Raw/toc-wikisource/{oid}.md",
                "note": (f"The commentary's own table of contents: the inline headings of its Wikisource Index page "
                         f"({d['index_page']}, revision {d['index_revid']}), placed where its proofread pages put them "
                         f"(D6a, {STANDING}).")},
        "alignment": {
            "made_by": "Claude, on the vault owner's instruction of 2026-10-04 (\"you will need to do the alignment of the root and commentaries\"; \"Wikisource + Claude aligns\")",
            "method": align["method"],
            "evidence": f"0-INBOX/temp/align-{oid}/",
            "rows": align["rows"], "aligned_rows": align["aligned_rows"],
            "root_segments_transcluded": align["segments_aligned"],
            "date": TODAY,
        },
        "notes": ("Text from Wikisource only (D11 does not apply: the vault owner asked for the sheet's Wikisource "
                  "commentaries, 2026-10-04). Page markup and pecha line breaks removed, letters verbatim. Rows are cut "
                  "at every Index heading and before each passage where the commentary takes up a new root segment; "
                  f"wikisource-{oid}/{root_rows} is the generated root side of that pairing (row N = the display "
                  "segments row N comments on, verbatim), so the build's concordance carries it onto the display blocks."),
        "frontmatter": fm,
    })

# Backend ids written back by the uploaders on 2026-10-04 (root-text-upload, translation-upload, commentary-upload).
# build_sources.py rewrites each file from this manifest alone, so ids that are not repeated here would be wiped
# by the next rebuild. Keep this table in step with the files' frontmatter after every --execute.
BACKEND_IDS = {
    "1-SOURCES/Text/sa-vajracchedika.md": {
        "text_id": "KFDP2GKsN0LhzLoJ621MM",
        "edition_id": "JRah9DaEkM0e4VXWuClFz",
        "toc_id": "YhjbmoWfJw1R50OpGaVtw"
    },
    "1-SOURCES/Translations/bo-vajracchedika.md": {
        "text_id": "LHLu9gwHglREXXgehSJZ9",
        "edition_id": "DW28atCzbhhZoG6EMfcfF",
        "toc_id": "Qb1sqZWjFd1ScSCIEt7KC",
        "aligned_to_edition_id": "JRah9DaEkM0e4VXWuClFz"
    },
    "1-SOURCES/Translations/lzh-vajracchedika.md": {
        "text_id": "oaGiLLnmBXfVUfvQJKIRr",
        "edition_id": "yRy2qTNHCejeLRcV9XFVs",
        "toc_id": "lkKilEXKXM8jZxTw276UA",
        "aligned_to_edition_id": "DW28atCzbhhZoG6EMfcfF"
    },
    "1-SOURCES/Commentaries/bo-vasubandhu-saptartha-tika.md": {
        "text_id": "fvnQUTRKGXtlau5CJb5m4",
        "edition_id": "svxOOyUSGU0vPUVf6CNo1",
        "toc_id": "BwR8PZA3ciu4FzLn7sKaY",
        "aligned_to_edition_id": "DW28atCzbhhZoG6EMfcfF",
        "commentary_of": "LHLu9gwHglREXXgehSJZ9"
    },
    "1-SOURCES/Commentaries/bo-chone-drakpa-shedrub.md": {
        "text_id": "lBje379uSCW57yo5bYOHX",
        "edition_id": "1uQ5xraq1X88PYf4DGiVW",
        "toc_id": "NpICwlctKj9AxTYu4qi5v",
        "aligned_to_edition_id": "DW28atCzbhhZoG6EMfcfF",
        "commentary_of": "LHLu9gwHglREXXgehSJZ9"
    },
    "1-SOURCES/Commentaries/bo-kamalasila-tika.md": {
        "text_id": "kfLTel1b89XDojqoqM7V0",
        "edition_id": "wENonbecucCnfqU2QWeuK",
        "toc_id": "KqtqKWKDwvsxM2o8YUAxU",
        "aligned_to_edition_id": "DW28atCzbhhZoG6EMfcfF",
        "commentary_of": "LHLu9gwHglREXXgehSJZ9"
    }
}
for w in works:
    for k, v in BACKEND_IDS.get(w["path"], {}).items():
        w["frontmatter"][k] = v

man = {
    "raw_root": "0-INBOX/raw-data",
    "sidecar_dir": "1-SOURCES/Annotations",
    "works": works,
}
head = ("# Intake manifest — Diamond Sūtra (dorjeechoepa), 2026-10-04\n"
        "# GENERATED by 0-INBOX/temp/make_manifest.py — edit that, then re-run it.\n"
        "# Route B (md_rows). The previous intake's manifest (Drive docx + OpenPecha, 2026-10-02) is in git history.\n"
        "# Chinese root (Kumārajīva, dorjeechoepa-root-zh) added 2026-10-04 as lzh-translation, aligned to the Tibetan;\n"
        "# the Chinese commentaries (comm-5/6/8/9) are not handled yet (vault owner, 2026-10-04).\n"
        "# Upload metadata (category_id, tag_ids on the root, license, source, edition_type, author BDRC ids) added 2026-10-04.\n\n")
(RAW / "intake-manifest.yaml").write_text(head + yaml.safe_dump(man, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")
print("works:", [w["key"] for w in works])
