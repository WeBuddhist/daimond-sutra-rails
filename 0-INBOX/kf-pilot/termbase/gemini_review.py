#!/usr/bin/env python3
"""Cross-model review of the Claude-drafted termbase by Gemini, then apply and render.

  zsh -ic 'python3 gemini_review.py <run-dir>'      # review (one call, whole termbase)
  python3 gemini_review.py <run-dir> --apply-only   # re-apply an existing review

Reads <run-dir>/agents/batch-*.json (Claude's entries), style-sheet.md,
../registers.md and terms.json. Gemini sees every entry at once so it can judge
consistency, and returns objections only. Objections to `academic`, `children`
or `sanskrit` are applied (the reviewer approves on the user's behalf; there is
no human reviewer yet); objections to a sense split and to style-sheet policies
are recorded, not applied. Writes review.json, termbase.json, and the two
track termbases termbase-academic.md / termbase-children.md.
"""
import argparse
import importlib.util
import json
import os
import pathlib
import sys
import time
import types

HERE = pathlib.Path(__file__).resolve().parent
VAULT = HERE.parents[2]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


gm = load("gm_translate", VAULT / "4-SYSTEM/Skills/machine-translate/scripts/gm_translate.py")
ledger = load("usage_ledger", VAULT / "4-SYSTEM/scripts/usage-ledger/usage_ledger.py")

SYSTEM = """You are the reviewer of an English glossary (termbase) for the Tibetan Diamond Sutra, drafted by another model. You approve it on behalf of the editors, so be exacting: a wrong rendering here will be repeated in every translation.

You get the register definitions, the drafter's style sheet (policies and core terms), and every glossary entry: the Tibetan, its Sanskrit where known, its occurrence count, how two English machine translations (DharmaMitra `dm`, Gemini `gm`) rendered it, and the drafted senses with an academic and a children's rendering each.

Report OBJECTIONS ONLY, as JSON:
- `terms`: one item per problem: `term_id`, `sense` (the sense label as given), `field` ("academic" | "children" | "sanskrit" | "sense_split"), `current`, `suggested` (the replacement; for sense_split describe the split), `severity` ("major": wrong meaning, misleading, or inconsistent with a policy or a related term; "minor": a better established or clearer equivalent exists), `reason` (max 25 words).
- `policies`: objections to style-sheet policies: `policy` (its number), `suggested`, `reason`.
Check in particular: doctrinal accuracy; consistency between a compound and its parts and across related terms; the register rules (academic: established Buddhological English, IAST; children's: plain words for ages 8-12 that keep the meaning, no Sanskrit except names); one English rendering never used for two different Tibetan terms. Do not object to matters of taste where the draft is accurate and consistent. Return empty lists if nothing needs changing."""

SCHEMA = {
    "type": "object",
    "properties": {
        "terms": {"type": "array", "items": {"type": "object", "properties": {
            "term_id": {"type": "string"}, "sense": {"type": "string"},
            "field": {"type": "string", "enum": ["academic", "children", "sanskrit", "sense_split"]},
            "current": {"type": "string"}, "suggested": {"type": "string"},
            "severity": {"type": "string", "enum": ["major", "minor"]}, "reason": {"type": "string"}},
            "required": ["term_id", "sense", "field", "current", "suggested", "severity", "reason"]}},
        "policies": {"type": "array", "items": {"type": "object", "properties": {
            "policy": {"type": "string"}, "suggested": {"type": "string"}, "reason": {"type": "string"}},
            "required": ["policy", "suggested", "reason"]}},
    },
    "required": ["terms", "policies"],
}


def entries(run):
    src = {t["term_id"]: t for t in json.loads((run / "terms.json").read_text(encoding="utf-8"))}
    out = []
    for f in sorted((run / "agents").glob("batch-*.json")):
        for t in json.loads(f.read_text(encoding="utf-8"))["terms"]:
            s = src[t["term_id"]]
            out.append({"term_id": t["term_id"], "bo": s["bo"], "sanskrit": t.get("sanskrit"),
                        "count": s["count"], "dm": s["dm"], "gm": s["gm"], "occurrences": s["occurrences"],
                        "senses": t["senses"]})
    out.sort(key=lambda e: e["term_id"])
    return out


def review(run, ents, model):
    key = os.environ.get(gm.KEY_ENV, "")
    if not key:
        sys.exit("GEMINI_API_KEY is not set (run via: zsh -ic 'python3 ...')")
    compact = [{"term_id": e["term_id"], "bo": e["bo"], "sanskrit": e["sanskrit"], "count": e["count"],
                "dm": dict(list(e["dm"].items())[:4]), "gm": dict(list(e["gm"].items())[:4]),
                "senses": [{k: (v if k != "occurrences" or v == "all" else f"{len(v)} occurrences")
                            for k, v in s.items() if k != "reason"} for s in e["senses"]]} for e in ents]
    user = ("# Registers\n\n" + (HERE / "registers.md").read_text(encoding="utf-8")
            + "\n\n# Style sheet\n\n" + (run / "style-sheet.md").read_text(encoding="utf-8")
            + "\n\n# Glossary entries\n\n" + json.dumps(compact, ensure_ascii=False)
            + "\n\nReview the glossary. Return JSON only.")
    body = {"systemInstruction": {"parts": [{"text": SYSTEM}]},
            "contents": [{"role": "user", "parts": [{"text": user}]}],
            "generationConfig": {"responseMimeType": "application/json", "responseSchema": SCHEMA},
            "safetySettings": gm.SAFETY_OFF}
    args = types.SimpleNamespace(model=model, retries=6, timeout=1200)
    t0 = time.time()
    text, info = gm.call_api(body, args, key)
    u = info["usage"]
    ledger.log_call(step="termbase-review", text="vajracchedika", lang="en", engine="gemini-api",
                    model=info["model_version"], batch="all", segments=len(ents),
                    tokens={"input": u["prompt_tokens"], "output": u["output_tokens"], "thinking": u["thinking_tokens"]},
                    seconds=round(time.time() - t0, 1), note="Gemini review of Claude termbase (one call, all terms)")
    data = json.loads(text)
    (run / "review.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"objections terms={len(data['terms'])} policies={len(data['policies'])} tokens={u}")
    return data


def apply(run, ents, rev):
    by_id = {e["term_id"]: e for e in ents}
    applied, recorded = 0, 0
    for o in rev["terms"]:
        e = by_id.get(o["term_id"])
        if not e:
            continue
        o["applied"] = False
        if o["field"] == "sanskrit":
            e["sanskrit"] = o["suggested"]
            o["applied"] = True
        elif o["field"] in ("academic", "children"):
            for s in e["senses"]:
                if s["sense"] == o["sense"] or len(e["senses"]) == 1:
                    s.setdefault("draft", {})[o["field"]] = s[o["field"]]
                    s[o["field"]] = o["suggested"]
                    s.setdefault("review", []).append(f"{o['field']}: {o['severity']} — {o['reason']}")
                    o["applied"] = True
                    break
        applied += o["applied"]
        recorded += not o["applied"]
    ov_path = run / "overrides.json"
    overridden = 0
    if ov_path.exists():
        for ov in json.loads(ov_path.read_text(encoding="utf-8"))["overrides"]:
            for s in by_id[ov["term_id"]]["senses"]:
                if s.get(ov["field"]) != ov["value"]:
                    s[ov["field"]] = ov["value"]
                    s.setdefault("review", []).append(f"{ov['field']}: editor override — {ov['reason']}")
                    s.setdefault("override", {})[ov["field"]] = True
                    overridden += 1
    print(f"editor overrides applied={overridden}")
    (run / "termbase.json").write_text(json.dumps(ents, ensure_ascii=False, indent=1), encoding="utf-8")
    (run / "review.json").write_text(json.dumps(rev, ensure_ascii=False, indent=1), encoding="utf-8")
    for reg, title in (("academic", "Academic"), ("children", "Children's")):
        lines = [
            "---", f"track: en-{reg}", "text: Diamond Sutra (Vajracchedikā)", "source_lemma_language: bo",
            "target_language: en", f"register: {reg}", "status: draft",
            "built_by: Claude Sonnet agents (style sheet + 6 parallel batches), reviewed by Gemini 3.1 Pro",
            "---", "", f"# Termbase — Diamond Sutra, English, {title}", "",
            "One locked rendering per Tibetan term (per sense where the term has distinct senses). "
            "Head forms: the translator inflects them in context. ✎ = changed by the Gemini review "
            "(draft rendering in brackets).", "",
            "| Tibetan | Sanskrit | Sense | Rendering | Occ. | Basis | Reason |", "|---|---|---|---|---|---|---|"]
        for e in ents:
            for s in e["senses"]:
                changed = s.get("draft", {}).get(reg)
                if s.get("override", {}).get(reg):
                    changed = None
                rend = f"**{s[reg]}**" + (f" ✎ ({changed})" if changed else "")
                occ = e["count"] if s["occurrences"] == "all" else len(s["occurrences"])
                lines.append(f"| {e['bo']} | {e['sanskrit'] or ''} | {s['sense']} | {rend} | {occ} | {s['basis']} | {s['reason']} |")
        (run / f"termbase-{reg}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"applied={applied} recorded-only={recorded} policy-objections={len(rev['policies'])}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("run_dir")
    p.add_argument("--model", default=gm.DEFAULT_MODEL)
    p.add_argument("--apply-only", action="store_true")
    a = p.parse_args()
    run = pathlib.Path(a.run_dir)
    ents = entries(run)
    rev = json.loads((run / "review.json").read_text(encoding="utf-8")) if a.apply_only else review(run, ents, a.model)
    apply(run, ents, rev)


if __name__ == "__main__":
    main()
