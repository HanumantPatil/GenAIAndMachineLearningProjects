"""Tests for MAF agent factory functions (kb, ticket, escalation)."""
import json
import os
import tempfile
from unittest.mock import MagicMock, patch


def _prompt_file(content: str = "You are an IT agent.") -> str:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(content)
        return f.name


def _capture_functions(calls: list):
    """Return a FunctionTool side_effect that captures inner functions."""
    def _side_effect(functions):
        calls.extend(list(functions))
        return MagicMock()
    return _side_effect


class TestKBAgentAdapter:
    def test_create_kb_agent_calls_create_agent(self):
        from src.adapters.agents.kb_agent_adapter import create_kb_agent
        prompt = _prompt_file()
        captured = []
        try:
            project_client = MagicMock()
            search_fn = MagicMock(return_value=[{"id": "c1"}])
            with patch("azure.ai.projects.models.FunctionTool", side_effect=_capture_functions(captured)), \
                 patch("azure.ai.projects.models.ToolSet", create=True):
                create_kb_agent(project_client, "gpt-4o", prompt, search_fn)
            project_client.agents.create_agent.assert_called_once()
            assert any(fn.__name__ == "search_kb_tool" for fn in captured)
        finally:
            os.unlink(prompt)

    def test_search_kb_tool_returns_json(self):
        from src.adapters.agents.kb_agent_adapter import create_kb_agent
        prompt = _prompt_file()
        captured = []
        try:
            project_client = MagicMock()
            search_fn = MagicMock(return_value=[{"id": "c1", "content": "vpn docs"}])
            with patch("azure.ai.projects.models.FunctionTool", side_effect=_capture_functions(captured)), \
                 patch("azure.ai.projects.models.ToolSet", create=True):
                create_kb_agent(project_client, "gpt-4o", prompt, search_fn)
            tool_fn = next(f for f in captured if f.__name__ == "search_kb_tool")
            result = tool_fn("VPN setup", "employee", 3)
            data = json.loads(result)
            assert data[0]["id"] == "c1"
        finally:
            os.unlink(prompt)


class TestTicketAgentAdapter:
    def test_create_ticket_agent_calls_create_agent(self):
        from src.adapters.agents.ticket_agent_adapter import create_ticket_agent
        prompt = _prompt_file()
        captured = []
        try:
            project_client = MagicMock()
            with patch("azure.ai.projects.models.FunctionTool", side_effect=_capture_functions(captured)), \
                 patch("azure.ai.projects.models.ToolSet", create=True):
                create_ticket_agent(
                    project_client, "gpt-4o", prompt,
                    create_ticket_fn=MagicMock(return_value={"ticket_id": "T1"}),
                    get_ticket_fn=MagicMock(return_value={"status": "open"}),
                    update_ticket_fn=MagicMock(return_value={"status": "closed"}),
                )
            project_client.agents.create_agent.assert_called_once()
            fn_names = {f.__name__ for f in captured}
            assert "create_ticket" in fn_names
            assert "get_ticket_status" in fn_names
            assert "update_ticket_status" in fn_names
        finally:
            os.unlink(prompt)

    def test_ticket_tool_functions_return_json(self):
        from src.adapters.agents.ticket_agent_adapter import create_ticket_agent
        prompt = _prompt_file()
        captured = []
        try:
            project_client = MagicMock()
            with patch("azure.ai.projects.models.FunctionTool", side_effect=_capture_functions(captured)), \
                 patch("azure.ai.projects.models.ToolSet", create=True):
                create_ticket_agent(
                    project_client, "gpt-4o", prompt,
                    create_ticket_fn=MagicMock(return_value={"ticket_id": "T1"}),
                    get_ticket_fn=MagicMock(return_value={"status": "open"}),
                    update_ticket_fn=MagicMock(return_value={"status": "resolved"}),
                )
            fn_map = {f.__name__: f for f in captured}
            assert json.loads(fn_map["create_ticket"]("u1", "Screen issue", "Black screen"))["ticket_id"] == "T1"
            assert json.loads(fn_map["get_ticket_status"]("T1", "u1"))["status"] == "open"
            assert json.loads(fn_map["update_ticket_status"]("T1", "u1", "resolved"))["status"] == "resolved"
        finally:
            os.unlink(prompt)


class TestEscalationAgentAdapter:
    def test_create_escalation_agent_calls_create_agent(self):
        from src.adapters.agents.escalation_agent_adapter import create_escalation_agent
        prompt = _prompt_file()
        captured = []
        try:
            project_client = MagicMock()
            escalate_fn = MagicMock(return_value={"case_id": "ESC-001"})
            with patch("azure.ai.projects.models.FunctionTool", side_effect=_capture_functions(captured)), \
                 patch("azure.ai.projects.models.ToolSet", create=True):
                create_escalation_agent(project_client, "gpt-4o", prompt, escalate_fn)
            project_client.agents.create_agent.assert_called_once()
            assert any(fn.__name__ == "escalate_issue" for fn in captured)
        finally:
            os.unlink(prompt)

    def test_escalation_tool_returns_json(self):
        from src.adapters.agents.escalation_agent_adapter import create_escalation_agent
        prompt = _prompt_file()
        captured = []
        try:
            project_client = MagicMock()
            escalate_fn = MagicMock(return_value={"case_id": "ESC-XYZ"})
            with patch("azure.ai.projects.models.FunctionTool", side_effect=_capture_functions(captured)), \
                 patch("azure.ai.projects.models.ToolSet", create=True):
                create_escalation_agent(project_client, "gpt-4o", prompt, escalate_fn)
            tool_fn = next(f for f in captured if f.__name__ == "escalate_issue")
            result = tool_fn("s1", "u1", "User cannot access VPN")
            data = json.loads(result)
            assert data["case_id"] == "ESC-XYZ"
        finally:
            os.unlink(prompt)
