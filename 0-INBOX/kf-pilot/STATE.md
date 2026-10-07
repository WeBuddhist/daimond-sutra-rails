# KF pilot — Diamond Sutra pipeline state

Working area for the KF AI-translation pilot report (Diamond Sutra first, then Ratnaguṇa and BCA).
Scripts here are drafts; they become registered skills (via `create-skill`) once the whole flow works.

## Decisions (user, 2026-10-07)
- Gemini translates; Claude checks. Anything Claude produces is reviewed by Gemini, and vice versa. No human reviewer: the cross-model review approves.
- Agents orchestrate and run in parallel; scripts where needed (all Gemini calls are scripts).
- Versions: academic + children's (new); zero-shot (DharmaMitra/Gemini, exists) and commentary translations (exist). Word-by-word deferred.
- Build in this vault; sync the finished skills to the other vaults afterwards.

## Pipeline status (English)
| Step | Status | Where |
|---|---|---|
| 0 Setup: venv, usage ledger, Gemini key | done | `KF-project/.venv`; `4-SYSTEM/scripts/usage-ledger/`; key in ~/.zshrc (run Gemini scripts via `zsh -ic`) |
| 1 Term extraction (Claude, 13 agents) + Gemini review | done — 278 terms | `term-extract/vajracchedika-en/term-list.md` |
| 2 Termbase (style sheet + 6 agents) + Gemini review | done — draft | `termbase/vajracchedika-en/termbase-{academic,children}.md`, `style-sheet.md`, `review.json` |
| 3 Segment context (Tibetan + Sanskrit + 3 commentaries) | built | `context/segment_context.py` |
| 4 Academic translation (Gemini 3.1 Pro, termbase-locked, Sanskrit + 3 commentaries) | done — 446/446, 1,561/1,564 locked-term uses | `translate/gm_variant_translate.py` → `3-TRANSFORMATIONS/Translations/en-academic/` |
| 5 Fact-check (Claude Sonnet, 18 agents) + regenerate | done — 431/432 pass first time; 8-6 regenerated and passes; 32 minor issues open | `factcheck/academic-a1/verdicts.json`; calibration 17/18 planted errors caught, 0 false alarms (`factcheck/calibration/`) |
| 5b Academic minor fixes | done — 32 regenerated; re-check: 30 pass, 2 regressions reverted to attempt 1 (keep-best rule) | `factcheck/academic-a2/` |
| 6 Children's version (Gemini, from academic) + fact-check (Claude, 11 agents) | done — 430/432 pass first time; 4-1 fixed; 12-24 flagged after 2 retries; 31 minor open | `3-TRANSFORMATIONS/Translations/en-children/`, `factcheck/children-a1/`, `review-flags.md` |
| 7 Cost/quality report (Diamond, en) | draft done — $30.04 pipeline, $89.24 all work | `reports/vajracchedika-en-cost-quality.md`; prices in `4-SYSTEM/scripts/usage-ledger/prices.json` |
| 8 zh, hi | in progress | see below |

## Chinese and Hindi (2026-10-07)
| Step | zh | hi |
|---|---|---|
| Zero-shot baseline | existed (Gemini, Traditional) | done — Gemini/hi, 63 calls |
| Termbase | done; overrides: 相 mark / 相狀 sign; 想 kept for saṃjñā | done; overrides: धर्म for both senses of ཆོས (academic) + compounds |
| Academic translation | FINAL — all segments pass (a1 429/432 → 60 regenerated → 7-28, 10-52 reverted; 7-30 passes at attempt 3) | FINAL — all segments pass (a1 426/432 → 41 regenerated → a2 40/41; 5-6 reverted to attempt 1) |
| Children's | 300/446 when the session ended (`translate/zh-children-run.log`); resumable | not started |

### Resume here (next session)
1. ~~Hindi re-check a2~~ — done (keep-best rule: a re-check failure where attempt 1 passed → append the attempt-1 row with
   `call_id: revert`; failed both times → one more retry with `--attempt 3`, re-check, then `review-flags.md`).
2. **Chinese children's**: rerun the same command to finish (it skips done segments):
   `zsh -ic 'cd <vault> && python3 0-INBOX/kf-pilot/translate/gm_variant_translate.py --variant children --lang zh --from-track academic --workers 6'`
   then fact-check with `prep.py --variant children --lang zh` + prompt `factcheck-children-lang.md` (lang_name "Chinese (Traditional characters)").
3. **Hindi children's**: write `3-TRANSFORMATIONS/Translations/hi-children/requirements.md` + `audience.md` (in Hindi, mirror zh-children),
   copy termbase (already copied), run `--variant children --lang hi --from-track academic`, then fact-check.
4. **Report**: extend `reports/vajracchedika-en-cost-quality.md` to zh and hi (`usage_ledger.py summary --text vajracchedika`).
5. Then: register the scripts as skills (`create-skill`) and run Ratnaguṇa.

### Findings to carry into the report
- Hindi glossary over-application: locked བདག → आत्मन् was used for the pronoun "I" (7-8, 7-15); en/zh were fine.
- Sanskrit/Tibetan divergence: Hindi rendered མནར་བ as परिभूत (= Skt paribhūta) where the Tibetan + commentaries mean "tormented" (8-68–70).
- Glossary-check false positives by script: English plurals, Chinese punctuation, Hindi compounds (fixed: substring stems, skip helper verbs).
- Several Hindi checkers judged from Tibetan + Sanskrit + English reference without opening the commentaries.
- Long background runs: start with absolute paths (`zsh -ic 'cd <vault> && …'`); foreground commands time out at 10 min.

## Usage ledger
`usage-ledger.jsonl` — every model call. Gemini rows are exact (API usage). Claude agent rows: input/cache exact
from transcripts, output ESTIMATED (transcripts keep only the start-of-response usage; thinking is redacted).
Exact Claude usage needs the `claude` CLI logged in (`claude -p --output-format json`).

## Open items
- Termbase review applied some questionable Gemini changes (gandharva → scent-eater, guru → master, below → nadir,
  Perfection of Wisdom capitalised as a practice). Revisit before translation.
- ཆོས has a third sense (quality of a Buddha) that the reviewer wanted merged; recorded, not applied.
- Term-agent prompt gives 3 examples per term; multi-sense terms need all occurrences (batch-04 read segments.json itself).
