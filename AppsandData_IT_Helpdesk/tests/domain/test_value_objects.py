"""Tests for all domain value objects."""
import pytest
from src.domain.value_objects.confidence_score import ConfidenceScore
from src.domain.value_objects.intent import Intent
from src.domain.value_objects.ticket_status import TicketStatus
from src.domain.value_objects.user_role import UserRole


class TestConfidenceScore:
    def test_valid_boundary_zero(self):
        cs = ConfidenceScore(0.0)
        assert float(cs) == 0.0

    def test_valid_boundary_one(self):
        cs = ConfidenceScore(1.0)
        assert float(cs) == 1.0

    def test_mid_value(self):
        cs = ConfidenceScore(0.75)
        assert float(cs) == 0.75

    def test_is_low_confidence_below_threshold(self):
        assert ConfidenceScore(0.55).is_low_confidence() is True

    def test_is_low_confidence_at_threshold(self):
        assert ConfidenceScore(0.6).is_low_confidence() is False

    def test_is_low_confidence_above_threshold(self):
        assert ConfidenceScore(0.8).is_low_confidence() is False

    def test_invalid_below_zero(self):
        with pytest.raises(ValueError):
            ConfidenceScore(-0.1)

    def test_invalid_above_one(self):
        with pytest.raises(ValueError):
            ConfidenceScore(1.1)

    def test_escalation_threshold_constant(self):
        assert ConfidenceScore.ESCALATION_THRESHOLD == 0.6

    def test_repr(self):
        cs = ConfidenceScore(0.75)
        assert repr(cs) == "ConfidenceScore(0.750)"

    def test_eq_same_value(self):
        assert ConfidenceScore(0.5) == ConfidenceScore(0.5)

    def test_eq_different_type_returns_not_implemented(self):
        cs = ConfidenceScore(0.5)
        assert cs.__eq__(0.5) is NotImplemented

    def test_lt_ordering(self):
        assert ConfidenceScore(0.3) < ConfidenceScore(0.7)


class TestTicketStatus:
    def test_values(self):
        assert TicketStatus.OPEN.value == "open"
        assert TicketStatus.IN_PROGRESS.value == "in_progress"
        assert TicketStatus.RESOLVED.value == "resolved"
        assert TicketStatus.CLOSED.value == "closed"

    def test_valid_transitions_from_open(self):
        assert TicketStatus.OPEN.can_transition_to(TicketStatus.IN_PROGRESS) is True
        assert TicketStatus.OPEN.can_transition_to(TicketStatus.CLOSED) is True

    def test_invalid_transition_open_to_resolved(self):
        assert TicketStatus.OPEN.can_transition_to(TicketStatus.RESOLVED) is False

    def test_valid_transition_in_progress_to_resolved(self):
        assert TicketStatus.IN_PROGRESS.can_transition_to(TicketStatus.RESOLVED) is True

    def test_closed_has_no_transitions(self):
        for s in TicketStatus:
            assert TicketStatus.CLOSED.can_transition_to(s) is False


class TestUserRole:
    def test_values(self):
        assert UserRole.EMPLOYEE.value == "employee"
        assert UserRole.IT_ADMIN.value == "it_admin"


class TestIntent:
    def test_all_intents_accessible(self):
        intents = [
            Intent.KB_LOOKUP, Intent.TICKET_CREATE, Intent.TICKET_STATUS,
            Intent.TICKET_UPDATE, Intent.ESCALATION, Intent.MULTI_INTENT, Intent.UNKNOWN,
        ]
        assert len(intents) == 7
