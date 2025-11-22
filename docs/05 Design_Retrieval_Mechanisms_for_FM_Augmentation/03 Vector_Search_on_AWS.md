## Vector Search on AWS 🔍

Vector search lets you find results by **meaning**, not just matching words. This note connects foundation model embeddings, similarity metrics, and the main AWS services you’ll see on the exam.

---

## 1. From text to embeddings 🧠➡️🔢

Foundation models turn text into high‑dimensional vectors (embeddings) in four logical steps:
- **Preprocessing & tokenization**
  - Normalize text (case, punctuation, special chars) and split into tokens (subwords/word pieces).
- **Contextual encoding**
  - Multiple transformer layers build context across tokens (syntax + semantics).
- **Vector generation**
  - Final hidden states are combined into dense vectors (hundreds–thousands of dimensions).
- **Optimization & output**
  - Optional dimensionality reduction / normalization to make embeddings practical for search.

Result: Similar meanings → **nearby vectors** in a high‑dimensional space, even if the exact words differ.

---

## 2. Semantic similarity & vector space geometry 📐

- **Key ideas**
  - Embeddings live in a **high-dimensional vector space**.
  - **Semantic similarity ≈ geometric proximity** (close vectors = related meaning).
  - Related concepts form **clusters**; unrelated ones are far apart.
- **Common similarity metrics**
  - **Cosine similarity** – angle between vectors (−1 to 1). Most common for semantic search.
  - **Euclidean distance** – straight-line distance; considers magnitude.
  - **Dot product** – combines angle + magnitude; used in some ANN libraries.
  - **Manhattan distance** – sum of absolute differences (less common here).
- **Dimensionality tradeoffs**
  - Higher dimensions → richer nuance, more storage/compute.
  - Lower dimensions → faster, cheaper, but less expressive.
  - Typical ranges: **128–1536**; pick based on accuracy vs cost/latency needs.

---

## 3. Vector search vs keyword search ⚖️

**Vector search**
- Matches on **semantic similarity**, not exact terms.
- Handles synonyms, paraphrases, and even cross‑language (with multilingual models).
- Great for:
  - Natural language queries (“How can I reduce S3 costs?”).
  - FAQ matching and support assistants.
  - Recommendations based on content similarity.
  - Research / discovery where users don’t know exact terms.

**Keyword search**
- Matches **exact words/phrases**; often supports Boolean logic.
- Very fast and easy to index.
- Great for:
  - IDs / codes (error IDs, ticket numbers, SKUs).
  - Compliance / e‑discovery where **exact phrases** matter.
  - Highly structured fields and filters.

**Hybrid search**
- Combine **vector + keyword**:
  - Use embeddings for semantic matches.
  - Use keywords for exact matches and filters.
  - Fuse/weight results from both for robust behavior.

Exam anchor: For **natural language + ambiguity**, favor vector or hybrid; for **exact identifiers & compliance**, favor keyword (possibly with hybrid).

---

## 4. AWS vector search options 🧱

High level choices:

- **Amazon OpenSearch Service (with k‑NN/ANN)**
  - Best for: **high‑performance, low‑latency semantic search** with rich analytics and filters.
  - Capabilities:
    - Native k‑NN (multiple ANN algorithms).
    - Real‑time indexing + updates.
    - Advanced filtering, aggregations, dashboards.
    - Horizontal scaling via sharding + replicas.
  - Example pattern:
    - Store embeddings in a vector field.
    - Run a k‑NN query with your query embedding to get **top‑k similar docs**.

- **Amazon Aurora PostgreSQL with pgvector**
  - Best for: Apps that already use **PostgreSQL** and need **relational + vector** in one place.
  - Capabilities:
    - Vector type and indexes inside Postgres.
    - JOIN vectors with relational tables in SQL.
    - Managed HA, backups, read replicas from Aurora.
  - Good for:
    - Transactional systems needing light/medium vector search without extra infra.

- **Amazon S3 Vectors**
  - Best for: Large‑scale, **cost‑efficient vector storage** integrated with S3.
  - Capabilities:
    - Store embeddings alongside data in S3.
    - Serverless, pay‑per‑use semantics.
  - Typically used when you:
    - Need to keep cost low at very large scale.
    - Are comfortable orchestrating your own retrieval logic.

- **Amazon Bedrock Knowledge Bases**
  - Best for: **Managed RAG** – fast path to question‑answering over your data.
  - Capabilities:
    - Fully managed ingestion → chunking → embedding → vector storage.
    - Configurable sources (S3, Confluence, etc.) and embedding models.
    - Built‑in retriever API wired to Bedrock FMs.
  - Tradeoffs:
    - Minimal ops, but less low‑level control than custom OpenSearch/pgvector setups.

---

## 5. Choosing the right service 🧭

Use these guiding questions:
- **Do you need rich filters, dashboards, and sub‑ms latency?**
  - → **OpenSearch Service**.
- **Already on PostgreSQL and want relational + vector in one place?**
  - → **Aurora PostgreSQL with pgvector**.
- **Need ultra‑low‑cost, large‑scale vector storage and can build your own retrieval logic?**
  - → **S3 Vectors**.
- **Want a managed RAG solution with minimal plumbing?**
  - → **Bedrock Knowledge Bases**.

Always align:
- **Performance** (latency, throughput).
- **Scale** (data volume, growth).
- **Cost** (storage + queries + ops).
- **Operational complexity** (who will run and tune it).

If you can explain **how embeddings work**, **why cosine similarity is used**, and **which AWS vector service fits which scenario**, you’re in great shape for this part of the exam.


