"""IT Helpdesk DevUI — interactive web interface for testing all agents locally.

Launches Microsoft Agent Framework DevUI with all four helpdesk agents
(Orchestrator, KB, Ticket, Escalation) registered for in-browser testing.

Usage (Windows PowerShell):
    $env:PYTHONPATH = "."; python devui_app.py

    # Custom port / no auto-open:
    $env:PYTHONPATH = "."; python devui_app.py --port 9000 --no-open

    # Enable file-watch auto-reload during development:
    $env:PYTHONPATH = "."; python devui_app.py --reload

Linux / macOS:
    PYTHONPATH=. python devui_app.py

After launch, open  http://localhost:8080  (or your custom port) in a browser.
Select an agent from the left-hand panel and start chatting.

References:
    https://learn.microsoft.com/en-us/agent-framework/devui/?pivots=programming-language-python
"""
from __future__ import annotations

import argparse
import json
import os
import secrets
import sys
from pathlib import Path

# Ensure the project root is on sys.path so 'src.*' imports resolve.
sys.path.insert(0, str(Path(__file__).parent))

from agent_framework import Agent  # pip install agent-framework-devui --pre
from agent_framework.openai import OpenAIChatClient  # pip install agent-framework-openai --pre
from agent_framework.devui import serve

from src.adapters.agents.orchestrator_agent_adapter import OrchestratorAgentAdapter
from src.adapters.repositories.cosmos_escalation_repository import CosmosEscalationRepository
from src.adapters.repositories.cosmos_session_repository import CosmosSessionRepository
from src.adapters.repositories.cosmos_ticket_repository import CosmosTicketRepository
from src.adapters.services.azure_openai_service import AzureOpenAIService
from src.adapters.services.azure_search_service import AzureSearchService
from src.adapters.services.email_notification_service import EmailNotificationService
from src.application.use_cases.answer_kb_query_use_case import AnswerKBQueryUseCase
from src.application.use_cases.escalate_issue_use_case import EscalateIssueUseCase
from src.application.use_cases.manage_ticket_use_case import ManageTicketUseCase
from src.application.use_cases.process_chat_use_case import ProcessChatUseCase
from src.domain.value_objects.intent import Intent
from src.domain.value_objects.user_role import UserRole
from src.infrastructure.config.settings import get_settings


# ── Helpers ──────────────────────────────────────────────────────────────────

def _read_prompt(filename: str) -> str:
    """Return the contents of a system-prompt Markdown file."""
    prompt_dir = Path(__file__).parent / "src" / "adapters" / "agents" / "prompts"
    return (prompt_dir / filename).read_text(encoding="utf-8")


def _build_use_cases() -> tuple[
    ProcessChatUseCase,
    AnswerKBQueryUseCase,
    ManageTicketUseCase,
    EscalateIssueUseCase,
]:
    """Wire all use cases from settings — mirrors dependencies.py composition root."""
    s = get_settings()

    llm = AzureOpenAIService(
        endpoint=s.azure_openai_endpoint,
        api_key=s.azure_openai_api_key,
        deployment=s.azure_openai_deployment,
        api_version=s.azure_openai_api_version,
    )
    kb_search = AzureSearchService(
        endpoint=s.azure_search_endpoint,
        api_key=s.azure_search_api_key,
        index_name=s.azure_search_index,
    )
    ticket_repo = CosmosTicketRepository(
        endpoint=s.cosmos_endpoint,
        key=s.cosmos_key,
        database=s.cosmos_database,
        container=s.cosmos_tickets_container,
    )
    session_repo = CosmosSessionRepository(
        endpoint=s.cosmos_endpoint,
        key=s.cosmos_key,
        database=s.cosmos_database,
        container=s.cosmos_sessions_container,
    )
    escalation_repo = CosmosEscalationRepository(
        endpoint=s.cosmos_endpoint,
        key=s.cosmos_key,
        database=s.cosmos_database,
        container=s.cosmos_escalation_container,
    )
    notification = EmailNotificationService(escalation_email=s.escalation_email)

    kb_uc = AnswerKBQueryUseCase(kb_search=kb_search, llm=llm)
    ticket_uc = ManageTicketUseCase(ticket_repo=ticket_repo)
    escalation_uc = EscalateIssueUseCase(
        llm=llm, notification=notification, escalation_repo=escalation_repo
    )
    orchestrator_uc = ProcessChatUseCase(
        ticket_repo=ticket_repo,
        session_repo=session_repo,
        escalation_repo=escalation_repo,
        kb_search=kb_search,
        llm=llm,
        notification=notification,
    )
    return orchestrator_uc, kb_uc, ticket_uc, escalation_uc


# ── Agent factories ───────────────────────────────────────────────────────────

def _make_orchestrator_agent(
    client: OpenAIChatClient,
    use_case: ProcessChatUseCase,
) -> Agent:
    adapter = OrchestratorAgentAdapter(use_case)

    def route_helpdesk_request(
        session_id: str,
        user_id: str,
        user_role: str,
        message: str,
    ) -> str:
        """Route an IT helpdesk request through the full Orchestrator pipeline.

        The Orchestrator classifies the user's intent (KB lookup, ticket
        management, escalation, or multi-intent) and delegates to the
        appropriate sub-agent, then merges and returns the combined response.

        Args:
            session_id: Unique session identifier, e.g. 'devui-session-001'.
            user_id: Employee ID, e.g. 'emp-001'.
            user_role: 'employee' or 'it_admin'.
            message: The user's IT support question or request.

        Returns:
            JSON-encoded response with keys: session_id, response, sources,
            ticket_id, escalation_case, confidence_score.
        """
        result = adapter.chat(session_id, user_id, user_role, message)
        return json.dumps(result, indent=2, default=str)

    return Agent(
        name="IT-Helpdesk-Orchestrator",
        client=client,
        instructions=_read_prompt("orchestrator_prompt.md"),
        tools=[route_helpdesk_request],
        description=(
            "Main entry point for all IT helpdesk requests. "
            "Classifies intent and routes to KB, Ticket, or Escalation sub-agents. "
            "Use this agent for realistic end-to-end testing."
        ),
    )


def _make_kb_agent(
    client: OpenAIChatClient,
    use_case: AnswerKBQueryUseCase,
) -> Agent:
    def search_knowledge_base(
        query: str,
        user_role: str = "employee",
        top_k: int = 5,
    ) -> str:
        """Search the IT knowledge base and return a grounded answer with citations.

        Performs hybrid (semantic + keyword) retrieval over indexed IT documents
        (VPN manuals, laptop setup guides, software catalogs, etc.) and generates
        a grounded answer using Azure OpenAI GPT-4o.

        Args:
            query: Natural-language IT question, e.g. 'How do I configure VPN?'.
            user_role: 'employee' (public docs) or 'it_admin' (all docs including
                       restricted security playbooks).
            top_k: Number of knowledge base chunks to retrieve (1–10, default 5).

        Returns:
            JSON with 'response' (grounded answer), 'sources' (list of
            {source_file, page_number, doc_version, score}), and
            'confidence_score' (0.0 – 1.0).
        """
        result = use_case.execute(
            session_id="devui-kb",
            query=query,
            user_role=UserRole(user_role),
        )
        return json.dumps(
            {
                "response": result.response,
                "sources": result.sources,
                "confidence_score": result.confidence_score,
            },
            indent=2,
            default=str,
        )

    return Agent(
        name="IT-KB-Agent",
        client=client,
        instructions=_read_prompt("kb_agent_prompt.md"),
        tools=[search_knowledge_base],
        description=(
            "Answers IT procedure and policy questions using hybrid RAG "
            "(Azure AI Search + GPT-4o). Returns grounded answers with source "
            "citations and a confidence score. Test isolation: KB retrieval only."
        ),
    )


def _make_ticket_agent(
    client: OpenAIChatClient,
    use_case: ManageTicketUseCase,
) -> Agent:
    def create_support_ticket(user_id: str, title: str, description: str) -> str:
        """Create a new IT support ticket in Azure Cosmos DB.

        Args:
            user_id: Employee requesting support, e.g. 'emp-001'.
            title: Short issue summary, e.g. 'Laptop not booting'.
            description: Full description of the problem.

        Returns:
            JSON with 'response' (confirmation message) and 'ticket_id'
            (e.g. 'TKT-ABCD1234').
        """
        result = use_case.execute(
            session_id="devui-ticket",
            intent=Intent.TICKET_CREATE,
            user_id=user_id,
            title=title,
            description=description,
        )
        return json.dumps(
            {"response": result.response, "ticket_id": result.ticket_id},
            indent=2,
            default=str,
        )

    def get_ticket_status(ticket_id: str, user_id: str) -> str:
        """Retrieve the current status of an IT support ticket.

        Args:
            ticket_id: Ticket identifier, e.g. 'TKT-ABCD1234'.
                       Pass an empty string '' to fetch the user's most recent ticket.
            user_id: The employee who owns the ticket.

        Returns:
            JSON with 'response' containing ticket title, status, and timestamps.
        """
        result = use_case.execute(
            session_id="devui-ticket",
            intent=Intent.TICKET_STATUS,
            user_id=user_id,
            ticket_id=ticket_id or None,
        )
        return json.dumps(
            {"response": result.response, "ticket_id": result.ticket_id},
            indent=2,
            default=str,
        )

    def update_ticket_status(ticket_id: str, user_id: str, new_status: str) -> str:
        """Update the status of an existing IT support ticket.

        Args:
            ticket_id: Ticket identifier, e.g. 'TKT-ABCD1234'.
            user_id: The ticket owner.
            new_status: One of 'open', 'in_progress', 'resolved', 'closed'.

        Returns:
            JSON with 'response' confirming the status update.
        """
        result = use_case.execute(
            session_id="devui-ticket",
            intent=Intent.TICKET_UPDATE,
            user_id=user_id,
            ticket_id=ticket_id,
            new_status=new_status,
        )
        return json.dumps(
            {"response": result.response, "ticket_id": result.ticket_id},
            indent=2,
            default=str,
        )

    return Agent(
        name="IT-Ticket-Agent",
        client=client,
        instructions=_read_prompt("ticket_agent_prompt.md"),
        tools=[create_support_ticket, get_ticket_status, update_ticket_status],
        description=(
            "Creates, retrieves, and updates IT support tickets stored in "
            "Azure Cosmos DB. Test isolation: Cosmos DB ticket operations only."
        ),
    )


def _make_escalation_agent(
    client: OpenAIChatClient,
    use_case: EscalateIssueUseCase,
) -> Agent:
    def escalate_to_human_specialist(
        session_id: str,
        user_id: str,
        conversation_summary: str,
    ) -> str:
        """Escalate an unresolved IT issue to a human IT specialist.

        Composes a structured escalation summary using GPT-4o, simulates an
        IT admin notification (email/Teams), persists the escalation case in
        Cosmos DB, and returns a case reference ID.

        Args:
            session_id: Current session identifier, e.g. 'devui-session-001'.
            user_id: Employee requesting escalation, e.g. 'emp-001'.
            conversation_summary: Plain-text summary of the conversation and
                                  troubleshooting steps already attempted.

        Returns:
            JSON with 'response' (escalation confirmation) and
            'escalation_case' (e.g. 'ESC-xxxxxxxx-xxxx-...').
        """
        result = use_case.execute(
            session_id=session_id,
            user_id=user_id,
            conversation_history=[{"role": "user", "content": conversation_summary}],
        )
        return json.dumps(
            {
                "response": result.response,
                "escalation_case": result.escalation_case,
            },
            indent=2,
            default=str,
        )

    return Agent(
        name="IT-Escalation-Agent",
        client=client,
        instructions=_read_prompt("escalation_agent_prompt.md"),
        tools=[escalate_to_human_specialist],
        description=(
            "Escalates unresolved IT issues to human IT specialists. "
            "Generates a professional escalation summary via LLM and returns "
            "a unique case reference ID. Test isolation: escalation flow only."
        ),
    )


# ── Entry point ───────────────────────────────────────────────────────────────

def _prepare_devui_auth_token(host: str) -> str | None:
    """Ensure a DevUI auth token exists and return it when determinable.

    For loopback hosts, generate a token when one is not already provided via
    DEVUI_AUTH_TOKEN so startup logs can always display a copyable value.
    """
    token = os.getenv("DEVUI_AUTH_TOKEN")
    if token:
        return token

    if host in {"127.0.0.1", "localhost"}:
        token = secrets.token_urlsafe(32)
        os.environ["DEVUI_AUTH_TOKEN"] = token
        return token

    return None

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Launch the IT Helpdesk Agent Framework DevUI for local testing."
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=8080,
        help="HTTP port for the DevUI server (default: 8080).",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host address to bind to (default: 127.0.0.1).",
    )
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="Do not automatically open the browser on start.",
    )
    args = parser.parse_args()

    devui_token = _prepare_devui_auth_token(args.host)
    if devui_token:
        print("DevUI authentication is enabled.")
        print(f"Authentication token: {devui_token}")
        print("Use this value in the browser prompt or as Bearer token.\n")
    else:
        print("DEVUI_AUTH_TOKEN is not set. If auth is required, set it before startup.\n")

    print("Loading settings and building use cases...")
    settings = get_settings()

    # Shared Azure OpenAI chat client for all agents.
    # OpenAIChatClient uses the Responses API which requires api_version="preview".
    # Do NOT pass azure_openai_api_version from settings (that is for Chat Completions).
    chat_client = OpenAIChatClient(
        settings.azure_openai_deployment,
        api_key=settings.azure_openai_api_key,
        azure_endpoint=settings.azure_openai_endpoint,
        api_version="preview",
    )

    orchestrator_uc, kb_uc, ticket_uc, escalation_uc = _build_use_cases()

    agents = [
        _make_orchestrator_agent(chat_client, orchestrator_uc),
        _make_kb_agent(chat_client, kb_uc),
        _make_ticket_agent(chat_client, ticket_uc),
        _make_escalation_agent(chat_client, escalation_uc),
    ]

    print(f"\nRegistered {len(agents)} agents:")
    for agent in agents:
        print(f"  • {agent.name}")

    url = f"http://{args.host}:{args.port}"
    print(f"\nStarting DevUI → {url}")
    print(f"API (OpenAI-compatible) → {url}/v1/*")
    print("Press Ctrl+C to stop.\n")

    serve(
        entities=agents,
        host=args.host,
        port=args.port,
        auto_open=not args.no_open,
    )


if __name__ == "__main__":
    main()
