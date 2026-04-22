"""CosmosSessionRepository — ISessionRepository implementation using Azure Cosmos DB."""
from __future__ import annotations

from azure.cosmos import CosmosClient, exceptions as cosmos_exc

from src.domain.entities.session import Session
from src.domain.ports.session_repository_port import ISessionRepository


class CosmosSessionRepository(ISessionRepository):
    def __init__(
        self,
        endpoint: str,
        key: str,
        database: str,
        container: str,
    ) -> None:
        client = CosmosClient(endpoint, credential=key)
        db = client.get_database_client(database)
        self._container = db.get_container_client(container)

    def get_or_create(self, session_id: str, user_id: str) -> Session:
        try:
            item = self._container.read_item(item=session_id, partition_key=session_id)
            return Session.from_dict(item)
        except cosmos_exc.CosmosResourceNotFoundError:
            session = Session(session_id=session_id, user_id=user_id)
            self._container.create_item(body=session.to_dict())
            return session

    def save(self, session: Session) -> Session:
        self._container.upsert_item(body=session.to_dict())
        return session

    def get_history(self, session_id: str) -> Session | None:
        try:
            item = self._container.read_item(item=session_id, partition_key=session_id)
            return Session.from_dict(item)
        except cosmos_exc.CosmosResourceNotFoundError:
            return None
