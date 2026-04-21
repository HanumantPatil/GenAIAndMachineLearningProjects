"""Application settings loaded from environment variables via Pydantic BaseSettings."""
from __future__ import annotations
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # Azure AI Project
    azure_ai_project_conn_string: str = ""

    # Azure OpenAI
    azure_openai_endpoint: str = ""
    azure_openai_api_key: str = ""
    azure_openai_deployment: str = "gpt-4o"
    azure_openai_embedding_deployment: str = "text-embedding-3-large"
    azure_openai_api_version: str = "2024-02-01"

    # Azure AI Search
    azure_search_endpoint: str = ""
    azure_search_api_key: str = ""
    azure_search_index: str = "it-helpdesk-kb"

    # Azure Cosmos DB
    cosmos_endpoint: str = ""
    cosmos_key: str = ""
    cosmos_database: str = "it-helpdesk"
    cosmos_tickets_container: str = "Tickets"
    cosmos_sessions_container: str = "Sessions"
    cosmos_escalation_container: str = "EscalationCases"

    # Notification
    escalation_email: str = "it-support@company.com"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
