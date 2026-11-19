---
title: Gao et al. 2023 — RAG 綜述
type: source
summary: 把 RAG 分成 Naive、Advanced、Modular 三個範式，整理檢索、生成、增強三大元件的技術與評估方法。
tags: [rag, survey]
raw: raw/papers/2312.10997.md
arxiv: 2312.10997
updated: 2026-11-18
---
## 書目
Gao, Y. et al. *Retrieval-Augmented Generation for Large Language Models: A Survey*. arXiv:2312.10997（2023 年 12 月）。

## 一句話
最常被引用的 RAG 綜述，給了「Naive RAG → Advanced RAG → Modular RAG」這條大家常用的演進分類。

## 核心主張
- LLM 的三個痛點：幻覺、知識過期、推理追不到出處；RAG 用外部資料庫補上，知識可以持續更新。
- **Naive RAG**：切塊、嵌入、檢索 top-k、塞進 prompt 生成。
- **Advanced RAG**：在檢索前（索引優化、查詢改寫）與檢索後（重排、壓縮）加優化。
- **Modular RAG**：搜尋、記憶、路由、融合等做成可重組的模組，流程不再是固定一條線。
- 另整理了評估框架與基準，以及尚未解決的挑戰。

## 對本 wiki 的貢獻
- [[rag]]：三個範式的分類與 RAG 要解決的痛點。
- [[rag-evaluation]]：評估為什麼要分檢索與生成兩段看。
