---
title: "KF AI Translation Pilot — Diamond Sutra, English, Chinese and Hindi: cost and quality"
status: draft
date: 2026-10-07
source_data: 0-INBOX/kf-pilot/usage-ledger.jsonl; factcheck/*/verdicts.json; factcheck/calibration/result.json
prices: 4-SYSTEM/scripts/usage-ledger/prices.json (list prices as of 2026-10-07)
---

# Diamond Sutra (Vajracchedikā), English, Chinese and Hindi — cost and quality

Draft section for the KF pilot report. All figures come from the usage ledger, which records every model call
made for this text; costs are API list prices on 2026-10-07 (see *Method and caveats*).

## 1. What was produced

Source text: 446 segments (432 text segments + 14 headings), 10,680 Tibetan syllables.
Languages: English (en), Chinese in Traditional characters (zh), Hindi (hi).

| Output | Built by | Checked by | en | zh | hi |
|---|---|---|---|---|---|
| Zero-shot translation (baseline) | Gemini 3.1 Pro; DharmaMitra (en) | — | ✓ | ✓ | ✓ |
| Commentary translations, 3 commentaries (baseline) | Gemini 3.1 Pro, DharmaMitra | — | ✓ | ✓ | — |
| Term list: 278 Tibetan terms (shared by all languages) | Claude Sonnet 5.5 agents | Gemini 3.1 Pro | ✓ | | |
| Glossary, academic + children's renderings | Claude Sonnet 5.5 agents | Gemini 3.1 Pro | ✓ | ✓ | ✓ |
| **Academic translation** — glossary-locked, with Sanskrit + 3 commentaries per segment | Gemini 3.1 Pro | Claude Sonnet 5.5 agents | 7,754 words | 10,831 characters | 6,488 words |
| **Children's version** (ages 8–12) — from the academic version + children's glossary | Gemini 3.1 Pro | Claude Sonnet 5.5 agents | 7,974 words | 13,224 characters | 7,925 words |

Every governed translation covers all 446 segments.

## 2. Cost

### By step and language (USD)

| Step | Model | en | zh | hi |
|---|---|---|---|---|
| Term extraction (13 parallel agents; shared) | Claude Sonnet 5.5 | 3.40 | — | — |
| Term review (shared) | Gemini 3.1 Pro | 1.70 | — | — |
| Glossary (style sheet + parallel agents) | Claude Sonnet 5.5 | 3.93 | 2.95 | 3.24 |
| Glossary review | Gemini 3.1 Pro | 0.26 | 0.25 | 0.28 |
| Academic translation, incl. retries and fixes | Gemini 3.1 Pro | 6.22 | 9.21 | 6.38 |
| Academic fact-check, incl. re-checks | Claude Sonnet 5.5 | 7.20 | 5.97 | 4.70 |
| Children's version, incl. retries and fixes | Gemini 3.1 Pro | 3.98 | 5.00 | 4.29 |
| Children's fact-check, incl. re-checks | Claude Sonnet 5.5 | 2.98 | 3.05 | 2.85 |
| Fact-checker reliability test | Claude Sonnet 5.5 | 0.37 | — | — |
| **Pipeline total (new work)** | | **30.04** | **26.43** | **21.74** |
| Zero-shot root translation (baseline) | Gemini 3.1 Pro | 3.59 | 3.73 | 3.49 |
| Commentary translations, 3 commentaries (baseline, earlier) | Gemini 3.1 Pro | 24.19 | 27.69 | — |
| **All work on this text** | | **57.83** | **57.84** | **25.24** |

Pipeline total for the three languages: **$78.21**. All work on this text: **$140.90**. DharmaMitra calls are free and not in the totals.

### By version

| Version | en | zh | hi | per 1,000 Tibetan syllables (en / zh / hi) |
|---|---|---|---|---|
| Glossary | 9.29 (incl. shared term list) | 3.20 | 3.52 | 0.87 / 0.30 / 0.33 |
| Academic (translation + fact-check + fixes) | 13.42 | 15.18 | 11.08 | 1.26 / 1.42 / 1.04 |
| Academic incl. its glossary | 22.71 | 18.38 | 14.60 | 2.13 / 1.72 / 1.37 |
| Children's (translation + fact-check + fixes) | 6.96 | 8.05 | 7.14 | 0.65 / 0.75 / 0.67 |
| Zero-shot | 3.59 | 3.73 | 3.49 | 0.34 / 0.35 / 0.33 |

- **Each further language costs less than the first.** The term list is built once, so a new language needs only its own glossary: about $3.20–3.50 against $9.29 for English. A full new language (glossary + academic + children's) cost $26.43 for Chinese and $21.74 for Hindi.
- **Governed vs zero-shot.** The governed academic version, including its glossary, costs 6.3× a zero-shot run in English, 4.9× in Chinese and 4.2× in Hindi. Whether that buys quality worth the difference is what the blind evaluation (section 4) has to show.
- **Chinese academic cost the most to translate ($9.21).** Gemini's thinking ran longer (607K thinking tokens, against 388K for English and Hindi). Chinese also regenerated 60 segments to fix minor issues, against 32 for English and 41 for Hindi.

**Where the money goes:**
- **Gemini thinking tokens.** These are billed at the output rate and are 60–90% of every Gemini step's cost (e.g. English academic translation: 389K thinking tokens against 26K visible output).
- **Claude cache reads.** The Claude agents' cost is almost all cache reads and writes, because each agent re-reads its packet on every turn. Their visible output is small.

## 3. Quality

### Glossary consistency (automatic check)

| Version | Locked-term uses required | en | zh | hi |
|---|---|---|---|---|
| Academic | 1,564 per language | 1,563 (99.9%) | 1,558 (99.6%) | 1,563 (99.9%) |
| Children's | 1,564 per language | 1,563 (99.9%) | 1,558 (99.6%) | 1,562 (99.9%) |

- **English academic:** the one gap is the closing title (13-3), where the glossary contradicts its own style sheet; it needs a glossary decision, not a translation fix.
- **Chinese:** the 6 academic gaps are mostly 世間 and 佛 in passages where the fact-checker accepted the chosen wording.
- **Hindi children's:** 7-29 uses चाह where the locked term is चाहत. In 8-118, a relative pronoun inside the locked phrase changed with the sentence.

**The check itself needed fixing for each script.** It first raised false alarms on English plurals, Chinese punctuation, and Hindi compounds and inflections. Before the last fix, 17 of the 18 segments it flagged in Hindi children's were Hindi plural or verb forms (चीज़ें → चीज़ों, नदी → नदियों, देना → देता), not missing terms. Each language needs its own rule for matching inflected forms before the check can be trusted.

### Fact-check (Claude checks Gemini's output, segment by segment)

**Academic** — checked against the Tibetan, the Sanskrit and 3 aligned commentaries:

| | en | zh | hi |
|---|---|---|---|
| Passed first time | 431 / 432 (99.8%) | 429 / 432 (99.3%) | 426 / 432 (98.6%) |
| Major errors found | 1 | 3 | 6 |
| Critical errors found | 0 | 0 | 0 |
| Segments regenerated (major + minor issues) | 33 | 60 | 41 |
| Regressions on re-check, restored to the earlier version | 2 | 2 | 1 |
| Needed a third attempt | 0 | 1 (7-30) | 0 |
| Final state | all pass | all pass | all pass |

The major errors:
- **en:** 8-6, a comparison lost.
- **zh:** 7-30, the negation of "would not have declared" missed; 9-11 and 9-13, glossary terms.
- **hi:**
  - 7-8 and 7-15: the locked term आत्मन् (self) was used for the plain pronoun "I".
  - 8-68 to 8-70: परिभूत, which follows the Sanskrit, was used where the Tibetan and the commentaries mean "tormented".
  - 7-78: "taught as a non-particle" became "did not call them particles", which denies the naming instead of predicating it.

**Children's** — checked against the Tibetan and the approved academic version:

| | en | zh | hi |
|---|---|---|---|
| Passed first time | 430 / 432 (99.5%) | 428 / 432 (99.1%) | 427 / 432 (98.8%) |
| Major errors found | 2 | 4 | 5 |
| Critical errors found | 0 | 0 | 0 |
| Fixed by regeneration | 1 / 2 | 4 / 4 | 5 / 5 |
| Left for a human | 1 (12-24) | 0 | 0 |
| Minor issues still open | 31 | 40 | 40 |

The children's errors are of the kinds a simplifying rewrite produces:
- **Added ideas:** "clings to the fruit" (zh 7-8); "the Buddha obtained" something (hi 6-31); "the gift is very large" (zh 6-46).
- **Added comparison:** "much bigger than this" where the source has none (hi 6-43).
- **Lost or narrowed scope:** the whole universe narrowed to one world (hi 12-1); a number of buddhas reduced to "very many" (zh 8-72).
- **Garbled clauses:** hi 10-42, 11-10.

**Fixing minor issues can break correct sentences.** Across the three academic versions, 134 segments were regenerated to fix issues. Five regenerations made a correct segment worse, for example "do not designate as destroyed" became "do not destroy". Those five were restored to their earlier, correct versions. So a retry must always be re-checked, and the best attempt kept.

**Error rates rise as the language moves away from English.** English, then Chinese, then Hindi produced more errors at first pass, in both versions. The Hindi errors come from two sources the other languages did not show:
- **Glossary over-application:** a locked doctrinal term was used for an everyday word.
- **Source divergence:** the model followed the Sanskrit where the Tibetan and its commentaries differ.

Both were caught and fixed, but they show where a specialist's review time would go.

### How reliable is the checker?

The same checker prompt was run on 24 segments of the finished English academic translation:
- **18 with one planted error:** reversed negation, changed number, wrong name, dropped clause, added claim, swapped glossary term or wrong word.
- **6 left unchanged** as controls.

| Planted errors | Caught (failed the segment) | Missed | False alarms on controls |
|---|---|---|---|
| 18 | 17 (94%) | 1 | 0 of 6 |

The one miss was a swapped glossary term ("enlightenment" for the locked "awakening"). The checker flagged it but
rated it minor instead of major. The automatic glossary check catches that kind of error anyway. So the high pass
rates above reflect the translation, not a lenient checker.

**This test was run in English only.** Two observations from the Chinese and Hindi runs:
- **Severity varies between checkers.** The Chinese checker failed 8-72 for reducing a number to "very many". The Hindi checker rated a clumsy but complete rendering of the same number as minor. Both calls were correct, but the line between minor and major is drawn by each checker agent.
- **Some checkers skipped the commentaries.** Several Hindi academic checkers judged from the Tibetan, the Sanskrit and the English reference without opening the commentaries they were given.

A planted-error test in Chinese and Hindi would confirm the checker is as reliable outside English.

## 4. Still to do for this text

- **Blind quality comparison:** a sample of about 40 segments scored with the MQM error-scoring scheme:
  - the zero-shot versions vs the academic version vs a human translation;
  - the human reference has to be Chinese (Kumārajīva, Bodhiruci or the modern-Chinese version), because no English or Hindi human translation is in the vault;
  - scored by AI (GEMBA) and, if possible, by a specialist.
- **Checker reliability in zh and hi:** repeat the planted-error test on Chinese and Hindi segments.
- **Human comparison:** the cost of a human translation of the same 10,680 syllables at a stated rate, and the specialist time needed to bring the AI versions to publication. Neither is measured yet; no specialist time has been spent so far, apart from the editor decisions recorded in the glossary overrides.

## Method and caveats

- **Prices:** Gemini 3.1 Pro preview at $2 input / $12 output per 1M tokens, with thinking billed as output (prompts under 200K tokens). Claude Sonnet 5.5 at $2 input / $10 output / $0.20 cache read / $2.50 cache write per 1M tokens. Sources and dates are in `prices.json`.
- **Gemini tokens are exact,** from the API's usage report for every call. The earlier zero-shot and commentary runs were de-duplicated from their logs, which had copied one call's usage onto every segment in the batch.
- **Claude tokens are partly estimated.**
  - The agents ran inside Claude Code, which records input and cache tokens exactly but only a start-of-response snapshot of output. Output is therefore estimated from the text each agent wrote (about 3 characters per token).
  - Thinking tokens are stored only in encrypted form and are not counted. Claude costs are a lower bound.
  - Exact figures need the agents to run through the `claude` command-line tool with usage reporting.
- **Claude costs are API-equivalent.** The agents ran under a Claude Code plan, so these are list-price equivalents, not invoiced amounts.
- **Shared costs sit under English.** The term list (extraction + review, $5.10) and the checker reliability test ($0.37) serve all three languages but are counted in the English column.
- **Not counted:** the orchestrating session that planned and ran the pipeline (development work, not per-text cost), and the one-time tool-building.
