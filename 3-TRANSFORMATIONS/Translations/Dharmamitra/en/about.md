---
title: "Diamond Sūtra — DharmaMitra zero-shot (english, root)"
track_type: machine-baseline
target_language: english
lang_tag: en
generator: dharmamitra cat-translate v1
endpoint: https://dharmamitra.org/api-search/cat-translate/v1/translate
rails_used: none
termbase: none
status: draft
seeded: 2026-10-04
---

# Dharmamitra/en — about this track

A **machine baseline**, not a rails-governed translation track.

Every file here is raw output of DharmaMitra's public `cat-translate` endpoint, produced in small batches of adjacent block IDs by `4-SYSTEM/Skills/machine-translate/scripts/dm_translate.py` (Engine 2 of the `machine-translate` skill), then split back apart on segment markers so each block keeps its own record. Nothing in it passed through `2-RAILS/`: no verse-context package, no consolidated bilingual glossary, no per-track `termbase.md`, no human review. It therefore does **not** satisfy the Translation-track contract in [`../../../About Transformations.md`](../../../About%20Transformations.md) §3, and it is not eligible to be marked `status: complete` or to be cited by any other transformation. Layout and conventions follow `heart-sutra-rails/3-TRANSFORMATIONS/Translations/Dharmamitra/` (2026-10-04).

## Files

| Translation | Source | Title (machine) |
| --- | --- | --- |
| `bo-vajracchedika-en.md` | [`1-SOURCES/Translations/bo-vajracchedika.md`](1-SOURCES/Translations/bo-vajracchedika.md) | The Noble Mahāyāna Sūtra Entitled The Diamond-Cutter Perfection of Wisdom |

## What governs it

| File | Role |
| --- | --- |
| `style-<source stem>.md` | The `style_instruction` sent **verbatim** on every call for that source (`style.md` is the track default). |
| `heading-style.md` | The instruction for `--headings` (one call per section heading). Headings become the translation's table of contents on upload. |
| `context-header.md` | A work-neutral preamble prepended to every call's `context`; the per-text `Work: …` line is derived from the source's frontmatter. |
| `work/<stem>-en.jsonl` | Append-only ledger: one record per block / heading — the audit trail and the resume point. |
| `work/extra-fm-<stem>.json` | Frontmatter seeded on render: the machine-translated title, `category_id`, `license`, `source`, `edition_type`. |

## Regenerate or extend

```bash
python3 4-SYSTEM/Skills/machine-translate/scripts/dm_translate.py \
  --source "<source>" --lang "english" --lang-tag en --out "3-TRANSFORMATIONS/Translations/Dharmamitra/en" \
  --style-file "3-TRANSFORMATIONS/Translations/Dharmamitra/en/style-<stem>.md" \
  --context-header "3-TRANSFORMATIONS/Translations/Dharmamitra/en/context-header.md" \
  --extra-fm "3-TRANSFORMATIONS/Translations/Dharmamitra/en/work/extra-fm-<stem>.json"
```

Upload is a separate decision, made with the `translation-upload` skill.
