---
title: Lewis et al. 2020 — RAG 原始論文
type: source
summary: 提出「檢索增強生成」一詞的 NeurIPS 2020 論文：把 DPR 檢索器與 BART 生成器接起來端到端訓練。
tags: [rag, foundation]
raw: raw/papers/2005.11401.md
arxiv: 2005.11401
updated: 2026-11-12
---
## 書目
Lewis, P. et al. *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. NeurIPS 2020. arXiv:2005.11401。

## 一句話
把「參數記憶」（預訓練的 seq2seq 模型）和「非參數記憶」（維基百科的稠密向量索引）結合，讓模型生成時先檢索再作答。

## 核心主張
- 檢索器用 DPR（雙塔稠密檢索），生成器用 BART；兩者可一起微調，但文件索引固定不動。
- 兩種變體：RAG-Sequence 整段答案用同一組檔；RAG-Token 每個 token 可以參考不同文件。
- 在開放域問答上贏過只靠參數的 seq2seq 模型與抽取式基線；生成的語言更具體、更少幻覺。
- 知識可以「換索引就更新」，不必重訓模型。

## 對本 wiki 的貢獻
- [[rag]]：RAG 的定義、三階段流程與名詞由來。
- [[graph-rag]]：作為比較基線的向量 RAG。
