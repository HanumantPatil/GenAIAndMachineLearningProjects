"""IntentClassifier — classifies user intent using the LLM port."""
from __future__ import annotations
import json

from src.domain.ports.llm_port import ILLMService
from src.domain.value_objects.intent import Intent

_SYSTEM_PROMPT = """You are an intent classifier for an IT helpdesk assistant.
Analyse the user message and return a JSON object with:
  - "intent": one of kb_lookup | ticket_create | ticket_status | ticket_update | escalation | multi_intent | unknown
  - "sub_intents": list of intents when intent is multi_intent (e.g. ["kb_lookup","ticket_status"])
  - "kb_query": extracted knowledge search query (when kb_lookup is present)
  - "ticket_id": extracted ticket ID if mentioned (e.g. "TKT-0042")
  - "doc_versions": list of doc versions to compare (e.g. ["v1_2025","v1_2026"]) or null

Return ONLY valid JSON. No explanation."""


class IntentClassifier:
    def __init__(self, llm: ILLMService) -> None:
        self._llm = llm

    def classify(self, message: str, history: list[dict] | None = None) -> dict:
        """
        Classify the user message into an Intent with supporting metadata.

        Returns a dict with keys: intent, sub_intents, kb_query, ticket_id, doc_versions.
        """
        messages = [{"role": "system", "content": _SYSTEM_PROMPT}]
        if history:
            messages.extend(history[-6:])  # last 3 turns for context
        messages.append({"role": "user", "content": message})

        raw = self._llm.complete(messages)
        try:
            data = json.loads(raw)
        except (json.JSONDecodeError, ValueError):
            data = {"intent": Intent.UNKNOWN.value, "sub_intents": []}

        # Normalise intent to enum, fall back to UNKNOWN
        intent_str = data.get("intent", Intent.UNKNOWN.value)
        try:
            data["intent"] = Intent(intent_str)
        except ValueError:
            data["intent"] = Intent.UNKNOWN

        return data
