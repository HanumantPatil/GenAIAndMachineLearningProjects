"""Tests for DI dependencies wiring."""
from unittest.mock import MagicMock, patch
from src.application.use_cases.process_chat_use_case import ProcessChatUseCase
from src.infrastructure.api.dependencies import _build_use_case, get_process_chat_use_case


_PATCHES = [
    "src.adapters.repositories.cosmos_ticket_repository.CosmosClient",
    "src.adapters.repositories.cosmos_session_repository.CosmosClient",
    "src.adapters.repositories.cosmos_escalation_repository.CosmosClient",
    "src.adapters.services.azure_openai_service.AzureOpenAI",
    "src.adapters.services.azure_search_service.SearchClient",
    "src.adapters.services.azure_search_service.AzureKeyCredential",
]


def _apply_patches(fn):
    import functools
    from unittest.mock import patch as _patch
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        patchers = [_patch(p) for p in _PATCHES]
        for p in patchers:
            p.start()
        try:
            return fn(*args, **kwargs)
        finally:
            for p in reversed(patchers):
                p.stop()
    return wrapper


@_apply_patches
def test_build_use_case_returns_process_chat_use_case():
    settings = MagicMock()
    _build_use_case.cache_clear()
    use_case = _build_use_case(settings)
    assert isinstance(use_case, ProcessChatUseCase)


@_apply_patches
def test_get_process_chat_use_case_returns_use_case():
    settings = MagicMock()
    with patch("src.infrastructure.api.dependencies.get_settings", return_value=settings):
        _build_use_case.cache_clear()
        use_case = get_process_chat_use_case()
        assert isinstance(use_case, ProcessChatUseCase)
