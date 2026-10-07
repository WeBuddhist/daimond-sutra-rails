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
| 8 zh, hi | todo | |

## Usage ledger
`usage-ledger.jsonl` — every model call. Gemini rows are exact (API usage). Claude agent rows: input/cache exact
from transcripts, output ESTIMATED (transcripts keep only the start-of-response usage; thinking is redacted).
Exact Claude usage needs the `claude` CLI logged in (`claude -p --output-format json`).

## Open items
- Termbase review applied some questionable Gemini changes (gandharva → scent-eater, guru → master, below → nadir,
  Perfection of Wisdom capitalised as a practice). Revisit before translation.
- ཆོས has a third sense (quality of a Buddha) that the reviewer wanted merged; recorded, not applied.
- Term-agent prompt gives 3 examples per term; multi-sense terms need all occurrences (batch-04 read segments.json itself).
