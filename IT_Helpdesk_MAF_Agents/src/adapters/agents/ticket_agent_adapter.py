"""TicketAgentAdapter — registers ticket management tools with Microsoft Agent Framework."""
from __future__ import annotations
import json
from typing import Any


def create_ticket_agent(
    project_client: Any,
    model_deployment: str,
    system_prompt_path: str,
    create_ticket_fn: "Callable[[str, str, str], dict]",
    get_ticket_fn: "Callable[[str, str], dict]",
    update_ticket_fn: "Callable[[str, str, str], dict]",
) -> Any:
    from azure.ai.projects.models import FunctionTool, ToolSet

    def create_ticket(user_id: str, title: str, description: str) -> str:
        """Create a new IT support ticket.

        Args:
            user_id: The ID of the requesting user.
            title: Short title for the ticket.
            description: Full description of the issue.

        Returns:
            JSON with created ticket details.
        """
        return json.dumps(create_ticket_fn(user_id, title, description))

    def get_ticket_status(ticket_id: str, user_id: str) -> str:
        """Get the current status of a support ticket.

        Args:
            ticket_id: The ticket identifier (e.g. TKT-ABCD1234).
            user_id: The user who owns the ticket.

        Returns:
            JSON with ticket status information.
        """
        return json.dumps(get_ticket_fn(ticket_id, user_id))

    def update_ticket_status(ticket_id: str, user_id: str, new_status: str) -> str:
        """Update the status of a support ticket.

        Args:
            ticket_id: The ticket identifier.
            user_id: The ticket owner.
            new_status: New status ('open', 'in_progress', 'resolved', 'closed').

        Returns:
            JSON with updated ticket.
        """
        return json.dumps(update_ticket_fn(ticket_id, user_id, new_status))

    with open(system_prompt_path, encoding="utf-8") as fh:
        system_prompt = fh.read()

    toolset = ToolSet()
    toolset.add(FunctionTool(functions={create_ticket, get_ticket_status, update_ticket_status}))

    return project_client.agents.create_agent(
        model=model_deployment,
        name="IT-Ticket-Agent",
        instructions=system_prompt,
        toolset=toolset,
    )
