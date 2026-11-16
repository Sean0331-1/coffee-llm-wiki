#!/usr/bin/env python3
"""簡報檢查腳本：python scripts/check_slides.py [簡報路徑]（在 repo 根目錄執行）。

預設檢查 slides/index.html。檢查：
(a) 每個 class 含 "slide" 的 <section> 都有非空的 data-wiki；
(b) data-wiki 裡每個路徑（以空白分隔，相對 repo 根目錄）都存在；
(c) 頁數介於 15 到 20 頁。
全部通過輸出 `OK: N slides` 並以 0 結束；否則每個問題一行，以 1 結束。
"""
import sys
from html.parser import HTMLParser
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
MIN_SLIDES, MAX_SLIDES = 15, 20


class SlideParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.slides = []  # list of (line, data-wiki or None)

    def handle_starttag(self, tag, attrs):
        if tag != "section":
            return
        attrs = dict(attrs)
        classes = (attrs.get("class") or "").split()
        if "slide" in classes:
            self.slides.append((self.getpos()[0], attrs.get("data-wiki")))


def check(path):
    problems = []
    if not path.is_file():
        return [f"{path}: file not found"], 0
    parser = SlideParser()
    parser.feed(path.read_text(encoding="utf-8"))
    for n, (line, wiki) in enumerate(parser.slides, 1):
        where = f"slide {n} (line {line})"
        if wiki is None or not wiki.strip():
            problems.append(f"{where}: missing or empty data-wiki")
            continue
        for rel in wiki.split():
            target = (ROOT / rel).resolve()
            if not target.is_file():
                problems.append(f"{where}: data-wiki path not found: {rel}")
    count = len(parser.slides)
    if not MIN_SLIDES <= count <= MAX_SLIDES:
        problems.append(f"slide count {count} not in {MIN_SLIDES}-{MAX_SLIDES}")
    return problems, count


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "slides/index.html"
    path = Path(arg)
    if not path.is_absolute():
        path = ROOT / path
    problems, count = check(path)
    if problems:
        for p in problems:
            print(p)
        sys.exit(1)
    print(f"OK: {count} slides")


if __name__ == "__main__":
    main()
