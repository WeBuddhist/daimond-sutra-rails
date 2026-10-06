# Pair review: dorjeechoepa-root-sa(sa-bo) vs dorjeechoepa-root-bo(sa-bo)

Method: all 434 row pairs read in full (row N of Sanskrit "SA" against row N of Tibetan "BO"). Both files have exactly 434 rows.

## Verdict
Rows 1-229 and 328-434 are paired correctly, apart from the small local irregularities below.
There is ONE long drift, at a constant offset of exactly one row (it never grows to two): **rows 230-327, where BO row N renders SA row N-1.** The earlier suspicion (drift from about 229) is confirmed. The "later two" is not present in this copy.

## 1. Main drift: rows 230-327 (offset +1, BO ahead of SA)

Cause. BO 230 ("'di'i rnam par smin pa yang bsam gyis mi khyab pa nyid du rig par bya'o", the *acintya vipaka* sentence) is an extra Tibetan row. It sits in the Tibetan after "chos kyi rnam grangs 'di ni bsam gyis mi khyab" (BO 229). The same sentence appears again verbatim at BO 253. The Sanskrit has it only once, at SA 252 (*asya acintya eva vipakah pratikankshitavyah*). So:
- SA 229 / BO 229: correct (*acintyo 'tulyo 'yam dharmaparyayah* / "bsam gyis mi khyab ... mtshungs pa med de").
- SA 230 (*ayam ca subhute dharmaparyayas ... agrayana ... shreshthayana*) / BO 230 (vipaka sentence): WRONG. The correct Tibetan for SA 230 is BO 231 ("theg pa mchog la ... theg pa phul du phyin pa").
- Then, consistently, SA N is rendered by BO N+1 for N = 230 to 326.

Anchor checks (BO row -> SA row it renders), confidence high for all:
- BO 231 -> SA 230 (theg pa mchog; agrayana)
- BO 232 -> SA 231 (len pa, 'dzin pa ... mkhyen, gzigs; jnatah ... drshtah)
- BO 233 -> SA 232; BO 234 -> SA 233 (bsam gyis mi khyab pa dang mi mtshungs; acintyena atulyena)
- BO 235 -> SA 234 (byang chub phrag pa la thogs; samamshena bodhim)
- BO 236-239 -> SA 235-238 (dman pa la mos pa; hinadhimuktikaih ... nedam sthanam vidyate)
- BO 240 -> SA 239 (mchod pa bya bar 'os; pujaniyah)
- BO 241 -> SA 240 (phyag bya bar 'os, bskor ba; vandaniyah pradakshiniyah)
- BO 242 -> SA 241 (mchod rten lta bur; caityabhutah)
- BO 243 -> SA 242 (mnar bar 'gyur; paribhutah); BO 244 -> SA 243 (shin tu mnar; suparibhutah)
- BO 245-246 -> SA 244-245 (ngan song du skye ba ... sangs rgyas kyi byang chub; buddhabodhim)
- BO 247-250 -> SA 246-249 (mar me mdzad; ma mnyes par ma byas; stong gi cha ... dpe dang zla)
- BO 251 -> SA 250 (myo myor 'gyur; unmadam); BO 252 -> SA 251; BO 253 -> SA 252 (vipaka)
- BO 254 -> SA 253 (atha khalv ayushman subhutih ...)
- BO 255 -> SA 254; BO 256 -> SA 255; BO 257 -> SA 256 (katham sthatavyam / pratipattavyam / cittam pragrahitavyam)
- BO 258 -> SA 257 (bhagavan aha)
- BO 259-263 -> SA 258-262 (iha subhute ... parinirvapya ... nasti sa kashcid dharmo bodhisattvayana-)
- BO 264-274 -> SA 263-273 (Dipamkara passage; vyakrta; tathagata = bhutatathata)
- BO 275 -> SA 274 (gang la la zhig 'di skad du ... rdzun du smra; vitatham vadet)
- BO 276 -> SA 275 (SA 275 is EMPTY; BO 276 "de de bzhin gshegs pas byang chub sems dpa' byang chub sems dpa' zhes brjod do" has no evident Sanskrit counterpart; low confidence on what this line is)
- BO 277-281 -> SA 276-280 (nasti ... na satyam na mrisha; sarvadharma buddhadharma)
- BO 282-293 -> SA 281-292 (upetakaya mahakaya; nirat-mano dharmah; kshetravyuha; "chos rnams bdag med")
- BO 294-310 -> SA 293-309 (the five eyes: mamsa-, divya-, prajna-, dharma-, buddha-cakshuh)
- BO 311 (EMPTY) <-> SA 310 (long *Ganga-valuka* question "bhagavan aha ... bhashitah tathagatena valukah"): the Tibetan has no text for SA 310; BO 311 is an empty placeholder.
- BO 312-327 -> SA 311-326 (Ganga sand worlds; cittadhara; atitam/anagatam/pratyutpannam cittam nopalabhyate; trisahasra worlds of seven jewels; "bahu ... punyaskandham")

Re-synchronisation at row 328:
- SA 326 -> BO 327. SA 327 (*tatkasya hetoh punyaskandhah punyaskandha iti subhute askandhah sa tathagatena bhashitah*) has NO Tibetan counterpart; the Tibetan canon omits this explanation.
- BO 328 ("yang rab 'byor gal te bsod nams kyi phung po bsod nams kyi phung por gyur pa na ... mi gsung ngo") renders SA 328 (*sacet punah subhute punyaskandho 'bhavishyat ...*). From here BO N = SA N again (confirmed 328, 329, 330 ... 374). High confidence.

Suggested repair (not applied): treat BO 230 as an inserted/duplicate Tibetan row (delete it, or put an empty SA row opposite it), and give SA 327 an empty Tibetan row. Doing both restores a 1:1 pairing for 231-326 with no residual offset.

## 2. Local irregularities (no lasting drift)

- Rows 85-87: SA 85 *bahu sugata sa kulaputro ... prasunuyat* is rendered by BO 85 ("bde bar gshegs pa mang lags so") plus BO 86 ("rigs kyi bu ... bsod nams mang du bskyed do"). BO 87 renders SA 86 + 87 together ("de ci'i slad du zhe na ... phung po ma mchis pa'i slad du"). SA 88 / BO 88 correct. Medium confidence, harmless.
- Rows 121-124: BO 121-122 spread SA 121 across two rows; BO 123-124 are fine. Harmless.
- Rows 375-376: SA 375 (*yathaham bhagavato bhashitasyartham ajanami*) has no Tibetan. BO 375 ("mtshan phun sum tshogs pas ... mi bgyi lags so") renders SA 376 (*na lakshanasampada tathagato drashtavyah*). BO 376 is empty. Pairing should be SA 376 <-> BO 375. High confidence.
- Rows 378-379: SA 378 (*evam etad yatha vadasi*) has no Tibetan. BO 378 ("mtshan phun sum tshogs pas ... mi bya ste") renders SA 379. BO 379 is empty. Pairing should be SA 379 <-> BO 378. High confidence.
- Rows 419-420: SA 419 (*na samyag vadamano vadet*) has no Tibetan. BO 419 ("de ci'i slad du zhe na ... bdag tu lta ba ... lta ba ma mchis par") renders SA 420 (*tatkasya hetoh ya sa bhagavan atmadrishtih ... adrishtih*). BO 420 is empty. Pairing should be SA 420 <-> BO 419. High confidence.
- Rows 428-431: SA 428 (*tadyatha akashe-*, lead-in to the verse) has no Tibetan. BO 428 ("des na yang dag par rab tu ston pa zhes bya'o") renders SA 430 (*tatha prakashayet, tenocyate samprakashayed iti*). BO 429 (verse "skar ma rab rib mar me dang") <-> SA 429 is correct. BO 430 ("bcom ldan 'das kyis de skad ces bka' stsal nas ... yi rangs te") renders SA 431 (*idam avocad bhagavan attamanah ...*). BO 431 is empty. SA 432/BO 432 and 433/433 are correct. Order is therefore: SA 430 <-> BO 428, SA 431 <-> BO 430. High confidence.
- Row 215-216: SA 215 and 216 both say "do not give attached to form etc."; BO 215 renders the sense and BO 216 is empty. No shift (SA 217 <-> BO 217 is correct).
- Rows 108-109: SA empty, BO has the Tibetan of the stock sentence "gal te lan cig phyir 'ong ba ... bdag tu 'dzin par 'gyur lags so" (the sakrdagamin version of the formula). The Sanskrit omits it. No shift (SA 110 <-> BO 110).
- Row 1-3: SA 1 is the Sanskrit title (*vajracchedika nama trishatika prajnaparamita*). BO 1 is the Tibetan title; BO 2 (Indic-language title in transliteration, "rgya gar skad du ...") and BO 3 (Tibetan title) have no Sanskrit row (SA 2-3 empty). SA 4 <-> BO 4 (homage) is correct. Medium confidence that BO 2 is really the counterpart of SA 1.

## 3. Rows empty on one side only

SA empty (BO has text):
- 2: BO "rgya gar skad du / a-rya-bajra-ccheda-ka ..." (Indic-language title in Tibetan transliteration)
- 3: BO "bod skad du / 'phags pa shes rab kyi pha rol tu phyin pa rdo rje gcod pa ..." (Tibetan title)
- 108: BO "bcom ldan 'das gal te lan cig phyir 'ong ba 'di snyam du ..."
- 109: BO "sems can du 'dzin pa dang srog tu 'dzin pa dang gang zag tu 'dzin par 'gyur lags so"
- 275: BO "yang rab 'byor gang la la zhig 'di skad du de bzhin gshegs pa ... zer na de log par smra ba yin no" (this row's text is the counterpart of SA 274, because of the +1 drift; see section 1)
- 434: BO dharani and closing verse (Tibetan-only appendix, no Sanskrit)

BO empty (SA has text):
- 216: SA "na rupa-shabda-gandha-rasa-sparsha-dharma-pratishthitena danam datavyam"
- 311: SA long "bhagavan aha ... yavantyo gangayam mahanadyam valukah ... bhashitah tathagatena valukah" (Tibetan absent; also see drift section)
- 376: SA "na lakshanasampada tathagato drashtavyah" (its Tibetan sits at BO 375)
- 379: SA "na lakshanasampada tathagato drashtavyah" (its Tibetan sits at BO 378)
- 420: SA "tatkasya hetoh ya sa bhagavan atmadrishtih ... adrishtih" (its Tibetan sits at BO 419)
- 431: SA "idam avocad bhagavan attamanah sthavira-subhutih ..." (its Tibetan sits at BO 430)

## 4. Where the problem sits relative to the stated suspicion
- Drift starts at row 230 (offset one: BO row N renders SA row N-1), i.e. the Tibetan is one row "ahead" / Sanskrit "behind". Confirmed.
- It does not reach offset two in this copy. It ends at row 327/328.
- SA rows with no Tibetan counterpart: 327 (and in the shifted frame 310 is covered by empty BO 311). Other SA rows without Tibetan: 375, 378, 419, 428 (see section 2).
