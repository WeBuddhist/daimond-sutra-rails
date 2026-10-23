#!/usr/bin/env python3
"""A/B test of the zh-academic system prompt: current (A) vs Chinese-only draft (B).

  python3 ab_test.py --arm A                # dry run: batches, prompt sizes, cost estimate; no API call
  python3 ab_test.py --arm B --run 1 --go   # translate the test segments with arm B (needs GEMINI_API_KEY)
  python3 ab_test.py --eval --run 1         # automatic metrics + pairs file for the blind pairwise judge

Both arms get identical input: the same segments, batches, model, context (Tibetan, Sanskrit, 3 commentaries,
english_academic, kumarajiva, zero_shot) and locked terms. Only the system instruction and the user-message
header differ. No term retry, no fact-check feedback: this measures first-pass output.
Writes only inside this folder (arm-<A|B>-run<N>.jsonl, eval-run<N>.json, pairs-run<N>.json) and the usage
ledger (step "ab-test-zh-prompt"). Never touches the zh-academic track.
"""
import argparse
import datetime as _dt
import importlib.util
import json
import os
import pathlib
import re
import sys
import time
import types
import uuid

HERE = pathlib.Path(__file__).resolve().parent
VAULT = HERE.parents[2]
KF = VAULT / "0-INBOX/kf-pilot"
_spec = importlib.util.spec_from_file_location("tr", KF / "translate" / "gm_variant_translate.py")
tr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tr)
tr.LANG = "zh"

TRACK = VAULT / "3-TRANSFORMATIONS/Translations/zh-academic"
SEGMENTS = json.loads((HERE.parent / "ab-test-segments.json").read_text(encoding="utf-8"))["all"]

ARMS = {  # A = the prompt as it was before 2026-10-24 (requirements-v1.md); B = the track's current requirements.md
    "A": {"system": lambda: (HERE / "requirements-v1.md").read_text(encoding="utf-8") + tr.FORMAT,
          "user": ("Translate these segments of the Tibetan Diamond Sutra into modern written Chinese in Traditional "
                   "characters (academic register). Return JSON only.\n\n"
                   "Each segment also carries `english_academic` (the approved, fact-checked English academic "
                   "translation — use it to confirm the meaning, not as the text to translate), `kumarajiva` "
                   "(Kumārajīva's classical Chinese, for established terminology only) and `zero_shot` (an unreviewed "
                   "machine draft in the target language). Translate from the Tibetan.\n\n")},
    "B": {"system": lambda: tr.strip_frontmatter((TRACK / "requirements.md").read_text(encoding="utf-8")),
          "user": tr.ZH_TASK["academic"]},
}
# USD per 1M tokens and mean tokens per zh-academic call, from the usage ledger (121 calls, 2026-10-07)
PRICE_IN, PRICE_OUT = 2.00, 12.00
BASE_IN, OUT_THINK = 6523, 239 + 5014


def work(arm, run):
    return HERE / f"arm-{arm}-run{run}.jsonl"


def setup():
    segs = {s["id"]: s for s in json.loads((tr.TERM_RUN / "segments.json").read_text(encoding="utf-8"))}
    refs = {"english_academic": {i: r["translation"] for i, r in tr.latest(tr.work_file("en", "academic")).items()},
            "zero_shot": tr.zero_shot_lines("zh"), "kumarajiva": tr.kumarajiva_lines()}
    return segs, refs, tr.locked_terms("academic")


def call(arm, run, batch, segs, ctx, terms, refs, key, model):
    items = tr.payload(batch, segs, ctx, terms, 2500, None, refs)
    user = ARMS[arm]["user"] + json.dumps(items, ensure_ascii=False)
    body = {"systemInstruction": {"parts": [{"text": ARMS[arm]["system"]()}]},
            "contents": [{"role": "user", "parts": [{"text": user}]}],
            "generationConfig": {"responseMimeType": "application/json", "responseSchema": tr.SCHEMA},
            "safetySettings": tr.gm.SAFETY_OFF}
    t0, call_id = time.time(), uuid.uuid4().hex[:12]
    text, info = tr.gm.call_api(body, types.SimpleNamespace(model=model, retries=6, timeout=900), key)
    u = info["usage"]
    tr.ledger.log_call(step="ab-test-zh-prompt", text="vajracchedika", lang="zh", variant=f"academic-{arm}",
                       engine="gemini-api", model=info["model_version"], batch=call_id, segments=len(batch),
                       attempt=run, tokens={"input": u["prompt_tokens"], "output": u["output_tokens"],
                                            "thinking": u["thinking_tokens"]},
                       seconds=round(time.time() - t0, 1), note=f"{batch[0]}..{batch[-1]}")
    data = {b["id"]: b["translation"].strip() for b in json.loads(text).get("blocks", [])}
    with work(arm, run).open("a", encoding="utf-8") as fh:
        for i in batch:
            fh.write(json.dumps({"id": i, "translation": data.get(i, ""), "arm": arm, "run": run, "call_id": call_id,
                                 "model": info["model_version"],
                                 "ts": _dt.datetime.now().isoformat(timespec="seconds")}, ensure_ascii=False) + "\n")


CLASSICAL = ["之", "乎", "者", "也", "彼", "此", "皆", "於", "為無", "即非", "是名", "故名", "何以故", "云何", "爾時"]


def metrics(rows, segs, terms):
    ids = [i for i in SEGMENTS if i in rows]
    txt = {i: rows[i]["translation"] for i in ids}
    req = [(i, t) for i in ids for t in terms.get(i, [])]
    miss = [(i, t["rendering"]) for i, t in req if not tr.complies(t["rendering"], txt[i])]
    formula = {f: [i for i, r in miss if r == f] for f in ("這是為什麼呢？", "須菩提！")}
    par_c = [i for i in ids if re.search(r"དེས་ན་.{1,60}ཞེས་(བྱའོ|བགྱིའོ)", segs[i]["bo"])]
    chars = sum(len(t) for t in txt.values()) or 1
    return {
        "segments": len(ids), "empty": [i for i in ids if not txt[i]],
        "locked_terms_required": len(req), "locked_terms_missed": len(miss),
        "missed_other_terms": [m for m in miss if m[1] not in formula],
        "why_formula_missed": formula["這是為什麼呢？"], "vocative_missed": formula["須菩提！"],
        "paradox_C_with_所以才稱為": f"{sum('所以才稱為' in txt[i] for i in par_c)}/{len(par_c)}",
        "classical_markers_per_1000_chars": round(1000 * sum(t.count(w) for t in txt.values() for w in CLASSICAL) / chars, 1),
        "latin_or_digits": [i for i in ids if re.search(r"[A-Za-z0-9]", txt[i])],
        "commentary_titles_or_ids_leaked": [i for i in ids if re.search(r"bo-|蓮花戒|世親|確尼", txt[i])],
        "sample_vocabulary_leaked": [i for i in ids if re.search(r"賢友|尊者|念住", txt[i])],
        "ellipsis_used": [i for i in ids if "…" in txt[i] or "..." in txt[i]],
        "mean_chars": round(chars / len(ids), 1),
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--arm", choices=sorted(ARMS))
    p.add_argument("--run", type=int, default=1)
    p.add_argument("--go", action="store_true", help="actually call Gemini (default is a dry run)")
    p.add_argument("--eval", action="store_true")
    p.add_argument("--model", default=tr.gm.DEFAULT_MODEL)
    a = p.parse_args()
    segs, refs, terms = setup()
    batches = tr.make_batches(SEGMENTS, segs, 6, 1800)

    if a.eval:
        res = {}
        for arm in ARMS:
            rows = tr.latest(work(arm, a.run))
            res[arm] = metrics(rows, segs, terms) if rows else "not run"
        (HERE / f"eval-run{a.run}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
        ra, rb = tr.latest(work("A", a.run)), tr.latest(work("B", a.run))
        pairs = [{"track": "zh-academic", "id": i, "before": ra[i]["translation"], "after": rb[i]["translation"],
                  "before_verdict": "n/a", "after_verdict": "n/a"} for i in SEGMENTS if i in ra and i in rb]
        (HERE / f"pairs-run{a.run}.json").write_text(json.dumps(pairs, ensure_ascii=False, indent=1), encoding="utf-8")
        print(json.dumps(res, ensure_ascii=False, indent=1))
        print(f"pairs for the blind judge: {len(pairs)} -> pairs-run{a.run}.json (before = A, after = B)")
        return

    if not a.arm:
        sys.exit("--arm A|B or --eval")
    system = ARMS[a.arm]["system"]()
    extra = len(system) - len(ARMS["A"]["system"]())  # ~1 token per CJK/Tibetan character
    est = len(batches) * ((BASE_IN + max(extra, 0)) * PRICE_IN + OUT_THINK * PRICE_OUT) / 1e6
    print(f"arm {a.arm}: {len(SEGMENTS)} segments, {len(batches)} calls {[len(b) for b in batches]}; "
          f"system prompt {len(system)} chars; estimated ${est:.2f}")
    if not a.go:
        print("dry run: add --go to call Gemini")
        return
    key = os.environ.get(tr.gm.KEY_ENV, "")
    if not key:
        sys.exit("GEMINI_API_KEY is not set")
    done = set(tr.latest(work(a.arm, a.run)))
    ctx = tr.build_context(tr.ROOT)
    for b in batches:
        if all(i in done for i in b):
            continue
        call(a.arm, a.run, b, segs, ctx, terms, refs, key, a.model)
        print(f"  {b[0]}..{b[-1]} ok")


if __name__ == "__main__":
    main()
