"""Tests for AzureOpenAIService (mocked OpenAI SDK)."""
from unittest.mock import MagicMock, patch
from src.adapters.services.azure_openai_service import AzureOpenAIService


def _make_svc(content: str = "Hello") -> tuple:
    mock_choice = MagicMock()
    mock_choice.message.content = content
    mock_completions = MagicMock()
    mock_completions.choices = [mock_choice]

    with patch("src.adapters.services.azure_openai_service.AzureOpenAI") as MockOpenAI:
        MockOpenAI.return_value.chat.completions.create.return_value = mock_completions
        svc = AzureOpenAIService("https://endpoint", "key", "gpt-4o")
        return svc, MockOpenAI.return_value.chat.completions.create


def test_complete_returns_text():
    svc, mock_create = _make_svc("Use GlobalProtect for VPN.")
    result = svc.complete([{"role": "user", "content": "VPN help?"}])
    assert result == "Use GlobalProtect for VPN."
    mock_create.assert_called_once()


def test_complete_none_content_returns_empty_string():
    svc, _ = _make_svc(content=None)
    result = svc.complete([{"role": "user", "content": "?"}])
    assert result == ""


def test_complete_passes_model_deployment():
    svc, mock_create = _make_svc("answer")
    svc.complete([{"role": "user", "content": "test"}])
    call_kwargs = mock_create.call_args[1]
    assert call_kwargs["model"] == "gpt-4o"
    assert call_kwargs["temperature"] == 0.2
    assert call_kwargs["max_tokens"] == 1024
