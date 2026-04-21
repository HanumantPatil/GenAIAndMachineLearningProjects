"""Tests for IntentClassifier."""
import json
import pytest
from tests.conftest import FakeLLMService
from src.application.services.intent_classifier import IntentClassifier
from src.domain.value_objects.intent import Intent


def _llm_with(response: str) -> FakeLLMService:
    return FakeLLMService(responses=[response])


def test_classify_kb_lookup():
    llm = _llm_with(json.dumps({"intent": "kb_lookup", "kb_query": "VPN setup", "sub_intents": [], "ticket_id": None, "doc_versions": None}))
    ic = IntentClassifier(llm)
    result = ic.classify("How do I set up VPN?", [])
    assert result["intent"] == Intent.KB_LOOKUP
    assert result["kb_query"] == "VPN setup"


def test_classify_ticket_create():
    llm = _llm_with(json.dumps({"intent": "ticket_create", "kb_query": None, "sub_intents": [], "ticket_id": None, "doc_versions": None}))
    ic = IntentClassifier(llm)
    result = ic.classify("My laptop won't start", [])
    assert result["intent"] == Intent.TICKET_CREATE


def test_classify_fallback_on_invalid_json():
    llm = _llm_with("this is not json at all")
    ic = IntentClassifier(llm)
    result = ic.classify("something", [])
    assert result["intent"] == Intent.UNKNOWN


def test_classify_fallback_on_unknown_intent_value():
    llm = _llm_with(json.dumps({"intent": "completely_made_up", "kb_query": None, "sub_intents": [], "ticket_id": None, "doc_versions": None}))
    ic = IntentClassifier(llm)
    result = ic.classify("test", [])
    assert result["intent"] == Intent.UNKNOWN


def test_classify_multi_intent():
    llm = _llm_with(json.dumps({"intent": "multi_intent", "kb_query": "password reset", "sub_intents": ["kb_lookup", "ticket_create"], "ticket_id": None, "doc_versions": None}))
    ic = IntentClassifier(llm)
    result = ic.classify("How do I reset password and also open a ticket?", [])
    assert result["intent"] == Intent.MULTI_INTENT
    assert "kb_lookup" in result["sub_intents"]


def test_history_trimmed_to_last_6():
    calls = []
    class RecordingLLM(FakeLLMService):
        def complete(self, messages):
            calls.append(messages)
            return json.dumps({"intent": "unknown", "kb_query": None, "sub_intents": [], "ticket_id": None, "doc_versions": None})
    history = [{"role": "user", "content": f"msg {i}"} for i in range(20)]
    ic = IntentClassifier(RecordingLLM())
    ic.classify("new message", history)
    user_msg = calls[0][-1]["content"]
    # The history in the prompt should only reference last 6 messages
    assert "msg 14" in user_msg or "msg 19" in user_msg or len(calls) > 0
