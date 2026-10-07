#!/usr/bin/env python3
"""Plant one known error in 18 of 24 academic segments (same ids and kinds as the English test).

  python3 plant.py zh|hi   -> calibration-<lang>/{sample-raw,batch-cal,key}.json + prompt.md
"""
import json
import pathlib
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
FC = HERE.parent
EN_KEY = json.loads((HERE / "key.json").read_text(encoding="utf-8"))

# id -> (old, new) per language; kind and severity are taken from the English key
PLANTS = {
    "zh": {
        "10-51": ("如來說即非執著", "如來說即是執著"),
        "13-5": ("九千萬遍", "九百萬遍"),
        "12-22": ("如來說即是無想", "如來說即是真實想"),
        "7-35": ("燃燈佛", "釋迦牟尼佛"),
        "6-16": ("彼等為如來所知曉", "彼等不為如來所知曉"),
        "5-1": ("不住而行布施", "有所住而行布施"),
        "8-22": ("凡是在這部經被宣說時不驚恐", "凡是不驚恐"),
        "2-3": ("佛以所有最勝的饒益", "佛允諾諸菩薩摩訶薩往生其淨土，並以所有最勝的饒益"),
        "8-4": ("三十二相", "八十相"),
        "8-114": ("無壽者", "無靈魂"),
        "8-75": ("亦不能及", "亦能相及"),
        "11-9": ("不將任何法施設為毀壞，亦不施設為斷滅", "將某些法施設為毀壞，亦施設為斷滅"),
        "6-21": ("也將不會生起法想", "也將會生起法想"),
        "1-3": ("清晨時分", "傍晚時分"),
        "10-27": ("根本沒有任何教法可以被緣取", "確實有教法可以被緣取"),
        "12-27": ("幻、露、水泡", "幻、彩虹、水泡"),
        "8-97": ("無上正等菩提——阿耨多羅三藐三菩提", "無上正等正覺"),
        "6-28": ("連法尚且應當捨棄", "法應當執持"),
    },
    "hi": {
        "10-51": ("उसे ग्राह-रहित ही कहा है", "उसे ग्राह ही कहा है"),
        "13-5": ("नौ करोड़ बार", "नब्बे लाख बार"),
        "12-22": ("उसे असंज्ञा कहा है", "उसे सच्ची संज्ञा कहा है"),
        "7-35": ("दीपंकर", "शाक्यमुनि"),
        "6-16": ("तथागत उन्हें जानते हैं", "तथागत उन्हें नहीं जानते"),
        "5-1": ("अप्रतिष्ठित होकर", "प्रतिष्ठित होकर"),
        "8-22": ("जो सत्त्व इस सूत्र के उपदेश किए जाने पर त्रस्त", "जो सत्त्व त्रस्त"),
        "2-3": ("महासत्त्वों को जिस परम अनुग्रह से",
                "महासत्त्वों को अपनी शुद्ध भूमि में पुनर्जन्म का वचन देकर जिस परम अनुग्रह से"),
        "8-4": ("बत्तीस", "अस्सी"),
        "8-114": ("जीवरहित", "आत्मारहित"),
        "8-75": ("तुलना नहीं सहता है", "तुलना सहता है"),
        "11-9": ("किसी भी धर्म को विनाश या उच्छेद के रूप में प्रज्ञप्त नहीं किया है",
                 "कुछ धर्मों को विनाश या उच्छेद के रूप में प्रज्ञप्त किया है"),
        "6-21": ("धर्म-संज्ञा में और धर्म-अभाव-संज्ञा में भी प्रवृत्त नहीं होंगे",
                 "धर्म-संज्ञा में प्रवृत्त होंगे, पर धर्म-अभाव-संज्ञा में प्रवृत्त नहीं होंगे"),
        "1-3": ("पूर्वाह्न के समय", "सायंकाल के समय"),
        "10-27": ("ऐसा कोई भी धर्म नहीं है जिसे", "ऐसा एक धर्म है जिसे"),
        "12-27": ("ओस की बूँद", "इंद्रधनुष"),
        "8-97": ("अनुत्तर सम्यक्सम्बोधि", "अनुत्तर पूर्ण ज्ञानोदय"),
        "6-28": ("धर्मों को भी त्याग देना चाहिए", "धर्मों को पकड़े रहना चाहिए"),
    },
}
LANG_NAME = {"zh": "Chinese (Traditional characters)", "hi": "Hindi (Devanagari)"}


def main(lang):
    out = FC / f"calibration-{lang}"
    out.mkdir(exist_ok=True)
    src = FC / f"{lang}-academic-a90" / "batches" / "batch-01.json"
    segs = {s["id"]: s for s in json.loads(src.read_text(encoding="utf-8"))}
    order = list(EN_KEY)  # same (shuffled) order as the English test
    raw = [segs[i] for i in order]
    (out / "sample-raw.json").write_text(json.dumps(raw, ensure_ascii=False, indent=1), encoding="utf-8")
    key, cal = {}, []
    for s in raw:
        s = dict(s)
        if s["id"] in PLANTS[lang]:
            old, new = PLANTS[lang][s["id"]]
            assert s["translation"].count(old) == 1, (s["id"], old)
            s["translation"] = s["translation"].replace(old, new)
            en = EN_KEY[s["id"]]
            key[s["id"]] = {"planted": True, "kind": en["kind"], "severity": en["severity"], "old": old, "new": new}
        else:
            key[s["id"]] = {"planted": False}
        cal.append(s)
    (out / "batch-cal.json").write_text(json.dumps(cal, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "key.json").write_text(json.dumps(key, ensure_ascii=False, indent=1), encoding="utf-8")
    t = (FC / "prompts" / "factcheck-agent-lang.md").read_text(encoding="utf-8")
    t = t.format(lang_name=LANG_NAME[lang], batch_path=out / "batch-cal.json", out_path=out / "agent-out.json",
                 batch_name="calibration", check_script=FC / "check.py")
    (out / "prompt.md").write_text(t, encoding="utf-8")
    shutil.rmtree(FC / f"{lang}-academic-a90")
    print(f"{lang}: {sum(v['planted'] for v in key.values())} planted, "
          f"{sum(not v['planted'] for v in key.values())} controls -> {out}")


if __name__ == "__main__":
    main(sys.argv[1])
