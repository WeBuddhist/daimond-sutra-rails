---
title: "Diamond Sūtra — DharmaMitra zero-shot (modern chinese, commentaries)"
track_type: machine-baseline
target_language: modern chinese
lang_tag: zh
generator: dharmamitra cat-translate v1
endpoint: https://dharmamitra.org/api-search/cat-translate/v1/translate
rails_used: none
termbase: none
status: draft
seeded: 2026-10-04
---

# Dharmamitra/zh-commentaries — about this track

A **machine baseline**, not a rails-governed translation track.

Every file here is raw output of DharmaMitra's public `cat-translate` endpoint, produced in small batches of adjacent block IDs by `4-SYSTEM/Skills/machine-translate/scripts/dm_translate.py` (Engine 2 of the `machine-translate` skill), then split back apart on segment markers so each block keeps its own record. Nothing in it passed through `2-RAILS/`: no verse-context package, no consolidated bilingual glossary, no per-track `termbase.md`, no human review. It therefore does **not** satisfy the Translation-track contract in [`../../../About Transformations.md`](../../../About%20Transformations.md) §3, and it is not eligible to be marked `status: complete` or to be cited by any other transformation. Layout and conventions follow `heart-sutra-rails/3-TRANSFORMATIONS/Translations/Dharmamitra/` (2026-10-04).

## Files

| Translation | Source | Title (machine) |
| --- | --- | --- |
| `bo-vasubandhu-saptartha-tika-zh.md` | [`1-SOURCES/Commentaries/bo-vasubandhu-saptartha-tika.md`](1-SOURCES/Commentaries/bo-vasubandhu-saptartha-tika.md) | 世親菩薩造聖般若波羅蜜多金剛經七義廣釋 |
| `bo-kamalasila-tika-zh.md` | [`1-SOURCES/Commentaries/bo-kamalasila-tika.md`](1-SOURCES/Commentaries/bo-kamalasila-tika.md) | 蓮華戒所著聖般若波羅蜜多金剛能斷廣釋 |
| `bo-chone-drakpa-shedrub-zh.md` | [`1-SOURCES/Commentaries/bo-chone-drakpa-shedrub.md`](1-SOURCES/Commentaries/bo-chone-drakpa-shedrub.md) | 卓尼·扎巴謝珠所著金剛經釋：顯明深義之解脫善道日光 |

## What governs it

| File | Role |
| --- | --- |
| `style-<source stem>.md` | The `style_instruction` sent **verbatim** on every call for that source (`style.md` is the track default). |
| `heading-style.md` | The instruction for `--headings` (one call per section heading). Headings become the translation's table of contents on upload. |
| `context-header.md` | A work-neutral preamble prepended to every call's `context`; the per-text `Work: …` line is derived from the source's frontmatter. |
| `work/<stem>-zh.jsonl` | Append-only ledger: one record per block / heading — the audit trail and the resume point. |
| `work/extra-fm-<stem>.json` | Frontmatter seeded on render: the machine-translated title, `category_id`, `license`, `source`, `edition_type`. |

## Regenerate or extend

```bash
python3 4-SYSTEM/Skills/machine-translate/scripts/dm_translate.py \
  --source "<source>" --lang "modern chinese" --lang-tag zh --out "3-TRANSFORMATIONS/Translations/Dharmamitra/zh-commentaries" \
  --style-file "3-TRANSFORMATIONS/Translations/Dharmamitra/zh-commentaries/style-<stem>.md" \
  --context-header "3-TRANSFORMATIONS/Translations/Dharmamitra/zh-commentaries/context-header.md" \
  --extra-fm "3-TRANSFORMATIONS/Translations/Dharmamitra/zh-commentaries/work/extra-fm-<stem>.json"
```

Upload is a separate decision, made with the `translation-upload` skill.
