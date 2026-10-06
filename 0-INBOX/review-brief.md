---
title: "Diamond Sūtra — review brief for the text expert (2026-10-04)"
status: draft
source_description: "Scratch: what to check in the 2026-10-04 intake of the Sanskrit, the Tibetan root and three Tibetan commentaries. Not a source, never cited."
---

# Diamond Sūtra — review brief (2026-10-04)

Details and method: `0-INBOX/dorjeechoepa-intake-report.md`. "Root row N" = row N of the Tibetan display doc; block ids are those of `1-SOURCES/Translations/bo-vajracchedika.md` unless a file is named.

## At a glance

| File | Role | Blocks | Headings and their source | Transclusions |
|---|---|---|---|---|
| `Text/sa-vajracchedika.md` | Sanskrit root (D1) | 428 | 13, Wikisource Index of the Derge Kangyur; Sanskrit labels editorial (Claude) | — |
| `Translations/bo-vajracchedika.md` | Tibetan, translation of the Sanskrit; what the commentaries point at | 432 | 13, Wikisource Index, verbatim | 421 → Sanskrit (human row pairing, 102 pairs corrected by Claude) |
| `Commentaries/bo-vasubandhu-saptartha-tika.md` | Vasubandhu, from Wikisource | 177 | 38, its Wikisource Index | 417 → Tibetan (**Claude's alignment**) |
| `Commentaries/bo-chone-drakpa-shedrub.md` | Chone Drakpa Shedrub, from Wikisource | 176 | 21, its Wikisource Index | 430 → Tibetan (**Claude's alignment**) |
| `Commentaries/bo-kamalasila-tika.md` | Kamalaśīla, from Wikisource | 264 | 44, its Wikisource Index | 422 → Tibetan (**Claude's alignment**) |

## Checked automatically

- Every letter of every source is in the output, none added (`missing=0 extra=0`, all five files).
- Every row with text is exactly one block (rows 38 and 317 of the Tibetan: two, as declared).
- Every transclusion equals the pairing it comes from (`aligned_ok` n/n), and the paired text is really found in the transcluded blocks (`content_ok` n/n). For the commentaries, transclusions equal the reviewed placements exactly.
- Ids unique, headings well nested, no dangling transclusion, no brackets in body text.
- The publication linter and parser build text, TOC and alignment payloads for all five files (once `category_id` and the two missing `source` URLs are filled).

## Review checklist (most important first)

### Commentary alignments — made by Claude, no human alignment existed
- [ ] **Overall**: the rows of the three commentaries and their transclusions were made by Claude (letter matching of quotations, then a reading review with 253 corrections). Compared with the Dzongsar team's own alignment of these works from the old intake, the same row is chosen for 96 % (Chone), 89 % (Kamalaśīla), 88 % (Vasubandhu) of the segments both place. Spot-check a few sections per commentary; evidence per row: `0-INBOX/temp/align-<id>/alignment.tsv` and `overrides.yaml`.
- [ ] **Kamalaśīla & Vasubandhu cover more than the humans did**: a row is taken to comment on the root from its lemma up to the next lemma, so dialogue formulas (རབ་འབྱོར་འདི་ཇི་སྙམ་དུ་སེམས། …) are transcluded with the row that takes up their question, even where the commentary has no gloss for them. Decide whether that is wanted, or whether only explicitly glossed segments should be transcluded.
- [ ] **Out-of-order explanations** the one-placement-per-segment model cannot express:
  - Kamalaśīla `3-97` (row 102) takes up root `^7-39`–`^7-42` (དེ་ལྟ་བས་ན་ཞེས་བྱ་བ་ལ་སོགས་པ་… ལྷག་མ་ནི་སྔ་མ་བཞིན་ནོ) *before* `3-98` explains `^7-38`; they are left unplaced (coverage gap).
  - Kamalaśīla `3-92` explains root `^7-28`–`^7-31` in detail; `3-93`–`3-94` (after heading 3.4.2.5.2) repeat the lemmas of `^7-28`–`^7-29` with a short gloss and carry no transclusion — misplaced text, or the Wikisource heading in the wrong place?
  - Kamalaśīla row 110 (`3-105`) glosses མོས་པར་བྱ / ཁོང་དུ་ཆུད་པར་བྱ of root `^7-52`–`^7-53` after the passage of later segments; kept at `3-102`.
  - Vasubandhu: root `^6-41`–`^6-45` are explained again in `2-36`–`2-37` after the next segment; kept at `2-32`. Root `^3-4`–`^3-5` repeat the wording of `^2-3` and are explained with it in `2-2`; placed in `2-4` to keep the order.
  - Kamalaśīla root `^3-4`–`^3-5` (ཕན་གདགས་པའི་དམ་པ, ཡོངས་སུ་གཏད་པ) are explained only once, before the question; placed at `3-15`. Kamalaśīla `3-16`'s gloss on བྱང་ཆུབ་སེམས་དཔའི་ཐེག་པ could belong to several segments.
- [ ] **Grouped explanations**: Chone `2-47` explains the once-returner, non-returner and arhat passages (root `^7-10`–`^7-27`) together ("the same applies to the other three"); all are transcluded there. Chone `2-49`/`2-50` both take up root `^7-28`.
- [ ] Chone: root `^8-101` (Tibetan row 276, a line with no Sanskrit counterpart either) — the reviewer could not find where the commentary takes it up; placed at `2-106`.
- [ ] **Coverage gaps**: Vasubandhu never transcludes the opening narrative `^1-1`–`^1-8` (except `^1-5`), `^2-1`, `^2-2` (it does not discuss them); Kamalaśīla `^7-39`–`^7-42` (above). Chone: none.
- [ ] **Wikisource text**: all commentary pages are proofread (quality 3), not validated. The commentaries' rows were cut by Claude (at headings, before each new lemma, and at sentence ends in long stretches) — the Dzongsar commentary docs are cut by sentence; check the cutting suits the library.

### Root and Sanskrit
- [ ] **102 Sanskrit–Tibetan pairing corrections by Claude** (`0-INBOX/temp/pair-review/sa-bo.md`, manifest `pair_corrections` of `bo-display`): Tibetan doc rows 231–327 re-paired one row back (the doc's Tibetan row 230 = display `^8-55`, the Tibetan-only sentence འདིའི་རྣམ་པར་སྨིན་པ་ཡང་བསམ་གྱིས་མི་ཁྱབ་པ་…, sat opposite Sanskrit 230); local slips at doc rows 375, 378, 419, 428, 430. Unpaired after correction: `^8-55` and `^8-101`.
- [ ] Tibetan blocks with no Sanskrit (as made): `^0-2`, `^0-3` (Indic and Tibetan titles), `^7-15`–`^7-16`, `^8-55`, `^8-101`, the dhāraṇī/appendix `^13-4`–`^13-6`. Sanskrit rows with no Tibetan: 216, 310, 327, 375, 378, 419, 428 (doc numbering).
- [ ] **Root TOC placement**: five headings (3, 4, 6, 9, 12) moved by Claude from a few letters inside a row to the row boundary where the proofread page puts them; headings 5 and 10 split rows 38 and 317 after དེ་ཅིའི་ཕྱིར་ཞེ་ན། as on the page, with the row's Sanskrit shown with part 2. Outline: `2-RAILS/Sections/Raw/toc-wikisource/vajracchedika.md`.
- [ ] **13 editorial Sanskrit headings** (Claude), e.g. निदानम्, बोधिचित्तोत्पादः, लक्षणानुव्यञ्जनानि, चित्तचैतसिकाः, फलं धर्मकायः — check wording.
- [ ] Sanskrit `^8-99`: Claude removed a Markdown-export artifact (`000.` list marker on an indented continuation line) and rejoined the line.
- [ ] The Sanskrit keeps its edition's section numbers (॥१॥ … ॥३२॥) as in the doc — keep, or remove as in Phakpadoepa?

### Metadata and housekeeping
- [ ] `category_id` empty in all five files; `source` URL missing for the Sanskrit and the Tibetan (the sheets give none); `license: unknown` everywhere.
- [ ] **Stale links**: the Chinese files and `bo-asanga-rtsa-grel.md` (old intake, left untouched on instruction) still transclude `1-SOURCES/Text/bo-vajracchedika.md#^N`, which no longer exists — to be redone with the Chinese.
- [ ] Raw data: `dorjeechoepa-comm-4(root-comm).md` is the ཕན་ཡོན་ OCR text, not Kamalaśīla; `dorjeechoepa-root-bo-3(root-comm).md` has no commentary half; `dorjeecheopa.csv` duplicates `dorjeechoepa.csv`.

## Where to look

- Built files: `1-SOURCES/Text/`, `1-SOURCES/Translations/bo-vajracchedika.md`, `1-SOURCES/Commentaries/bo-{vasubandhu-saptartha-tika,chone-drakpa-shedrub,kamalasila-tika}.md`; sidecars in `1-SOURCES/Annotations/`.
- Outlines: `2-RAILS/Sections/Raw/toc-wikisource/`.
- Manifest and its generator: `0-INBOX/raw-data/intake-manifest.yaml`, `0-INBOX/temp/make_manifest.py`.
- Alignment evidence: `0-INBOX/temp/align-<id>/` (alignment.tsv, overrides.yaml, review packets, eval-vs-dzongsar.json); pairing review: `0-INBOX/temp/pair-review/`; coverage: `0-INBOX/temp/coverage.txt`; independent review: `0-INBOX/temp/independent-review.md`.
- Annex: `4-SYSTEM/Guidelines/vault-annex.md` (registered deviations and the ID-migration log).
