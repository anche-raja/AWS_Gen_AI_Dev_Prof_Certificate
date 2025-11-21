## Static vs Dynamic Model Routing in AI Systems – When to Use Which? 🤖⚙️

### Visual overview

**Static routing:**  
![Static model routing](./images/D1_L3_static_model_routing.png)

**Dynamic routing:**  
![Dynamic model routing](./images/D1_L4_dynamic_model_routing.jpg)

> Tip for LinkedIn: upload these two PNGs as images in your post and reference them near the relevant sections below.

---

### What is Static Model Routing?

Static model routing means you decide *up front* which model handles which request type, based on simple, predefined rules.

Typical pattern:

- A mapping such as `faq → Haiku`, `tech_support → Sonnet`, `creative → Opus`, `analytics → Titan`.
- The router inspects a **task label** (not the raw content) and calls the appropriate model.

**Characteristics**
- Decision at design/config time.
- Same model for the same category every time.
- No per-request intelligence beyond those rules.

**Advantages**
- Simple and easy to reason about.
- Highly predictable behavior → great for testing and compliance.
- Works very well when use cases are stable and clearly separated.

**Disadvantages**
- Limited flexibility – changing routing usually needs code/config changes.
- Can’t adapt to nuance inside a category.
- Needs manual retuning as new models, costs, and requirements appear.

**Best used when…**
- You have **well-defined workloads** (e.g., “FAQ bot” vs “Deep tech assistant”).  
- You want **deterministic behavior** and minimal operational overhead.

---

### What is Dynamic Model Routing?

Dynamic model routing chooses the model *at runtime* for each request, based on things like:

- Input characteristics (length, complexity, modality, risk)
- Live performance metrics (latency, error rate, SLOs)
- Cost constraints or user tier

On AWS, this pattern is embodied by **Amazon Bedrock Intelligent Prompt Routing**.

![Intelligent prompt routing](./images/D1_L4_intelligent_prompt_routing.png)

**Characteristics**
- Runtime, per-request decision-making.
- Input‑ and context‑aware selection.
- Can incorporate cost and performance signals in real time.

**Advantages**
- Flexibility: adapts as traffic patterns and model behavior change.
- Cost–performance balance: simple prompts → cheaper models; complex/high-value prompts → stronger models.
- Multi-model utilization: one app can exploit strengths of several models instead of one-size-fits-all.

**Disadvantages**
- More moving parts: routing logic, metrics, configuration (e.g., AppConfig), observability.
- Harder to predict exact behavior without good logging/dashboards.

**Best used when…**
- You serve **mixed or unpredictable workloads** through the same entry point.
- You care about **SLAs and budget** and want to continuously optimize both.
- You need **resilience** and automatic fallback between models/regions.

---

### Static vs Dynamic – How to Think About It

| Dimension          | Static Routing                           | Dynamic Routing                                         |
|--------------------|------------------------------------------|---------------------------------------------------------|
| Decision time      | Design/config time                       | Runtime, per request                                   |
| Inputs to decision | Route key / endpoint / task label        | Content, metrics, cost, user tier, config              |
| Complexity         | Low                                      | Medium–High                                            |
| Predictability     | Very high                                | Lower (requires strong observability)                  |
| Adaptability       | Low (manual updates)                     | High (reacts to data & performance)                    |
| Good for           | Stable, narrow workloads; compliance     | Mixed workloads; SLAs; cost optimization; resilience   |

**Practical pattern:**  
Start with **static routing** to get something reliable in production. As traffic and model choices grow, **layer dynamic routing** on top for:

- Cost optimization
- Latency control
- Resilience and failover

That way you keep the clarity of static mappings, while letting data and metrics drive fine-grained decisions behind the scenes.


