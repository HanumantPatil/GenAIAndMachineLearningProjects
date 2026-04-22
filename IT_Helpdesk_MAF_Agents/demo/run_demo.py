"""
demo/run_demo.py — Interactive CLI demo for the IT Helpdesk AI Assistant.

Usage:
    python demo/run_demo.py

Requires all env vars from .env to be set (Azure connections).
"""
from __future__ import annotations
import uuid
import sys
import os

# Ensure UTF-8 output on all platforms (Windows CP1252 compatibility)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.infrastructure.api.dependencies import get_process_chat_use_case
from src.application.dto.chat_request_dto import ChatRequestDTO
from src.domain.value_objects.user_role import UserRole

BANNER = """
╔══════════════════════════════════════════════════════╗
║          IT Helpdesk AI Assistant — Demo             ║
║  Type 'quit' to exit. Type 'role' to switch role.   ║
╚══════════════════════════════════════════════════════╝
"""

SAMPLE_QUERIES = [
    "How do I connect to the company VPN?",
    "My laptop screen went black and won't turn on. Please create a ticket.",
    "What is the password policy?",
    "Check my latest ticket status",
    "I need to speak with a human specialist",
]


def run_demo() -> None:
    print(BANNER)
    print("Sample queries you can try:")
    for i, q in enumerate(SAMPLE_QUERIES, 1):
        print(f"  {i}. {q}")
    print()

    use_case = get_process_chat_use_case()
    session_id = str(uuid.uuid4())
    user_id = "demo-user-001"
    user_role = UserRole.EMPLOYEE

    print(f"Session: {session_id}")
    print(f"User:    {user_id}  |  Role: {user_role.value}\n")

    while True:
        try:
            user_input = input("You> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() == "quit":
            print("Goodbye!")
            break
        if user_input.lower() == "role":
            new_role = input("Enter role (employee / it_admin): ").strip()
            try:
                user_role = UserRole(new_role)
                print(f"Role changed to: {user_role.value}\n")
            except ValueError:
                print("Invalid role. Keeping current role.\n")
            continue

        dto = ChatRequestDTO(
            session_id=session_id,
            user_id=user_id,
            user_role=user_role,
            message=user_input,
        )

        try:
            result = use_case.execute(dto)
        except Exception as exc:
            print(f"[ERROR] {exc}\n")
            continue

        print(f"\nAssistant> {result.response}")

        if result.ticket_id:
            print(f"  [Ticket] {result.ticket_id}")
        if result.escalation_case:
            print(f"  [Escalation] {result.escalation_case}")
        if result.confidence_score is not None:
            print(f"  [Confidence] {result.confidence_score:.2f}")
        if result.sources:
            print("  [Sources]")
            for s in result.sources:
                print(f"    - {s.get('source_file')} p.{s.get('page_number')} ({s.get('doc_version')})")
        print()


if __name__ == "__main__":
    run_demo()
