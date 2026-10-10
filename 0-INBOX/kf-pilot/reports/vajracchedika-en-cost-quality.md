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

Every governed translation covers all 446 segments. Commentary translations exist for English and Chinese only; Hindi commentaries are out of scope for this pilot (editor decision, 2026-10-07).

## 2. Cost

### By step and language (USD)

| Step | Model | en | zh | hi |
|---|---|---|---|---|
| Term extraction (13 parallel agents; shared) | Claude Sonnet 5.5 | 3.40 | — | — |
| Term review (shared) | Gemini 3.1 Pro | 1.70 | — | — |
| Glossary (style sheet + parallel agents) | Claude Sonnet 5.5 | 3.93 | 2.95 | 3.24 |
| Glossary review | Gemini 3.1 Pro | 0.26 | 0.25 | 0.28 |
| Academic translation, incl. retries and fixes | Gemini 3.1 Pro | 6.23 | 9.21 | 6.38 |
| Academic fact-check, incl. re-checks | Claude Sonnet 5.5 | 7.33 | 6.20 | 4.70 |
| Children's version, incl. retries and fixes | Gemini 3.1 Pro | 3.98 | 5.00 | 4.29 |
| Children's fact-check, incl. re-checks | Claude Sonnet 5.5 | 3.29 | 3.05 | 2.85 |
| **Pipeline total (new work)** | | **30.13** | **26.65** | **21.74** |
| Measurement: checker reliability test | Claude Sonnet 5.5 | 0.37 | 0.30 | 0.32 |
| Measurement: blind before/after judge | Gemini 3.1 Pro | 0.83 | 1.51 | 0.88 |
| Measurement: blind comparison with zero-shot and human (both annotators) | Claude Sonnet 5.5 + Gemini 3.1 Pro | 1.38 | 1.29 | 1.01 |
| Zero-shot root translation (baseline) | Gemini 3.1 Pro | 3.59 | 3.73 | 3.49 |
| Commentary translations, 3 commentaries (baseline, earlier) | Gemini 3.1 Pro | 24.19 | 27.69 | — |
| **All work on this text** | | **60.48** | **61.17** | **27.44** |

Pipeline total for the three languages: **$78.52**. Measurement: $7.88. All work on this text: **$149.09**. DharmaMitra calls are free and not in the totals.

### By version

| Version | en | zh | hi | per 1,000 Tibetan syllables (en / zh / hi) |
|---|---|---|---|---|
| Glossary | 9.29 (incl. shared term list) | 3.20 | 3.52 | 0.87 / 0.30 / 0.33 |
| Academic (translation + fact-check + fixes) | 13.56 | 15.41 | 11.08 | 1.27 / 1.44 / 1.04 |
| Academic incl. its glossary | 22.85 | 18.61 | 14.60 | 2.14 / 1.74 / 1.37 |
| Children's (translation + fact-check + fixes) | 7.27 | 8.05 | 7.14 | 0.68 / 0.75 / 0.67 |
| Zero-shot | 3.59 | 3.73 | 3.49 | 0.34 / 0.35 / 0.33 |

- **Each further language costs less than the first.** The term list is built once, so a new language needs only its own glossary: about $3.20–3.50 against $9.29 for English. A full new language (glossary + academic + children's) cost $26.65 for Chinese and $21.74 for Hindi.
- **Governed vs zero-shot.** The governed academic version, including its glossary, costs 6.4× a zero-shot run in English, 5.0× in Chinese and 4.2× in Hindi. Section 3 shows what that buys: the fact-check and fix remove the major errors, and in a blind comparison the governed version has the fewest errors in every language.
- **Chinese academic cost the most to translate ($9.21).** Gemini's thinking ran longer (607K thinking tokens, against 388K for English and Hindi). Chinese also regenerated 60 segments to fix minor issues, against 32 for English and 41 for Hindi.

**Where the money goes:**
- **Gemini thinking tokens.** These are billed at the output rate and are 60–90% of every Gemini step's cost (e.g. English academic translation: 389K thinking tokens against 26K visible output).
- **Claude cache reads.** The Claude agents' cost is almost all cache reads and writes, because each agent re-reads its packet on every turn. Their visible output is small.

### Compared with human translation

No human translation of this text was commissioned, so the human cost below comes from published rates, not a quote.
- **84000** (Kangyur into English) offers sponsorship of a sūtra at a flat **USD 400 per Tibetan page** (50 pages for $20,000 up to 200 pages for $80,000), covering its whole translation-to-publication process ([84000, Sponsor a Sūtra](https://84000.co/sponsor-a-sutra)). An earlier 84000 article put the cost of translating a page at $250 (*The Cost of a Page*, no longer online).
- **Prajna Fire**, a Dharma translation nonprofit, quotes **$100–300 per double-sided Tibetan page** for philosophical texts, and $150–250 an hour for proofreading, editing and consulting ([Prajna Fire, Translation services](https://www.prajnafire.com/translation-services)).

The Diamond Sutra's 10,680 Tibetan syllables come to roughly **20–25 Tibetan pages** (estimated at about 450 syllables per Degé page; not counted from the block print).
No published rates were found for translation from Tibetan into Chinese or Hindi; the same per-page rates are assumed for them.

| | One academic translation of the Diamond Sutra, one language |
|---|---|
| Human, at 84000's rate ($400/page) | $8,000–10,000 |
| Human, at Prajna Fire's rates ($100–300/page) | $2,000–7,500 |
| This pipeline, governed academic incl. its glossary | $22.85 (en) · $18.61 (zh) · $14.60 (hi) |
| Pipeline as a share of the human cost | 0.1–1.1% |

**This compares unequal products.** A human translation at these rates arrives edited and ready to publish; the pipeline's output is a checked draft that no specialist has yet reviewed. The real comparison is pipeline cost **plus** the specialist time to bring it to publication, which this pilot has not measured. The grant's target of "about 10% of the cost of traditional methods" sets a budget for that review: 10% of $2,000–10,000 is $200–1,000, which at $150–250 an hour pays for roughly **1–7 hours of specialist review** of these 20–25 pages, after the pipeline's own $15–23. Whether a specialist can finalise the governed version in that time is the next thing to measure. The blind comparison suggests the time would go to minor wording, since no major errors remain in the sample.

## 3. Quality

### Glossary consistency (automatic check)

| Version | Locked-term uses required | en | zh | hi |
|---|---|---|---|---|
| Academic | 1,564 per language | 1,564 (100%) | 1,557 (99.6%) | 1,563 (99.9%) |
| Children's | 1,564 per language | 1,562 (99.9%) | 1,558 (99.6%) | 1,562 (99.9%) |

- **English academic:** complete. The one earlier gap, the closing title (13-3), was settled by an editor decision: it now matches the opening title ("the Diamond Cutter Perfection of Wisdom").
- **Chinese:** the 7 academic gaps are mostly 世間 and 佛 in passages where the fact-checker accepted the chosen wording. In 9-11 the gap is correct: forcing the locked 教法 into the compound 法眼 produced a major error (see below).
- **English children's:** 8-98 ("foretell") and 8-65, restored to its original by the keep-best rule (the fix had added the locked phrase but also a redundant sentence).
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
| Regressions on re-check, restored to the earlier version | 2 | 3 | 1 |
| Needed a third attempt | 0 | 1 (7-30) | 0 |
| Re-checked because the text changed after its check | 0 | 12 (11 pass; 9-11 restored) | 0 |
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
| Fixed otherwise | 1 (12-24: the checker's own fix, approved by Gemini) | 0 | 0 |
| Left for a human | 0 | 0 | 0 |
| Minor issues still open | 31 | 40 | 40 |

The children's errors are of the kinds a simplifying rewrite produces:
- **Added ideas:** "clings to the fruit" (zh 7-8); "the Buddha obtained" something (hi 6-31); "the gift is very large" (zh 6-46).
- **Added comparison:** "much bigger than this" where the source has none (hi 6-43).
- **Lost or narrowed scope:** the whole universe narrowed to one world (hi 12-1); a number of buddhas reduced to "very many" (zh 8-72).
- **Garbled clauses:** hi 10-42, 11-10.

**Fixing minor issues can break correct sentences.** Across the three academic versions, 134 segments were regenerated to fix issues. Five regenerations made a correct segment worse, for example "do not designate as destroyed" became "do not destroy". Those five were restored to their earlier, correct versions. So a retry must always be re-checked, and the best attempt kept.

**Any change after a check needs a new check.** In Chinese, a glossary retry rewrote 12 segments after they had been checked. One of them, 9-11, gained a major error: the locked term 教法 was forced into the compound 法眼 ("eye of the teaching"). The improvement measurement (below) found the unchecked text, a re-check confirmed the error, and 9-11 was restored to its checked version. The measurement script now lists any segment whose current text no check has seen.

**Error rates rise as the language moves away from English.** English, then Chinese, then Hindi produced more errors at first pass, in both versions. The errors come from two sources English did not show:
- **Glossary over-application:** a locked term was used where it does not belong: आत्मन् (self) for the pronoun "I" in Hindi, 教法 inside the compound 法眼 in Chinese.
- **Source divergence:** the Hindi model followed the Sanskrit where the Tibetan and its commentaries differ.

Both were caught and fixed, but they show where a specialist's review time would go.

### Improvement from the fact-check and fix

Each version is measured twice: **before**, the translation as the first fact-check saw it, and **after**, the final text.
Four measures, recomputed by `factcheck/improvement.py` and `factcheck/pairwise_judge.py`:

**1. Fact-check findings, before → after.** For each segment, "after" is the verdict of the check that saw its final
text. The error score is MQM-style: minor = 1, major = 5, critical = 10 points, per 1,000 Tibetan syllables.
The figures are for the final text, after the keep-best step in measure 4 restored 18 originals.

| Version | Segments changed in the end | Failing segments | Issues per 100 segments | Error score per 1,000 syllables | Segments with no issue |
|---|---|---|---|---|---|
| Academic en | 26 | 1 → 0 | 7.6 → 2.3 | 3.46 → 0.94 (−73%) | 92.8% → 98.1% |
| Academic zh | 50 | 3 → 0 | 14.8 → 8.3 | 7.12 → 3.37 (−53%) | 86.1% → 91.9% |
| Academic hi | 36 | 6 → 0 | 9.5 → 2.1 | 6.09 → 0.84 (−86%) | 91.2% → 97.9% |
| Children's en | 3 | 2 → 0 | 7.6 → 7.6 | 3.84 → 3.09 (−20%) | 93.1% → 93.1% |
| Children's zh | 4 | 4 → 0 | 10.2 → 10.2 | 5.62 → 4.12 (−27%) | 90.5% → 90.7% |
| Children's hi | 5 | 5 → 0 | 10.4 → 10.0 | 6.09 → 4.03 (−34%) | 89.8% → 90.3% |

- **Academic versions:** both major and minor issues were fixed, so the error score fell by 53–86%.
- **Children's versions:** only the major errors were fixed, and all of them were removed. English 12-24 resisted three Gemini attempts and was fixed with the Claude checker's own wording, which then passed a fresh Claude check and Gemini's blind judgement. Re-checking the rewritten segments turned up a few new minor notes, so minor counts rose slightly.

**2. Glossary compliance, before → after.** The fixes left it essentially unchanged at 99.6–99.9% (largest change: Chinese academic
99.94% → 99.55%). In Chinese the fixes removed a few locked terms where the term did not fit the sentence. 9-11 is
the clearest case: there, keeping the term was the error.

**3. chrF against a human translation.** For the Diamond Sutra, only Chinese has a human translation aligned segment by segment:
Kumārajīva, in classical Chinese, which the Chinese translator was also shown as a terminology aid. Scores barely move
(whole text 17.96 → 17.97; the 48 changed segments 16.35 → 16.40). The measure is reported for completeness. Against a
classical reference it cannot show whether a fix in modern Chinese is right.

**4. Blind judgement by the other model.** Gemini compared each regenerated segment's original and final text, with the
Tibetan, Sanskrit, commentaries and reference translation. It was not told which text was which. Every pair was judged twice, with A and B swapped. A
result counts only when both orders agree; otherwise it is a tie. On single passes Gemini picked the first-shown text 58% of the time, so the swap was needed.

| Version | Pairs | Final text better | Tie | Original better |
|---|---|---|---|---|
| Academic en | 31 | 15 (48%) | 11 (35%) | 5 (16%) |
| Academic zh | 58 | 27 (47%) | 23 (40%) | 8 (14%) |
| Academic hi | 40 | 31 (78%) | 5 (12%) | 4 (10%) |
| Children's, all three | 13 | 9 (69%) | 2 (15%) | 2 (15%) |
| **All** | **142** | **82 (58%)** | **41 (29%)** | **19 (13%)** |

| Why the segment was regenerated | Pairs | Final text better | Tie | Original better |
|---|---|---|---|---|
| Major error | 21 | 19 (90%) | 1 | 1 |
| Minor issues only | 121 | 63 (52%) | 40 (33%) | 18 (15%) |

**Fixing major errors pays off; fixing minor issues is a coin toss with a cost.** Two independent models agree that the
major-error fixes improved the text: Claude's re-check passed them, and Gemini preferred the fixed text in 19 of 21 pairs.
For minor issues, Gemini preferred the fixed text in half the cases. It judged the change neutral in a third, and worse in 15%,
usually where the fix dropped a nuance the original kept. Claude's re-check had passed all of those 18. So on those 18 the two models disagreed.

**Keep-best rule for minor fixes (adopted 2026-10-07).** A fix made for minor issues only is kept when the blind judge
prefers it or ties. When the judge prefers the original in both orders, the original is restored; it had already passed the fact-check.
Major-error fixes are not subject to this rule. The 18 segments were restored (en academic 5, zh academic 8, hi academic 4, en children's 1).
By Claude's count this raises the final error score slightly, because the originals carry the minor notes Claude
raised; for example, English academic went from 0.84 to 1.03 per 1,000 syllables. The figures in measure 1 are after the restore.

### How reliable is the checker?

The checker prompt was tested in each language on the same 24 segments of the finished academic translation:
- **18 with one planted error**, the same error at the same place in each language: reversed negation, changed number, wrong name, dropped clause, added claim, swapped glossary term or wrong word.
- **6 left unchanged** as controls.

| | en | zh | hi |
|---|---|---|---|
| Planted errors caught (segment failed) | 17 / 18 (94%) | 17 / 18 (94%) | 17 / 18 (94%) |
| …and the reported issue points at the planted words | 17 | 17 | 17 |
| Severity matches the planted severity | 17 | 16 | 17 |
| False alarms on the 6 controls | 0 | 0 | 0 |
| Caught by checker **or** automatic glossary check | 18 / 18 | 18 / 18 | 18 / 18 |

The one miss is the same in all three languages: 8-97, where the locked term for "awakening" was swapped for a
near-synonym ("enlightenment"; 無上正等正覺; पूर्ण ज्ञानोदय). The checker flagged it but rated it minor. The automatic glossary check
catches exactly this kind of error, so the two checks together caught every planted error. The checker is as reliable in
Chinese and Hindi as in English, and the high pass rates above reflect the translations, not a lenient checker.

Two caveats:
- **The test planted one clear error per segment.** Real errors are subtler, so recall on real errors may be lower.
- **The zh and hi checkers had the English academic translation as a reference,** as they did in the real checks. It may have helped them spot the planted errors.

Two observations from the real Chinese and Hindi runs:
- **Severity varies between checkers.** The Chinese checker failed 8-72 for reducing a number to "very many". The Hindi checker rated a clumsy but complete rendering of the same number as minor. Both calls were correct, but the line between minor and major is drawn by each checker agent.
- **Some checkers skipped the commentaries.** Several Hindi academic checkers judged from the Tibetan, the Sanskrit and the English reference without opening the commentaries they were given.

### Blind comparison: governed vs zero-shot vs human

**Set-up.**
- **Sample:** 40 text segments, one drawn at random from each fortieth of the sutra, the same segments in every language.
- **Candidates:**

  | Language | Candidates |
  |---|---|
  | en | governed academic, DharmaMitra zero-shot, Gemini zero-shot |
  | zh | governed academic, Gemini zero-shot, Kumārajīva |
  | hi | governed academic, Gemini zero-shot |

  No English or Hindi human translation is in the vault.
- **Blinding:** each segment's candidates were shuffled under letters. Annotators saw the Tibetan, the neighbouring Tibetan segments, the Sanskrit and the three commentaries. They did not see the glossary or the English academic version, which would have favoured the governed text.
- **Scoring:** MQM error annotation (GEMBA-MQM style), with the same rubric for both annotators. Gemini wrote both the zero-shot and the governed versions, and Claude's fact-check shaped the governed one, so **both models annotated every candidate**. Penalty per segment: minor 1, major 5, critical 10.

**Errors per segment (mean penalty; lower is better)**, Claude / Gemini as annotator:

| System | en | zh | hi |
|---|---|---|---|
| **Governed academic** | **0.03 / 0.15** | **0.03 / 0.07** | **0.07 / 0.15** |
| Zero-shot, Gemini | 0.07 / 0.15 | 0.23 / 1.00 | 0.25 / 0.30 |
| Zero-shot, DharmaMitra | 0.10 / 0.65 | — | — |
| Human, Kumārajīva (classical Chinese) | — | 1.75 / 4.72 | — |

**Major errors in the 40 segments**, Claude / Gemini as annotator:

| System | en | zh | hi |
|---|---|---|---|
| **Governed academic** | **0 / 0** | **0 / 0** | **0 / 1** |
| Zero-shot, Gemini | 0 / 0 | 1 / 7 | 0 / 2 |
| Zero-shot, DharmaMitra | 0 / 3 | — | — |
| Human, Kumārajīva | — | 10 / 31 | — |

No critical errors were found in any candidate.

**Head to head (segments where the governed version has fewer / equal / more errors)**, Claude / Gemini as annotator:

| Governed vs | en | zh | hi |
|---|---|---|---|
| Zero-shot, Gemini | 2–38–0 / 1–38–1 | 5–34–1 / 10–29–1 | 8–29–3 / 4–34–2 |
| Zero-shot, DharmaMitra | 2–38–0 / 7–30–3 | — | — |

What this shows:
- **The governed version has the fewest errors in every language under both annotators.** It ties Gemini zero-shot in English under the Gemini annotator, and its only major error is one Hindi case marker (8-95, जिससे "by which" for जिसे "which").
- **The gain is concentrated where zero-shot follows the wrong tradition.** On most segments the two versions tie, because a strong model already translates this well-known sutra well. The zero-shot major errors almost all come from following the Sanskrit or the Chinese tradition instead of the Tibetan:
  - 相 ("mark") for འདུ་ཤེས (saṃjñā, "perception"; zh 6-23, 6-25, 12-23), as in Kumārajīva;
  - 非法 / अधर्म-संज्ञा ("non-dharma", Sanskrit *adharma*) where the Tibetan says "dharmas as selfless" (zh and hi 6-25);
  - "stopped begging" / "returned from the alms round" where the Tibetan has "gave up the later meal" (zh and hi 1-5).

  These are exactly what the governed pipeline's glossary and aligned commentaries are built to prevent.
- **The gap is largest in Chinese, smallest in English.**
  - Chinese: Gemini as annotator found 7 major errors in the Chinese zero-shot against 0 in the governed version. Claude found 1 against 0. Scaled to the 432 segments, that is between about 11 (Claude) and 75 (Gemini) major errors that the extra $14.88 avoids (governed academic with its glossary, $18.61, minus zero-shot, $3.73).
  - English: the two versions are nearly level.
  - Hindi: the governed version is ahead under both annotators.
- **The two annotators agree on direction but not on detail.**
  - Gemini marks more errors than Claude across the board.
  - On pairs where at least one annotator saw a difference, they ordered the two candidates the same way in 60% of Chinese pairs (47/78), but only 25% in English (6/24) and 42% in Hindi (5/12). There, the differences are a few minor errors and not reliable one by one.
  - System-level conclusions hold under both; segment-level ones do not.

**Kumārajīva is not a fair benchmark for fidelity to the Tibetan.** His version scores worst: 10 major errors (Claude) and 31 (Gemini) in 40 segments. Almost all are omissions measured against the Tibetan, such as shortened lists of practices and the dropped epithets "arhat, perfectly complete Buddha". Kumārajīva translated a shorter Sanskrit text in a famously concise style, so this measures distance from the Tibetan, not the quality of his translation. A fair human benchmark needs a translation made from the Tibetan, which the vault does not have for this text.

**Limits.**
- 40 segments per language is a small sample.
- Both annotators are language models, without a specialist.
- Claude's English and Hindi annotations found almost no errors in any system, so they cannot separate the systems there.
- The annotation files are in `blind-eval/`: `score.py` unblinds with `key.json` and recomputes every figure above.

## 4. Still to do for this text

- **Specialist scoring of the blind sample:** the 40 blind segments, already annotated by both models, scored by a specialist. This would test the AI annotators and settle the segment-level disagreements.
- **A human translation made from the Tibetan,** as a fair human benchmark. Kumārajīva translated a different source text.
- **Specialist review time:** the hours a specialist needs to bring the governed versions to publication. This is the number that decides the cost comparison with human translation (section 2). No specialist time has been spent so far, apart from the editor decisions recorded in the glossary overrides.

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
