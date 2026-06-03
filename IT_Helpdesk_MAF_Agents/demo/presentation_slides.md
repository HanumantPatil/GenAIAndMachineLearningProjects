# IT Helpdesk Multi-Agent Assistant — 4 Slide Talk

**Author:** Hanumant Patil
**Capstone:** Microsoft Agent Framework + Azure AI Search + Azure Cosmos DB

---

## Slide 1 — Use Case & Problem Statement

### Title: Automating L1/L2 IT Helpdesk with Multi-Agent AI

**The Problem**
- Employees flood IT helpdesks with repetitive questions (VPN, password resets, software install, access requests).
- L1/L2 agents spend 60–70% of their time on issues already documented in internal KB articles.
- Manual ticket creation, tracking, and escalation cause delays and inconsistent SLAs.

**The Use Case**
- An AI-powered helpdesk assistant that:
  - Answers employee questions grounded in the internal knowledge base (RAG with citations).
  - Creates, updates, and tracks support tickets per user in Cosmos DB.
  - Detects low-confidence answers and intelligently escalates to a human agent.
  - Maintains conversation memory across sessions for context-aware support.

**Business Value**
- Deflects 40–60% of L1 tickets through self-service.
- Reduces mean time to resolution (MTTR) for common issues from hours to seconds.
- Frees human agents to focus on complex, high-impact incidents.

---

## Slide 2 — Solution Architecture & Tech Stack

### Title: Multi-Agent Orchestration on Microsoft Agent Framework

**Architecture (4 Specialized Agents)**

```
Employee → Orchestrator Agent (intent + routing + session memory)
              ├── KB Agent          → Azure AI Search (hybrid RAG)
              ├── Ticket Agent      → Azure Cosmos DB (per-user tickets)
              └── Escalation Agent  → Email / Teams notification
```

**Technology Stack**

| Layer | Technology |
|---|---|
| Agent Framework | Microsoft Agent Framework (Azure AI Agent Service SDK) |
| Language / API  | Python 3.12, FastAPI |
| Retrieval (RAG) | Azure AI Search (hybrid: semantic + keyword) |
| State / Memory  | Azure Cosmos DB (sessions, tickets, escalations) |
| Embeddings / LLM| Azure OpenAI |
| UI              | Streamlit + DevUI for local agent testing |
| Deployment      | Docker, docker-compose |

**Engineering Highlights**
- Clean Architecture (Domain → Application → Adapters → Infrastructure) — testable and replaceable layers.
- Pluggable agent adapters via ports/interfaces — Inner layers never depend on Azure SDKs.
- High unit test coverage (htmlcov reports) and DevUI for agent-by-agent debugging.

---

## Slide 3 — Live Demo Walkthrough

### Title: Demo — From Question to Ticket to Escalation

**Demo Flow (≈ 5 minutes)**

1. **Knowledge Base Query (RAG)**
   - User: *"How do I connect to corporate VPN from a personal Mac?"*
   - Orchestrator → KB Agent → grounded answer with citations + confidence score.

2. **Ticket Creation**
   - User: *"My Outlook keeps crashing on launch — please open a ticket."*
   - Orchestrator → Ticket Agent → ticket persisted in Cosmos DB, ID returned.

3. **Ticket Status Lookup**
   - User: *"What's the status of my last ticket?"*
   - Orchestrator → Ticket Agent → retrieves user history (partitioned by `userId`).

4. **Low-Confidence Escalation**
   - User asks an obscure / out-of-KB question.
   - KB Agent confidence < threshold → Escalation Agent → notification simulated.

5. **Multi-Intent + Session Memory**
   - Single message combining a KB question + ticket update.
   - Session context recalled across turns via Cosmos DB.

**What to Watch For**
- Source citations and confidence scores in KB responses.
- Cosmos DB record appearing live for ticket creation.
- Orchestrator routing decisions logged in DevUI.

---

## Slide 4 — Recording the Demo & Program Experience

### Title: Recording the Demo + My Capstone Journey

**How the Demo Was Recorded**
- **Tooling:** Windows Game Bar / OBS Studio for screen + audio capture (1080p, 30fps).
- **Setup:**
  1. Start FastAPI backend: `uvicorn src.infrastructure.web.main:app --reload`
  2. Launch Streamlit UI: `streamlit run ui/app.py`
  3. Open DevUI side-panel to show agent traces in real time.
  4. Pre-seed Cosmos DB and Azure AI Search index using the indexing pipeline.
- **Script:** Followed the 5-step flow on Slide 3; voice-over explains routing decisions.
- **Output:** MP4 stored under `ScreenShots/` (and linked in README §13).

**Program Experience — Key Takeaways**
- **Hands-on with Microsoft Agent Framework** — moved from "what is an agent?" to building a 4-agent orchestrated system end-to-end.
- **Clean Architecture in practice** — the dependency rule made swapping mocks for real Azure SDKs trivial during testing.
- **RAG done right** — learned hybrid search tuning, chunking strategies, and confidence-based escalation patterns.
- **Production thinking** — containerization, structured logging, test coverage, and DevUI debugging shifted my mindset from prototype to product.
- **Biggest lesson:** Agent design is 20% prompts, 80% boundaries — clear tool contracts and intent classification beat clever prompts every time.

**Thank you — Q&A**
