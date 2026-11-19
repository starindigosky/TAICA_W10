---
title: Edge et al. 2024 — 微軟 GraphRAG 論文
type: source
summary: 「From Local to Global」：用 LLM 建實體知識圖與社群摘要，回答向量 RAG 答不了的全局問題。
tags: [graph-rag, microsoft]
raw: raw/papers/2404.16130.md
arxiv: 2404.16130
updated: 2026-11-12
---
## 書目
Edge, D. et al. *From Local to Global: A Graph RAG Approach to Query-Focused Summarization*. Microsoft Research. arXiv:2404.16130（2024 年 4 月）。

## 一句話
傳統 RAG 答不了「這批資料的主要主題是什麼」這種全局問題，因為那其實是查詢導向摘要（query-focused summarization, QFS）而不是檢索；GraphRAG 用知識圖加社群摘要把兩者接起來。

## 核心主張
- 索引分兩步：先用 LLM 從文件抽出實體知識圖，再對緊密相關的實體群（社群）預先生成社群摘要。
- 查詢時，每個社群摘要先各自產生部分回答，再把所有部分回答彙整成最終答案（map-reduce）。
- 在百萬 token 等級的資料集上，對全局性的「理解全貌」問題，答案的全面性（comprehensiveness）與多樣性（diversity）大幅優於傳統 RAG。

## 對本 wiki 的貢獻
- [[graph-rag]]：向量 RAG 的全局問題盲點、知識圖＋社群摘要的流程。
