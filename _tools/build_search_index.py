#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""扫 posts/*.html 生成 search-index.json（标题/日期/摘要/链接）。
用法：python _tools/build_search_index.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "posts"


def pick(pattern: str, text: str) -> str:
    m = re.search(pattern, text, re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def main() -> int:
    items = []
    for f in sorted(POSTS.glob("*.html")):
        text = f.read_text(encoding="utf-8", errors="replace")
        title = pick(r"<h1[^>]*>(.*?)</h1>", text) or pick(r"<title>(.*?)</title>", text)
        if not title:
            continue
        date = pick(r'class="date"[^>]*>(.*?)</p>', text)
        desc = pick(r'<meta name="description" content="(.*?)"', text)
        items.append({
            "title": title,
            "date": date,
            "desc": desc,
            "url": f"posts/{f.name}",
        })
    items.sort(key=lambda x: x["date"], reverse=True)
    out = ROOT / "search-index.json"
    out.write_text(json.dumps(items, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"写了 {len(items)} 条 → {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
