## Advanced Relevance Engineering with Rerankers 🎯

Once you have good **chunking** and **vector search**, the next lever for quality is **relevance engineering**: how you score, filter, and *rerank* candidates before sending them to the FM.

---

## 1. Multi-stage retrieval pipeline 🧵

Typical high-level flow:

1. **Candidate generation (fast, approximate)**
   - Vector search (OpenSearch, pgvector, S3 Vectors, KB index) returns top‑N chunks.
   - Optional keyword / metadata filters (doc type, region, date, ACLs).
2. **Reranking (slower, precise)**
   - A more expensive model reorders these N candidates by **true relevance** to the query.
   - Only top‑k (e.g., 5–10) are passed on to the FM as context.
3. **Answer generation**
   - FM consumes the reranked context + query and produces final answer.

Key idea: **cheap first, smart second** – use fast retrieval to narrow the field, then rerank with a more powerful model.

_Diagram (fits this flow conceptually):_

![Data ingestion pipeline](./images/data-ingestion-pipeline.svg)

---

## 2. Relevance signals & scoring ⚖️

Common relevance signals used before/with rerankers:

- **Vector similarity**
  - Cosine similarity / dot product from embedding search.
- **Keyword / BM25 scores**
  - Classic IR scores, great for matching exact terms and IDs.
- **Metadata boosts**
  - Recency (timestamp), authority (owner/department), document type (policy vs blog).
- **Behavioral signals**
  - Click‑throughs, “helpful” votes, downstream task success.

You can combine scores using:
- Weighted linear combinations (e.g., `0.6 * vector + 0.3 * BM25 + 0.1 * recency`).
- Reciprocal Rank Fusion (RRF) or similar fusion techniques for hybrid search.

Rerankers sit on top of these base scores to refine ordering even further.

---

## 3. Types of rerankers 🧠

- **Traditional ML rerankers**
  - Gradient-boosted trees / learning-to-rank models trained on features:
    - Base scores (vector/BM25), query/document features, metadata, engagement signals.
  - Pros: efficient, interpretable feature contributions; cons: need labeled data & feature engineering.

- **Neural cross-encoders**
  - Models that take **[query, document]** pairs and directly output a relevance score.
  - Much more accurate but higher latency; ideal as **final reranking layer on top‑N**.

- **FM/LLM-based rerankers**
  - Use a foundation model (Bedrock text model) with prompts like:
    - “Given the question and candidate passages, rank the passages from most to least relevant.”
  - Very flexible and strong, especially for nuanced enterprise language, at the cost of latency and tokens.

Exam angle: you should know that **LLM/FMs are often used as “last-mile rerankers”** after a fast vector/keyword candidate stage.

---

## 4. Implementing rerankers on AWS 🧱

Typical architecture:

- **Stage 1 – Retrieve**
  - Lambda or a service calls vector search (OpenSearch, KB index, pgvector, etc.) to get top‑N candidates.
  - Optionally pulls keyword/BM25 scores for hybrid retrieval.
- **Stage 2 – Rerank (Lambda + Bedrock)**
  - Lambda batches `[query, candidate_chunk]` pairs.
  - Calls **Amazon Bedrock** (e.g., Claude / Nova) or a smaller cross‑encoder model hosted on SageMaker.
  - Receives a relevance score per candidate and reorders them.
- **Stage 3 – Generate**
  - Lambda selects top‑k, builds a context‑rich prompt, and calls a Bedrock FM to answer.

You can also deploy:
- Lightweight rerank models via **SageMaker Endpoints** for lower latency.
- Feature stores (e.g., DynamoDB) to track and reuse relevance features.

---

## 5. Evaluating and tuning relevance 📊

Key metrics:
- **Offline**
  - NDCG, MRR, precision@k, recall@k on labeled query–doc sets.
  - Ablation: compare baseline vector-only vs reranked pipeline.
- **Online**
  - Click‑through rate, “answer helpful” scores, time‑to‑resolution.
  - Guardrail metrics (hallucination rate, off‑topic answers) with and without rerankers.

Practical tuning tips:
- Start with **simple hybrid scoring** (vector + BM25 + recency).
- Add a **small reranker** (ML or FM) only on top‑N candidates to control latency.
- Log **features + outcomes** to iteratively improve models and weights.

---

## 6. Why this matters for the exam ✅

Be prepared to:
- Recognize multi‑stage retrieval architectures and **where rerankers fit**.
- Explain tradeoffs between **speed vs quality** when introducing FM-based rerankers.
- Choose appropriate AWS components (OpenSearch/KB for retrieval, Bedrock/SageMaker for reranking, Lambda/APIGW for orchestration).

Advanced relevance engineering is often what turns a “works on paper” RAG system into a **reliable, production‑grade assistant**. 

---

## 7. Relevance across document lifecycle & KB configuration 🔁

Reranking quality depends heavily on **where your content is in its lifecycle** and **how your KB/index is configured**:

- **Document lifecycle signals**
  - Use lifecycle stage (draft, approved, deprecated) as **boosts/filters** in relevance.
  - Prefer **current, approved** docs; down‑rank or exclude retired content.
  - Incorporate **effective/expiry dates** into scoring to keep answers fresh.

_Diagram:_  
![Document lifecycle management](./images/document-lifecycle-management.svg)

- **Knowledge base configuration levers**
  - Choose embedding model and chunking strategy appropriate for your domain.
  - Tune `top_k`, similarity thresholds, and filters (doc type, region, business unit).
  - Decide where to apply **rerankers**: inside app code, via Bedrock, or on a custom index.

_Diagram:_  
![Bedrock Knowledge Bases foundation](./images/kb-creation-foundation.svg)

On the exam, be ready to connect **lifecycle, KB configuration, and rerankers** as a single system: the better your upstream curation and KB setup, the less work your reranker has to do—and the more consistent your answers will be.


