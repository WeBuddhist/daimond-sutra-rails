#!/usr/bin/env python3
"""Rebuild a Chinese track's requirements.md from its prompt draft.

  python3 assemble.py              # academic: zh-academic-prompt-draft.md -> zh-academic/requirements.md
  python3 assemble.py children     # children: zh-children-prompt-draft.md -> zh-children/requirements.md

Each draft holds sections 一…五, each in Chinese, then its English mirror and design notes. This script puts the
sections in order, takes only the Chinese part of each, and writes it into requirements.md below that file's own
frontmatter and title, which are kept as they are. The whole of requirements.md minus its frontmatter is what
Gemini receives (gm_variant_translate.py --system). Edit the draft, never requirements.md directly; then run this.
"""
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
TRACKS = HERE.parents[1] / "3-TRANSFORMATIONS/Translations"
TITLES = {"academic": "# 翻譯要求 —— 金剛經，中文學術版", "children": "# 翻譯要求 —— 金剛經，中文兒童版"}

variant = sys.argv[1] if len(sys.argv) > 1 else "academic"
draft = HERE / f"zh-{variant}-prompt-draft.md"
req = TRACKS / f"zh-{variant}" / "requirements.md"

text = draft.read_text(encoding="utf-8")
head, *parts = re.split(r"\n---\n\n(?=## )", text)
order = "一二三四五"
parts.sort(key=lambda p: order.index(p[3]))
assert [p[3] for p in parts] == list(order), [p[:8] for p in parts]
draft.write_text("\n---\n\n".join([head] + [p.rstrip("\n") for p in parts]) + "\n", encoding="utf-8")

zh = "\n\n".join(p.split("\n### English mirror")[0].rstrip() for p in parts)
assert "English mirror" not in zh and "Design notes" not in zh
fm = re.match(r"\A---\n.*?\n---\n", req.read_text(encoding="utf-8"), flags=re.S).group(0)
req.write_text(f"{fm}\n{TITLES[variant]}\n\n{zh}\n", encoding="utf-8")
print(f"wrote zh-{variant}/{req.name}: {len(zh)} chars, sections {[p.split(chr(10))[0] for p in parts]}")
