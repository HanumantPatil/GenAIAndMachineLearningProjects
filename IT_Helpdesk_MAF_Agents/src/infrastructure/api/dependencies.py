"""FastAPI dependency-injection helpers."""
from __future__ import annotations
from functools import lru_cache

from src.adapters.repositories.cosmos_escalation_repository import CosmosEscalationRepository
from src.adapters.repositories.cosmos_session_repository import CosmosSessionRepository
from src.adapters.repositories.cosmos_ticket_repository import CosmosTicketRepository
from src.adapters.services.azure_openai_service import AzureOpenAIService
from src.adapters.services.azure_search_service import AzureSearchService
from src.adapters.services.email_notification_service import EmailNotificationService
from src.application.use_cases.process_chat_use_case import ProcessChatUseCase
from src.infrastructure.config.settings import get_settings


@lru_cache(maxsize=1)
def _build_use_case() -> ProcessChatUseCase:
    settings = get_settings()
    ticket_repo = CosmosTicketRepository(
        endpoint=settings.cosmos_endpoint,
        key=settings.cosmos_key,
        database=settings.cosmos_database,
        container=settings.cosmos_tickets_container,
    )
    session_repo = CosmosSessionRepository(
        endpoint=settings.cosmos_endpoint,
        key=settings.cosmos_key,
        database=settings.cosmos_database,
        container=settings.cosmos_sessions_container,
    )
    escalation_repo = CosmosEscalationRepository(
        endpoint=settings.cosmos_endpoint,
        key=settings.cosmos_key,
        database=settings.cosmos_database,
        container=settings.cosmos_escalation_container,
    )
    llm = AzureOpenAIService(
        endpoint=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_api_key,
        deployment=settings.azure_openai_deployment,
        api_version=settings.azure_openai_api_version,
    )
    kb_search = AzureSearchService(
        endpoint=settings.azure_search_endpoint,
        api_key=settings.azure_search_api_key,
        index_name=settings.azure_search_index,
    )
    notification = EmailNotificationService(
        escalation_email=settings.escalation_email,
    )
    return ProcessChatUseCase(
        ticket_repo=ticket_repo,
        session_repo=session_repo,
        escalation_repo=escalation_repo,
        kb_search=kb_search,
        llm=llm,
        notification=notification,
    )


def get_process_chat_use_case() -> ProcessChatUseCase:
    return _build_use_case()
