"""CosmosTicketRepository — ITicketRepository implementation using Azure Cosmos DB."""
from __future__ import annotations

from azure.cosmos import CosmosClient, exceptions as cosmos_exc

from src.domain.entities.ticket import Ticket
from src.domain.ports.ticket_repository_port import ITicketRepository


class CosmosTicketRepository(ITicketRepository):
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

    def create(self, ticket: Ticket) -> Ticket:
        self._container.create_item(body=ticket.to_dict())
        return ticket

    def get_by_id(self, ticket_id: str, user_id: str) -> Ticket | None:
        try:
            item = self._container.read_item(item=ticket_id, partition_key=user_id)
            return Ticket.from_dict(item)
        except cosmos_exc.CosmosResourceNotFoundError:
            return None

    def get_latest(self, user_id: str) -> Ticket | None:
        query = (
            "SELECT TOP 1 * FROM c WHERE c.userId = @uid ORDER BY c.created_at DESC"
        )
        params = [{"name": "@uid", "value": user_id}]
        items = list(
            self._container.query_items(
                query=query,
                parameters=params,
                partition_key=user_id,
            )
        )
        return Ticket.from_dict(items[0]) if items else None

    def update(self, ticket: Ticket) -> Ticket:
        self._container.replace_item(item=ticket.id, body=ticket.to_dict())
        return ticket

    def list_by_user(self, user_id: str) -> list[Ticket]:
        query = "SELECT * FROM c WHERE c.userId = @uid ORDER BY c.created_at DESC"
        params = [{"name": "@uid", "value": user_id}]
        items = list(
            self._container.query_items(
                query=query, parameters=params, partition_key=user_id
            )
        )
        return [Ticket.from_dict(i) for i in items]
