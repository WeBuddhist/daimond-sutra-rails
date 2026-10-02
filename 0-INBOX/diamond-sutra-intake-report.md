---
title: "Diamond Sūtra — intake report"
status: draft
source_description: "Report of the first aligned-corpus-intake build (2026-10-02) from 0-INBOX/raw-data/intake-manifest.yaml. Scratch — not a source, never cited. Machine-readable detail: 0-INBOX/temp/diamond-intake-report.json."
---

# Diamond Sūtra — intake report (2026-10-02, revised)

**Revision.** The first build keyed the Tibetan root to the 430-row Tsadel split and translated every commentary number onto it (`1-3` became `^2 ^3 ^4`). Rebuilt so the root is the numbered root the commentaries were aligned against: block `^N` = root segment N, and every number in front of a commentary segment is transcluded as written. Checked per block: in all 14 commentaries every numbered segment transcludes exactly the ids its number names (2,359 of 2,359), and every unnumbered segment transcludes nothing. 聖嚴 講記 and the Tibetan Asaṅga verse commentary, first held back as "candidate" numbers, are aligned too: their numbers check out against the root text.

Built with `4-SYSTEM/Skills/aligned-corpus-intake/` from the raw data in `0-INBOX/raw-data/` (OpenPecha API download + Dzongsar Drive export). Every file records its raw sources (with sha1) in `raw_sources:`; every block's provenance and all annotation layers are in `1-SOURCES/Annotations/<stem>.annotations.json`.

**Verifier:** all 20 files `OK` — every letter of every raw source is in the output (`missing=0`), ids are unique and at most three parts, headings start at `#` and never skip a level, no transclusion points at a missing id. **Publication dry run** (WeBuddhist linter + parser, on a scratch copy): every file lints and produces text, edition, TOC and alignment payloads; the only error is the empty `category_id`.

## Files

| File | From | Blocks | Headings | Transclusions | Alignment source |
|---|---|---:|---:|---:|---|
| `Text/bo-vajracchedika.md` | numbered root (`It is for reference only/…Root text`, 431 segments) | 431 | — | — | (root; Tsadel split in sidecar) |
| `Translations/lzh-kumarajiva.md` | MFF4994FD, 127 numbered segments | 127 | 32 分 | 378 → bo | Chinese–Tibetan Tsawa rows, located in both texts |
| `Translations/lzh-kumarajiva-tibetan-order.md` | Chinese–Tibetan Tsawa | 368 | — | 370 → bo | row pairing; identity except the 2 rows covering root 14+15 and 183+184 |
| `Translations/zh-baihua.md` | OpenPecha gmqBB9… | 76 | 32 分 | 127 → lzh | OpenPecha alignment, projected |
| `Translations/lzh-bodhiruci.md` | R434373A0 root Tsadrel | 37 | — | — | none exists |
| `Translations/sa-vajracchedika.md` | Sanskrit–Tibetan pair | 422 | — | 426 → bo | row pairing — **needs review** |
| `Commentaries/bo-vasubandhu-saptartha-tika.md` | D3 (E4C456D1) | 423 | 38 *sa bcad* | 392 → bo | its numbers, as written (366 segments) |
| `Commentaries/bo-chone-drakpa-shedrub.md` | Cone "Segm" | 366 | 8 *sa bcad* | 1035 → bo | its numbers, as written (349; `189190` read as 189,190) |
| `Commentaries/bo-kamalasila-tika.md` | D4 (E4BF16EE) | 287 | 43 *sa bcad* | 290 → bo | its numbers, as written (268 segments) |
| `Commentaries/bo-asanga-rtsa-grel.md` | R3C4E9ABF | 79 | — | 11 → bo | its numbers (6 stanzas; 73 unnumbered) |
| `Commentaries/lzh-huineng-jieyi.md` | R2A8AD21D | 256 | 32 分 | 181 → lzh | typed MFF refs; Tsadrel agrees 125/126 |
| `Commentaries/lzh-vasubandhu-lun.md` | R434373A0 | 448 | — | 356 → lzh | typed MFF refs (lemma is Bodhiruci) |
| `Commentaries/lzh-asanga-lun.md` | R43644D12 | 298 | — | 256 → lzh | typed MFF refs |
| `Commentaries/lzh-zongle-zhujie.md` | R96396549 | 237 | 27 斷疑 | 225 → lzh | typed MFF refs; Tsadrel agrees 78/81 |
| `Commentaries/lzh-gunada-pojuzhe.md` | R67954D57 | 145 | — | 187 → lzh | typed MFF refs; Tsadrel agrees 55/55 |
| `Commentaries/lzh-taixu-yimai.md` | R92439761 | 43 | 21 科判 | 364 → lzh | typed MFF ranges; Tsadrel agrees 14/16 |
| `Commentaries/lzh-tanxu-jiangyi.md` | R2FB78325 | 210 | 1 | 171 → lzh | typed MFF refs; Tsadrel agrees 68/68 |
| `Commentaries/zh-hsingyun-jianghua.md` | R3E4D8B99 (split at line breaks) | 3182 | 96 | 741 → lzh | typed MFF refs |
| `Commentaries/zh-shengyen-jiangji.md` | R2BF994FF | 275 | 27 | 137 → lzh | typed MFF refs (114) |
| `Commentaries/lzh-jizang-shu.md` | R89643BF0 | 88 | 1 卷 | — | none exists |

Second layers kept in the sidecars: OpenPecha alignments of Chone (183/198 pairs placed) and Kamalaśīla (226/228); the older Cone D2 alignment (342/354 paragraphs placed); 997/1015 Kamalaśīla and 16/17 Vasubandhu variant readings (Snar thang / Peking / Co ne); Kamalaśīla verse italics from the partial A5 segmentation; every colour / bold / italic run with its meaning; 7 Word reviewer comments (Tenzin Tsering, Dec 2024); the row-level Tsadrel pairs of every Chinese commentary; the root's Tsadel split and its two later letter corrections (`alt_segmentations` in the root sidecar).

## Decided (2026-10-02)

- **Chone `189190`** (paragraphs 381, 383, 385 → blocks `^2-160`–`^2-162`) read as **189,190** — confirmed by the vault owner; the text echoes root 189 and 190 and the next paragraph is `191-192`. Recorded as `ref_corrections` in the manifest and as `ref_correction` on each block in the sidecar; the raw doc is unchanged.
- **Root text corrections applied** from the Tsadel doc: segment ^29 `དུ་ཤེས་ཅན་ནམ` → `འདུ་ཤེས་ཅན་ནམ` (*saṃjñin*), segment ^146 `ཁྱོད་ཀྱི་ཁོང` → `ཁྱོད་ཀྱིས་ཁོང` (Tenzin Tsering, from the Sanskrit *prativedayāmi te*). Recorded as `text_corrections` in the manifest; the original readings are kept on the blocks in the sidecar.
- **One-to-two alignments kept as made.** Root ^14/^15 and ^183/^184 are two exclamations (བཅོམ་ལྡན་འདས་ངོ་མཚར་ / བདེ་བར་གཤེགས་པ་ངོ་མཚར་); Kumārajīva has a single 希有世尊 and the Sanskrit a single *āścaryaṃ bhagavan, paramāścaryaṃ sugata* sentence. So the Chinese and Sanskrit blocks ^14 and ^183 each transclude both root segments — splitting them would invent an alignment.

## Still open

1. **`category_id`** — empty in all 20 files; the WeBuddhist category must be chosen before upload.
2. **Sanskrit pairing drift** (`sa-vajracchedika.md`, `alignment_status: needs-review`). From Tibetan row 229 the Sanskrit column sits one row behind (T230 ཐེག་པ་མཆོག ↔ S229 अग्रयान), later two (T372 ↔ S374, T428 ↔ S429). Reproduced as made. Six Sanskrit rows with no Tibetan row (216, 311, 376, 379, 420, 431) are kept with the preceding block and flagged.
3. **註解 Tsadrel rows 102, 104, 106** have the root on the lemma row instead of the explanation row; the typed references (which the files use) are unaffected.
4. **Contributors without ids** — the linter skips names with no `[bdrc:…]`/`[op:…]`: all Chinese authors/translators, the Buddha.
5. **Licences** — `unknown` for 白話, Sanskrit, and the 20th-century works (太虛, 倓虛, 星雲, 聖嚴). Check before publishing.
6. **Annex** — registered ids, the flat `^N` rule and the `Annotations/` folder in `4-SYSTEM/Guidelines/vault-annex.md`; please review.

## Publishing

All 20 files lint and parse into text, edition, TOC and alignment payloads. `translation-upload`, however, only accepts translations that cover every root segment one-for-one — a machine-translation assumption. Every human alignment here is partial (e.g. root ^1–^3 have no Chinese) and some are one-to-two (^14+^15), and the commentaries have no upload path at all. Publishing them needs an upload mode for human alignments; nothing was uploaded.

## Not ingested (raw files kept in `0-INBOX/raw-data/`)

| Raw item | Why |
|---|---|
| 5 English translations (`D1…/Root texts in English/`) | Unsegmented and unaligned; three are PDF/web extractions with page headers or site chrome (one truncated at ch. 12); modern copyrighted translations. Need cleanup, segmentation and a rights decision. |
| R3452D71B (bsdus don), R76E83977 (ཕན་ཡོན།), `Sanskrit.docx` (Sarnath 1997 edition) | Raw OCR with page breaks and junk — run `tibetan-ocr-quality` / `clean-raw-text` / `format-commentary` first. |
| R0FCDD06D (clean ཕན་ཡོན། text) | Filed under the Chone commentary's ID but is a different text — needs an ID decision. |
| `H_Root_text/…Tibetan - Chinese.docx` (348 rows), `B_Clean_Text` root | Older states of the Tibetan root; no partner file. Superseded by the Tsadel (Tenzin Tsering's corrections). |
| `RF161D626 … Root text Tsadrel.docx` | Its commentary partner is missing from the Drive (404); the Kamalaśīla alignment comes from D4's numbers. Listed under `raw_sources`. |
| `other/Untitled document.docx` | Same text as the numbered root; its 251 dark-red lines have no known meaning. |
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
