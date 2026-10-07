# Style sheet — Hindi (Devanagari) termbase of the Vajracchedikā

Shared conventions for the Hindi glossary. The English glossary fixes the sense distinctions; this sheet fixes how Hindi keeps them. Registers: academic (शैक्षणिक) and children's (बच्चों का).

## Policies

1. Script: Devanagari only, never Roman transliteration in a rendering; sentence-final stop is the danda (।), commas and hyphens as in modern Hindi; numerals in terms are spelled out in words (बत्तीस, सात). Reason: one script for both registers and clean matching in the later translation.
2. Spelling of tatsama words: write nasals before a consonant as anusvāra (संज्ञा, संघ, दीपंकर, कलिंग), but keep the conjunct म् in सम्बोधि, सम्बुद्ध, सम्पदा, and write सत्त्व, बोधिसत्त्व with त्त्व; keep the spellings in the Core terms table exactly. Reason: the registers file already uses सम्यक्सम्बोधि and बोधिसत्त्व, and one spelling per term keeps lookup consistent.
3. Academic register, evidence order: (a) the terms listed in registers-hi.md; (b) established Hindi Buddhist tatsama forms that the Gemini zero-shot also uses; (c) where Gemini differs, the Sanskrit tatsama that matches the Sanskrit equivalent in overview.md; (d) everyday Hindi only when the tatsama is opaque or misleading to a Hindi reader (for example कुलपुत्री instead of कुलदुहिता). Reason: Gemini is evidence of attested usage, not an authority; it is consistent with Sanskrit terms in most places but sometimes merges senses or spells loosely.
4. Gemini is overridden when it (i) renders both senses of ཆོས as धर्म, (ii) renders both ཕུང་པོ senses as स्कन्ध, (iii) spells variably (अर्हत/अर्हत्, महासहस्र for महासाहस्र), or (iv) uses an ambiguous Hindi word such as प्रतिष्ठित alone in a sentence where it could mean "prestigious". Reason: the glossary must keep the sense distinctions that the approved English glossary makes.
5. Never use Hindu-devotional or Urdu-Persian substitutes for technical terms: no आत्मा, ईश्वर, प्रभु, मोक्ष, पाप, अवतार, फ़रिश्ता, दुनियावी; ātman is आत्मन्, never आत्मा. Reason: they import another doctrine and the registers file forbids them. (भगवान, दान, पुण्य are kept because the registers file lists them.)
6. The two senses of ཆོས stay apart by word choice, decided by sense in the overview: teaching = धर्म (children's शिक्षा); phenomena = पदार्थ (children's चीज़); quality of a Buddha = गुण (children's गुण). Bare धर्म is never used for phenomena and bare पदार्थ is never used for the teaching; अधर्म is never used for adharma, because in Hindi it means unrighteousness. Reason: Hindi has no capital letter to separate "Dharma" from "phenomenon", so two different words are needed.
7. Compounds with ཆོས follow the sense of ཆོས inside them: teaching compounds keep धर्म (धर्मपर्याय, सद्धर्म, धर्मदेशना, धर्मकाय, धर्म-चक्षु); phenomena compounds take पदार्थ (सभी पदार्थ, पदार्थ-संज्ञा, अपदार्थ, पदार्थ-स्वभाव, कुशल पदार्थ); buddhadharma is बुद्ध-गुण, never बुद्धधर्म, which means "Buddhism". Reason: the English glossary resolves each compound by sense, and Hindi बुद्धधर्म would change the meaning.
8. Epithets of the Buddha: academic uses the Sanskrit tatsama in the nominative form without a vocative ending (भगवान, तथागत, सुगत, अर्हत्, सम्यक्सम्बुद्ध, बुद्ध), each term always the same word; children's keeps भगवान and बुद्ध, and renders the meaning of the others in plain Hindi (इसी तरह गए हुए, भली-भाँति गए हुए, पूर्ण बुद्ध). When a list of epithets occurs, the parts are joined by commas in the same order as the Tibetan. Reason: the epithets are distinct terms in the text, and the Hindi must keep them distinct.
9. Titles of address and honorifics: ཚེ་དང་ལྡན་པ is आयुष्मान् (children's आदरणीय) placed before the name (आयुष्मान् सुभूति); the Sanskrit-origin honorific is not replaced by Hindu forms like श्री or स्वामी. Reason: it keeps the monastic register without borrowing from other traditions.
10. Names: proper names take the Sanskrit form in Devanagari in both registers (सुभूति, श्रावस्ती, जेतवन, अनाथपिण्डद, दीपंकर, शाक्यमुनि, कलिंग, सुमेरु, गंगा नदी), and are never translated, with the single exception of the sage Kṣāntivādin in the children's register (धैर्यवादी). Reason: registers-hi.md says names keep their Sanskrit form; children recognise them as names.
11. The sūtra title: academic uses the Sanskrit title वज्रच्छेदिका (full Sanskrit title in Devanagari when the Tibetan transliterates it); children's uses the plain phrase हीरा काटने वाला (full title: हीरे की तरह काटने वाली पूर्ण समझदारी). Reason: the English glossary translates the title for children and keeps the title meaning visible.
12. The cosmological measure: academic writes the Sanskrit counted compound exactly, त्रिसाहस्र-महासाहस्र लोकधातु, and does not turn it into a number; children's uses the approved "billion worlds" idea as अरब दुनियाओं वाला ब्रह्माण्ड (अरब = a thousand million). Reason: the academic reader needs the traditional unit, the child needs a size they can picture, and both stay with the same meaning.
13. Children's register simplifies by replacing a technical word with a short plain phrase that translates its parts (संज्ञा becomes विचार, पुण्य becomes जमा हुई भलाई, निर्वाण becomes शोक से मुक्ति), never by substituting a different doctrinal idea; no Sanskrit technical compound is left unexplained, and names stay. Reason: registers-hi.md; the child must reach the same meaning as the scholar.
14. Children's wording avoids clashes: each plain phrase is used for one term only (जीव is not used for sattva, because jīva is जीवन; शोक, not दुःख, for mya ngan, because दुःख would read as duḥkha). Reason: one rendering per term and per sense.
15. Compounds take their parts' renderings: where the parts are themselves core terms, the compound is built from them, with a hyphen in the academic register (सत्त्व-संज्ञा, आत्म-ग्राह, आत्म-दृष्टि, जीव-दृष्टि), and as a plain "X का Y" phrase in the children's register (जीवित प्राणी का विचार); the established single-word forms in the table (तथागत, प्रज्ञापारमिता, लोकधातु, धर्मपर्याय, सम्यक्सम्बोधि) are written as one word. Reason: it keeps terms predictable across the 278 entries.
16. Repeated-stem sets keep one stem: संज्ञा for འདུ་ཤེས in every compound; ग्राह for འཛིན་པ; दृष्टि for ལྟ་བ; सत्त्व / जीव / पुद्गल for the three persons in the four bases of grasping; बोधि / जागृति for བྱང་ཆུབ in every compound. Reason: these compounds are the most repeated in the text.
17. Variant spellings and fragments in the Tibetan (ཚེ་དང༌ལྡན་པ, བྱང་ཆུབ་སེམས་དཔ, སྤྱན་ལྔ etc.) take the rendering of the standard form; mantras and dhāraṇī syllables are written in Devanagari as in the Sanskrit; a note records the variant. Reason: the same term must not receive two renderings because of spelling.
18. Verbs of practice (generate the mind, hold the mind) use the infinitive form with ना (चित्त उत्पन्न करना, चित्त को थामे रखना), and the term lemma is given without inflection; the translation inflects as the sentence needs. Reason: one lemma per term, and Hindi verb endings vary with person, number and gender.

## Core terms

| Tibetan | Sense | Academic | Children's | Reason |
|---|---|---|---|---|
| རབ་འབྱོར | name of the disciple | सुभूति | सुभूति | Sanskrit name kept in both registers. |
| བཅོམ་ལྡན་འདས | epithet of the Buddha | भगवान | भगवान | Listed in the registers file; plain and familiar for children. |
| དེ་བཞིན་གཤེགས་པ | epithet of the Buddha | तथागत | इसी तरह गए हुए | Established tatsama; children's gives the meaning "thus gone". |
| ཆོས | teaching | धर्म | शिक्षा | Teaching sense; bare धर्म is reserved for it (policy 6). |
| ཆོས | phenomena | पदार्थ | चीज़ | Separate word so that धर्म is never read as "phenomenon"; Gemini's धर्म is overridden. |
| ཆོས | quality (of a Buddha) | गुण | गुण | Third sense kept apart from both others. |
| སེམས་ཅན | sentient being | सत्त्व | प्राणी | Tatsama used by Hindi Buddhist writers and Gemini; children's plain word. |
| བྱང་ཆུབ་སེམས་དཔའ | bodhisattva | बोधिसत्त्व | जागृति-वीर | Listed in the registers file; children's translates bodhi and sattva (hero). |
| སངས་རྒྱས | Buddha | बुद्ध | बुद्ध | Name kept in both registers. |
| འདུ་ཤེས | perception (one of the aggregates; in the four graspings) | संज्ञा | विचार | Tatsama used by Gemini in all compounds; children's "idea". |
| བསོད་ནམས | merit | पुण्य | जमा हुई भलाई | पुण्य is in the registers file; children's keeps the idea of stored-up goodness. |
| ཚེ་དང་ལྡན་པ | honorific before a name | आयुष्मान् | आदरणीय | Gemini and Sanskrit agree; children's plain honorific. |
| དགྲ་བཅོམ་པ | arhat | अर्हत् | सम्मान के योग्य | अर्हत् is in the registers file; children's "worthy one". |
| གང་ཟག | person | पुद्गल | व्यक्ति | Technical term in Hindi Buddhist writing; plain word for children. |
| བསོད་ནམས་ཀྱི་ཕུང་པོ | accumulation of merit | पुण्यराशि | जमा हुई भलाई का ढेर | ཕུང་པོ as heap takes राशि, not स्कन्ध, to differ from the aggregates. |
| ཆོས་ཀྱི་རྣམ་གྲངས | discourse on the teaching | धर्मपर्याय | शिक्षा का पाठ | Established compound with धर्म in the teaching sense. |
| སྦྱིན་པ | generosity (virtue, practice of giving) | दान | देना | दान in the registers file; plain verb for children. |
| སྦྱིན་པ | gift (what is given) | उपहार | उपहार | Separate word from the virtue दान. |
| སྲོག | life-force (one of four bases of grasping) | जीव | जीवन | Fourth of the four bases; must differ from सत्त्व. |
| མཚན་ཕུན་སུམ་ཚོགས་པ | perfection of marks | लक्षणसम्पदा | सम्पूर्ण चिह्न | Gemini and Sanskrit agree; children's plain phrase. |
| བདག | self | आत्मन् | अपना आप | Avoids the Hindu आत्मा; children's "one's own self". |
| འཇིག་རྟེན་གྱི་ཁམས | world system | लोकधातु | दुनिया-क्षेत्र | Established tatsama; children's translates loka and dhātu. |
| མཚན | mark of a Buddha | लक्षण | चिह्न | Plain parallel to the academic tatsama. |
| བླ་ན་མེད་པ་ཡང་དག་པར་རྫོགས་པའི་བྱང་ཆུབ | unsurpassed perfect awakening | अनुत्तर सम्यक्सम्बोधि | सर्वोच्च पूर्ण जागृति | Registers file form; children's is built from जागृति. |
| བྱང་ཆུབ་སེམས་དཔའ་སེམས་དཔའ་ཆེན་པོ | bodhisattva great being | बोधिसत्त्व महासत्त्व | महान जागृति-वीर | Registers file form; children's built from its parts. |
| ཡང་དག་པར་རྫོགས་པའི་སངས་རྒྱས | epithet of the Buddha | सम्यक्सम्बुद्ध | पूर्ण बुद्ध | Tatsama in epithet lists; children's "complete Buddha". |
| མི་གནས་པ | not abiding | अप्रतिष्ठित | टिके बिना | Established term; lemma is अप्रतिष्ठित (used as "अप्रतिष्ठित रहकर"). |
| མངོན་པར་རྫོགས་པར་སངས་རྒྱས་པ | fully awakened (of a Buddha's realization) | अभिसम्बुद्ध | पूरी तरह जागे हुए | Gemini and Sanskrit agree; children's keeps "fully awake". |
| བྱང་ཆུབ | awakening | बोधि | जागृति | Stem for every compound with awakening. |
| རིགས་ཀྱི་བུ་མོ | daughter of a good family | कुलपुत्री | अच्छे परिवार की बेटी | Everyday Hindi putrī is clearer than Gemini's कुलदुहिता; stem कुल kept. |
| རིགས་ཀྱི་བུ | son of noble family | कुलपुत्र | अच्छे परिवार का बेटा | Pairs with the term above. |
| ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པ | perfection of wisdom (title) | प्रज्ञापारमिता | पूर्ण समझदारी | Listed in the registers file; children's "perfect wisdom". |
| འཛིན་པ | grasping | ग्राह | चिपके रहना | Stem for all grasping compounds (आत्म-ग्राह); children's "clinging". |
| སེམས | mind | चित्त | मन | Tatsama used by Gemini; children's everyday word. |
| ཕ་རོལ་ཏུ་ཕྱིན་པ | perfection | पारमिता | पूर्णता | Stem of प्रज्ञापारमिता; children's plain noun. |
| བདེ་བར་གཤེགས་པ | epithet of the Buddha | सुगत | भली-भाँति गए हुए | Used by Gemini; children's meaning of "well gone". |
| སྟོང་གསུམ་གྱི་སྟོང་ཆེན་པོའི་འཇིག་རྟེན་གྱི་ཁམས | cosmological measure | त्रिसाहस्र-महासाहस्र लोकधातु | अरब दुनियाओं वाला ब्रह्माण्ड | Exact counted compound; children's "billion worlds" (policy 12). |
| རིན་པོ་ཆེ་སྣ་བདུན | the seven precious things | सप्तरत्न | सात कीमती चीज़ें | Gemini and Sanskrit agree; children's keeps seven. |
| མར་མེ་མཛད | name of a past Buddha | दीपंकर | दीपंकर | Name kept in both registers. |
| སེམས་བསྐྱེད | generate the mind | चित्त उत्पन्न करना | मन में ठानना | Literal verb for scholars; children's "set the mind". |
| ཡང་དག་པར་རྫོགས་པའི་བྱང་ཆུབ | perfect awakening | सम्यक्सम्बोधि | पूर्ण जागृति | Base of the longer awakening term above. |
| ཕུང་པོ | heap (as in the mass of merit) | राशि | ढेर | Heap sense kept apart from the aggregates. |
| ཕུང་པོ | skandha (as in nirvāṇa without remainder of the aggregates) | स्कन्ध | समूह | Gemini's स्कन्ध kept only for this sense. |
| ཤེས་རབ | wisdom | प्रज्ञा | समझदारी | Stem of प्रज्ञापारमिता; children's plain word. |
| ཞིང | Buddha-field | बुद्धक्षेत्र | बुद्ध-भूमि | Tatsama; children's "Buddha-land". |
| རྡོ་རྗེ་གཅོད་པ | title of the sutra | वज्रच्छेदिका | हीरा काटने वाला | Hindi title; children's "Diamond Cutter" (policy 11). |
| ཐེག་པ | vehicle | यान | वाहन | Stem of बोधिसत्त्वयान and महायान. |
| དངོས་པོ | entity, basis for attachment | वस्तु | असली वस्तु | Gemini uses वस्तु; children's "real object". |
| རྒྱུན་དུ་ཞུགས་པ | first fruit-bearer | स्रोतापन्न | धारा में उतरने वाला | In the registers file; children's keeps "stream-enterer". |
| ལྟ་བ | view | दृष्टि | मान्यता | Stem for the "view of a self" compounds. |
| མཉན་ཡོད | place name | श्रावस्ती | श्रावस्ती | In the registers file; name kept. |
| ལྷ་མ་ཡིན | asura, class of beings | असुर | ईर्ष्यालु देवता | Class of beings, not "demon"; children's "jealous god". |
| མྱ་ངན་ལས་འདས་པ | nirvāṇa | निर्वाण | शोक से मुक्ति | Tatsama; children's "freedom from sorrow", not दुःख. |
| མཚན་མ | sign | निमित्त | संकेत | Gemini and Sanskrit agree; children's plain word. |
