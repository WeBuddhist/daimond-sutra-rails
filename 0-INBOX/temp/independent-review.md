# Independent review — Diamond Sūtra source rebuild (2026-10-04)

Read-only review of:

- `1-SOURCES/Text/sa-vajracchedika.md`
- `1-SOURCES/Translations/bo-vajracchedika.md`
- `1-SOURCES/Commentaries/bo-vasubandhu-saptartha-tika.md`, `bo-chone-drakpa-shedrub.md`, `bo-kamalasila-tika.md`
- their sidecars in `1-SOURCES/Annotations/`

Method: I parsed every file into blocks, each with the transclusions that stand directly before it. I checked ids, headings and transclusion targets with scripts. For the alignments I read samples: every root section boundary, at least 8 sections per commentary, about 16 blocks per commentary, and every block a lexical-overlap scan flagged. Raw Wikisource `pages.json` was used to confirm where the commentary headings stand. Sidecar `targets` and `text` match the files for all four Tibetan files (0 mismatches).

---

## 1. Section starts across languages (sa ↔ bo)

**No problems found.** For all 13 headings, the first transclusion after the Tibetan `^N-0` is Sanskrit `^N-1`. No Tibetan block transcludes a Sanskrit block from another section. I read the text at every boundary, and each matches (e.g. `^8-0` लक्षणानुव्यञ्जनानि ↔ མཚན་དང་དཔེ་བྱད།, both opening on the 32-marks question).

Notes, not errors:

- **`^5-0` and `^10-0` (row split, D7).** The Tibetan `དེ་ཅིའི་ཕྱིར་ཞེ་ན།` stays above the heading (bo `^4-10`, `^9-25`, with no transclusion). The matching Sanskrit `तत्कस्य हेतोः ?` opens sa `^5-1` and `^10-1`. This is the D7 split registered in the annex.
- **One backward jump, `^12-26` and `^12-27`.** bo `^12-26` transcludes sa `^12-29`, and bo `^12-27` transcludes sa `^12-28`. The cause is a real recension difference: the Sanskrit has `तथा प्रकाशयेत्…` after the verse, and the Tibetan has it before. This is correct.
- **Sanskrit with no Tibetan counterpart:** sa `^8-42`, `^9-18`, `^10-10`, `^10-58`, `^10-61`, `^12-18`, `^12-27` (e.g. `^12-27` तद्यथाकाशे-). This looks like content the Tibetan lacks, not a dropped transclusion.
- **Tibetan with no Sanskrit:** bo `^0-2`, `^0-3`, `^4-10`, `^7-15`, `^7-16`, `^8-55`, `^8-101`, `^9-25`, `^13-4`–`^13-6`. These are Tibetan pluses (dhāraṇī, Sanskrit and Tibetan title lines, extra sakṛdāgāmin lines).

## 2. Id sequence

**No problems with ids.** In sa and bo, headings are `^N-0` and body ids run `^N-1…` with no gaps or duplicates. In the commentaries, body ids are `^<top>-<n>` counted through deeper headings, as registered in the annex. Heading paths, ordinals and markdown levels are consistent, including the bolded level-7 `######` headings in Kamalaśīla. `^0` on the `#` title is permitted by the annex and `annotation-conventions.md`.

**One defect, sa `^8-99` (file line ~587):** the block contains a stray `000.` and an embedded line break:

```
तत्कस्य हेतोः ? तथागत इति सुभूते भूततथताया एतदधिवचनम्।
000. तथागत इति सुभूते अनुत्पादधर्मताया एतदधिवचनम्। … ^8-99
```

`000\.` is the source doc's marker for an unnumbered continuation row (raw row 273/274). The sidecar `text` has the `000.` too, but no newline. The marker should be removed and the block joined into one line.

## 3. Commentary alignment

**Section level.** Where titles match, the commentary sections transclude the right root ranges. Vasubandhu and Kamalaśīla, aligned independently and both following Asaṅga's 18 points, give almost the same ranges for each point.

- **Chone:** ཞུགས་གནས་བརྒྱད་ 7-1–7-81, མཚན་དང་དཔེ་བྱད་ 8-1–8-5, སྤྱན་ལྔ་ 9-1–9-24, སེམས་སེམས་བྱུང་ 9-25–10-63, ཆོས་སྐུ་ 10-64–11-17, རྡུལ་ཕྲ་རབ་ 12-1–12-6, མཇུག་ 13-1/2/4/5. All are correct.
- **Commentary heading positions.** I checked these against the raw `<includeonly>` heading markup for Vasubandhu 2.2, 2.3, 2.3.1, 2.3.2, 2.3.15, 2.3.17, 2.3.18 and 2.3.18.1. All are placed exactly as in the source.
- **Mismatches that come from the source.** A few title mismatches are caused by where Wikisource puts the headings, not by the alignment. Examples: Vasubandhu's comment on root 4-1–4-4 sits under 2.1 (lineage), and root 8-111–8-114 sits under 2.3.18.1 (field purity).

**Block level.** I read about 16 blocks per commentary. Almost all are correct.

Clear or probable misalignments:

1. **Kamalaśīla `^3-97`: missing transclusion of root `^7-39`–`^7-42`.** The block explicitly comments on དེ་ལྟ་བས་ན་… མི་གནས་པར་སེམས་བསྐྱེད་པར་བྱའོ (the "produce an unabiding mind" passage, `7-39`–`7-42`) but has no transclusion. These four root blocks are the only ones in sections 1–12 that Kamalaśīla never transcludes. Both other commentaries do transclude them.
2. **Kamalaśīla `^3-241` (weak): block straddles two root sections.** The first half finishes the comment on root `^11-17` (…ཡང་དག་པར་རྫོགས་པའི་སངས་རྒྱས་ཞེས་བྱའོ). Only the end introduces `12-1`, yet the block transcludes `12-1`–`12-3`. Splitting the block, or moving `12-1`–`12-3` to `^3-242` (which glosses `12-1` directly), would be cleaner.
3. **Vasubandhu `^2-155` → root `^13-3` (weak).** The block is the commentary's own Sanskrit verses and colophon, not a comment on the sūtra's colophon.
4. **Chone `^2-106` → root `^8-100` + `^8-101` (minor).** The comment covers only `8-100`. Root `^8-101` is an odd line that is also in the raw Dzongsar doc.

Minor imprecisions, acceptable:

- Kamalaśīla `^3-103` transcludes `7-59` but begins with a summary of `7-60`–`7-63`.
- Kamalaśīla `^3-114` transcludes `7-76`/`7-77`, but the gloss is on `7-74`/`7-75`.
- Title-to-title pairings in the `^0-*` blocks of Vasubandhu and Kamalaśīla.

All three commentaries are already marked `alignment_status: needs-review`.

## 4. Stray markup and odd headings

**No markup leaks found.** I scanned every body block for `<`, `{{`, `}}`, `[[` or `]]` outside the transclusion lines, URLs, ASCII or Tibetan page numbers, empty blocks and leftover granular headings. None of the Wikisource `<section>`, `<includeonly>` or `<center>` markup leaked into the files.

Source-faithful oddities, for awareness only:

- **Space after tsheg.** Many blocks have a space after a tsheg where the source page broke a line (e.g. `བླ་ན་མེད་ པ་`). Counts: Chone 81 instances in 43 blocks, Kamalaśīla 14, Vasubandhu 7. The same spaces are in the Wikisource text.
- **Chone `^2-131`** has the edition's correction mark `(ཞེས){ཅེས}`. Its `(A,B)` variant readings (`^2-9`, `^2-12`, `^2-14`, `^2-65`, `^2-96`) are also from the source.
- **Typos in source headings:** Kamalaśīla `^3-4-2-7-0` སངས་རྒྱས་ཀྱ་ས, and `^3-4-2-5-5-0` བསྟན་བཅོས་་ (double tsheg).
- **Double space** in bo `^3-7`.
- The only real body defect is the `000.` and line break in sa `^8-99` (see §2).

---

## Verdict

The build is structurally sound. Ids, heading paths, cross-language section starts, sidecars and transclusion targets are all correct. One mechanical defect needs fixing: sa `^8-99` (`000.` and line break). One clear alignment gap needs fixing: Kamalaśīla `^3-97` should transclude root `^7-39`–`^7-42`. Kamalaśīla `^3-241` and Vasubandhu `^2-155` deserve a second look. The rest of the commentary alignment held up on reading.
