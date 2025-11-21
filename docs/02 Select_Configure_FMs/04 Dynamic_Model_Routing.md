## Dynamic Model Routing 🔄

![Dynamic model routing](./images/D1_L4_dynamic_model_routing.jpg)

Dynamic model routing = choosing the **best foundation model at runtime** based on:

- Input characteristics
- Current performance metrics
- Cost constraints
- Business / user requirements

**Key difference vs. static routing:**
- **Static:** Pre-defined rules → same model for the same category.
- **Dynamic:** Evaluates each request individually and **adapts in real time**.

**Key characteristics:**
- Runtime decision-making
- Adaptive selection criteria
- Real-time cost & performance optimization
- Input- and context-aware routing

---

## 2. Amazon Bedrock Intelligent Prompt Routing 🧠

![Intelligent prompt routing](./images/D1_L4_intelligent_prompt_routing.png)

Amazon Bedrock **Intelligent Prompt Routing**:

- Automatically picks the most appropriate FM per request.
- Evaluates input characteristics, such as:
  - Prompt length
  - Complexity
  - Content type
- Evaluates performance metrics, such as:
  - Response time (latency)
  - Accuracy / quality
  - Throughput / SLO requirements

Does **not** consider (from quizzes and docs):
- Client geographic location
- Database schema
- Network bandwidth, etc.

### Advantages over static routing
- **Flexibility & adaptability**
  - Adapts to new input patterns, model performance changes, and evolving business needs **without code changes**.
- **Cost & performance optimization**
  - Uses historical + real-time metrics to:
    - Send simple queries to cheaper models.
    - Use powerful models only when needed.
- **Multi-model utilization**
  - Leverages strengths of multiple models in one app instead of one-size-fits-all.

---

## 3. Use cases for dynamic routing 📌

### 3.1 Diverse input applications
- **Content management systems**
  - Text → text model
  - Images → vision model
  - Structured data → specialized model
- **Customer service**
  - Simple FAQ → small/cheap model
  - Complex technical issues → stronger model

### 3.2 Performance-sensitive systems
- Systems with strict SLAs:
  - Time-critical queries → fast, high-performance models
  - Routine jobs → cost-effective models
- Real-time recommendations adjusting based on current load and latency.

### 3.3 Multi-modal applications
- One app using multiple specialized models:
  - Text extraction
  - Sentiment analysis
  - Summarization
- Routing based on document characteristics and task requirements.

### 3.4 Cost-conscious implementations
- Different models by user tier:
  - Premium users → advanced, more expensive models
  - Free/standard users → basic, cheaper models
- Adjust routing when approaching budget thresholds.

---

## 4. Implementation approaches 🧩

### 4.1 Content-based routing with AWS Step Functions
Use Step Functions state machines with **choice states**:

1. `AnalyzeContent` (Lambda) → compute complexity / type.
2. `RouteBasedOnComplexity` → choice:
   - High → Claude 3 Opus
   - Medium → Claude 3 Sonnet
   - Default/low → Titan Express

This ensures powerful models are used only when needed.

### 4.2 API Gateway + Lambda routing logic
- **API Gateway:**
  - Unified entry point; passes headers/body to Lambda.
- **Lambda router example:**
  - Checks `X-User-Tier` header and content length.
  - Chooses Opus / Sonnet / Haiku accordingly.
  - Invokes selected Bedrock model and returns `X-Selected-Model` in response.

This balances performance vs cost using request properties.

### 4.3 Performance-based fallback mechanisms
**Primary purpose (exam hook):**
> Maintain service availability and quality when primary models experience performance degradation.

How it works:
- Monitor model health via CloudWatch metrics (e.g., `InvocationLatency`, errors).
- Logic:
  - Prefer primary models if latency < threshold.
  - If both are slow or failing → fallback model (e.g., Haiku).
- On errors:
  - Retry with fallback model.

Ensures:
- Consistent user experience.
- Automatic handling during outages, spikes, or regressions.

---

## 5. Cost-optimized routing strategies 💰

Four key strategies:

1. **Query complexity analysis**
   - Simple queries → cheaper models.
   - Complex analytical tasks → premium models.
2. **Tiered routing based on business priorities**
   - Premium vs standard users mapped to different model tiers.
3. **Budget-aware model selection**
   - Monitor usage costs in real time.
   - When nearing daily/monthly limits → shift to cheaper models automatically.
4. **Performance–cost balance optimization**
   - Use historical data to find the “sweet spot” model per query type.
   - Continuously refine routing rules for maximum value per dollar.

---

## 6. Best practices & considerations ✅

### Monitoring & observability
- Use CloudWatch to track:
  - Latency
  - Error rates
  - Throughput
  - Routing patterns (which models are used, how often)
- Build dashboards to spot optimization opportunities.

### Fallback & error handling
- Implement:
  - Circuit breakers – stop using a bad/slow model temporarily.
  - Fallback models – cheaper or more reliable backups.
  - Graceful degradation – provide a simpler but still useful response.

### Testing & validation
- Test routing logic under:
  - Different loads
  - Different input types
  - Failure scenarios
- Use:
  - A/B testing to compare routing strategies.
  - Canary deployments for safe routing changes.

### Security & compliance
- Ensure consistent auth, encryption, and data handling across all model endpoints.
- Apply security and compliance policies regardless of which model handles the request.


