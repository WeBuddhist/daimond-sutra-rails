---
title: "OpenPecha API download — Diamond Sūtra"
status: draft
source_description: "Index of the verbatim OpenPecha backend API v2 download in 0-INBOX/raw-data/openpecha-api/: the Tibetan root text, every translation and commentary linked to it, and their alignment annotations. Scratch — not a source, never cited."
---

# OpenPecha API download — Diamond Sūtra

**Root:** འཕགས་པ་ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པ་རྡོ་རྗེ་གཅོད་པ་ཞེས་བྱ་བ་ཐེག་པ་ཆེན་པོའི་མདོ། (`OQLxJCPiXhRTJK9yiTviM`, BDRC `WA0RK0016`)

**Downloaded:** 2026-10-02 from the old OpenPecha backend (`https://api-aq25662yyq-uc.a.run.app`, API 0.1.0 @ `ecdf248`). The root text's files were copied from the earlier full download in `Nalanda-texts-rails/0-INBOX/raw-data/openpecha-api/` (downloaded 2026-09-27); everything else was fetched fresh. Every file under `raw-data/openpecha-api/` is the API response exactly as received.

**Contents:** 10 texts. That is the root, 3 translations and 6 commentaries. 6 of the 9 derived texts carry an alignment upstream. Nothing here has been converted or checked yet.

## Texts

`#` is the row number; "translation of #4" means the text is aligned to row 4, not to the root. **Chars** and **Segs** are for the critical instance: character count, and the number of segments in its segmentation annotation. **Alignment** gives the number of spans on the derived text ↔ the number of spans on its parent.

| # | Relation | Language | Title | Text ID | Source · licence | Chars | Segs | Alignment | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 0 | **root** | Tibetan | འཕགས་པ་ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པ་རྡོ་རྗེ་གཅོད་པ་ཞེས་བྱ་བ་ཐེག་པ་ཆེན་པོའི་མདོ། | `OQLxJCPiXhRTJK9yiTviM` | bdrc.io · Public Domain Mark | 42,971 | 207 |  |  |
| 1 | translation | Literary Chinese | 金剛般若波羅密多經 | `i5gV2cTZzE5NEl4DObMKu` | unknown · unknown | 7,040 | 114 | — none upstream |  |
| 2 | translation of #1 | Modern Chinese | 《金剛般若波羅蜜經》白話 | `gmqBB9aIgbuZhaFDK8s9m` | unknown · unknown | 9,560 | 112 | ✓ 112 ↔ 112 | **near-identical to #6 (2 chars differ)** |
| 3 | commentary of #1 | Literary Chinese | 金剛經解義 | `SoWrvGSigom4RZe1EENev` | unknown · unknown | 21,436 | 293 | ✓ 161 ↔ 161 |  |
| 4 | commentary of #1 | Literary Chinese | 金剛般若波羅蜜經破取著不壞假名論 | `sUjAy5TUlP0GZDGrQ25fl` | unknown · unknown | 17,303 | 148 | ✓ 93 ↔ 97 |  |
| 5 | commentary of #1 | Literary Chinese | 金剛般若波羅蜜經論 | `gRRECLslNb5yg3Hg7lBpX` | unknown · unknown | 25,768 | 75 | ✓ 39 ↔ 39 |  |
| 6 | translation | Modern Chinese | 《金剛般若波羅蜜經》白話 | `CudRcM2Y8ZUlGY55GP0cg` | unknown · unknown | 9,560 | 112 | — none upstream | **near-identical to #2 (2 chars differ)** |
| 7 | commentary | Tibetan | འཕགས་པ་ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པ་རྡོ་རྗེ་གཅོད་པ་ཞེས་བྱ་བ་ཐེག་པ་ཆེན་པོའི་མདོ། (Commentary) | `pR5GpBvpuXeqfkM0A7ay7` | bdrc.io · unknown | 97,568 | 300 | — none upstream | **same content as #9** |
| 8 | commentary | Tibetan | འཕགས་པ་ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པ་རྡོ་རྗེ་གཅོད་པའི་རྒྱ་ཆེར་འགྲེལ་པ། | `dnFy5O0ji9QDgE1Wh1IR7` | bdrc.io · Public Domain Mark | 209,039 | 1915 | ✓ 228 ↔ 228 |  |
| 9 | commentary | Tibetan | རྡོར་གཅོད་ཀྱི་འགྲེལ་པ་ཐར་པར་བགྲོད་པའི་ལམ་བཟང་ཟབ་དོན་གསལ་བའི་ཉི་མ་ཞེས་བྱ་བ་བཞུགས་སོ། | `eMxgLFLT1xz6OOgpsY1h7` | bdrc.io · Public Domain Mark | 97,568 | 300 | ✓ 198 ↔ 198 | **same content as #7** |

## Not downloaded

Texts linked to this tree upstream but titled "Delete this" (test records):

- `w49T5btRrJJ9EfscBSuhI` (Literary Chinese) — Delete this
- `uC6EHISQ40iHptCbMKkNP` (Literary Chinese) — Delete this
- `Nx11PgwEr9fiIAohE83NV` (Literary Chinese) — Delete this

## Layout

```
0-INBOX/raw-data/openpecha-api/
  manifest.json                         run metadata (API base and version, dates, counts)
  tree.json                             every text with its parent and relationship; every
                                        derived→parent pair with its instance IDs and alignment file
  texts.json                            the GET /v2/texts entries for these texts
  categories.json                       category titles (bo, en), copied from Nalanda-texts-rails
  texts/<text_id>/
    text.json                           GET /v2/texts/<id>
    instances.json                      GET /v2/texts/<id>/instances
    instances/<instance_id>.json        GET /v2/instances/<id>?content=true&annotation=true
    annotations/<annotation_id>.json    GET /v2/annotations/<id>   (segmentation, bibliography, …)
    related/<instance_id>.json          GET /v2/instances/<id>/related
    alignments/<annotation_id>.json     GET /v2/annotations/<id>   (type alignment, derived text only)
```

**Reading an alignment.** The spans in an alignment file's `alignment_annotation` are character offsets into this text's critical-instance `content`. Each span's `aligned_segments` lists IDs from `target_annotation`, whose spans are offsets into the **parent** instance's `content`. `tree.json` → `pairs` names both instance IDs.

**Next step.** In `Nalanda-texts-rails`, the `json-to-source-text` skill's `openpecha_api_v2.py` converter reads this exact layout (`text.json` / `instances/` / `annotations/`, plus `manifest.json` and `categories.json`). It is not yet installed in this vault. It renders original texts, so the alignment-driven intake of translations and commentaries is still to be decided.
