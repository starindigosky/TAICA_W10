---
title: Es et al. 2023 — RAGAS
type: source
summary: 不需要人工標準答案的 RAG 評估框架：用 LLM 自動評檢索找得準不準、生成有沒有忠於上下文。
tags: [evaluation]
raw: raw/papers/2309.15217.md
arxiv: 2309.15217
updated: 2026-11-18
---
## 書目
Es, S. et al. *RAGAS: Automated Evaluation of Retrieval Augmented Generation*. arXiv:2309.15217（2023 年 9 月）。

## 一句話
RAG 難評估，因為要同時看檢索找得準不準、生成有沒有忠於上下文、答案本身好不好；RAGAS 給一組不依賴人工標註的指標，讓迭代快起來。

## 核心主張
- 評估維度分開：檢索模組能否找到相關且聚焦的段落；LLM 是否忠實地使用這些段落；生成品質本身。
- 指標由 LLM 當評審計算，不需要 ground truth 標註。
- 目標是加速 RAG 架構的評估循環，因為 LLM 應用迭代很快。

## 對本 wiki 的貢獻
- [[rag-evaluation]]：三個評估維度與「不用標準答案」的做法。
