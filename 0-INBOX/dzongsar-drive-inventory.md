---
title: "Dzongsar Drive export — Diamond Sūtra"
status: draft
source_description: "Index of the Google Drive export (the Dzongsar tracking sheet and the Docs/Sheets it links) copied into 0-INBOX/raw-data/dzongsar-drive/. Scratch — not a source, never cited."
---

# Dzongsar Drive export — Diamond Sūtra

**From:** `Dzongsar_corpus.zip`, `Dzongsar_missing_diamond.zip` in ~/Downloads (exported from Google Drive on 2026-10-02 with the Claude in Chrome extension). Copied 2026-10-02; checksums are in `raw-data/dzongsar-drive/manifest.json`.

**What's here:** the `01_རྡོ་རྗེ་གཅོད་པ།` section of the tracking sheet. That is 233 files: metadata sheets, clean texts, TOCs, segmentations, and root-text and commentary alignment docs. The folder paths are exactly as they were inside the zips. Three files are shared by all texts and copied whole: `Dzongsar_sheet.csv`, `links_manifest.csv` (which says what was downloaded from each sheet cell), and `Tibetan_Catalogue_Seg-Align_full_workbook.xlsx` (the master catalogue, with its authors and segmentation-guideline tabs).

## Sheet rows

Column letters are the sheet's columns. A Metadata · B Clean text · C TOC · D Sentence segmentation · E Verse segmentation · F Citation · H Root text (alignment) · I Commentary / other language (alignment). Files sit under `Dzongsar_corpus/Dzongsar/01_རྡོ་རྗེ་གཅོད་པ།/<column folder>/`, and each file name starts with the row's ID.

| Row | ID | Title | Author | Kind | Downloaded | Missing | Sheet notes |
|---|---|---|---|---|---|---|---|
| 7 | M42AE7A72 | རྡོ་རྗེ་གཅོད་པ། | སྟོན་པ་བཅོམ་ལྡན་འདས། | རྩ་བ། Sanskrit Tsawa Align · Sanskrit Alignments | A, H, I |  |  |
| 8 | M42AE7A72 | རྡོ་རྗེ་གཅོད་པ། | སྟོན་པ་བཅོམ་ལྡན་འདས། | རྩ་བ། Chinese Tsawa Align | H, I |  |  |
| 9 | M42AE7A72 | རྡོ་རྗེ་གཅོད་པ། | སྟོན་པ་བཅོམ་ལྡན་འདས། | རྩ་བ། · Tsawa | B, G | A ✗ failed |  |
| 10 | RF67A9A4E | རྡོ་རྗེ་གཅོད་པའི་དོན་བདུན་གྱི་རྒྱ་ཆེར་འགྲེལ་པ། | སློབ་དཔོན་དབྱིག་གཉེན། | འགྲེལ་བ། {ཡི་གེ} | A, B, C | H ✗ failed; I ✗ failed |  |
| 11 | R4B9A8FB5 | རྡོ་རྗེ་གཅོད་བའི་འགྲེལ་བ།_ཅོ་ནེ། | ཅོ་ནེ་གྲགས་པ་བཤད་སྒྲུབ། | འགྲེལ་བ། {ཡི་གེ} | A, B, C | H ✗ failed; I ✗ failed |  |
| 12 | RF161D626 | རྡོ་རྗེ་གཅོད་པའི་རྒྱ་ཆེར་འགྲེལ་པ། | ཀ་མ་ལ་ཤཱི་ལ། | འགྲེལ་བ། {ཡི་གེ} | A, B, C, H | I ✗ failed |  |
| 13 | R3452D71B |  |  |  | I |  |  |
| 14 | R76E83977 |  |  |  | I |  |  |
| 16 | MFF4994FD |  |  | རྩ་བ། | A |  |  |
| 17 | R434373A0 |  | 釋迦佛 | འགྲེལ་བ། {ཡི་གེ} | A, H, I |  |  |
| 18 | R2A8AD21D |  | 天親/Vasubandhu/སློབ་དཔོན་དབྱིག་གཉེན། | འགྲེལ་བ། {ཡི་གེ} | A, H, I |  |  |
| 19 | RAF408FDA |  | 唐 慧能說 | འགྲེལ་བ། {ཡི་གེ} | — | A ✗ failed; H ✗ failed; I ✗ failed |  |
| 20 | R92439761 |  | 唐 窺基撰 | འགྲེལ་བ། {ཡི་གེ} | A, H, I |  |  |
| 21 | R96396549 |  | 金剛般若波羅蜜經註解 |  | A, H, I |  |  |
| 22 |  |  | 太虛大師 |  | — |  |  |

## Failed downloads

These links in the sheet could not be exported on the first pass. "Second pass" shows the result of the follow-up download (see below).

| Row | Column | Label | Link | Second pass |
|---|---|---|---|---|
| 9 | A (Metadata) | M42AE7A72 རྡོ་རྗེ་གཅོད་པ། Metadata.xlsx | [open](https://docs.google.com/spreadsheets/d/1qfweXue782RcawYpHym51FDFq3amj7zB/edit) | ✗ not-found |
| 10 | H (Root text (aligned)) | RF67A9A4E རྡོ་རྗེ་གཅོད་པ་རྩ་བ། - Root text Tsadrel | [open](https://docs.google.com/document/d/1YbH1M2SuojxzlhooOOLzt_wAG6w7-fR8X7_Xyx9HugA/edit) | ✗ not-found |
| 10 | I (Commentary / other language (aligned)) | RF67A9A4E རྡོ་རྗེ་གཅོད་པའི་དོན་བདུན་གྱི་རྒྱ་ཆེར་འགྲེལ་པ། - Tsadrel | [open](https://docs.google.com/document/d/1gWYustxDsJLMAdjbeXqyH5jHnR08eQAF3Fvhm61CtTU/edit) | ✗ not-found |
| 11 | H (Root text (aligned)) | R4B9A8FB5 རྡོ་རྗེ་གཅོད་པ་རྩ་བ། - Root text Tsadrel | [open](https://docs.google.com/document/d/1Jr9PWeaval71bIHOA3ts_lWBRQ0eN3SdoF2vqVd7Vus/edit) | ✗ not-found |
| 11 | I (Commentary / other language (aligned)) | R4B9A8FB5 རྡོ་རྗེ་གཅོད་བའི་འགྲེལ་བ།_ཅོ་ནེ།  - Tsadrel | [open](https://docs.google.com/document/d/1wHeHwLEAbcCHQq62p7fu1igbY1TwZzne9ZrMwT2GOSg/edit) | ✗ not-found |
| 12 | I (Commentary / other language (aligned)) | RF161D626 རྡོ་རྗེ་གཅོད་པའི་རྒྱ་ཆེར་འགྲེལ་པ། - Tsadrel | [open](https://docs.google.com/document/d/19w_fbZQvB0_0svsJiVRnZ1Lwmog4rG9Dzp7s51YqYtg/edit) | ✗ not-found |
| 19 | A (Metadata) | RAF408FDA 金剛般若經贊述- Metadata.xlsx.xlsx | [open](https://docs.google.com/spreadsheets/d/1L27Q3j-1DIyoonB_9Wd5kfQimwxkz2u3/edit) | ✗ not-found |
| 19 | H (Root text (aligned)) | RAF408FDA 金剛波羅蜜經 - Root text Tsadrel | [open](https://docs.google.com/document/d/1Dsi3ZX2ZgHHFMlqNLPwfBbrkTThDaIgRJwxgDrSHVjg/edit) | ✗ not-found |
| 19 | I (Commentary / other language (aligned)) | RAF408FDA 金剛般若經贊述   - Commentary Tsadrel Alignment | [open](https://docs.google.com/document/d/1H7FB-eJLSb1350Z603Z5qJXFndB-KXF_xcCy0wCO92E/edit) | ✗ not-found |

## External links in the sheet

- row 22: https://cbetaonline.dila.edu.tw/mulu/TX

## Second pass: `Dzongsar_missing_diamond.zip`

The first two zips skipped or failed some links. The Chrome extension then fetched every link the sheet lists for this text that was still missing, including the Tibetan, Chinese and General-list tabs and everything inside linked folders. The result is in `raw-data/dzongsar-drive/Dzongsar_missing_diamond/`. Each top-level name starts with its number in the request: A = linked on the Dzongsar tab but never crawled, B = failed on the first pass, C = uploaded files skipped in the commentary folders, D = linked only from the other tabs.

- **Downloaded:** 196 files (A: 5, D: 191).
- **Renamed:** 18 paths. A name over 200 bytes was shortened at a tsheg, keeping its ID and extension, and extension-less files got one. Some nested Tibetan folder names had pushed full paths past macOS's 1024-byte limit. `path-renames.json` maps each original path to its new one; `missing_manifest.csv` still uses the original paths.
- **Overlap:** many items, especially a text's main folder, contain copies of files already in the first two zips. Nothing has been de-duplicated.

Still unavailable (13 distinct links). Reasons: Drive file page HTTP 404 in every signed-in account (9); Drive shortcut (4).

| # | Item | Status | Link |
|---|---|---|---|
| B1 | M42AE7A72 རྡོ་རྗེ་གཅོད་པ། Metadata.xlsx | not-found | [open](https://docs.google.com/spreadsheets/d/1qfweXue782RcawYpHym51FDFq3amj7zB/edit) |
| B2 | RF67A9A4E རྡོ་རྗེ་གཅོད་པ་རྩ་བ། - Root text Tsadrel | not-found | [open](https://docs.google.com/document/d/1YbH1M2SuojxzlhooOOLzt_wAG6w7-fR8X7_Xyx9HugA/edit) |
| B3 | RF67A9A4E རྡོ་རྗེ་གཅོད་པའི་དོན་བདུན་གྱི་རྒྱ་ཆེར་འགྲེལ་པ། - Tsadrel | not-found | [open](https://docs.google.com/document/d/1gWYustxDsJLMAdjbeXqyH5jHnR08eQAF3Fvhm61CtTU/edit) |
| B4 | R4B9A8FB5 རྡོ་རྗེ་གཅོད་པ་རྩ་བ། - Root text Tsadrel | not-found | [open](https://docs.google.com/document/d/1Jr9PWeaval71bIHOA3ts_lWBRQ0eN3SdoF2vqVd7Vus/edit) |
| B5 | R4B9A8FB5 རྡོ་རྗེ་གཅོད་བའི་འགྲེལ་བ།_ཅོ་ནེ། - Tsadrel | not-found | [open](https://docs.google.com/document/d/1wHeHwLEAbcCHQq62p7fu1igbY1TwZzne9ZrMwT2GOSg/edit) |
| B6 | RF161D626 རྡོ་རྗེ་གཅོད་པའི་རྒྱ་ཆེར་འགྲེལ་པ། - Tsadrel | not-found | [open](https://docs.google.com/document/d/19w_fbZQvB0_0svsJiVRnZ1Lwmog4rG9Dzp7s51YqYtg/edit) |
| B7 | RAF408FDA 金剛般若經贊述- Metadata.xlsx.xlsx | not-found | [open](https://docs.google.com/spreadsheets/d/1L27Q3j-1DIyoonB_9Wd5kfQimwxkz2u3/edit) |
| B8 | RAF408FDA 金剛波羅蜜經 - Root text Tsadrel | not-found | [open](https://docs.google.com/document/d/1Dsi3ZX2ZgHHFMlqNLPwfBbrkTThDaIgRJwxgDrSHVjg/edit) |
| B9 | RAF408FDA 金剛般若經贊述 - Commentary Tsadrel Alignment | not-found | [open](https://docs.google.com/document/d/1H7FB-eJLSb1350Z603Z5qJXFndB-KXF_xcCy0wCO92E/edit) |
| D1 | E4BF16EE འཕགས་པ་ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པ་རྡོ་རྗེ་གཅོད་པའི་རྒྱ་ཆེར་འགྲེལ་པ།-1 | failed | [open](https://drive.google.com/file/d/1nVcoYM__pNtJ9aKMb5cziWBqHg0RahSA/view) |
| D1 | E4BF16EE འཕགས་པ་ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པ་རྡོ་རྗེ་གཅོད་པའི་རྒྱ་ཆེར་འགྲེལ་པ།-2 | failed | [open](https://drive.google.com/file/d/1eUCznekItOjgTcCYH1CFx52ONE_TCUjq/view) |
| D1 | E4BF16EE འཕགས་པ་ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པ་རྡོ་རྗེ་གཅོད་པའི་རྒྱ་ཆེར་འགྲེལ་པ།-3 | failed | [open](https://drive.google.com/file/d/17dfGS0di99PWMYTdEnUramMYGn0XqaCG/view) |
| D1 | E4BF16EE འཕགས་པ་ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པ་རྡོ་རྗེ་གཅོད་པའི་རྒྱ་ཆེར་འགྲེལ་པ།-4 | failed | [open](https://drive.google.com/file/d/1rbjhDQ-QZEA7kvKB3HbldvCjjojK5C1V/view) |

## Next step

None of this has been converted. The .docx alignment docs pair root-text segments with commentary or translation segments; their structure still needs a look before choosing a converter.
