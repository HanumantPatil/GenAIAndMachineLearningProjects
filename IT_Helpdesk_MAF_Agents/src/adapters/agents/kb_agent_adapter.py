"""KBAgentAdapter — registers search_kb_tool with Microsoft Agent Framework."""
from __future__ import annotations
import json
from typing import Any


def create_kb_agent(
    project_client: Any,
    model_deployment: str,
    system_prompt_path: str,
    search_fn: "Callable[[str, str, int], list[dict]]",
) -> Any:
    """
    Create a KB sub-agent using AIProjectClient + FunctionTool.

    Parameters
    ----------
    project_client  : azure.ai.projects.AIProjectClient
    model_deployment: e.g. "gpt-4o"
    system_prompt_path: path to kb_agent_prompt.md
    search_fn       : callable(query, user_role, top_k) → list of source dicts
    """
    from azure.ai.projects.models import FunctionTool, ToolSet

    def search_kb_tool(query: str, user_role: str = "employee", top_k: int = 5) -> str:
        """Search the IT knowledge base for relevant information.

        Args:
            query: The search query string.
            user_role: The role of the requesting user ('employee' or 'it_admin').
            top_k: Number of top results to return.

        Returns:
            JSON string containing matching knowledge base chunks.
        """
        results = search_fn(query, user_role, top_k)
        return json.dumps(results)

    with open(system_prompt_path, encoding="utf-8") as fh:
        system_prompt = fh.read()

    tool = FunctionTool(functions={search_kb_tool})
    toolset = ToolSet()
    toolset.add(tool)

    agent = project_client.agents.create_agent(
        model=model_deployment,
        name="IT-KB-Agent",
        instructions=system_prompt,
        toolset=toolset,
    )
    return agent
