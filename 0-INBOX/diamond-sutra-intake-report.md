---
title: "Diamond Sūtra — intake report"
status: draft
source_description: "Report of the first aligned-corpus-intake build (2026-10-02) from 0-INBOX/raw-data/intake-manifest.yaml. Scratch — not a source, never cited. Machine-readable detail: 0-INBOX/temp/diamond-intake-report.json."
---

# Diamond Sūtra — intake report (2026-10-02)

Built with `4-SYSTEM/Skills/aligned-corpus-intake/` from the raw data in `0-INBOX/raw-data/` (OpenPecha API download + Dzongsar Drive export). Every file records its raw sources (with sha1) in `raw_sources:`; every block's provenance and all annotation layers are in `1-SOURCES/Annotations/<stem>.annotations.json`.

**Verifier:** all 20 files `OK` — every letter of every raw source is in the output (`missing=0`), ids are unique and at most three parts, headings start at `#` and never skip a level, no transclusion points at a missing id. **Publication dry run** (WeBuddhist linter + parser, on a scratch copy): every file lints and produces text, edition, TOC and alignment payloads; the only error is the empty `category_id`.

## Files

| File | From | Blocks | Headings | Transclusions | Alignment source |
|---|---|---:|---:|---:|---|
| `Text/bo-vajracchedika.md` | Dzongsar Tsadel (430 rows) | 430 | — | — | (root) |
| `Translations/lzh-kumarajiva.md` | MFF4994FD, 127 numbered segments | 127 | 32 分 | 376 → bo | Chinese–Tibetan Tsawa rows, located in both texts |
| `Translations/lzh-kumarajiva-tibetan-order.md` | Chinese–Tibetan Tsawa | 369 | — | 369 → bo | row pairing, **identity** (uploadable now) |
| `Translations/zh-baihua.md` | OpenPecha gmqBB9… | 76 | 32 分 | 127 → lzh | OpenPecha alignment, projected |
| `Translations/lzh-bodhiruci.md` | R434373A0 root Tsadrel | 37 | — | — | none exists |
| `Translations/sa-vajracchedika.md` | Sanskrit–Tibetan pair | 423 | — | 425 → bo | row pairing — **needs review** |
| `Commentaries/bo-vasubandhu-saptartha-tika.md` | D3 (E4C456D1) | 423 | 38 *sa bcad* | 392 → bo | typed numbers (366 blocks) via ref431 |
| `Commentaries/bo-chone-drakpa-shedrub.md` | Cone "Segm" | 366 | 8 *sa bcad* | 1026 → bo | typed numbers (349 blocks) via ref431 |
| `Commentaries/bo-kamalasila-tika.md` | D4 (E4BF16EE) | 287 | 43 *sa bcad* | 290 → bo | typed numbers (268 blocks) via ref431 |
| `Commentaries/bo-asanga-rtsa-grel.md` | R3C4E9ABF | 79 | — | — | 6 candidate refs only |
| `Commentaries/lzh-huineng-jieyi.md` | R2A8AD21D | 256 | 32 分 | 181 → lzh | typed MFF refs; Tsadrel agrees 125/126 |
| `Commentaries/lzh-vasubandhu-lun.md` | R434373A0 | 448 | — | 356 → lzh | typed MFF refs (lemma is Bodhiruci) |
| `Commentaries/lzh-asanga-lun.md` | R43644D12 | 298 | — | 256 → lzh | typed MFF refs |
| `Commentaries/lzh-zongle-zhujie.md` | R96396549 | 237 | 27 斷疑 | 225 → lzh | typed MFF refs; Tsadrel agrees 78/81 |
| `Commentaries/lzh-gunada-pojuzhe.md` | R67954D57 | 146 | — | 185 → lzh | typed MFF refs; Tsadrel agrees 55/55 |
| `Commentaries/lzh-taixu-yimai.md` | R92439761 | 43 | 21 科判 | 364 → lzh | typed MFF ranges; Tsadrel agrees 14/16 |
| `Commentaries/lzh-tanxu-jiangyi.md` | R2FB78325 | 210 | 1 | 171 → lzh | typed MFF refs; Tsadrel agrees 68/68 |
| `Commentaries/zh-hsingyun-jianghua.md` | R3E4D8B99 (split at line breaks) | 3182 | 96 | 741 → lzh | typed MFF refs |
| `Commentaries/zh-shengyen-jiangji.md` | R2BF994FF | 275 | 27 | — | 114 candidate refs only |
| `Commentaries/lzh-jizang-shu.md` | R89643BF0 | 88 | 1 卷 | — | none exists |

Second layers kept in the sidecars: OpenPecha alignments of Chone (183/198 pairs placed) and Kamalaśīla (226/228); the older Cone D2 alignment (342/354 paragraphs placed); 997/1015 Kamalaśīla and 16/17 Vasubandhu variant readings (Snar thang / Peking / Co ne); Kamalaśīla verse italics from the partial A5 segmentation; every colour / bold / italic run with its meaning; 7 Word reviewer comments (Tenzin Tsering, Dec 2024); the row-level Tsadrel pairs of every Chinese commentary; the ref431 → Tsadel concordance (431/431, identical to the hand-derived table).

## Needs a human

1. **`category_id`** — empty in all 20 files; the WeBuddhist category must be chosen before upload.
2. **Sanskrit pairing drift** (`sa-vajracchedika.md`, `alignment_status: needs-review`). From Tibetan row 229 the Sanskrit column sits one row behind (T230 ཐེག་པ་མཆོག ↔ S229 अग्रयान), later two (T372 ↔ S374, T428 ↔ S429). Reproduced as made. Six Sanskrit rows with no Tibetan row (216, 311, 376, 379, 420, 431) are kept with the preceding block and flagged.
3. **Chone reference `189190`** on blocks `^2-160`–`^2-162` — probably `189,190`; not resolved, no transclusion made.
4. **ref431 number 146** — its row reads ཀྱི where Tsadel has the corrected ཀྱིས (Tenzin Tsering's comment); mapped to Tsadel ^146 by position, recorded as `inferred_by_position`.
5. **Candidate references** — 聖嚴 講記 (114 numeric prefixes mixing MFF refs with the author's lists) and the Tibetan Asaṅga verse commentary (6 numbers, numbering unstated): kept in the text, listed in the sidecar, no transclusions until confirmed.
6. **註解 Tsadrel rows 102, 104, 106** have the root on the lemma row instead of the explanation row (3 of the 81 disagreements); typed references were used.
7. **Contributors without ids** — the linter skips names with no `[bdrc:…]`/`[op:…]`: all Chinese authors/translators, the Buddha. BDRC ids were added where the source gives them (Vasubandhu P6119, Kamalaśīla P7641, Chone P1629, Asaṅga P6117, translators P318, P856, P8205).
8. **Licences** — set `public` where OpenPecha says Public Domain Mark or the work is pre-modern; `unknown` for 白話, Sanskrit, and the 20th-century works (太虛, 倓虛, 星雲, 聖嚴). Check before publishing.
9. **Registered ids and the `Annotations/` folder** were written into `4-SYSTEM/Guidelines/vault-annex.md` — please review.

## Publishing

`translation-upload` publishes translations whose alignment is **identity**; of these files only `lzh-kumarajiva-tibetan-order.md` is ready for it once the Tibetan root is uploaded and carries `text_id`/`edition_id`. The commentaries and the non-identity translations parse into valid alignment payloads, but there is no upload skill for them in this vault yet. Nothing was uploaded.

## Not ingested (raw files kept in `0-INBOX/raw-data/`)

| Raw item | Why |
|---|---|
| 5 English translations (`D1…/Root texts in English/`) | Unsegmented and unaligned; three are PDF/web extractions with page headers or site chrome (one truncated at ch. 12); modern copyrighted translations. Need cleanup, segmentation and a rights decision. |
| R3452D71B (bsdus don), R76E83977 (ཕན་ཡོན།), `Sanskrit.docx` (Sarnath 1997 edition) | Raw OCR with page breaks and junk — run `tibetan-ocr-quality` / `clean-raw-text` / `format-commentary` first. |
| R0FCDD06D (clean ཕན་ཡོན། text) | Filed under the Chone commentary's ID but is a different text — needs an ID decision. |
| `H_Root_text/…Tibetan - Chinese.docx` (348 rows), `B_Clean_Text` root | Older states of the Tibetan root; no partner file. Superseded by the Tsadel (Tenzin Tsering's corrections). |
| `RF161D626 … Root text Tsadrel.docx` | Its commentary partner is missing from the Drive (404); the Kamalaśīla alignment comes from D4's numbers. Listed under `raw_sources`. |
| `other/Untitled document.docx` | Same text as the ref431 numbered root; its 251 dark-red lines have no known meaning. |
| A1/A2/A3/A4/A5, TOC and Clean commentary docs | Contained in the more complete D3 / Cone Segm / D4 docs (checked syllable by syllable); listed under `raw_sources`. |
| OpenPecha CudRcM2Y8ZUlGY55GP0cg, pR5GpBvpuXeqfkM0A7ay7 | Duplicates of gmqBB9… (2 characters differ) and eMxgLF… (identical). |
| OpenPecha SoWrv…, sUjAy…, gRREC… (Chinese commentaries) | Same works as the Dzongsar docs used; their alignments are not yet carried as overlays. |
| RAF408FDA 金剛般若經贊述, 4 E4BF16EE parts, other B-series links | Not downloadable (404 / Drive shortcuts) — see `0-INBOX/dzongsar-drive-inventory.md`. |
| Metadata `.xlsx`, Resources catalogues, PDFs | Used for frontmatter and identification; 67 empty templates ignored. |

## Re-running

```bash
python3 4-SYSTEM/Skills/aligned-corpus-intake/scripts/build_sources.py 0-INBOX/raw-data/intake-manifest.yaml --report 0-INBOX/temp/diamond-intake-report.json
python3 4-SYSTEM/Skills/aligned-corpus-intake/scripts/verify.py 0-INBOX/raw-data/intake-manifest.yaml
```
Fix the manifest, never the outputs. Once a rail cites these files, a rebuild that changes ids is a migration to log in the annex.
