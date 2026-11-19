# log.md — 工作紀錄

> 每次攝取／簡報／健檢各記一筆，最新的放最上面。有錯要寫錯在哪、怎麼修。

## 2026-11-18 ｜ 簡報 ｜ 從 wiki 生成「RAG 是什麼？從向量 RAG 到 Graph RAG」12 頁
- 大綱寫在 `slides/slides.md`，每頁標 `來源: slug`。使用者未回應，照大綱直接生成。
- **第 1 次 build**：格式檢查全過（每頁有來源、來源頁存在、有標題）。
- **人工對照**每頁與來源頁：第 2 頁有兩句 wiki 沒寫的內容（「公司內部文件它更沒看過」、「重新訓練模型既貴又慢」）。前者在 Gao 綜述摘要有依據，補進 `wiki/rag.md` 並附來源；後者沒來源，從簡報刪掉。
- 因為格式檢查抓不到這種「AI 混入 wiki 沒有的內容」，在 `build.py` 加了一條檢查：簡報裡的**粗體詞必須出現在來源頁**。
- **第 2 次 build**：新檢查報 4 個錯：
  - 第 2 頁「知識有截止日期」「看不到你的資料」：wiki 有講同一件事但用詞不同 → 改簡報用詞對齊 wiki。
  - 第 5 頁「不訓練模型」：這句其實來自 `rag` 頁，不是該頁標的來源 `lewis-2020-rag` → 取消粗體，改成連回 `[[rag]]`。
  - 第 10 頁「雙索引」：來自 `graph-rag` 頁的講法，來源頁 `guo-2024-lightrag` 寫的是「圖與向量可以一起用」→ 改成來源頁的講法。
- **第 3 次 build**：0 錯誤，輸出 `docs/slides.html`。

## 2026-11-18 ｜ 攝取 ｜ 3 篇新來源：LightRAG、Gao 綜述、RAGAS
- **提案**（寫下來代替討論，使用者未回應即照做）：
  - 2410.05779 LightRAG → 新開來源頁 `guo-2024-lightrag`；`graph-rag` 頁補一段「省成本的做法」並把原本的「待攝取」註記換成連結。
  - 2312.10997 Gao 綜述 → 新開 `gao-2023-rag-survey`；`rag` 頁補 Naive／Advanced／Modular 三範式。
  - 2309.15217 RAGAS → 新開 `es-2023-ragas`；評估是新主題，新開概念頁 `rag-evaluation`，從 `rag`、`graph-rag` 連過去。首頁閱讀順序加第 3 步。
- 執行結果：`build.py --check` 9 頁 0 錯誤 0 警告，一次過。

## 2026-11-18 ｜ 規則 ｜ CLAUDE.md 加入資料取得、簡報生成、整個 loop 三節
- 新增 `slides/`、`templates/slides.html`、`WORKFLOW.md`；`build.py` 多了簡報的轉換與檢查。

## 2026-11-12 ｜ 攝取 ｜ 建立 wiki：2 篇來源、2 頁知識頁
- 來源頁 `lewis-2020-rag`、`edge-2024-graphrag`；知識頁 `rag`、`graph-rag`；總覽 `index`。

## 2026-11-12 ｜ 建立專案 ｜ CLAUDE.md、建站腳本、版型

---

## 待攝取
- 2405.14831 HippoRAG（知識圖＋Personalized PageRank 做多跳）
- 2310.11511 Self-RAG、2401.15884 CRAG（自我反思與修正式 RAG）
- 2407.16833 RAG 與長上下文的比較
