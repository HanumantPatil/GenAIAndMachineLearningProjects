# IT Helpdesk Multi-Agent Assistant

**Author:** Hanumant Patil — [hapatil@microsoft.com](mailto:hapatil@microsoft.com)

**Capstone Project — Microsoft Agent Framework + Azure AI Search + Azure Cosmos DB**

A production-grade IT helpdesk chatbot that resolves employee technical support queries by retrieving answers from an internal knowledge base, tracking ticket history per user, and routing complex issues to specialized sub-agents — deployed as a FastAPI web endpoint using the Microsoft Agent Framework (Azure AI Agent Service SDK).

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture](#2-architecture)
3. [Clean Architecture Design](#3-clean-architecture-design)
4. [Technology Stack](#4-technology-stack)
5. [Directory Structure](#5-directory-structure)
6. [Implementation Plan](#6-implementation-plan)
   - [Phase 1 — Environment & Azure Resource Setup](#phase-1--environment--azure-resource-setup)
   - [Phase 2 — Domain Layer](#phase-2--domain-layer)
   - [Phase 3 — Application Layer (Use Cases)](#phase-3--application-layer-use-cases)
   - [Phase 4 — Adapters Layer](#phase-4--adapters-layer)
   - [Phase 5 — Infrastructure Layer](#phase-5--infrastructure-layer)
   - [Phase 6 — Knowledge Base Indexing Pipeline](#phase-6--knowledge-base-indexing-pipeline)
   - [Phase 7 — Testing](#phase-7--testing)
   - [Phase 8 — Containerization & Deployment](#phase-8--containerization--deployment)
   - [Phase 9 — Demo & Validation](#phase-9--demo--validation)
7. [Sample Queries & Expected Outputs](#7-sample-queries--expected-outputs)
8. [Key Differentiators](#8-key-differentiators)
9. [Deliverables Checklist](#9-deliverables-checklist)
10. [Setup & Running Locally](#10-setup--running-locally)
11. [Streamlit UI](#11-streamlit-ui)

---

## 1. Project Overview

| Field | Details |
|---|---|
| **Project Title** | IT Helpdesk Multi-Agent Assistant |
| **Framework** | Microsoft Agent Framework (Azure AI Agent Service SDK) |
| **Language** | Python 3.12+ |
| **Web API** | FastAPI |
| **Pattern** | Multi-agent orchestration with RAG, ticket management, and escalation |

### Problem Statement

Employees submit IT support requests through various channels. The goal is to automate L1/L2 support by:
- Answering questions from internal knowledge base documents (RAG)
- Creating and tracking support tickets in a NoSQL store
- Intelligently escalating unresolved issues to human agents
- Supporting multi-intent queries, version comparison, RBAC filtering, and multi-language responses

---

## 2. Architecture

```
Employee (Web Chat / API Client)
              │
              ▼
┌─────────────────────────────────┐
│     Orchestrator Agent (MAF)    │
│  - Intent classification        │
│  - Conversation routing         │
│  - Session memory (Cosmos DB)   │
└──────┬──────────┬───────────────┘
       │          │              │
       ▼          ▼              ▼
┌──────────┐ ┌──────────┐ ┌──────────────┐
│ KB Agent │ │  Ticket  │ │  Escalation  │
│  (RAG)   │ │  Agent   │ │    Agent     │
└────┬─────┘ └────┬─────┘ └──────┬───────┘
     │            │              │
     ▼            ▼              ▼
Azure AI       Azure Cosmos    Email / Teams
Search         DB (NoSQL)      Notification
(Hybrid)       (Chat + Ticket  (Simulated)
               History)
```

### Agent Responsibilities

| Agent | Responsibility |
|---|---|
| **Orchestrator** | Classifies user intent, routes to correct sub-agent, maintains session context via Cosmos DB |
| **KB Agent** | Performs hybrid RAG (semantic + keyword) over IT documents; returns grounded answers with source citations and confidence scores |
| **Ticket Agent** | Creates, updates, and retrieves support tickets in Cosmos DB partitioned by `userId` |
| **Escalation Agent** | Triggers when KB confidence is below threshold or user requests human help; composes escalation summary and simulates IT admin notification |

---

## 3. Clean Architecture Design

This project follows **Clean Architecture** (Robert C. Martin). The core principle is the **Dependency Rule**: source code dependencies always point inward — outer layers know about inner layers, but inner layers never know about outer layers.

### Layer Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│  Layer 4 — Infrastructure  (FastAPI, Azure SDKs, Docker, MAF)   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Layer 3 — Adapters  (Repository impls, Azure wrappers,   │  │
│  │                        Agent adapters, Tool adapters)      │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  Layer 2 — Application  (Use Cases, Intent          │  │  │
│  │  │                          Classifier, DTOs)           │  │  │
│  │  │  ┌───────────────────────────────────────────────┐  │  │  │
│  │  │  │  Layer 1 — Domain  (Entities, Value Objects,  │  │  │  │
│  │  │  │                     Ports / Interfaces)        │  │  │  │
│  │  │  └───────────────────────────────────────────────┘  │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
         Dependencies point INWARD ──►  (outer depends on inner)
```

### Layer Responsibilities

| Layer | Package | Contents | Depends On |
|---|---|---|---|
| **Domain** | `src/domain/` | Entities (`Ticket`, `Session`, `KBChunk`), Value Objects (`Intent`, `UserRole`, `TicketStatus`), Port interfaces (`ITicketRepository`, `IKBSearchService`, `INotificationService`, `ILLMService`) | Nothing external |
| **Application** | `src/application/` | Use Cases (`ProcessChatUseCase`, `AnswerKBQueryUseCase`, `ManageTicketUseCase`, `EscalateIssueUseCase`), Intent Classifier, DTOs, Response Merger | Domain only |
| **Adapters** | `src/adapters/` | Cosmos DB repository implementations, Azure AI Search service, Azure OpenAI service, Notification service, MAF agent adapters | Domain + Application |
| **Infrastructure** | `src/infrastructure/` | FastAPI app, DI wiring, configuration (`Settings`), indexing pipeline | All layers |

### Key Principles Applied

- **Dependency Inversion** — Use cases depend on `ITicketRepository` (port), not `CosmosTicketRepository` (adapter). The DI container wires them at startup.
- **Framework Independence** — `domain/` and `application/` contain zero imports from `fastapi`, `azure-cosmos`, or `azure-ai-projects`. They can run without Azure credentials.
- **Testability** — Unit tests for inner layers use simple in-memory fakes, not Azure mocks. Only adapter tests need Azure SDK mocks.
- **Database Independence** — Swap Cosmos DB for PostgreSQL by writing a new `ITicketRepository` adapter — use cases are untouched.
- **Agent as Adapter** — MAF agents live in `adapters/agents/`. They translate between the agent framework's protocol and the `Application` use case interfaces.

---

## 4. Technology Stack

| Component | Technology |
|---|---|
| Agent framework | Microsoft Agent Framework (Azure AI Agent Service SDK) |
| Language | Python 3.12+ |
| Web API | FastAPI |
| Document indexing | Azure AI Search (hybrid: semantic + keyword) |
| Chat & ticket store | Azure Cosmos DB for NoSQL |
| LLM | Azure OpenAI GPT-4o (via Azure AI Foundry) |
| Embedding model | Azure OpenAI `text-embedding-3-large` |
| Interactive UI | Streamlit (`ui/streamlit_app.py`) |
| Deployment | Azure Container Apps or local Docker |

---

## 5. Directory Structure

The project source is organised into four Clean Architecture layers under `src/`, with supporting folders for data, tests, and deployment at the root.

```
AppsandData_IT_Helpdesk/
├── README.md
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
│
├── data/
│   ├── raw/                                   # Original PDFs and Word knowledge base docs
│   │   ├── 01-laptop-setup-guide.docx
│   │   ├── 02-vpn-configuration-manual-2025-v1.pdf
│   │   ├── 03-vpn-configuration-manual-2026-v1.docx
│   │   ├── 04-software-installation-procedures.pdf
│   │   ├── 05-network-troubleshooting-runbook.docx
│   │   ├── 06-office365-admin-faq.pdf
│   │   ├── 07-password-reset-mfa-guide.docx
│   │   ├── 08-printer-setup-instructions.pdf
│   │   └── 09-approved-software-catalog.docx
│   └── processed/                             # Chunked JSON (output of indexing pipeline)
│
├── src/
│   │
│   ├── domain/                                # LAYER 1 — Domain (no external imports)
│   │   ├── entities/
│   │   │   ├── ticket.py                      # Ticket entity (id, userId, title, status, ...)
│   │   │   ├── session.py                     # Session entity (sessionId, messages, ttl)
│   │   │   ├── message.py                     # Message value object (role, content, timestamp)
│   │   │   ├── kb_chunk.py                    # KBChunk entity (content, source, version, score)
│   │   │   └── escalation_case.py             # EscalationCase entity (caseId, summary, ...)
│   │   ├── value_objects/
│   │   │   ├── ticket_status.py               # Enum: open, in_progress, resolved, closed
│   │   │   ├── user_role.py                   # Enum: employee, it_admin
│   │   │   ├── intent.py                      # Enum: kb_lookup, ticket_create, escalation, ...
│   │   │   └── confidence_score.py            # Float wrapper with threshold logic (< 0.6 → escalate)
│   │   └── ports/                             # Abstract interfaces (dependency inversion)
│   │       ├── ticket_repository_port.py      # ITicketRepository (create/get/update/list)
│   │       ├── session_repository_port.py     # ISessionRepository (get_or_create/append/history)
│   │       ├── escalation_repository_port.py  # IEscalationRepository (create/get)
│   │       ├── kb_search_port.py              # IKBSearchService (search(query, role, top_k, doc_versions?))
│   │       ├── llm_port.py                    # ILLMService (complete(messages) → str)
│   │       └── notification_port.py           # INotificationService (notify(userId, summary))
│   │
│   ├── application/                           # LAYER 2 — Application (use cases; depends on domain only)
│   │   ├── use_cases/
│   │   │   ├── process_chat_use_case.py       # Orchestrate intent → route to KB/Ticket/Escalate
│   │   │   ├── answer_kb_query_use_case.py    # RAG: search → generate grounded answer
│   │   │   ├── manage_ticket_use_case.py      # Create / read / update tickets
│   │   │   └── escalate_issue_use_case.py     # Compose summary → trigger notification
│   │   ├── services/
│   │   │   ├── intent_classifier.py           # Classify intent label from user message via LLM port
│   │   │   └── response_merger.py             # Merge parallel KB + Ticket responses (multi-intent)
│   │   └── dto/
│   │       ├── chat_request_dto.py            # Input DTO: sessionId, userId, userRole, message
│   │       ├── chat_response_dto.py           # Output DTO: response, sources, ticketId, caseRef
│   │       └── ticket_dto.py                  # Ticket data transfer object
│   │
│   ├── adapters/                              # LAYER 3 — Adapters (implements domain ports)
│   │   ├── repositories/
│   │   │   ├── cosmos_ticket_repository.py    # ITicketRepository → Azure Cosmos DB
│   │   │   ├── cosmos_session_repository.py   # ISessionRepository → Azure Cosmos DB
│   │   │   └── cosmos_escalation_repository.py # IEscalationRepository → Azure Cosmos DB
│   │   ├── services/
│   │   │   ├── azure_search_service.py        # IKBSearchService → Azure AI Search (hybrid)
│   │   │   ├── azure_openai_service.py        # ILLMService → Azure OpenAI GPT-4o
│   │   │   └── email_notification_service.py  # INotificationService → simulated email/Teams
│   │   └── agents/                            # MAF agent adapters (translate MAF ↔ use cases)
│   │       ├── orchestrator_agent_adapter.py  # Calls ProcessChatUseCase
│   │       ├── kb_agent_adapter.py            # Calls AnswerKBQueryUseCase
│   │       ├── ticket_agent_adapter.py        # Calls ManageTicketUseCase
│   │       ├── escalation_agent_adapter.py    # Calls EscalateIssueUseCase
│   │       └── prompts/
│   │           ├── orchestrator_prompt.md     # System prompt: intent classification + routing rules
│   │           ├── kb_agent_prompt.md         # System prompt: RAG, confidence, multilang, versioning
│   │           ├── ticket_agent_prompt.md     # System prompt: ticket CRUD + confirmation flow
│   │           └── escalation_agent_prompt.md # System prompt: summary composition + handoff
│   │
│   └── infrastructure/                        # LAYER 4 — Infrastructure (frameworks & drivers)
│       ├── api/
│       │   ├── main.py                        # FastAPI application entry point
│       │   ├── dependencies.py                # DI container: wire ports → adapter implementations
│       │   ├── routers/
│       │   │   └── chat.py                    # POST /chat, GET /sessions, GET /tickets, GET /health
│       │   └── models/
│       │       └── schemas.py                 # Pydantic request/response schemas
│       ├── config/
│       │   └── settings.py                    # Pydantic BaseSettings: load .env variables
│       └── indexing/                          # One-time KB indexing pipeline (infra concern)
│           ├── chunker.py                     # PDF/Markdown → overlapping text chunks
│           ├── embedder.py                    # Chunks → text-embedding-3-large vectors
│           ├── index_schema.py                # Azure AI Search index schema definition
│           └── run_indexing_pipeline.py       # Entry point: load → chunk → embed → upload
│
├── demo/
│   └── run_demo.py                            # Interactive CLI demo (type queries, see responses live)
│
├── ui/
│   └── streamlit_app.py                       # Streamlit web UI — chat, tickets, escalations, sources
│
└── tests/
    ├── conftest.py                            # Shared fixtures: in-memory port fakes, sample DTOs
    ├── domain/                                # Pure unit tests — no mocks, no Azure needed
    │   ├── test_entities.py                   # Ticket, Session, KBChunk construction + validation
    │   └── test_value_objects.py              # TicketStatus, Intent, ConfidenceScore logic
    ├── application/                           # Use-case tests with in-memory port fakes
    │   ├── test_process_chat_use_case.py
    │   ├── test_answer_kb_query_use_case.py
    │   ├── test_manage_ticket_use_case.py
    │   └── test_escalate_issue_use_case.py
    ├── adapters/                              # Adapter tests with mocked Azure SDK clients
    │   ├── test_cosmos_ticket_repository.py
    │   ├── test_cosmos_session_repository.py
    │   ├── test_azure_search_service.py
    │   └── test_agent_adapters.py
    └── infrastructure/                        # Integration + API tests
        ├── test_api.py                        # FastAPI endpoint tests (httpx TestClient)
        └── test_orchestration_e2e.py          # End-to-end all 10 sample queries
```

---

## 6. Implementation Plan

> **Development order follows the Dependency Rule: build inner layers first, outer layers last.**
> Each phase only imports from layers already built in a previous phase.

### Phase 1 — Environment & Azure Resource Setup

**Goal:** Provision all Azure resources and configure local development environment.

#### Step 1.1 — Create Python Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

**Key dependencies (`requirements.txt`):**
```
# Agent framework — Azure AI Agent Service SDK
azure-ai-projects>=1.0.0

# Azure service SDKs (Layer 4 — outer)
azure-search-documents>=11.4.0
azure-cosmos>=4.6.0
azure-identity>=1.15.0
openai>=1.30.0

# Web API
fastapi>=0.111.0
uvicorn>=0.29.0
python-multipart>=0.0.9

# Document processing (indexing pipeline)
pypdf>=4.2.0

# Configuration
pydantic-settings>=2.2.0
python-dotenv>=1.0.0

# Streamlit UI
streamlit>=1.35.0

# Testing
pytest>=8.2.0
pytest-asyncio>=0.23.0
httpx>=0.27.0
```

#### Step 1.2 — Provision Azure Resources

Provision the following resources via Azure Portal, Azure CLI, or Bicep:

| Resource | Purpose | Notes |
|---|---|---|
| Azure AI Foundry project | Host GPT-4o and embedding model | Create in East US or Sweden Central |
| Azure OpenAI GPT-4o deployment | LLM for all agents | Deployment name: `gpt-4o` |
| Azure OpenAI text-embedding-3-large | Embeddings for RAG | Deployment name: `text-embedding-3-large` |
| Azure AI Search (Standard S1) | Hybrid knowledge base index | Enable semantic ranking |
| Azure Cosmos DB for NoSQL | Tickets + session store | Create DB: `HelpDeskDB` |
| Azure Container Registry (optional) | Docker image registry | For Azure Container Apps deployment |
| Azure Container Apps (optional) | Host FastAPI app | Serverless container hosting |

#### Step 1.3 — Configure Environment Variables

All configuration is loaded through `src/infrastructure/config/settings.py` (Pydantic `BaseSettings`). This is the **only** place in the codebase that reads from `.env`. Inner layers receive config values via dependency injection — they never call `os.getenv` directly.

Create `.env` from `.env.example`:

```ini
# Azure AI Foundry / Agent Service
AZURE_AI_PROJECT_CONN_STRING=<your-connection-string>
AZURE_OPENAI_ENDPOINT=https://<your-openai>.openai.azure.com/
AZURE_OPENAI_API_KEY=<your-key>
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4o
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large

# Azure AI Search
AZURE_SEARCH_ENDPOINT=https://<your-search>.search.windows.net
AZURE_SEARCH_API_KEY=<your-key>
AZURE_SEARCH_INDEX_NAME=it-helpdesk-kb

# Azure Cosmos DB
COSMOS_ENDPOINT=https://<your-cosmos>.documents.azure.com:443/
COSMOS_KEY=<your-key>
COSMOS_DATABASE=HelpDeskDB
COSMOS_TICKET_CONTAINER=Tickets
COSMOS_SESSION_CONTAINER=Sessions

# Escalation (simulated)
ESCALATION_EMAIL=it-support@company.com
```

---

### Phase 2 — Domain Layer

**Goal:** Build the innermost layer — pure Python, zero external dependencies, independently testable.

This layer defines **what** the system does without specifying **how** it does it.

#### Step 2.1 — Entities (`src/domain/entities/`)

Create plain Python dataclasses or Pydantic models for each business entity:

| Entity | Key Fields | Notes |
|---|---|---|
| `Ticket` | `id`, `userId`, `title`, `description`, `status: TicketStatus`, `created_at`, `updated_at`, `resolution_notes` | Core support ticket |
| `Session` | `sessionId`, `userId`, `messages: list[Message]`, `created_at`, `ttl` | Conversation history |
| `Message` | `role` (`user`/`assistant`), `content`, `timestamp` | Single chat turn |
| `KBChunk` | `chunk_id`, `content`, `source_file`, `doc_version`, `page_number`, `access_role`, `score` | Retrieved knowledge chunk |
| `EscalationCase` | `case_id`, `userId`, `summary`, `created_at`, `notified` | Escalation record |

#### Step 2.2 — Value Objects (`src/domain/value_objects/`)

| Value Object | Type | Values / Logic |
|---|---|---|
| `TicketStatus` | Enum | `open`, `in_progress`, `resolved`, `closed` |
| `UserRole` | Enum | `employee`, `it_admin` |
| `Intent` | Enum | `kb_lookup`, `ticket_create`, `ticket_status`, `ticket_update`, `escalation`, `multi_intent` |
| `ConfidenceScore` | Float wrapper | `is_low_confidence() → score < 0.6` |

#### Step 2.3 — Ports / Interfaces (`src/domain/ports/`)

Define abstract base classes that the application layer depends on:

```python
# src/domain/ports/ticket_repository_port.py
from abc import ABC, abstractmethod
from src.domain.entities.ticket import Ticket

class ITicketRepository(ABC):
    @abstractmethod
    def create(self, ticket: Ticket) -> Ticket: ...
    @abstractmethod
    def get_by_id(self, ticket_id: str, user_id: str) -> Ticket | None: ...
    @abstractmethod
    def get_latest(self, user_id: str) -> Ticket | None: ...
    @abstractmethod
    def update(self, ticket: Ticket) -> Ticket: ...
    @abstractmethod
    def list_by_user(self, user_id: str) -> list[Ticket]: ...
```

```python
# src/domain/ports/kb_search_port.py
from abc import ABC, abstractmethod
from src.domain.entities.kb_chunk import KBChunk
from src.domain.value_objects.user_role import UserRole

class IKBSearchService(ABC):
    @abstractmethod
    def search(
        self,
        query: str,
        user_role: UserRole,
        top_k: int = 5,
        doc_versions: list[str] | None = None,  # e.g. ["v1_2025", "v1_2026"] for Query 5
    ) -> list[KBChunk]: ...
```

```python
# src/domain/ports/escalation_repository_port.py
from abc import ABC, abstractmethod
from src.domain.entities.escalation_case import EscalationCase

class IEscalationRepository(ABC):
    """Persists escalation cases to Azure Cosmos DB (EscalationCases container)."""
    @abstractmethod
    def create(self, case: EscalationCase) -> EscalationCase: ...
    @abstractmethod
    def get_by_id(self, case_id: str) -> EscalationCase | None: ...
```

Same port pattern for `ISessionRepository`, `ILLMService`, `INotificationService`.

---

### Phase 3 — Application Layer (Use Cases)

**Goal:** Implement the application's business workflows. Depends on domain ports only — no Azure SDK, no FastAPI.

#### Step 3.1 — DTOs (`src/application/dto/`)

```python
# src/application/dto/chat_request_dto.py
from dataclasses import dataclass
from src.domain.value_objects.user_role import UserRole

@dataclass
class ChatRequestDTO:
    session_id: str
    user_id: str
    user_role: UserRole
    message: str
```

```python
# src/application/dto/chat_response_dto.py
@dataclass
class ChatResponseDTO:
    session_id: str
    response: str
    sources: list[dict]
    ticket_id: str | None = None
    escalation_case: str | None = None
    confidence_score: float | None = None
```

```python
# src/application/dto/ticket_dto.py
from dataclasses import dataclass
from src.domain.value_objects.ticket_status import TicketStatus

@dataclass
class TicketDTO:
    ticket_id: str
    user_id: str
    title: str
    description: str
    status: TicketStatus
    created_at: str
    updated_at: str
    resolution_notes: str | None = None
```

#### Step 3.2 — Intent Classifier (`src/application/services/intent_classifier.py`)

- Accepts a user message and conversation history
- Calls `ILLMService.complete()` with the orchestrator system prompt
- Parses the LLM output into an `Intent` enum value
- Returns `Intent` + detected sub-intents for `multi_intent` cases

#### Step 3.3 — Use Cases (`src/application/use_cases/`)

**`AnswerKBQueryUseCase`**
```
Input:  query (str), user_role (UserRole)
Steps:  1. call IKBSearchService.search(query, user_role, top_k=5)
        2. build grounded prompt from KBChunk list
        3. call ILLMService.complete(prompt)
        4. compute ConfidenceScore from chunk scores
Output: ChatResponseDTO (answer, sources, confidence_score)
```

> **Note:** The RAG system prompt (`_RAG_SYSTEM_PROMPT`) instructs the LLM to **always respond in English**, regardless of the language of the source documents. This prevents the model from mirroring Spanish KB chunks when the user asks in English. For multilingual support, detect the user's language explicitly and pass it as part of the prompt.

**`ManageTicketUseCase`**
```
Input:  intent (ticket_create | ticket_status | ticket_update), userId, message fields
Steps:  1. extract structured fields (title, description, ticket_id) from message
        2. call ITicketRepository.create / get_by_id / update
Output: ChatResponseDTO (confirmation + ticket_id)
```

**`EscalateIssueUseCase`**
```
Input:  userId, session history, last confidence score
Steps:  1. compose structured escalation summary via ILLMService
        2. call INotificationService.notify(userId, summary) → returns case_id
        3. persist EscalationCase via IEscalationRepository.create()
           (stored in Cosmos DB container: EscalationCases, partition key /userId)
Output: ChatResponseDTO (escalation_case reference = case_id)
```

**`ProcessChatUseCase`** ← main orchestrator use case
```
Input:  ChatRequestDTO
Steps:  1. load session history via ISessionRepository
        2. call IntentClassifier → Intent
        3. if kb_lookup   → AnswerKBQueryUseCase
           if ticket_*   → ManageTicketUseCase
           if escalation → EscalateIssueUseCase
           if multi_intent →
               # Parallel execution with asyncio.gather (Key Differentiator)
               kb_result, ticket_result = await asyncio.gather(
                   AnswerKBQueryUseCase.execute(kb_query, user_role),
                   ManageTicketUseCase.execute(ticket_intent, user_id, message),
               )
               merged = ResponseMerger.merge([kb_result, ticket_result])
        4. if KB confidence < 0.6 → also await EscalateIssueUseCase.execute(...)
        5. append turn to session via ISessionRepository.append_message()
        6. return merged ChatResponseDTO
```

#### Step 3.4 — Response Merger (`src/application/services/response_merger.py`)

- Takes a list of `ChatResponseDTO` from parallel use-case calls
- Merges `response` texts, concatenates `sources`, coalesces `ticket_id` and `escalation_case`

> **CA Rule:** All use-case constructors accept port interfaces as parameters. No concrete adapter classes are imported here.

---

### Phase 4 — Adapters Layer

**Goal:** Implement domain ports using concrete Azure services and wire MAF agents to use cases.

#### Step 4.1 — Repository Adapters (`src/adapters/repositories/`)

**`CosmosTicketRepository`** implements `ITicketRepository`
- Constructor accepts `CosmosClient` (injected from infrastructure)
- Maps between `Ticket` domain entity ↔ Cosmos DB JSON document
- Cosmos document schema (partition key `/userId`):
```json
{
  "id": "TKT-0042",
  "userId": "emp_123",
  "title": "Laptop not booting",
  "status": "open",
  "created_at": "2026-04-21T10:00:00Z",
  "updated_at": "2026-04-21T10:00:00Z",
  "resolution_notes": null
}
```

**`CosmosSessionRepository`** implements `ISessionRepository`
- Cosmos document schema (partition key `/sessionId`):
```json
{
  "id": "session_abc123",
  "sessionId": "session_abc123",
  "userId": "emp_123",
  "messages": [{"role": "user", "content": "..."}],
  "created_at": "2026-04-21T09:55:00Z",
  "ttl": 86400
}
```

#### Step 4.2 — Service Adapters (`src/adapters/services/`)

**`AzureSearchService`** implements `IKBSearchService`
- Calls `Azure AI Search` with hybrid (vector + BM25) retrieval
- Applies `$filter=access_role eq 'public' or access_role eq 'it_admin'` based on `UserRole`
- Maps search results to `list[KBChunk]`
- Search index fields:

| Field | Type | Notes |
|---|---|---|
| `id` | String (key) | Unique chunk ID |
| `content` | String | Chunk text — searchable |
| `content_vector` | Collection(Single) | 3072-dim embedding |
| `source_file` | String (filterable) | Document filename |
| `doc_version` | String (filterable) | e.g. `v1_2025`, `v1_2026` |
| `page_number` | Int32 | Page number |
| `access_role` | String (filterable) | `public` or `it_admin` |

Enable semantic configuration named `it-helpdesk-semantic` on the `content` field.

**`AzureOpenAIService`** implements `ILLMService`
- Wraps `openai.AzureOpenAI` client
- Calls `chat.completions.create` with the injected deployment name
- Returns response text; handles streaming via async generator

**`EmailNotificationService`** implements `INotificationService`
- Simulates sending an email/Teams notification to IT admin
- Generates a `case_id` (UUID) and logs the structured escalation summary
- Returns the `case_id` as escalation reference

#### Step 4.3 — MAF Agent Adapters (`src/adapters/agents/`)

MAF agents act as the **entry point** into the application layer. Each adapter:
1. Uses `AIProjectClient` (injected from infrastructure) to register an agent with its tools
2. Receives input from the MAF framework (tool call arguments)
3. Converts it to an appropriate DTO or domain call
4. Calls the corresponding use case
5. Converts the `ChatResponseDTO` back to MAF's expected output format

**MAF Tool Registration Pattern (Key Pro-Code Differentiator):**
```python
# src/adapters/agents/kb_agent_adapter.py
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FunctionTool, ToolSet
from src.application.use_cases.answer_kb_query_use_case import AnswerKBQueryUseCase

class KBAgentAdapter:
    def __init__(self, client: AIProjectClient, kb_use_case: AnswerKBQueryUseCase):
        self._client = client
        self._kb_use_case = kb_use_case

    def search_kb_tool(self, query: str, user_role: str, doc_versions: list[str] | None = None) -> str:
        """MAF tool: searches the IT knowledge base and returns a grounded answer."""
        result = self._kb_use_case.execute(query, UserRole(user_role), doc_versions)
        return result.response  # MAF receives plain text; sources attached as annotations

    def create_agent(self):
        """Register this adapter's tools with Azure AI Agent Service."""
        toolset = ToolSet()
        toolset.add(FunctionTool(self.search_kb_tool))
        return self._client.agents.create_agent(
            model="gpt-4o",
            name="kb-agent",
            instructions=open("src/adapters/agents/prompts/kb_agent_prompt.md").read(),
            toolset=toolset,
        )
```

Same pattern for `TicketAgentAdapter` (`manage_ticket_tool`), `EscalationAgentAdapter` (`notify_escalation_tool`).

**Agent ↔ Use Case mapping:**

| Agent Adapter | Use Case Called | MAF Tools Registered |
|---|---|---|
| `OrchestratorAgentAdapter` | `ProcessChatUseCase` | (routes internally to sub-agents) |
| `KBAgentAdapter` | `AnswerKBQueryUseCase` | `search_kb_tool` |
| `TicketAgentAdapter` | `ManageTicketUseCase` | `manage_ticket_tool` |
| `EscalationAgentAdapter` | `EscalateIssueUseCase` | `notify_escalation_tool` |

**System prompts** live in `src/adapters/agents/prompts/` (adapter-layer concern, not domain):
- `orchestrator_prompt.md` — Intent classification labels, routing rules, session context usage
- `kb_agent_prompt.md` — Grounding rules, confidence disclaimers, multilingual response, version diffing
- `ticket_agent_prompt.md` — Intent extraction, confirmation before creation, status formatting
- `escalation_agent_prompt.md` — Summary structure, professional tone, handoff language

> **CA Rule:** Agent adapters import from `src/application/` and `src/domain/`. They never import from `src/infrastructure/`.

---

### Phase 5 — Infrastructure Layer

**Goal:** Wire all layers together via FastAPI and dependency injection. This is the only layer that knows about all other layers.

#### Step 5.1 — Configuration (`src/infrastructure/config/settings.py`)

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Azure AI Foundry / Agent Service (azure-ai-projects SDK)
    azure_ai_project_conn_string: str          # required — MAF agent orchestration

    # Azure OpenAI
    azure_openai_endpoint: str
    azure_openai_api_key: str
    azure_openai_chat_deployment: str = "gpt-4o"
    azure_openai_embedding_deployment: str = "text-embedding-3-large"

    # Azure AI Search
    azure_search_endpoint: str
    azure_search_api_key: str
    azure_search_index_name: str = "it-helpdesk-kb"

    # Azure Cosmos DB
    cosmos_endpoint: str
    cosmos_key: str
    cosmos_database: str = "HelpDeskDB"
    cosmos_ticket_container: str = "Tickets"
    cosmos_session_container: str = "Sessions"
    cosmos_escalation_container: str = "EscalationCases"

    # Escalation notification (simulated)
    escalation_email: str = "it-support@company.com"

    class Config:
        env_file = ".env"
```

#### Step 5.2 — Dependency Injection (`src/infrastructure/api/dependencies.py`)

This file is the **composition root** — the only place that instantiates concrete adapters and wires them to ports:

```python
from functools import lru_cache
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from src.infrastructure.config.settings import Settings
from src.adapters.repositories.cosmos_ticket_repository import CosmosTicketRepository
from src.adapters.repositories.cosmos_session_repository import CosmosSessionRepository
from src.adapters.repositories.cosmos_escalation_repository import CosmosEscalationRepository
from src.adapters.services.azure_search_service import AzureSearchService
from src.adapters.services.azure_openai_service import AzureOpenAIService
from src.adapters.services.email_notification_service import EmailNotificationService
from src.application.use_cases.process_chat_use_case import ProcessChatUseCase

@lru_cache
def get_settings() -> Settings:
    return Settings()

@lru_cache
def get_ai_project_client() -> AIProjectClient:
    """
    Azure AI Agent Service client (azure-ai-projects SDK).
    Used by agent adapters to create and run MAF agents.
    Authenticates via connection string; uses DefaultAzureCredential in production.
    """
    s = get_settings()
    return AIProjectClient.from_connection_string(
        conn_str=s.azure_ai_project_conn_string,
        credential=DefaultAzureCredential(),
    )

def get_process_chat_use_case() -> ProcessChatUseCase:
    s = get_settings()
    return ProcessChatUseCase(
        ticket_repo=CosmosTicketRepository(s.cosmos_endpoint, s.cosmos_key, s.cosmos_database, s.cosmos_ticket_container),
        session_repo=CosmosSessionRepository(s.cosmos_endpoint, s.cosmos_key, s.cosmos_database, s.cosmos_session_container),
        escalation_repo=CosmosEscalationRepository(s.cosmos_endpoint, s.cosmos_key, s.cosmos_database, s.cosmos_escalation_container),
        kb_search=AzureSearchService(s.azure_search_endpoint, s.azure_search_api_key, s.azure_search_index_name),
        llm=AzureOpenAIService(s.azure_openai_endpoint, s.azure_openai_api_key, s.azure_openai_chat_deployment),
        notification=EmailNotificationService(s.escalation_email),
    )
```

#### Step 5.3 — Pydantic API Schemas (`src/infrastructure/api/models/schemas.py`)

```python
class ChatRequest(BaseModel):
    session_id: str
    user_id: str
    user_role: str = "employee"   # maps to UserRole enum in domain
    message: str

class ChatResponse(BaseModel):
    session_id: str
    response: str
    sources: list[dict] = []
    ticket_id: str | None = None
    escalation_case: str | None = None
    confidence_score: float | None = None
```

#### Step 5.4 — Chat Router (`src/infrastructure/api/routers/chat.py`)

**Endpoint: `POST /chat`**
- Accept `ChatRequest` → map to `ChatRequestDTO`
- Call injected `ProcessChatUseCase.execute(dto)`
- Map `ChatResponseDTO` → `ChatResponse`
- Support streaming via `StreamingResponse` (async generator from `ILLMService`)

**Endpoint: `GET /sessions/{session_id}/history`**
- Call `ISessionRepository.get_history(session_id)`

**Endpoint: `GET /tickets/{user_id}`**
- Call `ITicketRepository.list_by_user(user_id)`

**Endpoint: `GET /health`**
- Returns `{"status": "ok"}` — used as container readiness probe

#### Step 5.5 — FastAPI App (`src/infrastructure/api/main.py`)

- Configure CORS middleware
- Include routers with `/api/v1` prefix
- Add lifespan event to verify Azure connections on startup
- Add global exception handler returning structured error responses

---

### Phase 6 — Knowledge Base Indexing Pipeline

**Goal:** One-time pipeline to chunk, embed, and index all IT knowledge base documents in Azure AI Search.

> This lives in `src/infrastructure/indexing/` — it is an infrastructure concern and runs separately from the API server.

#### Step 6.1 — Prepare Raw Documents

Place the following documents in `data/raw/` (mix of `.docx` and `.pdf` supported):
- `01-laptop-setup-guide.docx`
- `02-vpn-configuration-manual-2025-v1.pdf`
- `03-vpn-configuration-manual-2026-v1.docx`
- `04-software-installation-procedures.pdf`
- `05-network-troubleshooting-runbook.docx`
- `06-office365-admin-faq.pdf`
- `07-password-reset-mfa-guide.docx`
- `08-printer-setup-instructions.pdf`
- `09-approved-software-catalog.docx`

**Metadata to capture per chunk:**
- `source_file` (filename)
- `doc_version` (e.g., `v1_2025`, `v1_2026`)
- `page_number`
- `chunk_id`
- `access_role` (`public` or `it_admin`) — for RBAC filtering (Query 7)

#### Step 6.2 — Define Azure AI Search Index Schema (`src/infrastructure/indexing/index_schema.py`)

Fields:
| Field | Type | Notes |
|---|---|---|
| `id` | String (key) | Unique chunk ID |
| `content` | String | Chunk text — searchable |
| `content_vector` | Collection(Single) | 3072-dim embedding vector |
| `source_file` | String (filterable) | Document filename |
| `doc_version` | String (filterable) | Version tag |
| `page_number` | Int32 | Page number |
| `access_role` | String (filterable) | `public` or `it_admin` |

Enable: **semantic configuration** named `it-helpdesk-semantic` pointing at the `content` field.

#### Step 6.3 — Implement Chunker (`src/infrastructure/indexing/chunker.py`)

- Uses `pdfplumber` for PDF text extraction; `python-docx` for `.docx` files
- Supports `.txt`, `.pdf`, `.docx`/`.doc` via unified `_extract_text()` helper in the pipeline
- Split by 500-token windows with 50-token overlap (preserves context across boundaries)
- Tag each chunk with metadata (filename, version, page, access_role)
- Returns `list[KBChunk]` — domain entities, not raw dicts

#### Step 6.4 — Implement Embedder (`src/infrastructure/indexing/embedder.py`)

- Call `Azure OpenAI text-embedding-3-large` via `openai` SDK
- Batch calls in groups of 16 to respect rate limits
- Returns each `KBChunk` annotated with its `content_vector`

#### Step 6.5 — Run Indexing Pipeline (`src/infrastructure/indexing/run_indexing_pipeline.py`)

```
load docs → chunk → embed → upload to Azure AI Search index
```

Run once to populate the index:

**Windows (PowerShell):**
```powershell
$env:PYTHONPATH = "."
python src/infrastructure/indexing/run_indexing_pipeline.py --data-dir data/raw --doc-version v1.0 --access-role public
```

**Linux/macOS:**
```bash
PYTHONPATH=. python src/infrastructure/indexing/run_indexing_pipeline.py --data-dir data/raw --doc-version v1.0 --access-role public
```

> **Note:** `PYTHONPATH=.` is required so that `src.*` module imports resolve correctly.

**Expected output:**
```
INFO Index 'it-helpdesk-kb' created/updated.
INFO Indexed 01-laptop-setup-guide.docx (2 chunks).
INFO Indexed 02-vpn-configuration-manual-2025-v1.pdf (2 chunks).
INFO Indexed 03-vpn-configuration-manual-2026-v1.docx (3 chunks).
INFO Indexed 04-software-installation-procedures.pdf (2 chunks).
INFO Indexed 05-network-troubleshooting-runbook.docx (2 chunks).
INFO Indexed 06-office365-admin-faq.pdf (3 chunks).
INFO Indexed 07-password-reset-mfa-guide.docx (2 chunks).
INFO Indexed 08-printer-setup-instructions.pdf (2 chunks).
INFO Indexed 09-approved-software-catalog.docx (1 chunks).
INFO Total chunks indexed: 19
INFO Indexing complete.
```

**Azure AI Search index `it-helpdesk-kb`** is now live with 19 chunks, hybrid (keyword + semantic vector via `text-embedding-3-large`) retrieval enabled.

---

### Phase 7 — Testing

**Goal:** Tests are organised to match the layer they test, with each inner layer requiring fewer/no mocks.

#### Step 7.1 — Domain Tests (`tests/domain/`) — No mocks required

| Test File | What it Tests |
|---|---|
| `test_entities.py` | `Ticket` creation, `TicketStatus` transitions, `Session` message append |
| `test_value_objects.py` | `ConfidenceScore.is_low_confidence()`, `Intent` enum exhaustiveness |

These tests have **zero dependencies** on Azure or any external service.

#### Step 7.2 — Application Tests (`tests/application/`) — In-memory port fakes

Create lightweight in-memory implementations of each port interface for testing:

```python
class InMemoryTicketRepository(ITicketRepository):
    def __init__(self): self._store: dict[str, Ticket] = {}
    def create(self, ticket): self._store[ticket.id] = ticket; return ticket
    # ... other methods
```

| Test File | What it Tests |
|---|---|
| `test_process_chat_use_case.py` | Intent routing, multi-intent fan-out, escalation trigger at < 0.6 confidence |
| `test_answer_kb_query_use_case.py` | RBAC filter, version comparison, multilingual detection |
| `test_manage_ticket_use_case.py` | Create / status / update intents, missing-field handling |
| `test_escalate_issue_use_case.py` | Summary composition, case reference generation |

No Azure SDK mocks needed — in-memory fakes implement the port interfaces.

#### Step 7.3 — Adapter Tests (`tests/adapters/`) — Mocked Azure SDK clients

| Test File | What it Tests |
|---|---|
| `test_cosmos_ticket_repository.py` | Cosmos partition key logic, document mapping, error handling |
| `test_cosmos_session_repository.py` | TTL setting, message append, session creation |
| `test_azure_search_service.py` | Hybrid search query construction, RBAC filter expression |
| `test_agent_adapters.py` | MAF tool input/output mapping ↔ use case DTOs |

Use `unittest.mock.patch` to mock Azure SDK calls only at this layer.

#### Step 7.4 — Infrastructure Tests (`tests/infrastructure/`)

| Test File | What it Tests |
|---|---|
| `test_api.py` | All API endpoints using `httpx.AsyncClient` with the FastAPI test client |
| `test_orchestration_e2e.py` | All 10 sample queries end-to-end against live Azure resources (integration) |

Run all tests:
```bash
# All unit tests (no Azure credentials needed)
pytest tests/domain/ tests/application/ tests/adapters/ -v --tb=short

# Full suite including integration tests (requires .env)
pytest tests/ -v --tb=short
```

---

### Phase 8 — Containerization & Deployment

**Goal:** Package the app as a Docker container and deploy to Azure Container Apps.

#### Step 8.1 — Dockerfile

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
EXPOSE 8000
CMD ["uvicorn", "src.infrastructure.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Step 8.2 — Local Docker Compose (`docker-compose.yml`)

```yaml
version: "3.9"
services:
  helpdesk-api:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
```

Run locally:
```bash
docker compose up --build
```

#### Step 8.3 — Deploy to Azure Container Apps (Optional)

```bash
# Login
az login

# Build and push image
az acr build --registry <acr-name> --image helpdesk-api:latest .

# Deploy
az containerapp create \
  --name helpdesk-api \
  --resource-group <rg> \
  --environment <env-name> \
  --image <acr-name>.azurecr.io/helpdesk-api:latest \
  --target-port 8000 \
  --ingress external \
  --env-vars @.env
```

---

### Phase 9 — Demo & Validation

**Goal:** Demonstrate all 10 sample queries and validate deliverables.

#### Step 9.1 — Run Demo Script

`demo/run_demo.py` is an **interactive CLI** that connects directly to the application layer (bypassing HTTP) for a fast local demo. Type any message at the `You>` prompt and press Enter to get a response.

**Features:**
- Connects directly via `get_process_chat_use_case()` (no HTTP round-trip needed)
- Maintains a session across the conversation
- Displays confidence score, ticket ID, escalation case, and source citations per response
- Supports `role` command to switch between `employee` and `it_admin` mid-session
- Type `quit` to exit

**Run (Windows PowerShell):**
```powershell
$env:PYTHONPATH = "."; $env:PYTHONUTF8 = "1"; python demo/run_demo.py
```

> **`PYTHONUTF8=1`** is required on Windows to display box-drawing characters in the banner. The script also calls `sys.stdout.reconfigure(encoding='utf-8', errors='replace')` at startup for compatibility.

**Sample session:**
```
You> How do I connect to the company VPN?
Assistant> To connect... [step-by-step instructions]
  [Confidence] 1.00
  [Sources]
    - 02-vpn-configuration-manual-2025-v1.pdf p.1 (v1.0)
    - 03-vpn-configuration-manual-2026-v1.docx p.1 (v1.0)

You> My laptop screen went black. Please create a ticket.
Assistant> Ticket TKT-XXXXXXXX has been created successfully.
  [Ticket] TKT-XXXXXXXX

You> quit
Goodbye!
```

#### Step 9.2 — Validate Deliverables

- [ ] VPN / password / software queries return grounded English answers with source citations
- [ ] RBAC filter blocks non-admin access to restricted documents
- [ ] Ticket creation flow returns a new `TKT-XXXXXXXX` ID in Cosmos DB
- [ ] Explicit escalation request returns an `ESC-XXXXXXXX` case reference
- [ ] Confidence score displayed correctly per response
- [ ] Escalation auto-triggers when KB confidence < 0.6

> For browser-based end-to-end testing, use the **Streamlit UI** at `http://localhost:8501` (see [Section 11](#11-streamlit-ui)).

---

## 7. Sample Queries & Expected Outputs

| # | Query | Agent(s) Invoked | Expected Output |
|---|---|---|---|
| 1 | How do I connect to the corporate VPN? | KB Agent | Step-by-step VPN setup from manual with OS-specific sections cited |
| 2 | My VPN keeps disconnecting after 10 minutes. (Steps don't help) | KB Agent → Escalation Agent | Troubleshooting steps; if unresolved, escalation case reference |
| 3 | Create a ticket for my laptop not booting. | Ticket Agent | New ticket ID created and confirmed |
| 4 | What's the status of my last ticket? | Ticket Agent | Most recent ticket with status and timestamp |
| 5 | What changed in VPN config between v1 2025 and v1 2026? | KB Agent (multi-version) | Diff highlighting new MFA requirement, deprecated split-tunnel |
| 6 | What software is approved for code editing? | KB Agent | Approved IDE list with license type and installation link |
| 7 | Show me the security incident playbook. | KB Agent (RBAC) | Access-denied for employees; content returned for it_admin |
| 8 | I need to talk to a human about a recurring issue. | Escalation Agent | Conversation summary + escalation confirmation with case reference |
| 9 | How do I set up the office printer? Also, what's my ticket TKT-0042 status? | KB Agent + Ticket Agent (parallel) | Merged response: printer setup steps + ticket status |
| 10 | Responde en español: ¿cómo reseteo mi contraseña? | KB Agent (multilingual) | Password reset steps returned in Spanish with source citation |

---

## 8. Key Differentiators

| Feature | This Solution | Copilot Studio |
|---|---|---|
| Multi-agent orchestration with conditional routing | ✅ Custom Python logic | ❌ Requires Power Automate |
| Custom tool definitions (Search, Cosmos, Email) | ✅ MAF function-calling | ❌ Limited connectors |
| Persistent conversation memory in Cosmos DB | ✅ Full session + ticket cross-reference | ⚠️ Limited |
| Confidence-based escalation threshold | ✅ Programmatic 0.6 threshold | ❌ Not possible |
| Unit + integration tests, CI/CD deployable | ✅ pytest + Docker | ❌ |
| RBAC-based document filtering | ✅ Azure AI Search filter | ⚠️ Limited |
| Multi-language response | ✅ Detected and responded in-language | ⚠️ Limited |

---

## 9. Deliverables Checklist

- [x] **D1** — Python project with MAF-based multi-agent system (Orchestrator, KB Agent, Ticket Agent, Escalation Agent) — fully runnable locally and in Azure
- [x] **D2** — Azure AI Search index `it-helpdesk-kb` live with 19 chunks across 9 documents; hybrid search (BM25 + `text-embedding-3-large` vectors) enabled
- [x] **D3** — Azure Cosmos DB `HelpDeskDB` provisioned with `Tickets`, `Sessions`, and `EscalationCases` containers partitioned by `userId`
- [x] **D4** — FastAPI endpoint exposing `/api/v1/chat` with session management
- [x] **D5** — Agent instruction prompts for each agent covering intent classification, version comparison, multi-language responses, confidence disclaimers, and escalation criteria
- [x] **D6** — Demo script (`demo/run_demo.py`) with 10 sample queries covering all scenarios
- [x] **D7** — 145 unit + integration tests passing at **98.64% code coverage** (`pytest` + `pytest-cov`)
- [x] **D8** — Streamlit web UI (`ui/streamlit_app.py`) with live chat, confidence indicators, ticket/escalation display, source citation expander, session management, role switching, and sample query shortcuts

---

## 10. Setup & Running Locally

### Prerequisites

- Python 3.12+
- Docker Desktop
- Azure CLI (`az`)
- Active Azure subscription with the resources listed in Phase 1

### Quick Start

```bash
# 1. Clone the repo and navigate to project folder
cd AppsandData_IT_Helpdesk

# 2. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy and fill in environment variables
copy .env.example .env
# Edit .env with your Azure resource keys

# 5. Run the knowledge base indexing pipeline (one-time)
# Windows PowerShell:
$env:PYTHONPATH = "."; python src/infrastructure/indexing/run_indexing_pipeline.py --data-dir data/raw --doc-version v1.0 --access-role public
# Linux/macOS:
# PYTHONPATH=. python src/infrastructure/indexing/run_indexing_pipeline.py --data-dir data/raw --doc-version v1.0 --access-role public

# 6. Start the FastAPI server
$env:PYTHONPATH = "."; uvicorn src.infrastructure.api.main:app --reload --port 8000

# 7. Test with a sample query
curl -X POST http://localhost:8000/api/v1/chat `
  -H "Content-Type: application/json" `
  -d '{"session_id":"s1","user_id":"emp_1","user_role":"employee","message":"How do I connect to VPN?"}'

# 8. Run all tests
pytest tests/ -v

# 9. Run the interactive CLI demo (requires FastAPI server NOT needed — uses app layer directly)
$env:PYTHONUTF8 = "1"; python demo/run_demo.py

# 10. Launch the Streamlit web UI (requires FastAPI server on port 8000)
.venv\Scripts\streamlit run ui\streamlit_app.py --server.port 8501
```

> **Running both the API and Streamlit simultaneously:**
> Open two terminal windows — run the FastAPI server in one and Streamlit in the other.
> Then open **http://localhost:8501** in your browser.

### API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/api/v1/chat` | POST | Send a message, receive agent response |
| `/api/v1/sessions/{session_id}/history` | GET | Retrieve full conversation history |
| `/api/v1/tickets/{user_id}` | GET | List all tickets for a user |
| `/api/v1/health` | GET | Health check |

---

## Implementation Phases Summary

Phases are ordered to respect the Clean Architecture dependency rule — inner layers always before outer:

```
Phase 1 ──► Environment & Azure Resource Setup         (~1 day)
Phase 2 ──► Domain Layer (entities, VOs, ports)        (~1 day)     ← innermost, no deps
Phase 3 ──► Application Layer (use cases, DTOs)        (~2 days)    ← depends on domain only
Phase 4 ──► Adapters Layer (repos, services, agents)   (~3 days)    ← depends on domain + app
Phase 5 ──► Infrastructure Layer (FastAPI, DI, config) (~1 day)     ← outermost, wires all
Phase 6 ──► Knowledge Base Indexing Pipeline           (~1–2 days)
Phase 7 ──► Testing (domain → app → adapters → infra)  (~2 days)
Phase 8 ──► Containerization & Deployment              (~1 day)
Phase 9 ──► Demo & Validation                          (~1 day)
                                               Total: ~13–14 days
```

### Dependency Flow Verification

Before each PR, verify no layer violates the dependency rule:

```bash
# Ensure domain layer has no imports from adapters or infrastructure
grep -r "from src.adapters\|from src.infrastructure" src/domain/  # must return nothing

# Ensure application layer has no imports from adapters or infrastructure
grep -r "from src.adapters\|from src.infrastructure" src/application/  # must return nothing

# Ensure adapters layer has no imports from infrastructure
grep -r "from src.infrastructure" src/adapters/  # must return nothing
```

---

## 11. Streamlit UI

A browser-based chat interface for testing the full end-to-end agent flow without needing `curl` or a REST client.

### Prerequisites

- FastAPI server running on port 8000 (see [Setup & Running Locally](#10-setup--running-locally))
- `streamlit` installed (included in `requirements.txt`)

### Launch

```powershell
# From project root (Windows)
.venv\Scripts\streamlit run ui\streamlit_app.py --server.port 8501
```

Open **http://localhost:8501** in your browser.

### Features

| Feature | Details |
|---|---|
| **Live API status** | Sidebar shows 🟢 online / 🔴 offline; chat input disabled when API is down |
| **User & role selector** | Switch between `employee` and `it_admin` mid-session; change user ID freely |
| **Session management** | Session ID shown; "New Session" button resets history and generates a new UUID |
| **Sample query shortcuts** | 7 one-click buttons in the sidebar to fire common queries instantly |
| **Metrics row** | Live counts of messages sent, KB answers, tickets created, and escalations |
| **Confidence indicator** | 🟢 ≥70%, 🟡 40–69%, 🔴 <40% — colour-coded per response |
| **Ticket & escalation IDs** | Displayed inline with each assistant response |
| **Source citations** | Collapsible expander listing document name, page, and version per chunk |
| **Error handling** | Connection errors, timeouts, and HTTP errors shown as inline alerts |

### Screenshot overview

```
┌─────────────────────┬────────────────────────────────────────────────┐
│  ⚙️ Settings        │  🛠️ IT Helpdesk AI Assistant                   │
│  🟢 API online      │  Session abc123… | User demo-001 | Role emp    │
│                     │  ─────────────────────────────────────────────  │
│  👤 User            │  Messages: 2  KB: 1  Tickets: 1  Escalations: 0│
│  demo-user-001      │  ─────────────────────────────────────────────  │
│  Role: Employee     │  👤 How do I connect to the VPN?               │
│                     │                                                 │
│  🔑 Session         │  🛠️ To connect to the VPN...                   │
│  abc123…            │     🟢 Confidence: 100%                        │
│  [🔄 New Session]   │     📚 Sources (5) ▼                           │
│                     │       - 02-vpn-manual-2025.pdf · p.1 · v1.0   │
│  💡 Sample Queries  │                                                 │
│  [How do I VPN?  ]  │  👤 Create a ticket for my black screen        │
│  [Password reset ]  │                                                 │
│  [Create a ticket]  │  🛠️ Ticket TKT-BF28F727 created.              │
│  ...                │     🎫 TKT-BF28F727                            │
│                     │  ─────────────────────────────────────────────  │
│                     │  [ Ask a question or describe your IT issue… ] │
└─────────────────────┴────────────────────────────────────────────────┘
```

### File

`ui/streamlit_app.py` — self-contained, no changes required to any other source file. Calls `POST /api/v1/chat` via `requests` and renders the full `ChatResponse` payload.
