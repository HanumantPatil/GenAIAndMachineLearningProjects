"""CosmosEscalationRepository — IEscalationRepository using Azure Cosmos DB."""
from __future__ import annotations

from azure.cosmos import CosmosClient, exceptions as cosmos_exc

from src.domain.entities.escalation_case import EscalationCase
from src.domain.ports.escalation_repository_port import IEscalationRepository


class CosmosEscalationRepository(IEscalationRepository):
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

    def create(self, case: EscalationCase) -> EscalationCase:
        self._container.create_item(body=case.to_dict())
        return case

    def get_by_id(self, case_id: str) -> EscalationCase | None:
        try:
            item = self._container.read_item(item=case_id, partition_key=case_id)
            return EscalationCase.from_dict(item)
        except cosmos_exc.CosmosResourceNotFoundError:
            return None
