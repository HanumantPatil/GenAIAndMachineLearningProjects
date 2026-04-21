"""ILLMService port — abstract interface for language model completions."""
from abc import ABC, abstractmethod


class ILLMService(ABC):
    @abstractmethod
    def complete(self, messages: list[dict]) -> str:
        """
        Call the LLM with a list of OpenAI-format messages.

        Args:
            messages: List of {"role": ..., "content": ...} dicts.

        Returns:
            The assistant's response text.
        """
        ...
