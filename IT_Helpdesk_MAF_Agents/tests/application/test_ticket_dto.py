"""Tests for TicketDTO."""
from src.application.dto.ticket_dto import TicketDTO
from src.domain.value_objects.ticket_status import TicketStatus
import datetime


def test_ticket_dto_fields():
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    dto = TicketDTO(
        ticket_id="TKT-001",
        user_id="u1",
        title="Screen broken",
        description="Black screen after update",
        status=TicketStatus.OPEN,
        created_at=now,
        updated_at=now,
        resolution_notes=None,
    )
    assert dto.ticket_id == "TKT-001"
    assert dto.user_id == "u1"
    assert dto.status == TicketStatus.OPEN
    assert dto.resolution_notes is None


def test_ticket_dto_with_resolution_notes():
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    dto = TicketDTO(
        ticket_id="TKT-002",
        user_id="u2",
        title="VPN issue",
        description="Cannot connect",
        status=TicketStatus.RESOLVED,
        created_at=now,
        updated_at=now,
        resolution_notes="Reinstalled VPN client",
    )
    assert dto.resolution_notes == "Reinstalled VPN client"
    assert dto.status == TicketStatus.RESOLVED
