"""ConfidenceScore value object — wraps a float with threshold business logic."""
from __future__ import annotations

ESCALATION_THRESHOLD = 0.6


class ConfidenceScore:
    """Immutable float wrapper that encodes KB confidence threshold logic."""

    ESCALATION_THRESHOLD: float = ESCALATION_THRESHOLD  # expose as class attribute

    def __init__(self, value: float) -> None:
        if not (0.0 <= value <= 1.0):
            raise ValueError(f"ConfidenceScore must be in [0, 1], got {value}")
        self._value = value

    @property
    def value(self) -> float:
        return self._value

    def is_low_confidence(self) -> bool:
        """Returns True when confidence is below the escalation threshold (< 0.6)."""
        return self._value < ESCALATION_THRESHOLD

    def __float__(self) -> float:
        return self._value

    def __repr__(self) -> str:
        return f"ConfidenceScore({self._value:.3f})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ConfidenceScore):
            return self._value == other._value
        return NotImplemented

    def __lt__(self, other: "ConfidenceScore") -> bool:
        return self._value < other._value
