#!/usr/bin/env python3
"""Rebuild zh-academic/requirements.md from the prompt draft.

  python3 assemble.py

The draft (zh-academic-prompt-draft.md) holds each section in Chinese, then its English mirror and design notes.
This script puts the sections in order (一…五), takes only the Chinese part of each, and writes it into
requirements.md below that file's own frontmatter and title, which are kept as they are. The whole of
requirements.md minus its frontmatter is what Gemini receives (gm_variant_translate.py --system).
Edit the draft, never requirements.md directly; then run this script.
"""
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
DRAFT = HERE / "zh-academic-prompt-draft.md"
REQ = HERE.parents[1] / "3-TRANSFORMATIONS/Translations/zh-academic/requirements.md"
TITLE = "# 翻譯要求 —— 金剛經，中文學術版"

text = DRAFT.read_text(encoding="utf-8")
head, *parts = re.split(r"\n---\n\n(?=## )", text)
order = "一二三四五"
parts.sort(key=lambda p: order.index(p[3]))
assert [p[3] for p in parts] == list(order), [p[:8] for p in parts]
DRAFT.write_text("\n---\n\n".join([head] + [p.rstrip("\n") for p in parts]) + "\n", encoding="utf-8")

zh = "\n\n".join(p.split("\n### English mirror")[0].rstrip() for p in parts)
assert "English mirror" not in zh and "Design notes" not in zh
fm = re.match(r"\A---\n.*?\n---\n", REQ.read_text(encoding="utf-8"), flags=re.S).group(0)
REQ.write_text(f"{fm}\n{TITLE}\n\n{zh}\n", encoding="utf-8")
print(f"wrote {REQ.name}: {len(zh)} chars, sections {[p.split(chr(10))[0] for p in parts]}")
