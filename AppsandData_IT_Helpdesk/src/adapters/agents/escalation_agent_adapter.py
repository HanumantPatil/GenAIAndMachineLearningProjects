"""EscalationAgentAdapter — registers escalation tool with Microsoft Agent Framework."""
from __future__ import annotations
import json
from typing import Any


def create_escalation_agent(
    project_client: Any,
    model_deployment: str,
    system_prompt_path: str,
    escalate_fn: "Callable[[str, str, list], dict]",
) -> Any:
    from azure.ai.projects.models import FunctionTool, ToolSet

    def escalate_issue(session_id: str, user_id: str, conversation_summary: str) -> str:
        """Escalate an unresolved IT issue to a human specialist.

        Args:
            session_id: The current session identifier.
            user_id: The user requesting escalation.
            conversation_summary: Plain-text summary of the conversation so far.

        Returns:
            JSON with escalation case ID and confirmation message.
        """
        return json.dumps(
            escalate_fn(session_id, user_id, [{"role": "user", "content": conversation_summary}])
        )

    with open(system_prompt_path, encoding="utf-8") as fh:
        system_prompt = fh.read()

    toolset = ToolSet()
    toolset.add(FunctionTool(functions={escalate_issue}))

    return project_client.agents.create_agent(
        model=model_deployment,
        name="IT-Escalation-Agent",
        instructions=system_prompt,
        toolset=toolset,
    )
