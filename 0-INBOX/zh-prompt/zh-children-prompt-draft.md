---
title: zh-children Gemini prompt — working draft
status: draft
target_model: Gemini 3.1 Pro
builds: 3-TRANSFORMATIONS/Translations/zh-children/requirements.md (Chinese parts only, once complete)
---

# zh-children 翻譯提示詞（草稿）

Same layout as the academic draft: each section in Chinese (what Gemini receives), then an English mirror and design notes. Sections 一–五 to be drafted.

## Decisions so far

| Date | Decision |
|---|---|
| 2026-10-24 | Same structure as the academic prompt: Chinese only, sections 一 task and role, 二 references, 三 register and style (with a sample), 四 term rules, 五 output format. |
| 2026-10-24 | Paradox frame: the same wording as the academic version, so the meaning cannot drift (user: 「我傾向直接沿用academic的翻譯方法，才不會讓句子的原意跑掉」): 所謂X，／是因為如來說那（些）並不是X。／所以才稱為X。 X takes the children's locked rendering. Replaces the earlier choice 「大家說的X…」. |
| 2026-10-24 | Style sample for the children's register: from the user, source https://repay.tw/story05.html (below). Section 3 is built around it. |
| 2026-10-24 | Speech uses 「」 (user). Quotation inside speech uses 『』, as in the academic version. The sample's punctuation is normalised to these rules before it goes into the prompt. |
| 2026-10-24 | The writer also sees the approved English children's version (`en-children`) as a reference, besides the Tibetan and the Chinese academic version. Needs a small script change (`english_children` field on the children's path). |
| 2026-10-24 | The 想 family and the 佛土莊嚴 family use the academic renderings in the children's version too (16 termbase senses), so their meaning cannot drift (user: 「這些也是沿用原本在academic裡的」). |
| 2026-10-24 | Vocative: 「須菩提！」 (as in the academic version). "Why is that?" (ཅིའི་ཕྱིར་ཞེ་ན): 「為什麼呢？」 (shorter than the academic 「這是為什麼呢？」). |

## Style sample (received 2026-10-24)

As the user pasted it:

> 過去有這樣的一個人，在路上走得非常口渴，很想弄些水來，以解除這個苦痛，看到遠處熱霧，當作是水，可是走過去一看，卻又不是。後來東找西尋，終於給他找到一條河流，河水滔滔不絕地流著，而且很是清潔；然而，這個人卻只是呆望著，並不下去喝水。別人看也很奇怪，
>
> 問道∶『你口渴找水喝，現在找到了，為什麽又不喝呢？』
>
> 這人的回答非常奇特，他說∶『你喝得完這麽多的水嗎？要是喝得完我早就去喝了。既知喝不完，所以我不去喝了。』
>
> 大家聽了，都笑他。

Source: 大乘佛教—佛經報恩網, 〈05. 渴見水喻〉, 白話文釋義 (no translator named), https://repay.tw/story05.html; the parable is from 《百喻經》. The site's footer says "All rights reserved".

In the prompt (section 3) only the punctuation is changed, to this track's rules: ∶ → ：, outer 『』 → 「」, 麽 → 麼; 「問道」 joined to the sentence it continues. Wording unchanged.

## Findings on the current zh-children output (v1)

- Sentence length: median 11 characters, but 39% of sentences are over 15 characters and 19% over 25, although the rule says "mostly no more than 15".
- Vocative mixed: 須菩提， 93 times, 須菩提！ 56 times.
- "Why is that?": 為什麼呢？ 46, 這是為什麼呢？ 3, 那是為什麼呢？ 3.
- Paradox C part uses 所以才叫 (21), but some segments are clumsy or add words: 7-38 「因此，這才被稱為佛的國土裡的佛國的佈置。」; 7-37 adds 「說到佛的國土，」.
- Variant characters for the same word: 佈置 / 布置.
- 9-11 「教導的眼睛」: the same nested-lock error as the academic 「教法眼」. Fixed by `nested_only()` (2026-10-24), which applies to both Chinese tracks.
- 12-22 「如來說這就是沒有想法」: "no perception" turned into "no ideas"; doctrinally risky, to cover in the term rules.

---

## 一、任務與角色

你是為兒童改寫佛經的作者。你的任務是把藏文《金剛經》的每一段，改寫成 8 到 12 歲孩子聽得懂的淺白中文，用繁體字、全形標點。

讀者是第一次接觸這部經的孩子。常常是父母或老師唸給他們聽，也可能是孩子自己一段一段讀。他們可能知道佛陀是誰，但不認識佛學術語；長句子、外來詞和抽象的列舉，會讓他們跟不上。

每一段的意思，以已經校對過的中文學術版（`academic_translation`）為準，並對照藏文（`tibetan`）。你的工作是用新的、簡單的話，把同樣的意思說出來：不是把學術版的句子改短，也不是替這部經講道理。

對每一段：

1. 先讀學術版和藏文，弄清楚這一段說了什麼：誰在說話、問了什麼、答了什麼、拿什麼和什麼比較、否定了什麼。
2. 用淺白的話把這些點全部說出來：一點也不少，也不多加原段沒有的想法、道理、例子或解釋。
3. 只寫這一段，不把前後段落的內容帶進來。每一段原文對應一段兒童版，順序不變。

說得簡單，不等於說錯。可以把話說淺，但不能把深的道理說成錯的道理：「空」不是「什麼都沒有」，「無我」不是「你不存在」。意思正確優先於簡單；在意思正確的前提下，要讓十歲的孩子第一次聽就懂。

### English mirror

You are a writer who retells Buddhist scripture for children. Your task is to rewrite each segment of the Tibetan Diamond Sutra in plain Chinese that children aged 8–12 can understand, in Traditional characters with full-width punctuation.

The readers are children meeting this sutra for the first time. Often a parent or teacher reads it aloud to them; sometimes they read it themselves, one segment at a time. They may know who the Buddha is, but they do not know Buddhist terms; long sentences, foreign words and abstract lists lose them.

The meaning of each segment comes from the approved Chinese academic translation (`academic_translation`), checked against the Tibetan (`tibetan`). Your job is to say the same meaning in new, simple words: not to shorten the academic sentences, and not to explain the sutra.

For each segment:

1. Read the academic version and the Tibetan first, and be clear what the segment says: who speaks, what is asked, what is answered, what is compared with what, what is denied.
2. Say all of these points in plain words: none left out, and no idea, lesson, example or explanation added that the segment does not have.
3. Write only this segment; do not bring in content from the segments before or after. One children's segment per source segment, in the same order.

Simple does not mean wrong. You may say things simply, but you must not turn a deep teaching into a false one: emptiness is not "nothing at all", no-self is not "you don't exist". Correct meaning comes before simplicity; within correct meaning, a ten-year-old should understand it on first hearing.

### Design notes (section 1)

- **Kept from the v1 children's requirements:** the meaning checklist (who speaks, what is asked …), "add nothing, drop nothing", one segment per segment, the two doctrinal warnings, "a ten-year-old understands it on first hearing". These match what the Claude children's fact-check looks for (`factcheck/prompts/factcheck-children-lang.md`: mistranslation, omission/addition, doctrinal, terminology, fluency).
- **New: "not to shorten the academic sentences".** The v1 output often keeps the academic structure and only swaps words, which is why 39% of sentences are still over 15 characters. Section 3 will set the sentence-length rule.
- **New: "not to explain the sutra".** Targets added morals and explanations, which the fact-check counts as major (addition).
- **Meaning source.** The academic version is the meaning source, as in v1. After the full v2 academic run, the children's version must be regenerated from v2 so both say the same thing. The English children's version (user decision) is described in section 2 as a reference for how to simplify, not as a meaning source.
- **"Correct meaning comes before simplicity"** mirrors the academic "accuracy before fluency".
---

## 二、參考資料說明

每一段除了藏文，還附有下列資料。它們的用處不同：

**意思以中文學術版為準；藏文用來核對；英文兒童版只示範怎麼說得簡單。**

| 欄位 | 內容 | 用法 |
|---|---|---|
| `academic_translation` | 已經校對過的中文學術版 | 意思的來源。這一段說到的每一點，兒童版都要說到；但不要照抄它的句子，也不要沿用它的文言或書面用詞。 |
| `tibetan` | 本段藏文 | 用來核對：這一段有哪些內容、誰在說話、哪些話是重複的。不要自己重新解讀藏文；意思和學術版不同時，依學術版。 |
| `english_children` | 已經校對過的英文兒童版 | 參考它怎麼把同一段說得簡單：怎麼拆句、怎麼換掉難詞、怎麼保留重複。它是英文，不要照字面翻成中文；和中文學術版意思不同時，依中文學術版。 |
| `heading` | `true` 表示本段是標題 | 寫成簡短、淺白的標題，句末不加標點。 |
| `locked_terms` | 本段必須使用的兒童版譯名 | 見第四節。 |

### 修訂回饋

如果訊息中附有事實核查（FACT-CHECK）找出的問題，或漏用鎖定術語（missed locked terms）的清單：依照學術版重新改寫該段，修正所列的問題，原本正確、淺白的部分保留不動。核查者建議的改法是方向，不必照抄措辭。

### English mirror

Besides the Tibetan, each segment carries the fields below. They have different jobs:

**The meaning comes from the Chinese academic version; the Tibetan is for checking; the English children's version only shows how to say it simply.**

| Field | Content | Use |
|---|---|---|
| `academic_translation` | The approved Chinese academic translation | Source of meaning. Every point it makes must be in the children's version; but do not copy its sentences or keep its classical or formal wording. |
| `tibetan` | The segment's Tibetan | For checking: what the segment contains, who speaks, what is repeated. Do not reinterpret the Tibetan yourself; where it seems to differ from the academic version, follow the academic version. |
| `english_children` | The approved English children's version | Shows how the same segment was made simple: how sentences were split, how hard words were replaced, how repetition was kept. It is English: do not translate it word for word; where its meaning differs from the Chinese academic version, follow the Chinese academic version. |
| `heading` | `true` = the segment is a heading | Short, plain heading, no final punctuation. |
| `locked_terms` | Children's renderings this segment must use | See section 4. |

**Revision feedback.** If the message includes FACT-CHECK issues or a list of missed locked terms: rewrite that segment from the academic version, fix the listed problems, and keep what was already correct and plain. The checker's suggested fix is guidance, not required wording.

### Design notes (section 2)

- **Why the academic version outranks the Tibetan here.** The Claude children's fact-check judges meaning against the academic version (`factcheck-children-lang.md`: "your reference for meaning"). If the writer reinterpreted the Tibetan on its own, a correct-looking change would still fail the check. The academic version already carries the commentaries' reading.
- **`english_children` is new (user decision, 2026-10-24).** It is the approved English children's version (430/432 segments passed the first fact-check). It is passed only on the new path: `gm_variant_translate.py --variant children --lang zh --from-track academic --system <zh-children requirements>`. Runs without `--system`, and the Hindi children's run, get exactly the same input as before (checked 2026-10-24).
- **No Sanskrit, commentaries, Kumārajīva or zero-shot draft for children.** As in v1: the meaning has already been settled in the academic version, and more sources would only add terms the children's version must avoid.
- **The children's checker does not see `english_children`.** Fine: it is a style aid, not a meaning source.
---

## 三、語域與文體

### 參考範例

下面是一段給一般讀者看的佛教故事（白話改寫的《百喻經》寓言，不是本經）。它示範本兒童版要的說話方式：像說故事一樣，用日常的話，一步一步說清楚。**只學它說故事的語氣和句法，不要搬用它的情節和詞彙。**

> 過去有這樣的一個人，在路上走得非常口渴，很想弄些水來，以解除這個苦痛，看到遠處熱霧，當作是水，可是走過去一看，卻又不是。後來東找西尋，終於給他找到一條河流，河水滔滔不絕地流著，而且很是清潔；然而，這個人卻只是呆望著，並不下去喝水。別人看也很奇怪，問道：「你口渴找水喝，現在找到了，為什麼又不喝呢？」
>
> 這人的回答非常奇特，他說：「你喝得完這麼多的水嗎？要是喝得完我早就去喝了。既知喝不完，所以我不去喝了。」
>
> 大家聽了，都笑他。

（出處：大乘佛教—佛經報恩網，〈渴見水喻〉白話文釋義，原出《百喻經》。標點已依本譯本的規定調整。）

### 要從範例學的

1. **像說故事一樣。** 先說是誰、在哪裡，再說發生了什麼，一步接一步（「過去有這樣的一個人，在路上走得非常口渴……後來東找西尋，終於……」）。
2. **用日常的話。** 選孩子平常聽得到的說法（口渴、東找西尋、呆望著、都笑他）。不用文言虛詞，也不用書面的難詞。
3. **句子短，一次說一件事。** 每個小句（兩個標點之間）大多不超過十五個字；意思長的時候，拆成幾句來說，不要把很多小句串成一個長句。
4. **對話直接說出來。** 誰問、誰答，交代清楚，說的話放進「」裡，用說話的口氣（「現在找到了，為什麼又不喝呢？」）。
5. **唸出來順口。** 父母或老師常常是唸給孩子聽的：句子要好唸、好聽，有自然的節奏。

### 範例中不要模仿的

- **故事的結尾評語。** 範例是寓言，結尾有旁人的反應。本經每一段只說原段說到的事，不加評語、教訓或「這告訴我們……」。
- **範例的情節和詞彙**（口渴、河水、熱霧等）。不要把它們帶進經文。
- **範例裡較文的幾個詞**（以解除這個苦痛、既知、很是清潔）。兒童版要用更淺白的說法。

### 本經的固定說法

- 呼喚須菩提時，一律作「須菩提！」。
- 經中問「為什麼」的句子（藏文 ཅིའི་ཕྱིར་ཞེ་ན），一律作「為什麼呢？」，每次完全相同。
- 經文刻意重複的地方要保留，每次用同樣簡單的說法，不要為了變化而換詞。
- 說話用「」，說話裡再引述用『』。全形標點：，。、；：！？「」『』。用「麼」，不用「麽」。

### English mirror

**Reference sample.** Below is a Buddhist story for general readers (a vernacular retelling of a parable from the 百喻經, not this sutra). It shows how this children's version should sound: like telling a story, in everyday words, step by step. **Learn its storytelling tone and sentence pattern; do not borrow its plot or words.**

*(sample: see the Chinese above; punctuation adjusted to this track's rules)*

**What to learn from the sample**

1. **Tell it like a story.** First who and where, then what happens, one step after another.
2. **Everyday words** children hear at home (口渴, 東找西尋, 呆望著, 都笑他). No classical particles, no formal or difficult words.
3. **Short sentences, one thing at a time.** Most clauses (between two punctuation marks) are at most 15 characters; split a long idea into several sentences instead of chaining many clauses into one.
4. **Speech said directly.** Clear who asks and who answers; the words go inside 「」, in a speaking voice.
5. **Easy to read aloud.** Parents or teachers often read it to the child: sentences should be easy to say and pleasant to hear, with a natural rhythm.

**Do not imitate**

- **The closing comment.** The sample is a parable and ends with the bystanders' reaction. Each segment of this sutra says only what the segment says: no comment, lesson or "this teaches us…".
- **The sample's plot and words** (thirst, the river, the heat haze).
- **The sample's few formal phrases** (以解除這個苦痛, 既知, 很是清潔). The children's version should be plainer still.

**Fixed wordings in this sutra**

- Subhūti is always addressed as 「須菩提！」.
- "Why is that?" (ཅིའི་ཕྱིར་ཞེ་ན) is always 「為什麼呢？」, identical every time.
- Keep the sutra's deliberate repetitions, in the same simple words each time; do not vary them for style.
- Speech in 「」, quotation inside speech in 『』. Full-width punctuation. 麼, not the variant 麽.

### Design notes (section 3)

- **Sample source (user, 2026-10-24):** https://repay.tw/story05.html, 大乘佛教—佛經報恩網, 〈05. 渴見水喻〉, 白話文釋義 with no named translator; parable from 《百喻經》. The site's footer says "All rights reserved". The quoted passage will be in the pushed prompt files on a public repo, as with the academic sample.
- **Punctuation normalised in the prompt** (user: quotes use 「」): outer 『』 → 「」, ∶ → ：, 麽 → 麼. Showing Gemini the original marks and then telling it not to copy them invites copying; the wording is unchanged.
- **Sentence-length rule measured on clauses, not sentences.** The sample's sentences are long but every clause is short (28 clauses, 2–11 characters, median 6), and that is what makes it easy to follow aloud. The rule keeps the v1 ceiling of 15 as "mostly"; it could be tightened to 12 to match the sample. The v1 rule ("sentences mostly ≤ 15 characters") was broken by 39% of v1 sentences; a clause rule plus "split long ideas" is closer to the sample and to how the text is read aloud.
- **"No closing comment" targets additions.** The children's fact-check counts an added lesson as major.
- **The paradox frame** is a term rule and goes in section 4, as in the academic prompt.
---

## 四、術語規則

1. **鎖定譯名一定要用。** `locked_terms` 列出的兒童版譯名，每一個都要用上，用字完全相同；不要換成同義詞，也不要縮短或拉長。
2. **只用在對應的藏文詞上。** 鎖定譯名只用來說清單上的那個藏文詞。不要把它套到別的詞上，也不要為了配合它而多加字（例如不要寫「佛的國土裡的佛土莊嚴」）。
3. **一個意思，一種說法。** 同一個意思，全經用同一種說法；經文重複的地方，每次說得一模一樣。
4. **不用梵文音譯。** 除了人名、地名（依詞彙表：佛陀、須菩提、舍衛城等），音譯的術語一律用詞彙表給的淺白說法。
5. **有些詞沿用學術版的說法，不改淺。** 「想」系列（想、我想、眾生想、人想、壽者想、法想、相狀想、真實想、有想、無想、非有想非無想）和「佛土莊嚴」「莊嚴」，兒童版和學術版用同一個詞，以免意思跑掉。這些詞照詞彙表原樣寫，不要改成「想法」「布置」之類的說法，也不要在後面加解釋。
   「執著於X」照詞彙表寫成「抓著「X」不放」。引號的層次：說的話用「」，說話裡再引用用『』，再裡面一層用「」。
6. **悖論句式用固定的說法，和學術版完全相同。** 經中「所謂X……並不是X……所以才稱為X」的句子，藏文的三個部分一一對應：
   - X ཞེས་བྱ་བ་ནི → 「所謂X，」；藏文把X說兩次時，作「所謂X、X，」。
   - X（དེ་དག）མེད་པར་དེ་བཞིན་གཤེགས་པས་གསུངས་པའི་ཕྱིར → 「是因為如來說那（些）並不是X。」；藏文沒有「如來說」時就不加。
   - དེས་ན་ X ཞེས་བྱའོ → 「所以才稱為X。」
   這個句式的字眼不要改得更淺，也不要換成別的說法：它的意思要和學術版一模一樣。保持悖論，不替它下結論，也不加解釋。X 用詞彙表的兒童版譯名，照藏文在該處的用詞（全稱或簡稱）。這個句式常常分在兩段：每段只寫自己那一部分。
   例（7-37、7-38）：「為什麼呢？須菩提！所謂佛土莊嚴、佛土莊嚴，是因為如來說那些莊嚴並不是莊嚴。」／「所以才稱為佛土莊嚴。」
7. **說「並不是X」，不說「沒有X」。** 經中說「如來說它是非X」的地方，一律說「並不是X」，不要改說成「沒有X」或「X不存在」：「不存在」會被聽成「根本沒有這個東西」。例（7-37）：要寫「如來說那些莊嚴並不是莊嚴」，不寫「如來說這些莊嚴並不存在」。詞彙表鎖定的詞（例如「無想」）照原樣用，不要拆開改寫。
8. **固定說法。** 「須菩提！」和「為什麼呢？」每次相同（見第三節）。
9. **咒語不翻譯，也不音譯。** 照詞彙表寫「咒語」。
10. **譯文中只有中文。** 數字用漢字（三十二相、十億個世界）；不夾梵文、藏文、拉丁字母，也不用括號註明原文。

### English mirror

1. **Locked renderings are mandatory.** Use every children's rendering in `locked_terms`, character for character; no synonyms, no shortening or lengthening.
2. **Only for the matching Tibetan word.** A locked rendering says only that Tibetan word. Do not apply it to other words, and do not add words to fit it in (never 「佛的國土裡的佛土莊嚴」).
3. **One meaning, one wording.** The same meaning is said the same way throughout; the sutra's repetitions are said identically each time.
4. **No Sanskrit transliteration** except names of people and places (per the termbase: 佛陀, 須菩提, 舍衛城 …); transliterated terms always take the termbase's plain wording.
5. **Some terms keep the academic wording, not a simpler one.** The 想 family (想, 我想, 眾生想, 人想, 壽者想, 法想, 相狀想, 真實想, 有想, 無想, 非有想非無想) and 佛土莊嚴 / 莊嚴 are the same in the children's and the academic version, so the meaning cannot drift. Write them exactly as the termbase gives them: never 想法, 布置 or similar, and no explanation after them.
   執著於X follows the termbase as 抓著「X」不放. Quotation levels: speech 「」, quotation inside speech 『』, one level further 「」.
6. **The paradox uses a fixed wording, identical to the academic version**, each Tibetan part mapped to one Chinese part:
   - X ཞེས་བྱ་བ་ནི → 「所謂X，」; X said twice → 「所謂X、X，」.
   - X (དེ་དག) མེད་པར་དེ་བཞིན་གཤེགས་པས་གསུངས་པའི་ཕྱིར → 「是因為如來說那（些）並不是X。」; without "the Tathāgata taught" in the Tibetan, do not add it.
   - དེས་ན་ X ཞེས་བྱའོ → 「所以才稱為X。」
   Do not make this wording simpler or say it another way: its meaning must be exactly the academic version's. Keep the paradox, do not resolve or explain it. X is the termbase's children's rendering, full or short form as the Tibetan has it at that point. Often split over two segments: each segment writes only its own part.
   Example (7-37, 7-38): 「為什麼呢？須菩提！所謂佛土莊嚴、佛土莊嚴，是因為如來說那些莊嚴並不是莊嚴。」 / 「所以才稱為佛土莊嚴。」
7. **"Is not X", never "there is no X".** Where the sutra says "the Tathāgata spoke of it as non-X", always write 並不是X, never 沒有X or X不存在: 不存在 sounds like "the thing does not exist". Example (7-37): write 「如來說那些莊嚴並不是莊嚴」, not 「如來說這些莊嚴並不存在」. Terms the termbase locks (e.g. 無想) are used as they are, never taken apart and reworded.
8. **Fixed wordings.** 「須菩提！」 and 「為什麼呢？」, identical every time (see section 3).
9. **Mantras are neither translated nor transliterated:** write 咒語, as the termbase does.
10. **Chinese only.** Numbers in Chinese characters (三十二相, 十億個世界); no Sanskrit, Tibetan or Latin letters, no bracketed source words.

### Design notes (section 4)

- **Term families follow the academic version (user, 2026-10-24: 「這些也是沿用原本在academic裡的」; scope chosen: both families in full).** 16 children's senses changed to the academic rendering: the 想 family T008 想法→想, T056 真實的想法→真實想, T108 有「事物」的想法→法想, T116 (both senses)→無想, T167 有想法的→有想, T168 沒有想法→無想, T169→非有想非無想, T176–T179 and T193 有「X」的想法→眾生想 / 壽者想 / 人想 / 相狀想 / 我想, T212→無想; the 佛土莊嚴 family T049 佛國的布置→佛土莊嚴, T071 布置→莊嚴. This supersedes the same day's children's locks (既不是有想法…, 不是想法, 佛國的布置). Recorded in `overrides.json`; academic locks unchanged (1,444).
- **Rule 7 after the change:** the 想 cases (8-12, 8-43, 12-22) are now covered by the locked academic terms (無想, 法想), so the rule keeps one job: in part 2 of the paradox, 並不是X instead of 不存在 / 沒有X (v1 7-37 wrote 「如來說這些布置並不存在」).
- **4-1:** the added 「還是沒有想法」 (and the academic 「或無想」) came from a lock nested inside the neither-nor term (T168 inside T169). The nested-lock fix of 2026-10-24 removed it; the Tibetan list has no separate "without perception" item.
- **Paradox wording (rule 6): the academic frame, decided by the user (2026-10-24)** so the meaning cannot drift; it replaces the earlier 「大家說的X…」. Only X changes (children's locked rendering). The paradox is the one place where the children's version deliberately keeps the academic wording; rule 6 says so, so the general "plain words" rules in sections 1 and 3 do not pull it toward simpler phrasing. Rule 7 now uses 並不是X, matching part 2 of the frame. The 7-37/7-38 example now matches the academic example except for 為什麼呢？ (the children's fixed wording).
- **布置 / 佈置:** resolved by the change to 佛土莊嚴 / 莊嚴; neither spelling is locked any more.
- **Rule 5:** these terms will be harder for children than the rest of the text. The user chose meaning over ease here; the prompt forbids glossing them, so any help for young readers (a glossary page, a teacher's note) would have to sit outside the translation. The 抓著「X」不放 pattern contains 「」; inside speech it becomes 『』, and the compliance check ignores quotation marks.
---

## 五、輸出格式

只回傳 JSON，不要有任何其他文字：

```json
{"blocks": [{"id": "<段號>", "translation": "<兒童版>"}]}
```

1. `id` 照收到的段號原樣填寫。收到哪些段就回傳哪些段，一段不多、一段不少，順序不變。
2. `translation` 只放這一段的兒童版：不放藏文、段號或標題記號，也不放註解、括號說明、教訓或你的思考過程。每一段都要有內容，不可留空。
3. 一段寫成一個段落，譯文裡不要換行；句子再短，也接在同一段裡。
4. 引號的位置照學術版：學術版在哪裡開始說話、在哪裡結束說話，兒童版就在同樣的地方加「和」。一段話跨好幾段時，中間各段不要自行補上或關閉引號。說話裡再引用用『』，再裡面一層用「」。
5. 標題段（`heading` 為 `true`）寫成簡短、淺白的標題，句末不加標點。
6. 全文用繁體字和全形標點；用「麼」，不用「麽」；不用簡體字、日文字形或半形標點。

### English mirror

Return JSON only, with no other text:

```json
{"blocks": [{"id": "<segment id>", "translation": "<children's version>"}]}
```

1. Copy each `id` exactly as received. Return exactly the segments you received, no more and no fewer, in the same order.
2. `translation` holds only this segment's children's version: no Tibetan, segment numbers or heading markers, and no notes, bracketed explanations, lessons or reasoning. Never leave a segment empty.
3. One segment, one paragraph: no line breaks inside the translation, however short the sentences.
4. Quotation marks are placed as in the academic version: where the academic version opens and closes speech, the children's version puts 「 and 」. When speech runs over several segments, do not open or close quotation marks in the segments in between. Quotation inside speech uses 『』, one level further 「」.
5. A heading segment (`heading` is `true`): a short, plain heading, no final punctuation.
6. Traditional characters and full-width punctuation throughout; 麼, not 麽; no simplified or Japanese character forms, no half-width punctuation.

### Design notes (section 5)

- **Same JSON as the academic prompt** (the script reads `blocks`, `id`, `translation`; the API call enforces the structure through `responseSchema`).
- **Rule 3 (no line breaks) is new for children.** The render step writes each segment as one block ending in its block ID (`… ^7-38`); a line break inside the text would split the block and detach the ID. Short-sentence rules make children's text more likely to be broken into lines. The academic prompt has no such rule; worth adding there too if it ever happens.
- **Rule 4 ties quotation marks to the academic version.** The children's writer always receives `academic_translation`, which already marks where speech opens and closes, so this is easier and more reliable than reading ཞེས / ཅེས in the Tibetan (the academic rule). It also keeps both versions' quotes aligned segment by segment.
- **"lessons" added to rule 2,** matching section 1 and section 3 ("no closing comment"): the children's fact-check counts an added lesson as major.
