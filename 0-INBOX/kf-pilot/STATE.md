# KF pilot — Diamond Sutra pipeline state

Working area for the KF AI-translation pilot report (Diamond Sutra first, then Ratnaguṇa and BCA).
Scripts here are drafts; they become registered skills (via `create-skill`) once the whole flow works.

## Decisions (user, 2026-10-07)
- Gemini translates; Claude checks. Anything Claude produces is reviewed by Gemini, and vice versa. No human reviewer: the cross-model review approves.
- Agents orchestrate and run in parallel; scripts where needed (all Gemini calls are scripts).
- Versions: academic + children's (new); zero-shot (DharmaMitra/Gemini, exists) and commentary translations (exist). Word-by-word deferred.
- Build in this vault; sync the finished skills to the other vaults afterwards.
- Keep-best rule for minor fixes (2026-10-07): after a minor-fix round and its re-check, run the blind pairwise judge (`improvement.py --pairs` → `pairwise_judge.py --revert-losses`); a minor-only fix is kept when Gemini prefers it or ties, and the original is restored when both A/B orders prefer it. Major-error fixes are not reverted by the judge.

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
| 7 Cost/quality report (Diamond, en + zh + hi) | draft done — pipeline $29.78 en / $26.66 zh / $21.74 hi ($78.18); measurement $4.17; all work $145.04; incl. checker reliability and before/after improvement | `reports/vajracchedika-en-cost-quality.md`; prices in `4-SYSTEM/scripts/usage-ledger/prices.json` |
| 8 zh, hi | done — all four tracks final; report extended | see below |

## Chinese and Hindi (2026-10-07)
| Step | zh | hi |
|---|---|---|
| Zero-shot baseline | existed (Gemini, Traditional) | done — Gemini/hi, 63 calls |
| Termbase | done; overrides: 相 mark / 相狀 sign; 想 kept for saṃjñā | done; overrides: धर्म for both senses of ཆོས (academic) + compounds |
| Academic translation | FINAL — all segments pass (a1 429/432 → 60 regenerated → 7-28, 10-52 reverted; 7-30 passes at attempt 3; a4 re-check 2026-10-07 of 12 segments whose text changed after their check: 11 pass, 9-11 failed → reverted to its a2-passing text) | FINAL — all segments pass (a1 426/432 → 41 regenerated → a2 40/41; 5-6 reverted to attempt 1) |
| Children's | FINAL — all segments pass (a1 428/432; 4 major regenerated → a2 4/4 pass); 40 minor open | FINAL — all segments pass (a1 427/432; 5 major regenerated → a2 5/5 pass); 40 minor open; glossary-check: 17/18 flags false positives (oblique case); 4-1 paraphrases the locked nirvāṇa term (term itself ungrammatical in context — glossary note) |

### Resume here (next session)
1. ~~Hindi re-check a2~~ — done (keep-best rule: a re-check failure where attempt 1 passed → append the attempt-1 row with
   `call_id: revert`; failed both times → one more retry with `--attempt 3`, re-check, then `review-flags.md`).
2. ~~Chinese children's~~ — done (`factcheck/zh-children-a1`, `zh-children-a2`; agent usage harvested; the previous session's agents live under the `-daimond-sutra-rails` project dir).
3. ~~Hindi children's~~ — done (`factcheck/hi-children-a1`, `hi-children-a2`; usage harvested).
4. ~~Report~~ — extended to zh + hi (filename still `-en-`; rename to `vajracchedika-cost-quality.md` if no links depend on it). Hindi glossary check fixed (strips inflectional endings); hi tracks re-rendered.
5. ~~Checker reliability zh + hi~~ — done: 17/18 caught, 0/6 false alarms in both (same as en); the one miss in all three languages is 8-97 (locked term swapped for a near-synonym, rated minor), which the automatic glossary check catches → checker + glossary check = 18/18. `factcheck/calibration{,-zh,-hi}/`, `calibration/plant.py`, `calibration/score.py`.
6. ~~Improvement metrics~~ — done and in the report (§3 "Improvement from the fact-check and fix"): `factcheck/improvement.py --json reports/improvement-vajracchedika.json --pairs reports/improvement-pairs-vajracchedika.json`; `zsh -ic '… factcheck/pairwise_judge.py reports/improvement-pairs-vajracchedika.json --out reports/improvement-judged-vajracchedika.json'` (two passes, A/B swapped). Result: major-error fixes judged better 19/21; minor-only fixes better 52%, tie 33%, worse 15% (18 segments).
   **Decided (user, 2026-10-07):** the 18 minor-fix segments the judge rated worse were restored (`pairwise_judge.py --revert-losses`), and that keep-best rule applies to every future minor-fix round (see Decisions).
7. ~~Blind comparison~~ — done 2026-10-07, in the report (§3 "Blind comparison"): 40 segments × en/zh/hi, governed vs zero-shot (+ DharmaMitra en, Kumārajīva zh), MQM-annotated blind by Claude agents AND Gemini (`blind-eval/`: `build.py`, `rubric-mqm.md`, `judge_gemini.py`, `score.py`, key in `key.json`). Governed has the fewest errors in every language under both annotators; zero-shot major errors come from following the Sanskrit / Chinese tradition (相 for saṃjñā, adharma). Kumārajīva scores worst against the Tibetan (different recension — not a fair benchmark).
   Loose ends closed 2026-10-07: en-children 12-24 (Claude checker's fix → Claude re-check pass + Gemini blind judge win in both orders); en-academic 13-3 (user: match the opening title; override T274; regenerated; check passes; en academic glossary 1,564/1,564); Hindi commentary translations out of scope (user); human-cost comparison from published rates (84000 $400/page; Prajna Fire $100–300/page) in report §2.
   **Published report (2026-10-08):** Claude Docs doc "KF Pilot — Diamond Sutra: Cost and Quality", https://claude.ai/artifact/8j6Cqn62otc5TQbZW1P5BF (source of its content: `reports/vajracchedika-en-cost-quality.md`; edit the doc through the Docs connector, not by republishing). Plan (user): one report doc per text, then a combined report at the end.
   **Diamond Sutra: complete for the pilot scope.** Only open item: specialist review time (needs a human; decides the 10%-of-human-cost question) and optional specialist scoring of the blind sample.
9. Then: register the scripts as skills (`create-skill`) and run Ratnaguṇa.
8. Bodhicaryāvatāra (Chonjuk) started 2026-10-07 in `bodhisattvacharyavatara-rails/0-INBOX/kf-pilot/` (scripts copied and adapted; see its STATE.md). The user asked for before/after improvement metrics for every fact-check + fix round; compute them retroactively here too (list in that STATE.md).

### Findings to carry into the report
- Hindi glossary over-application: locked བདག → आत्मन् was used for the pronoun "I" (7-8, 7-15); en/zh were fine.
- Sanskrit/Tibetan divergence: Hindi rendered མནར་བ as परिभूत (= Skt paribhūta) where the Tibetan + commentaries mean "tormented" (8-68–70).
- Glossary-check false positives by script: English plurals, Chinese punctuation, Hindi compounds (fixed: substring stems, skip helper verbs).
- Several Hindi checkers judged from Tibetan + Sanskrit + English reference without opening the commentaries.
- Glossary check misses Hindi oblique/inflected forms (चीज़ें→चीज़ों, नदी→नदियों, देना→देता, मानना→मानेंगे): 17 of 18 hi-children flags were false positives.
- Text changed after its check is unverified: a term-retry run at 19:06 rewrote 12 zh academic segments after the a2 check, and one (9-11) gained a major error (教法 forced into 法眼). `improvement.py` now lists any segment whose current text no check has seen (`unchecked_current_text`) — run it before declaring a track final.
- Reverts must restore the text the check actually saw: 7-28's revert restored the pre-term-retry text, which no check had seen (it passed on a4).
- Long background runs: start with absolute paths (`zsh -ic 'cd <vault> && …'`); foreground commands time out at 10 min.

## Usage ledger
`usage-ledger.jsonl` — every model call. Gemini rows are exact (API usage). Claude agent rows: input/cache exact
from transcripts, output ESTIMATED (transcripts keep only the start-of-response usage; thinking is redacted).
Exact Claude usage needs the `claude` CLI logged in (`claude -p --output-format json`).

## Open items
- ~~Termbase review's questionable changes~~ — resolved before translation by editor overrides (gandharva, guru, below, perfection of wisdom; `termbase/vajracchedika-en/overrides.json`).
- ཆོས has a third sense (quality of a Buddha) that the reviewer wanted merged; recorded, not applied.
- Term-agent prompt gives 3 examples per term; multi-sense terms need all occurrences (batch-04 read segments.json itself).

## Combined report (2026-10-08)
Claude Docs doc "KF Pilot — Three Texts: Cost and Quality of AI Translation", https://claude.ai/artifact/MMVkU1Pf5KyJFpnnRovMqM, built from the three per-text reports (Diamond, Ratnaguṇa, Bodhicaryāvatāra). Edit through the Docs connector. Totals: pipeline $360.49, measurement $44.00, all work $587.64.
