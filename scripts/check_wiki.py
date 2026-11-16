#!/usr/bin/env python3
"""Wiki 檢查腳本：python scripts/check_wiki.py（在 repo 根目錄執行）。

檢查：(a) 壞連結 (b) frontmatter 必要欄位 (c) concept 頁來源
(d) 孤兒頁（除 index.md、log.md 外，沒有其他 wiki 頁連入；index.md 的連結算數）。
全部通過輸出 `OK: N pages` 並以 0 結束；否則每個問題一行，以 1 結束。
"""
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
REQUIRED = ("title", "type", "sources", "updated")
TYPES = {"source", "concept", "overview", "output", "synthesis"}
LINK_RE = re.compile(r"\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
FENCE_RE = re.compile(r"^(```|~~~).*?^\1[^\n]*$", re.S | re.M)


def parse(text):
    """回傳 (frontmatter dict 或 None, 內文)。sources 解析成 list。"""
    text = text.lstrip("\ufeff")
    m = re.match(r"---\r?\n(.*?)\r?\n---\r?\n?(.*)", text, re.S)
    if not m:
        return None, text
    fm, key = {}, None
    for line in m.group(1).splitlines():
        if re.match(r"^\s+-\s*", line) and key is not None:
            item = re.sub(r"^\s+-\s*", "", line).strip().strip("\"'")
            if item:
                fm[key].append(item)
            continue
        kv = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if not kv:
            continue
        key, val = kv.group(1), kv.group(2).strip()
        if key == "sources":
            if val.startswith("["):
                inner = val.strip("[]").strip()
                fm[key] = [s.strip().strip("\"'") for s in inner.split(",") if s.strip()]
            else:
                fm[key] = [val.strip("\"'")] if val else []
        else:
            fm[key] = val.strip("\"'")
    return fm, m.group(2)


def links(body):
    body = FENCE_RE.sub("", body)
    for target in LINK_RE.findall(body):
        if re.match(r"^(https?:|mailto:|#)", target):
            continue
        target = target.split("#", 1)[0]
        if target:
            yield target


def main():
    pages = sorted(WIKI.rglob("*.md"))
    problems, inbound = [], {p: set() for p in pages}
    for p in pages:
        rel = p.relative_to(ROOT).as_posix()
        fm, body = parse(p.read_text(encoding="utf-8"))
        if fm is None:
            problems.append(f"{rel}: 缺少 frontmatter")
        else:
            for f in REQUIRED:
                if f not in fm:
                    problems.append(f"{rel}: frontmatter 缺少欄位 {f}")
            if "type" in fm and fm["type"] not in TYPES:
                problems.append(f"{rel}: type 不合法 ({fm['type']})")
            if fm.get("type") == "concept":
                if not fm.get("sources"):
                    problems.append(f"{rel}: concept 頁 sources 為空")
                if not any("sources/" in t.replace("\\", "/") for t in links(body)):
                    problems.append(f"{rel}: concept 頁內文沒有 sources/ 連結")
        for t in links(body):
            dest = (p.parent / t).resolve()
            if not dest.exists():
                problems.append(f"{rel}: 壞連結 -> {t}")
            elif dest in inbound and dest != p.resolve():
                inbound[dest].add(p)
    for p in pages:
        if p.name in ("index.md", "log.md") and p.parent == WIKI:
            continue
        if not {q for q in inbound[p] if q.resolve() != p.resolve()}:
            problems.append(f"{p.relative_to(ROOT).as_posix()}: 孤兒頁（沒有其他頁連入）")
    if problems:
        print("\n".join(problems))
        return 1
    print(f"OK: {len(pages)} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
