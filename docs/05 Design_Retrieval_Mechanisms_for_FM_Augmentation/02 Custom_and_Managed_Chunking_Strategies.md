## Custom and Managed Chunking Strategies 🧩

This note builds on `Document_Segmentation_Fundamentals` and focuses on **how** you implement chunking in real systems: when to rely on **managed** chunking (e.g., Bedrock Knowledge Bases, Kendra) vs **custom pipelines**, and how that shows up on the exam.

---

## 1. Managed vs custom chunking – when to use which? ⚖️

- **Managed chunking (platform default)**
  - Examples: Bedrock Knowledge Bases, Kendra connectors, some SaaS search tools.
  - Pros:
    - Fast time-to-value, minimal engineering.
    - Tuned defaults for common doc types (Office/PDF/wiki pages).
    - Integrated with indexing, metadata, and security models.
  - Cons:
    - Less control over exact boundaries, overlaps, and metadata schema.
    - Harder to implement domain-specific logic (tables/diagrams/code blocks).

- **Custom chunking**
  - You control **how** docs are parsed and segmented before writing to a vector DB or KB.
  - Pros:
    - Fine-grained handling of **headings, layout, tables, code, multimodal content**.
    - Easier to align with **domain semantics** and downstream evaluation metrics.
    - Can keep **hierarchies and parent–child relationships** explicit in metadata.
  - Cons:
    - More engineering effort (parsers, pipelines, tests, monitoring).

**Exam tip:** Default/managed chunking is acceptable for many use cases, but for **regulated, highly-structured, or domain-heavy content**, expect to justify **custom chunking** for better control and explainability.

---

## 2. Common chunking patterns (what the diagrams are showing) 🧱

The course diagrams map to four practical patterns:

- **Fixed-size chunking**
  - Simple N-character or N-token windows (optionally with overlap).
  - Easy to implement; ignores semantics → better for logs, transcripts, raw text.

- **Default/managed chunking**
  - Service decides chunk boundaries based on built-in heuristics.
  - Good baseline; often enough for “standard enterprise documents.”

- **Hierarchical chunking**
  - Use structure: `chapter → section → subsection → paragraph`.
  - Ideal for long manuals, policies, and wikis where headings matter.

- **Semantic chunking**
  - Split based on **topic shifts** / semantic boundaries (embeddings, topic models).
  - Produces variable-sized chunks that stay highly coherent.

**Design pattern:** Many real systems use **hierarchical + semantic** chunking together: structure first, then semantic refinement inside sections.

---

## 3. Custom chunking pipelines on AWS ⚙️

Typical architecture for custom chunking and indexing:

- **Ingestion & parsing**
  - S3 for raw docs; Lambda / ECS for parsing (PDF → text/HTML; DOCX → structured text).
  - Use layout-aware tools (Textract, HTML/Markdown parsing) to preserve headings, lists, tables.

- **Segmentation service**
  - Lambda / container that:
    - Detects headings and structural markers.
    - Applies **hierarchical + semantic** chunking rules.
    - Adds metadata: `doc_id`, `section_path`, `chunk_level`, `order`, `parent_id`.

- **Embedding + storage**
  - Call Titan (or other) embeddings for each chunk.
  - Store in vector DB / KB with metadata for filtering:
    - `source_system`, `doc_type`, `section`, `last_reviewed`, `compliance_tag`, etc.

- **Configuration workflow**
  - Store chunking parameters (sizes, overlaps, allowed types, filters) in **AppConfig/Parameter Store** so you can tune behavior **without redeploying code**.

Key AWS services: S3, Lambda, ECS/EKS (if needed), Textract, AppConfig, Bedrock embeddings, OpenSearch / Knowledge Bases / DynamoDB+vector.

---

## 4. Where managed chunking still shines ✅

Use **managed chunking** when:
- You’re integrating with **SharePoint, Confluence, file shares** via Kendra or KB connectors.
- You need **security trimming** and ACL fidelity with minimal custom code.
- The exam scenario emphasizes **time-to-delivery** and **operational simplicity** over extreme tuning.

You can often combine both:
- Let connectors handle **source sync + security**.
- Add a **post-processing step** (Lambda pipeline) that re-chunks or re-embeds for specialized indexes.

---

## 5. Evaluation & tuning for custom vs managed 📏

For both approaches, use the same evaluation loop:
- **Offline metrics**
  - Relevance (precision/recall/F1) on a labeled QA set.
  - Chunk cohesion and redundancy (too many near-duplicates?).
- **Online metrics**
  - Click-through, “answer helpful?” ratings.
  - Coverage: % of queries resolved without escalation / handoff.
- **Cost & performance**
  - Latency per query, tokens per call, index size, re-index cost.

If managed chunking underperforms on **hard, domain-specific queries**, that’s your signal to introduce **custom strategies** for those collections.

---

## 6. Visual aids from the course 🖼️

Use these diagrams from `docs/tmp` as quick refreshers:

- **Chunking types overview**

  ![Chunking types](../tmp/AWS Generative AI Developer - Design Retrieval Mechanisms for FM Augmentation_files/chunking-types.svg)

- **Configuration / workflow**

  ![Chunking configuration workflow](../tmp/AWS Generative AI Developer - Design Retrieval Mechanisms for FM Augmentation_files/configuration-workflow.svg)

- **Custom use cases**

  ![Custom chunking use cases](../tmp/AWS Generative AI Developer - Design Retrieval Mechanisms for FM Augmentation_files/custom-use-cases.svg)

These mirror the ideas above and are useful “visual flashcards” before the exam.


