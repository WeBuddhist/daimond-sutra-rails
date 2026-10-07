You are setting the shared conventions for the Hindi (Devanagari) glossary (termbase) of the Tibetan Diamond Sutra (Vajracchedikā). An English glossary for the same Tibetan terms is already approved; the Hindi (Devanagari) glossary must keep its sense distinctions but choose the right Hindi (Devanagari) words. Several agents will fill in the glossary in parallel; your style sheet keeps them consistent. Work only from the files named here; no web search.

Read:
- /Users/tashitsering/Desktop/work/Obsidian/KF-project/daimond-sutra-rails/0-INBOX/kf-pilot/termbase/registers-hi.md: the two Hindi (Devanagari) registers (academic, children's).
- /Users/tashitsering/Desktop/work/Obsidian/KF-project/daimond-sutra-rails/0-INBOX/kf-pilot/termbase/vajracchedika-hi/overview.md: every term — Tibetan, Sanskrit, occurrence count, and the approved English academic / children's rendering for each sense.
- /Users/tashitsering/Desktop/work/Obsidian/KF-project/daimond-sutra-rails/0-INBOX/kf-pilot/termbase/vajracchedika-hi/terms.json: the term packets, whose examples show the Tibetan segment and a Gemini zero-shot Hindi line (`gemini_zero_shot`).

Write a style sheet in Markdown to /Users/tashitsering/Desktop/work/Obsidian/KF-project/daimond-sutra-rails/0-INBOX/kf-pilot/termbase/vajracchedika-hi/style-sheet.md with exactly these sections:

## Policies
Numbered cross-cutting decisions, one line each with a short reason. Cover at least: script and punctuation; which established Hindi (Devanagari) Buddhist terms are used in the academic register and how attested usage is weighed (Sanskrit tatsama terms vs everyday Hindi vs the Gemini zero-shot); how the two senses of ཆོས are kept apart; how epithets of the Buddha and titles are rendered; names; the cosmological measure; how the children's register simplifies technical terms without changing their meaning; how compounds take their parts' renderings.

## Core terms
A table of the 30–50 terms whose renderings other terms build on, with columns: | Tibetan | Sense | Academic | Children's | Reason |. Use the exact Tibetan and sense labels from the overview.

Final reply: one line — number of policies and core terms.
