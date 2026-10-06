#!/usr/bin/env python3
"""pair_corrections for bo-display from the full read of the Sanskrit-Tibetan pair (0-INBOX/temp/pair-review/sa-bo.md)."""
import sys, yaml, pathlib
sys.path.insert(0, "4-SYSTEM/Skills/aligned-corpus-intake/scripts")
from md_export import read_rows
from project import is_letter
has = lambda t: any(is_letter(c) for c in t)
sa = {r["row"]: r["text"] for r in read_rows("0-INBOX/raw-data/dorjeechoepa-root-sa(sa-bo).md")}
bo = {r["row"]: r["text"] for r in read_rows("0-INBOX/raw-data/dorjeechoepa-root-bo(sa-bo).md")}
CL = 'Claude (standing instruction "read it and fix if it really makes sense", carried over from heart-sutra-rails 2026-10-03) — for the text expert to check'
out = [{"row": 230, "target_side_rows": [],
        "reason": "Tibetan-only sentence (འདིའི་རྣམ་པར་སྨིན་པ་ཡང་བསམ་གྱིས་མི་ཁྱབ་པ་…, which the Tibetan also has at row 253 = Sanskrit 252); the Sanskrit here has no counterpart. In the doc it sits opposite Sanskrit 230, which shifts every following pair by one row down to row 327.",
        "decided_by": CL, "date": "2026-10-04"}]
for n in range(231, 328):
    if not has(bo.get(n, "")):
        continue
    t = [n - 1] if has(sa.get(n - 1, "")) else []
    why = (f"One-row drift from row 230 to 327 (see row 230): Tibetan row {n} renders Sanskrit row {n-1}." if t else
           f"One-row drift from row 230 to 327: Tibetan row {n} would pair with Sanskrit row {n-1}, which is empty; no Sanskrit counterpart found (left unpaired).")
    out.append({"row": n, "target_side_rows": t, "reason": why, "decided_by": CL, "date": "2026-10-04"})
local = {375: (376, "Sanskrit 375 (yathāhaṃ bhagavato bhāṣitasyārtham ājānāmi) has no Tibetan; Tibetan 375 renders Sanskrit 376 (na lakṣaṇasaṃpadā tathāgato draṣṭavyaḥ), whose Tibetan row 376 is empty."),
         378: (379, "Sanskrit 378 (evam etad yathā vadasi) has no Tibetan; Tibetan 378 renders Sanskrit 379, whose Tibetan row 379 is empty."),
         419: (420, "Sanskrit 419 (na samyag vadamāno vadet) has no Tibetan; Tibetan 419 renders Sanskrit 420 (ātmadṛṣṭiḥ … adṛṣṭiḥ), whose Tibetan row 420 is empty."),
         428: (430, "Tibetan 428 (དེས་ན་ཡང་དག་པར་རབ་ཏུ་སྟོན་པ་ཞེས་བྱའོ།) renders Sanskrit 430 (tenocyate saṃprakāśayed iti); Sanskrit 428 (tadyathākāśe) has no Tibetan."),
         430: (431, "Tibetan 430 (བཅོམ་ལྡན་འདས་ཀྱིས་དེ་སྐད་ཅེས་བཀའ་སྩལ་ནས།…) renders Sanskrit 431 (idam avocad bhagavān …), whose Tibetan row 431 is empty.")}
for n, (t, why) in local.items():
    out.append({"row": n, "target_side_rows": [t], "reason": why, "decided_by": CL, "date": "2026-10-04"})
pathlib.Path("0-INBOX/temp/pair-review/sa-bo-corrections.yaml").write_text(
    "# pair_corrections for bo-display (row = row of dorjeechoepa-root-bo(sa-bo).md). Evidence: sa-bo.md (full read, 2026-10-04).\n"
    + yaml.safe_dump({"pair_corrections": out}, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
print(len(out), "corrections;", sum(1 for c in out if not c["target_side_rows"]), "unpaired")
