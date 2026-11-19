# RAG Wiki

一座關於檢索增強生成（RAG）的 **LLM Wiki**：原始論文摘要放在 `raw/`（人放、不改），AI 讀完後整理成互相連結的知識頁放在 `wiki/`，再由 `scripts/build.py` 建成靜態網站 `docs/`，用 GitHub Pages 發布。

- Wiki 網站：`https://<你的帳號>.github.io/rag-wiki/`
- 教學簡報：`https://<你的帳號>.github.io/rag-wiki/slides.html`（從 wiki 生成，每頁標出處）
- 規則：[`CLAUDE.md`](CLAUDE.md)；loop 設計、執行紀錄與反思：[`WORKFLOW.md`](WORKFLOW.md)；工作紀錄：[`log.md`](log.md)

## 怎麼用
```bash
pip install mistune
python3 scripts/build.py --check   # 健檢：壞連結、缺欄位、孤兒頁
python3 scripts/build.py           # 建站到 docs/，同時把 slides/slides.md 轉成 docs/slides.html 並檢查
```
把 `docs/` 一起 commit，GitHub Pages 設為 `main` 分支的 `/docs` 資料夾即可。

## 之後要新增內容時，規則怎麼幫 AI
AI 讀 `CLAUDE.md` 就知道：來源放哪、頁面檔名怎麼取、frontmatter 要填哪些欄位、每種頁型的章節順序、要用 `[[wikilink]]` 互連、主張要附來源；做完要跑 `--check` 再 build，再記 `log.md`。所以只要說「把這篇論文加進 wiki」，AI 就能照流程 A 自己完成，產出的頁面風格與結構會和現有的一致。
