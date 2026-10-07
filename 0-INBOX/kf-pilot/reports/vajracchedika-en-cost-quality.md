---
title: "KF AI Translation Pilot — Diamond Sutra, English: cost and quality"
status: draft
date: 2026-10-07
source_data: 0-INBOX/kf-pilot/usage-ledger.jsonl; factcheck/*/verdicts.json; factcheck/calibration/result.json
prices: 4-SYSTEM/scripts/usage-ledger/prices.json (list prices as of 2026-10-07)
---

# Diamond Sutra (Vajracchedikā), English — cost and quality

Draft section for the KF pilot report. All figures come from the usage ledger, which records every model call
made for this text; costs are API list prices on 2026-10-07 (see *Method and caveats*).

## 1. What was produced

| Output | Built by | Checked by | Size |
|---|---|---|---|
| Zero-shot translation (normal version), en + zh | Gemini 3.1 Pro, DharmaMitra (en) | — (baseline) | 446 segments each |
| Commentary translations, 3 commentaries × en + zh | Gemini 3.1 Pro, DharmaMitra | — (baseline) | 617 commentary blocks each |
| Glossary: 278 Tibetan terms, academic + children's renderings | Claude Sonnet 5.5 agents | Gemini 3.1 Pro | 283 entries per register |
| **Academic translation** | Gemini 3.1 Pro, glossary-locked, with Sanskrit + 3 commentaries per segment | Claude Sonnet 5.5 agents | 446 segments, 7,754 words |
| **Children's version** (ages 8–12) | Gemini 3.1 Pro, from the academic version + children's glossary | Claude Sonnet 5.5 agents | 446 segments, 7,974 words |

Source text: 446 segments (432 text segments + 14 headings), 10,680 Tibetan syllables.

## 2. Cost

### By step

| Step | Model | Calls | USD |
|---|---|---|---|
| Term extraction (13 parallel agents) | Claude Sonnet 5.5 | 62 | 3.40 |
| Term review | Gemini 3.1 Pro | 13 | 1.70 |
| Glossary (style sheet + 6 parallel agents) | Claude Sonnet 5.5 | 76 | 3.93 |
| Glossary review | Gemini 3.1 Pro | 1 | 0.26 |
| Academic translation, incl. retries and fixes | Gemini 3.1 Pro | 105 | 6.22 |
| Academic fact-check, incl. re-checks | Claude Sonnet 5.5 | 152 | 7.20 |
| Children's version, incl. retries | Gemini 3.1 Pro | 92 | 3.98 |
| Children's fact-check, incl. re-checks | Claude Sonnet 5.5 | 60 | 2.98 |
| Fact-checker reliability test | Claude Sonnet 5.5 | 10 | 0.37 |
| **Pipeline total (new work)** | | **571** | **30.04** |
| Zero-shot root translation, en + zh (earlier) | Gemini 3.1 Pro | 127 | 7.32 |
| Commentary translations, 3 × en + zh (earlier) | Gemini 3.1 Pro | 496 | 51.88 |
| **All work on this text** | | **1,194** | **89.24** |

DharmaMitra calls are free and not in the totals.

### By version

| Version | What it includes | USD | per 1,000 Tibetan syllables | per English word |
|---|---|---|---|---|
| Glossary (shared by both versions) | extraction, review, termbase, review | 9.29 | 0.87 | — |
| Academic | translation + fact-check + fixes | 13.42 | 1.26 | 0.0017 |
| Academic incl. the glossary | | 22.71 | 2.13 | 0.0029 |
| Children's | translation + fact-check + fixes | 6.96 | 0.65 | 0.0009 |
| Zero-shot, one language (approx.) | half of the en + zh run | ≈ 3.66 | ≈ 0.34 | — |

The governed academic version costs roughly six times a zero-shot run. Whether that buys quality worth the
difference is what the blind evaluation (section 4) has to show.

**Where the money goes:**
- **Gemini thinking tokens.** These are billed at the output rate and are 60–90% of every Gemini step's cost (e.g. academic translation: 389K thinking tokens against 26K visible output).
- **Claude cache reads.** The Claude agents' cost is almost all cache reads and writes, because each agent re-reads its packet on every turn. Their visible output is small.

## 3. Quality

### Glossary consistency (automatic check)

| Version | Locked-term uses required | Used | Rate |
|---|---|---|---|
| Academic | 1,564 | 1,563 | 99.9% |
| Children's | 1,564 | 1,563 | 99.9% |

The one academic gap is the closing title (13-3), where the glossary contradicts its own style sheet; it needs a
glossary decision, not a translation fix.

### Fact-check (Claude checks Gemini's output, segment by segment)

| | Academic | Children's |
|---|---|---|
| Checked against | Tibetan, Sanskrit, 3 aligned commentaries | Tibetan, approved academic version |
| Passed first time | 431 / 432 (99.8%) | 430 / 432 (99.5%) |
| Major errors found | 1 (8-6: comparison lost) | 2 (4-1: "designated" dropped; 12-24: comparison lost) |
| Critical errors found | 0 | 0 |
| Fixed by regeneration | 1 / 1 | 1 / 2 |
| Left for a human | 0 | 1 (12-24, after 2 retries) |
| Minor issues | 32 segments regenerated: 30 re-checked clean or near-clean, 2 reverted; 9 minor notes remain | 31 open (not yet regenerated) |

**Fixing minor issues can break correct sentences.** Regenerating the 32 segments with minor issues fixed 30 of them. The other 2 got worse: the fix introduced a major error, for example "do not designate as destroyed" became "do not destroy". Those 2 were restored to their earlier, correct versions. So a retry must always be re-checked, and the best attempt kept.

### How reliable is the checker?

The same checker prompt was run on 24 segments of the finished academic translation:
- **18 with one planted error:** reversed negation, changed number, wrong name, dropped clause, added claim, swapped glossary term or wrong word.
- **6 left unchanged** as controls.

| Planted errors | Caught (failed the segment) | Missed | False alarms on controls |
|---|---|---|---|
| 18 | 17 (94%) | 1 | 0 of 6 |

The one miss was a swapped glossary term ("enlightenment" for the locked "awakening"). The checker flagged it but
rated it minor instead of major. The automatic glossary check catches that kind of error anyway. So the high pass
rates above reflect the translation, not a lenient checker.

## 4. Still to do for this text

- **Blind quality comparison:** a sample of about 40 segments scored with the MQM error-scoring scheme:
  - the two zero-shot versions vs the academic version vs a human translation;
  - the human reference has to be Chinese (Kumārajīva, Bodhiruci or the modern-Chinese version), because no English human translation is in the vault;
  - scored by AI (GEMBA) and, if possible, by a specialist.
- **Human comparison:** the cost of a human translation of the same 10,680 syllables at a stated rate, and the specialist time needed to bring the AI versions to publication. Neither is measured yet; no specialist time has been spent so far, apart from the editor decisions recorded in the glossary overrides.

## Method and caveats

- **Prices:** Gemini 3.1 Pro preview at $2 input / $12 output per 1M tokens, with thinking billed as output (prompts under 200K tokens). Claude Sonnet 5.5 at $2 input / $10 output / $0.20 cache read / $2.50 cache write per 1M tokens. Sources and dates are in `prices.json`.
- **Gemini tokens are exact,** from the API's usage report for every call. The earlier zero-shot and commentary runs were de-duplicated from their logs, which had copied one call's usage onto every segment in the batch.
- **Claude tokens are partly estimated.**
  - The agents ran inside Claude Code, which records input and cache tokens exactly but only a start-of-response snapshot of output. Output is therefore estimated from the text each agent wrote (about 3 characters per token).
  - Thinking tokens are stored only in encrypted form and are not counted. Claude costs are a lower bound.
  - Exact figures need the agents to run through the `claude` command-line tool with usage reporting.
- **Claude costs are API-equivalent.** The agents ran under a Claude Code plan, so these are list-price equivalents, not invoiced amounts.
- **Not counted:** the orchestrating session that planned and ran the pipeline (development work, not per-text cost), and the one-time tool-building done this session.
