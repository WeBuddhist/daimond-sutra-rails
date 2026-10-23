---
title: Full run — Chinese academic translation with the v2 prompt
status: ready
date: 2026-10-24
for: the pipeline operator (Mac with GEMINI_API_KEY in ~/.zshrc)
---

# Full run — zh-academic with the v2 prompt

Regenerates the whole Chinese academic translation of the Diamond Sutra with the new Chinese prompt, then fact-checks and fixes it the same way as the pilot (Gemini translates, Claude checks; keep-best rule for minor fixes).

Run every command **from the vault root**. Gemini scripts go through `zsh -ic` so the key in `~/.zshrc` is loaded.

## What changed since the pilot (2026-10-24)

| Change | Where |
|---|---|
| New prompt, Chinese only (style sample, authority order, term rules, fixed formulas, output rules) | `3-TRANSFORMATIONS/Translations/zh-academic/requirements.md` (built from `0-INBOX/zh-prompt/zh-academic-prompt-draft.md` by `assemble.py`; the old version is `0-INBOX/zh-prompt/ab-test/requirements-v1.md`) |
| `--system <file>`: that file (minus frontmatter) is the whole system instruction; no English `FORMAT`; Chinese task line for zh academic | `0-INBOX/kf-pilot/translate/gm_variant_translate.py` |
| Two locked formulas, academic only: T279 ཅིའི་ཕྱིར་ཞེ་ན → 這是為什麼呢？ (31 segments), T280 vocative རབ་འབྱོར → 須菩提！ (140). Checked with their punctuation | `0-INBOX/kf-pilot/termbase/vajracchedika-zh/termbase.json`, `zh-academic/termbase.md` |
| zh only: a term that occurs only inside a longer locked term is no longer locked (ཆོས in 法眼, སངས་རྒྱས in 正等覺者, འཇིག་རྟེན in 世界). This removes the lock that produced 「教法眼」 at 9-11. English and Hindi locks are unchanged | `nested_only()` in `gm_variant_translate.py` |
| Helper to build the fix-request file from a fact-check run | `0-INBOX/zh-prompt/make_feedback.py` |

**Do not run the children's version yet.** Its prompt is being revised next; this guide will get a children's section when it is ready.

## Step 0 — Pull

```
git pull
```

## Step 1 — A/B test (gate)

Follow `0-INBOX/zh-prompt/ab-test/PLAN.md` ("How to run"): 34 Gemini calls, about $2.90 Gemini + $1.40 Claude.

Continue to step 2 only if the decision rule in PLAN.md holds (no more major errors in B, the blind judge prefers B, B follows the new rules). Otherwise stop and send the results to Jennifer.

## Step 2 — Archive the v1 academic output

Keeps the pilot's text and its checks, out of the way of the new run (the scripts only look at the top level of these folders).

```
mkdir -p 3-TRANSFORMATIONS/Translations/zh-academic/work/archive-v1 0-INBOX/kf-pilot/factcheck/archive-zh-academic-v1
git mv 3-TRANSFORMATIONS/Translations/zh-academic/work/bo-vajracchedika-zh.jsonl 3-TRANSFORMATIONS/Translations/zh-academic/work/termbase-compliance.json 3-TRANSFORMATIONS/Translations/zh-academic/work/archive-v1/
cp 3-TRANSFORMATIONS/Translations/zh-academic/bo-vajracchedika-zh.md 3-TRANSFORMATIONS/Translations/zh-academic/work/archive-v1/
git mv 0-INBOX/kf-pilot/factcheck/zh-academic-a1 0-INBOX/kf-pilot/factcheck/zh-academic-a2 0-INBOX/kf-pilot/factcheck/zh-academic-a3 0-INBOX/kf-pilot/factcheck/zh-academic-a4 0-INBOX/kf-pilot/factcheck/archive-zh-academic-v1/
git commit -m "zh-academic: archive v1 before the v2 run"
```

## Step 3 — Translate all 446 segments

```
zsh -ic 'python3 0-INBOX/kf-pilot/translate/gm_variant_translate.py --variant academic --lang zh --system 3-TRANSFORMATIONS/Translations/zh-academic/requirements.md'
```

75 batches, about $6.50. Resumable: rerun the same command after a failure. Missed locked terms get one automatic retry. At the end it renders `zh-academic/bo-vajracchedika-zh.md` and prints how many segments still miss a locked term (list in `work/termbase-compliance.json`).

## Step 4 — Claude fact-check, round 1

As in the pilot (STATE.md, step 5):

```
python3 0-INBOX/kf-pilot/factcheck/prep.py --variant academic --lang zh --attempt 1
```

Then run the Claude Sonnet agents over `0-INBOX/kf-pilot/factcheck/zh-academic-a1/batches/` with `0-INBOX/kf-pilot/factcheck/prompts/factcheck-agent-lang.md` (one agent per batch; outputs in `zh-academic-a1/agents/`), validate each output with `check.py <batch> <agent-out>`, and merge:

```
python3 0-INBOX/kf-pilot/factcheck/check.py --merge 0-INBOX/kf-pilot/factcheck/zh-academic-a1
```

About $5.40 of Claude for 432 segments.

## Step 5 — Fix and re-check

```
python3 0-INBOX/zh-prompt/make_feedback.py 0-INBOX/kf-pilot/factcheck/zh-academic-a1
zsh -ic 'python3 0-INBOX/kf-pilot/translate/gm_variant_translate.py --variant academic --lang zh --system 3-TRANSFORMATIONS/Translations/zh-academic/requirements.md --feedback 0-INBOX/kf-pilot/factcheck/zh-academic-a1/feedback-all.json --attempt 2'
python3 0-INBOX/kf-pilot/factcheck/prep.py --variant academic --lang zh --attempt 2 --only <the ids in feedback-all.json>
```

Run the agents on `zh-academic-a2`, then `check.py --merge` as in step 4. `--major-only` on `make_feedback.py` restricts the round to failing segments.

Then apply the pilot's rules (STATE.md, "Decisions" and "Resume here" 1):

- **Minor-only fixes — keep-best:** `improvement.py --pairs` → `pairwise_judge.py --revert-losses` (both in `0-INBOX/kf-pilot/factcheck/`). A minor fix stays when the blind judge prefers it or ties.
- **A re-check failure where attempt 1 passed:** restore attempt 1 (`call_id: revert`). Failed both times: one more retry with `--attempt 3`, re-check, then `review-flags.md`.

## Step 6 — Close

```
python3 0-INBOX/kf-pilot/factcheck/improvement.py
zsh -ic 'python3 0-INBOX/kf-pilot/translate/gm_variant_translate.py --variant academic --lang zh --render-only'
```

- `improvement.py` must list no `unchecked_current_text`: every segment's current text has been seen by a check (pilot lesson: a retry after the check once added a major error at 9-11).
- Leave `status: draft` in the translation's frontmatter; a specialist sets `complete`.
- Add a "zh-academic v2" line to `0-INBOX/kf-pilot/STATE.md`, commit and push.

## Cost (estimate)

| Step | Cost |
|---|---|
| A/B test | ≈ $4.30 |
| Translation, 75 calls | ≈ $6.50 |
| Fact-check round 1 (Claude) | ≈ $5.40 |
| Fixes and re-check (≈ 60 segments, as in the pilot) | ≈ $2.50 |
| **Total** | **≈ $19** |

Estimates from the usage ledger (pilot averages). Every call is logged there.
