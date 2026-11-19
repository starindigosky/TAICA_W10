---
title: RAG Wiki
type: hub
summary: 一座關於檢索增強生成（RAG）的 LLM Wiki：原始論文放 raw/，知識頁由 AI 依 CLAUDE.md 的規則整理在 wiki/。
tags: [hub]
updated: 2026-11-18
---
## 這座 wiki 怎麼運作
資料分兩層：`raw/` 是人放進來、不會被改的原始來源（論文摘要）；`wiki/` 是 AI 讀完 raw 後整理出來、會持續修改與互相連結的知識頁。網站由 `scripts/build.py` 從 `wiki/` 產生。每個主張都連到「來源」頁，來源頁再對應到 `raw/` 的原始檔。

## 建議閱讀順序
1. [[rag]]：先懂基本的三階段流程。
2. [[graph-rag]]：為什麼要把片段升級成知識圖。
3. [[rag-evaluation]]：怎麼知道自己的 RAG 做得好不好。

## 教學簡報
- [RAG 是什麼？從向量 RAG 到 Graph RAG](slides.html)：從這座 wiki 生出來的入門簡報。

## 目前狀態
- 已攝取 5 篇來源：[[lewis-2020-rag]]、[[gao-2023-rag-survey]]、[[edge-2024-graphrag]]、[[guo-2024-lightrag]]、[[es-2023-ragas]]。
- 想新增內容：把來源丟進 `raw/`，照 `CLAUDE.md` 的流程 A 攝取即可；待攝取清單在 `log.md`。
