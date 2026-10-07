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
| 7 Cost/quality report (Diamond, en + zh + hi) | draft done — pipeline $30.04 en / $26.43 zh / $21.74 hi ($78.21); all work $140.90 | `reports/vajracchedika-en-cost-quality.md`; prices in `4-SYSTEM/scripts/usage-ledger/prices.json` |
| 8 zh, hi | done — all four tracks final; report extended | see below |

## Chinese and Hindi (2026-10-07)
| Step | zh | hi |
|---|---|---|
| Zero-shot baseline | existed (Gemini, Traditional) | done — Gemini/hi, 63 calls |
| Termbase | done; overrides: 相 mark / 相狀 sign; 想 kept for saṃjñā | done; overrides: धर्म for both senses of ཆོས (academic) + compounds |
| Academic translation | FINAL — all segments pass (a1 429/432 → 60 regenerated → 7-28, 10-52 reverted; 7-30 passes at attempt 3) | FINAL — all segments pass (a1 426/432 → 41 regenerated → a2 40/41; 5-6 reverted to attempt 1) |
| Children's | FINAL — all segments pass (a1 428/432; 4 major regenerated → a2 4/4 pass); 40 minor open | FINAL — all segments pass (a1 427/432; 5 major regenerated → a2 5/5 pass); 40 minor open; glossary-check: 17/18 flags false positives (oblique case); 4-1 paraphrases the locked nirvāṇa term (term itself ungrammatical in context — glossary note) |

### Resume here (next session)
1. ~~Hindi re-check a2~~ — done (keep-best rule: a re-check failure where attempt 1 passed → append the attempt-1 row with
   `call_id: revert`; failed both times → one more retry with `--attempt 3`, re-check, then `review-flags.md`).
2. ~~Chinese children's~~ — done (`factcheck/zh-children-a1`, `zh-children-a2`; agent usage harvested; the previous session's agents live under the `-daimond-sutra-rails` project dir).
3. ~~Hindi children's~~ — done (`factcheck/hi-children-a1`, `hi-children-a2`; usage harvested).
4. ~~Report~~ — extended to zh + hi (filename still `-en-`; rename to `vajracchedika-cost-quality.md` if no links depend on it). Hindi glossary check fixed (strips inflectional endings); hi tracks re-rendered.
5. **Next:** planted-error checker test in zh + hi (report §4), then register the scripts as skills (`create-skill`) and run Ratnaguṇa.

### Findings to carry into the report
- Hindi glossary over-application: locked བདག → आत्मन् was used for the pronoun "I" (7-8, 7-15); en/zh were fine.
- Sanskrit/Tibetan divergence: Hindi rendered མནར་བ as परिभूत (= Skt paribhūta) where the Tibetan + commentaries mean "tormented" (8-68–70).
- Glossary-check false positives by script: English plurals, Chinese punctuation, Hindi compounds (fixed: substring stems, skip helper verbs).
- Several Hindi checkers judged from Tibetan + Sanskrit + English reference without opening the commentaries.
- Glossary check misses Hindi oblique/inflected forms (चीज़ें→चीज़ों, नदी→नदियों, देना→देता, मानना→मानेंगे): 17 of 18 hi-children flags were false positives.
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
