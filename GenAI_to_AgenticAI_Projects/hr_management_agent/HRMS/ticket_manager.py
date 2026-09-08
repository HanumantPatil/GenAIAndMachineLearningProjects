from datetime import UTC, datetime
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from .schemas import TicketCreate, TicketStatus, TicketStatusUpdate
elif __package__:
    from .schemas import TicketCreate, TicketStatus, TicketStatusUpdate
else:
    from schemas import TicketCreate, TicketStatus, TicketStatusUpdate


class TicketRecord(TypedDict):
    ticket_id: str
    emp_id: str
    item: str
    reason: str
    status: TicketStatus
    created_at: str
    updated_at: str


class TicketManager:
    def __init__(self) -> None:
        self.tickets: list[TicketRecord] = []
        self._next_id: int = 1

    def create_ticket(self, req: TicketCreate) -> str:
        ticket_id = f"T{self._next_id:04d}"
        now = datetime.now(UTC).isoformat()
        ticket: TicketRecord = {
            "ticket_id": ticket_id,
            "emp_id": req.emp_id,
            "item": req.item,
            "reason": req.reason,
            "status": "Open",
            "created_at": now,
            "updated_at": now,
        }
        self.tickets.append(ticket)
        self._next_id += 1
        return f"Ticket {ticket_id} created for {req.emp_id}."

    def update_ticket_status(self, req: TicketStatusUpdate, ticket_id: str) -> str:
        for t in self.tickets:
            if t["ticket_id"] == ticket_id:
                t["status"] = req.status
                t["updated_at"] = datetime.now(UTC).isoformat()
                return f"Ticket {ticket_id} status updated to {req.status}."
        raise ValueError(f"Ticket '{ticket_id}' not found.")

    def list_tickets(
            self,
                employee_id: str | None = None,
                status: TicketStatus | None = None
            ) -> list[TicketRecord]:
        results = self.tickets
        if employee_id:
            results = [t for t in results if t["emp_id"] == employee_id]
        if status:
            results = [t for t in results if t["status"].lower() == status.lower()]
        return results
