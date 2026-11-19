# CLAUDE.md

這是我的 LLM Wiki 專案，主題是 RAG。AI 動手前先看這份，再看 `log.md` 知道上次做到哪。

## 專案目的

做一個關於 RAG（檢索增強生成）的 wiki 網站。想法是 LLM Wiki 那套：
我把論文摘要之類的原始資料丟進 `raw/`，AI 讀完以後整理成 `wiki/` 裡一頁一頁的 markdown，頁面之間互相連結。
最後用 `scripts/build.py` 轉成 HTML 放在 `docs/`，用 GitHub Pages 公開。

網站就是一個 index 首頁，連到各個 RAG 相關的內容頁。之後想加什麼主題（Graph RAG、評估方法、Agentic RAG……）就再丟資料進來讓 AI 寫。

## 資料夾

```
raw/papers/     原始資料，一篇論文一個檔，檔名用 arXiv id。AI 只能讀，不能改
wiki/           AI 寫的知識頁，一個概念一個 .md，不分子資料夾
wiki/index.md   首頁內容
slides/slides.md  教學簡報的內容稿，一頁一段，每頁標來源 wiki 頁
scripts/build.py  把 wiki/ 轉成 docs/，把 slides/ 轉成 docs/slides.html，順便做檢查
templates/page.html   wiki 網頁版型
templates/slides.html 簡報版型
docs/           產生出來的網站，不要手改
log.md          做了什麼、還有哪些資料沒整理、每次執行的檢查紀錄
WORKFLOW.md     整個 loop 的流程說明與反思
```

## 資料怎麼取得

我自己放。到 arXiv 把論文的標題、作者、日期、摘要貼成 `raw/papers/<arxiv-id>.md`，格式照現有檔案。只放摘要原文，不翻譯、不加自己的話。
其他來源（官方文件、部落格）放 `raw/notes/`，一樣只放原文。

## 網頁風格

簡單乾淨就好：米白底、單欄、不要太花。每種頁面類型有一個代表色（概念藍綠、來源綠、比較橘、問答紅）。
版面都由 `templates/page.html` 決定，想改風格就改那一個檔，不要在 wiki 頁裡塞 HTML。

## 頁面結構

- 首頁（`wiki/index.md`）：說明這個 wiki 是什麼、建議的閱讀順序、目前整理到哪。建站時會自動在後面列出所有頁面的卡片。
- 內容頁：標題、一句話摘要、正文、底下列出引用的來源和反向連結。

## 新增頁面的格式

每個 wiki 頁開頭要有 frontmatter，`build.py` 會檢查：

```yaml
---
title: Graph RAG
type: concept          # hub / concept / method / comparison / source / qa
summary: 一句話講這頁在講什麼
sources: [edge-2024-graphrag]   # 引用了哪些來源頁；來源頁本身改填 raw: 和 arxiv:
updated: 2026-11-12
---
```

正文大概照這個順序寫，不用太死：概念頁講「是什麼、為什麼需要、怎麼運作、限制」；來源頁講「書目、重點、對 wiki 哪些頁有貢獻」；問答頁就是「問題、回答、依據」。

連到別頁用 `[[slug]]`，指到不存在的頁會報錯。寫到的事實要能追到來源頁，沒有來源就先註明「待攝取」。

## 命名

- 檔名全部英文小寫加連字號，因為會變成網址：`graph-rag.md` → `graph-rag.html`。
- 來源頁用「作者-年份-關鍵字」，像 `edge-2024-graphrag.md`。
- 問答頁用 `qa-` 開頭。
- 內文用繁體中文，術語第一次出現附英文。

## 教學簡報怎麼生成

簡報是從 wiki 長出來的，不是 AI 自己想的。流程：

1. 先決定要教什麼，從 `wiki/` 找出會用到的頁。
2. 先寫大綱到 `slides/slides.md`：一頁一段，用 `---` 分隔，每頁開頭寫 `來源: slug`，標這頁內容是從哪個 wiki 頁來的。內容只能用那頁 wiki 寫的東西。
3. 大綱先給我看（先討論、後生成）。我沒有回應就直接往下做，但大綱要留著。
4. `python3 scripts/build.py` 會把 `slides.md` 轉成 `docs/slides.html`，並檢查：每頁都有來源、來源頁存在、沒有一頁沒內容。有錯就回去改 slides.md 或補 wiki。
5. 簡報要讓完全不懂的人看得懂：先講問題再講解法，一頁一個重點，最後一頁放延伸閱讀連回 wiki。

## 整個 loop

```
放 raw → AI 提案（要開哪頁、改哪頁） → 寫/改 wiki 頁 → build --check
   ↑                                                        │ 有錯回去改
   └──── 簡報檢查發現 wiki 缺內容 ←── 寫 slides.md → build 檢查簡報 → 產出 docs/
```

會重跑的是兩個檢查：wiki 的格式檢查、簡報對 wiki 的對應檢查。每次跑的結果記在 `log.md`，出錯的地方與怎麼修要寫下來，之後反思用。

## AI 要遵守的規則

1. `raw/` 只讀，`docs/` 不手改。
2. 新增或修改頁面後，跑 `python3 scripts/build.py --check` 沒錯誤再跑 `python3 scripts/build.py`，然後在 `log.md` 記一筆。
3. 提到已經有頁面的概念就用 `[[連結]]`，不要重寫一遍。一頁只講一個概念，太長就拆。
4. 不確定的數字、論文、名稱不要寫，寧可寫「待查」。
5. 加一篇新論文的標準流程：資料放進 `raw/papers/` → AI 先提案（這篇重點是什麼、要新開哪頁、改哪頁），寫進 `log.md` → 寫來源頁 → 更新相關概念頁並加連結 → 需要的話加進首頁閱讀順序 → check、build、記 log。提案我沒回應就照提案做。
6. 每次跑 build 有錯，把錯誤和修法記在 `log.md`，不要只修不記。
7. 如果要改這份規則，改完也記在 `log.md`。
