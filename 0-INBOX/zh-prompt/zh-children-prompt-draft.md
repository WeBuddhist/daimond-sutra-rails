---
title: zh-children Gemini prompt — working draft
status: draft
target_model: Gemini 3.1 Pro
builds: 3-TRANSFORMATIONS/Translations/zh-children/requirements.md (Chinese parts only, once complete)
---

# zh-children 翻譯提示詞（草稿）

Same layout as the academic draft: each section in Chinese (what Gemini receives), then an English mirror and design notes. Sections 一–五 to be drafted.

## Decisions so far

| Date | Decision |
|---|---|
| 2026-10-24 | Same structure as the academic prompt: Chinese only, sections 一 task and role, 二 references, 三 register and style (with a sample), 四 term rules, 五 output format. |
| 2026-10-24 | Paradox frame, simpler wording: 「大家說的X，……其實不是X，所以才叫做X。」 (exact wording to be drafted and approved; it must keep the paradox open and map to the same three Tibetan parts as the academic rule 9). |
| 2026-10-24 | The user will provide a style sample for the children's register. |
| 2026-10-24 | The writer also sees the approved English children's version (`en-children`) as a reference, besides the Tibetan and the Chinese academic version. Needs a small script change (`english_children` field on the children's path). |
| open | Vocative for Subhūti and the wording of "why is that?". |

## Findings on the current zh-children output (v1)

- Sentence length: median 11 characters, but 39% of sentences are over 15 characters and 19% over 25, although the rule says "mostly no more than 15".
- Vocative mixed: 須菩提， 93 times, 須菩提！ 56 times.
- "Why is that?": 為什麼呢？ 46, 這是為什麼呢？ 3, 那是為什麼呢？ 3.
- Paradox C part uses 所以才叫 (21), but some segments are clumsy or add words: 7-38 「因此，這才被稱為佛的國土裡的佛國的佈置。」; 7-37 adds 「說到佛的國土，」.
- Variant characters for the same word: 佈置 / 布置.
- 9-11 「教導的眼睛」: the same nested-lock error as the academic 「教法眼」. Fixed by `nested_only()` (2026-10-24), which applies to both Chinese tracks.
- 12-22 「如來說這就是沒有想法」: "no perception" turned into "no ideas"; doctrinally risky, to cover in the term rules.
