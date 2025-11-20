## GenAI Developer Professional – Project Context 🎯

This repository is a learning lab for the **AWS Generative AI Developer Professional** certification. It’s organized around three core skill areas that you should be able to explain, design for, and implement in code.

---

## Section 1: Foundation Model Assessment and Selection 🧠

**Goal:** Systematically evaluate foundation models (FMs) and pick the right one for a business use case.

### What you should be able to do
- **Frame the business problem** as FM capabilities:
  - Classification, extraction, RAG, tool use, multi-modal, streaming, etc.
- **Compare models** using:
  - Quantitative metrics (latency, cost per 1K tokens, accuracy on eval sets).
  - Qualitative evals (prompt-response review, safety behavior, hallucinations).
- **Identify risks and constraints:**
  - Data residency and compliance (e.g., PII handling, regional endpoints).
  - Safety and guardrails (prompt injection, toxic content, data exfiltration).
  - Operational limits (rate limits, context window, max output tokens).
- **Make a data-driven selection:**
  - Map model strengths to user journeys and SLAs.
  - Justify tradeoffs (e.g., Haiku vs. Sonnet; Nova Micro vs. Nova Pro).

### Flash-card style prompts
- **Q:** What are three axes you’d use to compare FMs for a use case?  
  **A:** Quality (task performance), latency/throughput, and cost, plus safety/compliance if relevant.
- **Q:** Why do we run both automatic evals and manual reviews?  
  **A:** Automatic evals scale and detect regressions; manual reviews catch nuanced behaviors and UX issues.

---

## Section 2: Model Selection and Routing Strategies 🔀

**Goal:** Build **flexible, resilient AI integrations** that can switch models and providers without rewriting applications.

### Key ideas
- **Abstraction layer over providers:**
  - Wrap Bedrock (and others) behind a common interface (e.g., `invoke_model(request)`).
  - Keep provider-specific details in config, not scattered across business logic.
- **Dynamic routing and configuration:**
  - Use **AWS AppConfig** or Parameter Store to select:
    - Primary model ID per use case.
    - Fallback model(s) and routing weights.
    - Safety settings and guardrails per environment (dev/test/prod).
- **Serverless integration:**
  - **API Gateway** → **Lambda** → **Bedrock** pattern.
  - Keep Lambdas stateless; pass correlation IDs and metadata for observability.
  - Use **Lambda timeouts** and **retries** tuned to model latency.
- **Failover strategies:**
  - Fallback to cheaper/less capable model on errors or quota issues.
  - Use **feature flags** to roll out routing changes safely.

### Flash-card style prompts
- **Q:** Why use an abstraction layer for model calls?  
  **A:** To change models/providers without touching business logic, and to centralize routing, logging, and safety controls.
- **Q:** Name two AWS services commonly used for model routing config.  
  **A:** AWS AppConfig and AWS Systems Manager Parameter Store.

---

## Section 3: Resilient AI System Design 🛡️

**Goal:** Design AI systems that keep working even when parts of the system—or a region—fail.

### Core patterns
- **Cross-region Bedrock usage:**
  - Prefer regional endpoints close to users; design for **multi-region failover** if a region is impacted.
  - Consider using **Route 53** and **API Gateway regional endpoints** for traffic routing.
- **Graceful degradation:**
  - If the primary model or region is down:
    - Fall back to cheaper or simpler models.
    - Switch from generative explanations to cached templates or rules.
    - Return partial results instead of failing hard.
- **Fault tolerance and circuit breakers:**
  - Implement **circuit breaker** around model calls:
    - Open circuit after repeated failures; route to fallback or cached responses.
    - Use CloudWatch metrics + alarms to detect failure patterns.
- **Tiered fallback strategies:**
  - Tier 1: Primary model in primary region.
  - Tier 2: Alternate model or region with similar capabilities.
  - Tier 3: Static or heuristic responses to keep UX viable.

### Flash-card style prompts
- **Q:** What does “graceful degradation” mean for an AI feature?  
  **A:** When the AI path fails, the app still delivers a simplified or cached experience instead of an error.
- **Q:** What AWS patterns support multi-region resilience for AI APIs?  
  **A:** Route 53 health checks, API Gateway in multiple regions, Lambda + Bedrock in each region, and state/config replicated across regions.

---

## How this repo maps to the sections
- **Section 1 – FM Assessment & Selection**
  - Exercises and notes comparing models (e.g., Nova vs. Claude) and their fit for tasks like video, text gen, and extraction.
- **Section 2 – Model Selection & Routing**
  - Bedrock invocation exercise with multiple actions and IAM least privilege.
  - Patterns for sync, streaming, async, and batch, which feed into routing decisions.
- **Section 3 – Resilient AI Design**
  - IAM, S3 policies, async and batch flows, and notes in `docs/README.md` on error handling and tradeoffs (sync vs async vs batch).


