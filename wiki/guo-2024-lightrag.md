---
title: Guo et al. 2024 — LightRAG
type: source
summary: 圖結構＋向量的雙層檢索，目標是比 GraphRAG 便宜、快，而且支援增量更新。
tags: [graph-rag]
raw: raw/papers/2410.05779.md
arxiv: 2410.05779
updated: 2026-11-18
---
## 書目
Guo, Z. et al. *LightRAG: Simple and Fast Retrieval-Augmented Generation*. arXiv:2410.05779（2024 年 10 月）。程式碼開源。

## 一句話
既有 RAG 靠「平面」的片段表示，答案常常破碎、抓不到實體之間的關聯；LightRAG 把圖結構放進索引與檢索，並用雙層檢索同時照顧具體與抽象的問題。

## 核心主張
- 索引時用 LLM 抽實體與關係建成圖，再把節點與邊做成向量，圖與向量可以一起用。
- **雙層檢索**：低層針對具體實體與關係，高層針對主題與抽象概念。
- 有增量更新演算法，新文件進來只合併新圖，不必整批重建。
- 實驗顯示檢索準確度與效率都優於既有做法。

## 對本 wiki 的貢獻
- [[graph-rag]]：降低建圖成本與增量更新的做法。
