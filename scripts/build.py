#!/usr/bin/env python3
"""把 wiki/*.md 建成 docs/*.html（GitHub Pages 用）。

用法：
    python3 scripts/build.py           # 健檢 + 建站
    python3 scripts/build.py --check   # 只健檢（壞 wikilink、缺欄位、孤兒頁…），不輸出
需要：pip install mistune
"""
import datetime as dt, pathlib, re, shutil, sys
import mistune

ROOT = pathlib.Path(__file__).resolve().parents[1]
WIKI, DOCS, TPL = ROOT / "wiki", ROOT / "docs", ROOT / "templates" / "page.html"
SLIDES, SLIDES_TPL = ROOT / "slides" / "slides.md", ROOT / "templates" / "slides.html"
TYPES = {"hub": "總覽", "concept": "概念", "method": "方法", "comparison": "比較", "qa": "問答", "source": "來源"}
REQUIRED = ["title", "type", "summary", "updated"]
WIKILINK = re.compile(r"\[\[([^\]|]+?)(?:\|([^\]]+?))?\]\]")
FRONT = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.S)
md = mistune.create_markdown(escape=False, plugins=["table", "strikethrough"])


def load():
    pages, errs = {}, []
    for path in sorted(WIKI.glob("*.md")):
        m = FRONT.match(path.read_text(encoding="utf-8"))
        if not m:
            errs.append(f"{path.name}: 缺少 frontmatter"); continue
        meta = {}
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                v = v.split(" #")[0].strip().strip('"')
                meta[k.strip()] = [x.strip() for x in v[1:-1].split(",") if x.strip()] if v.startswith("[") else v
        pages[path.stem] = {"slug": path.stem, "meta": meta, "body": m.group(2)}
    return pages, errs


def check(pages):
    errs, warns, inbound = [], [], {s: set() for s in pages}
    for slug, p in pages.items():
        m = p["meta"]
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug): errs.append(f"{slug}: 檔名要英文小寫連字號")
        for k in REQUIRED:
            if not m.get(k): errs.append(f"{slug}: frontmatter 缺 {k}")
        if m.get("type") not in TYPES: errs.append(f"{slug}: type 不合法：{m.get('type')!r}")
        try: dt.date.fromisoformat(str(m.get("updated", "")))
        except ValueError: errs.append(f"{slug}: updated 要是 YYYY-MM-DD")
        if re.search(r"^# ", p["body"], re.M): errs.append(f"{slug}: 內文不要寫 H1")
        if m.get("type") == "source":
            if not m.get("raw") or not (ROOT / m["raw"]).exists(): errs.append(f"{slug}: raw 檔不存在：{m.get('raw')}")
        elif m.get("type") != "hub":
            if not m.get("sources"): warns.append(f"{slug}: 沒有填 sources")
            for s in m.get("sources") or []:
                if s not in pages or pages[s]["meta"].get("type") != "source": errs.append(f"{slug}: sources 裡的 {s} 不是存在的 source 頁")
        targets = {t.strip() for t, _ in WIKILINK.findall(p["body"])}
        for t in targets:
            if t in pages: inbound[t].add(slug)
            else: errs.append(f"{slug}: wikilink 指到不存在的頁 [[{t}]]")
        if not targets: warns.append(f"{slug}: 沒有連出任何頁")
    for slug, p in pages.items():
        p["in"] = sorted(inbound[slug])
        if p["meta"]["type"] != "hub" and not p["in"]: warns.append(f"{slug}: 孤兒頁")
    return errs, warns


def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
def link(pages, slug, text=None): return f'<a class="wl" href="{slug}.html">{esc(text or pages[slug]["meta"]["title"])}</a>'
def render(pages, body): return md(WIKILINK.sub(lambda m: link(pages, m.group(1).strip(), m.group(2)), body))
def card(pages, s):
    m = pages[s]["meta"]
    return f'<a class="card" href="{s}.html" style="--accent:var(--{m["type"]})"><span class="badge">{TYPES[m["type"]]}</span><b>{esc(m["title"])}</b><p>{esc(m["summary"])}</p></a>'


def build(pages):
    shutil.rmtree(DOCS, ignore_errors=True); DOCS.mkdir()
    (DOCS / ".nojekyll").write_text("")
    tpl = TPL.read_text(encoding="utf-8")
    nav = "".join(f'<a href="index.html#{t}">{n}</a>' for t, n in TYPES.items() if t != "hub")
    for slug, p in pages.items():
        m = p["meta"]
        if m["type"] == "source":
            srcs = f'<code>{esc(m["raw"])}</code>' + (f' ・ <a href="https://arxiv.org/abs/{m["arxiv"]}">arXiv:{m["arxiv"]}</a>' if m.get("arxiv") else "")
        else:
            srcs = "、".join(link(pages, s) for s in m.get("sources") or []) or "（無）"
        if m["type"] == "hub":  # 首頁：hub 內文 + 依類型列出所有頁
            extra = ""
            for t, n in TYPES.items():
                slugs = [s for s in pages if pages[s]["meta"]["type"] == t]
                if slugs: extra += f'<h2 id="{t}">{n}</h2><div class="grid">{"".join(card(pages, s) for s in slugs)}</div>'
        else:
            extra = '<aside class="backlinks"><h2>反向連結</h2><ul>' + ("".join(f"<li>{link(pages, s)}</li>" for s in p["in"]) or "<li>（尚無）</li>") + "</ul></aside>"
        html = tpl
        for k, v in dict(title=esc(m["title"]), type=m["type"], type_label=TYPES[m["type"]], summary=esc(m["summary"]), sources=srcs,
                         updated=str(m["updated"]), content=render(pages, p["body"]), extra=extra, nav=nav, slug=slug).items():
            html = html.replace("{{" + k + "}}", v)
        (DOCS / f"{slug}.html").write_text(html, encoding="utf-8")


def load_slides():
    """slides.md：第一行 title:，之後用 --- 分頁，每頁開頭 來源: slug。"""
    if not SLIDES.exists():
        return None, []
    text = SLIDES.read_text(encoding="utf-8")
    head, _, rest = text.partition("\n---\n")
    title = head.split(":", 1)[1].strip() if head.startswith("title:") else "教學簡報"
    slides = []
    for n, chunk in enumerate(rest.split("\n---\n"), 1):
        lines = chunk.strip().splitlines()
        src = lines[0].split(":", 1)[1].strip() if lines and lines[0].startswith("來源:") else None
        slides.append({"n": n, "src": src, "body": "\n".join(lines[1:] if src else lines)})
    return title, slides


def check_slides(pages, slides):
    """格式檢查 + 粗略的內容對應檢查：簡報裡的粗體詞要能在來源頁找到。"""
    errs = []
    for s in slides:
        if s["src"] in pages:
            src_text = pages[s["src"]]["meta"]["title"] + pages[s["src"]]["body"]
            for term in re.findall(r"\*\*([^*]+)\*\*", s["body"]):
                key = re.sub(r"（.*?）|\(.*?\)", "", term).strip()
                if key and key not in src_text:
                    errs.append(f"slides 第 {s['n']} 頁: 粗體詞「{term}」在來源頁 {s['src']} 找不到，內容可能不是從 wiki 來的")
        if not s["src"]: errs.append(f"slides 第 {s['n']} 頁: 沒有寫 來源: slug")
        elif s["src"] not in pages: errs.append(f"slides 第 {s['n']} 頁: 來源頁 {s['src']} 不存在")
        if not re.search(r"^#{1,2} ", s["body"], re.M): errs.append(f"slides 第 {s['n']} 頁: 沒有標題")
        if len(s["body"].strip()) < 20: errs.append(f"slides 第 {s['n']} 頁: 幾乎沒有內容")
        for t, _ in WIKILINK.findall(s["body"]):
            if t.strip() not in pages: errs.append(f"slides 第 {s['n']} 頁: wikilink 指到不存在的頁 [[{t}]]")
    return errs


def build_slides(pages, title, slides):
    html = "".join(f'<section class="slide">{render(pages, s["body"])}<div class="src">出處：{link(pages, s["src"])}</div></section>' for s in slides)
    out = SLIDES_TPL.read_text(encoding="utf-8").replace("{{title}}", esc(title)).replace("{{slides}}", html)
    (DOCS / "slides.html").write_text(out, encoding="utf-8")


def main(argv):
    pages, errs = load()
    e2, warns = check(pages); errs += e2
    title, slides = load_slides()
    errs += check_slides(pages, slides)
    for w in warns: print("WARN ", w)
    for e in errs: print("ERROR", e)
    print(f"{len(pages)} 頁，{len(errs)} 個錯誤，{len(warns)} 個警告")
    if errs: return 1
    if slides: print(f"簡報 {len(slides)} 頁")
    if "--check" not in argv:
        build(pages)
        if slides: build_slides(pages, title, slides)
        print("已輸出到 docs/")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
