---
title: A/B test — zh-academic prompt (current vs Chinese-only draft)
status: planned — not run, waiting for approval
date: 2026-10-23
---

# A/B test plan — zh-academic prompt

## Question

Does the new Chinese-only prompt (now `3-TRANSFORMATIONS/Translations/zh-academic/requirements.md`, built from `../zh-academic-prompt-draft.md`) give better first-pass Chinese academic translations than the current prompt, without losing accuracy?

## The two arms

| | A — current | B — new |
|---|---|---|
| System instruction | `requirements-v1.md` in this folder (the track's requirements before 2026-10-24) + English `FORMAT`, ~1,150 chars | `zh-academic/requirements.md` without its frontmatter (Chinese only, ~5,000 chars) |
| User-message header | English task line + English field notes, as in `gm_variant_translate.py` | 「請把下列《金剛經》藏文段落譯成中文學術版。各欄位的用法見系統指示。只回傳 JSON。」 |
| Everything else | identical | identical |

Identical for both: model (Gemini 3.1 Pro, the pipeline default), segments, batches (6 segments, ≤1,800 Tibetan chars), context (Tibetan, Sanskrit, 3 commentaries, `english_academic`, `kumarajiva`, `zero_shot`), and the locked terms (including the new T279/T280). No term retry and no fact-check feedback: the test measures first-pass output only.

## Segments (56)

Listed in `../ab-test-segments.json`.

- **40 from the existing blind-eval sample** (`kf-pilot/blind-eval/sample-zh-01/02.json`), spread evenly over the sutra, so results are comparable with the pilot report.
- **17 targeted** (one overlaps), because the blind sample barely touches the new rules:
  - Paradox formula pairs (A part + C part): 6-49/6-50, 7-37/7-38, 9-23/9-24, 10-43/10-44, 10-52/10-53, 12-22/12-23
  - Paradox variant without "the Tathāgata taught": 8-105/8-106
  - 9-11 (the 法眼 / 教法 failure)
  - Two headings: 7-0, 9-0

Coverage: 7 "why is that?" segments, 9+ vocatives, 9 "therefore called" segments, 2 headings.

## Measures

| # | Measure | Who | Cost |
|---|---|---|---|
| 1 | Automatic: locked-term compliance, 這是為什麼呢？ and 須菩提！ use, paradox frame 所以才稱為, classical-particle rate, Latin/digits, empty segments, leaks (commentary names, sample words 賢友/尊者, ellipsis) | `ab_test.py --eval` | free |
| 2 | Accuracy: the pilot's Claude Sonnet fact-check on both arms (Tibetan, Sanskrit, commentaries) — major/minor error counts | Claude agents | ~$1.40 |
| 3 | Preference: blind pairwise judge, each pair judged twice with A/B swapped (`kf-pilot/factcheck/pairwise_judge.py`) | Gemini | ~$1.25 |

Measures 2 and 3 keep the pilot's rule: Gemini translates, Claude checks; the Gemini judge sees both texts blind.

**Baseline of the current output on these 56 segments** (already in the track, after all fix rounds; for reference only, not one of the arms): 19 locked-term misses (7 "why", 9 vocative, 3 other), 0/9 paradox C parts with 所以才稱為, 31.4 classical markers per 1,000 characters.

## Decision rule

B replaces A if all three hold:

1. **No accuracy loss:** B has no more major errors than A in the Claude fact-check.
2. **Preferred:** the blind judge prefers B (wins in both orders) on more segments than it prefers A.
3. **Rules followed:** B's formula compliance and paradox frame are clearly higher, and none of the leak checks fire.

If 1 fails, we fix the prompt before anything else. If 2 or 3 is mixed, we look at the segments together and adjust.

## Calls and cost

| Step | Gemini calls | Estimated cost |
|---|---|---|
| Arm A translation | 10 | $0.76 |
| Arm B translation | 10 | $0.84 |
| Pairwise judge (56 pairs × 2 orders, 8 per call) | 14 | $1.25 |
| Claude fact-check (112 segment checks) | — | $1.40 |
| **Total** | **34** | **≈ $4.30** |

Estimates use the ledger averages for zh-academic calls (6,523 input, 5,253 output + thinking tokens per call) and `4-SYSTEM/scripts/usage-ledger/prices.json` (Gemini 3.1 Pro $2 in / $12 out per 1M; Sonnet as in the pilot). B's longer system prompt adds ~3,800 input tokens per call.

**Optional:** a second run of both arms to see run-to-run variation: +20 translation calls, +$1.60, and +$1.25 to judge → **≈ +$2.90**.

For scale: the full zh pipeline cost $26.66 in the pilot.

## How to run (after approval)

```
python3 ab_test.py --arm A --run 1 --go
python3 ab_test.py --arm B --run 1 --go
python3 ab_test.py --eval --run 1
python3 ../../kf-pilot/factcheck/pairwise_judge.py pairs-run1.json --out judged-run1.json
```

Then the Claude fact-check on both arms. Without `--go`, `ab_test.py` only prints the batches and the cost estimate.

**Nothing in the zh-academic track changes.** Output goes to this folder; every call is logged in the usage ledger under step `ab-test-zh-prompt`.

## Open issues before running

- **API key.** `GEMINI_API_KEY` is not set in this Windows shell. The pilot ran Gemini scripts through `zsh -ic` on the Mac, where the key lives in `~/.zshrc`. Either run there or set the key here.
- ~~Termbase bug at 9-11~~ — fixed 2026-10-24 for Chinese only: a term whose every occurrence lies inside a longer locked term (ཆོས in ཆོས་ཀྱི་སྤྱན 法眼, སངས་རྒྱས in 正等覺者, འཇིག་རྟེན in 世界) is no longer locked (`nested_only()` in `gm_variant_translate.py`). English and Hindi locks are unchanged.
- ~~Paradox example sentence~~ — approved by the user, 2026-10-24.
