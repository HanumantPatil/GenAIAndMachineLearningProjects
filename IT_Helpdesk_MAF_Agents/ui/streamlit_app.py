"""
ui/streamlit_app.py — Streamlit front-end for the IT Helpdesk AI Assistant.

Run (from project root):
    streamlit run ui/streamlit_app.py

Requires the FastAPI server to be running:
    python -m uvicorn src.infrastructure.api.main:app --host 0.0.0.0 --port 8000 --reload
"""
from __future__ import annotations

import uuid
import time
import requests
import streamlit as st

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IT Helpdesk AI Assistant",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Constants ──────────────────────────────────────────────────────────────
API_BASE = "http://localhost:8000/api/v1"

SAMPLE_QUERIES = [
    "How do I connect to the company VPN?",
    "What is the password reset procedure?",
    "My laptop screen went black and won't turn on. Please create a support ticket.",
    "I need to speak with a human IT specialist.",
    "What software is approved for installation?",
    "How do I set up multi-factor authentication?",
    "My email is not syncing. Create a ticket for me.",
]

ROLE_OPTIONS = {"Employee": "employee", "IT Admin": "it_admin"}

INTENT_LABELS = {
    "ticket": "🎫 Ticket",
    "escalation": "🚨 Escalation",
    "kb_query": "📚 Knowledge Base",
    "unknown": "❓ General",
}

# ─── Session state initialisation ───────────────────────────────────────────
def _init_state() -> None:
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "messages" not in st.session_state:
        st.session_state.messages = []  # list[dict]
    if "user_id" not in st.session_state:
        st.session_state.user_id = "streamlit-user-001"
    if "user_role" not in st.session_state:
        st.session_state.user_role = "employee"
    if "pending_query" not in st.session_state:
        st.session_state.pending_query = None


_init_state()


# ─── API helpers ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=10)
def _check_api_health() -> bool:
    try:
        r = requests.get(f"{API_BASE}/health", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


def _send_message(message: str) -> dict | None:
    payload = {
        "session_id": st.session_state.session_id,
        "user_id": st.session_state.user_id,
        "user_role": st.session_state.user_role,
        "message": message,
    }
    try:
        r = requests.post(f"{API_BASE}/chat", json=payload, timeout=60)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot reach the API server at `http://localhost:8000`. "
            "Start it with:\n```\npython -m uvicorn src.infrastructure.api.main:app "
            "--host 0.0.0.0 --port 8000 --reload\n```"
        )
        return None
    except requests.exceptions.Timeout:
        st.error("Request timed out (>60 s). The server may be overloaded.")
        return None
    except requests.exceptions.HTTPError as exc:
        st.error(f"API error {exc.response.status_code}: {exc.response.text}")
        return None
    except Exception as exc:
        st.error(f"Unexpected error: {exc}")
        return None


# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Settings")

    # API status
    healthy = _check_api_health()
    if healthy:
        st.success("🟢 API server online", icon="✅")
    else:
        st.error("🔴 API server offline", icon="⚠️")
        st.caption("Start the FastAPI server before chatting.")

    st.divider()

    # User settings
    st.subheader("👤 User")
    new_uid = st.text_input("User ID", value=st.session_state.user_id)
    if new_uid != st.session_state.user_id:
        st.session_state.user_id = new_uid

    role_label = st.selectbox(
        "Role",
        list(ROLE_OPTIONS.keys()),
        index=0 if st.session_state.user_role == "employee" else 1,
    )
    st.session_state.user_role = ROLE_OPTIONS[role_label]

    st.divider()

    # Session management
    st.subheader("🔑 Session")
    st.code(st.session_state.session_id, language=None)
    if st.button("🔄 New Session", use_container_width=True):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

    st.divider()

    # Quick-fire sample queries
    st.subheader("💡 Sample Queries")
    for q in SAMPLE_QUERIES:
        if st.button(q, use_container_width=True, key=f"sample_{hash(q)}"):
            st.session_state.pending_query = q
            st.rerun()

    st.divider()
    st.caption("IT Helpdesk AI Assistant · v1.0")


# ─── Main layout ─────────────────────────────────────────────────────────────
st.title("🛠️ IT Helpdesk AI Assistant")
st.caption(
    f"Session `{st.session_state.session_id[:8]}…`  |  "
    f"User `{st.session_state.user_id}`  |  "
    f"Role `{st.session_state.user_role}`"
)

# Metrics row (computed from history)
ticket_count = sum(1 for m in st.session_state.messages if m.get("ticket_id"))
escalation_count = sum(1 for m in st.session_state.messages if m.get("escalation_case"))
kb_count = sum(
    1 for m in st.session_state.messages
    if m.get("role") == "assistant" and m.get("sources")
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Messages", len([m for m in st.session_state.messages if m["role"] == "user"]))
col2.metric("KB Answers", kb_count)
col3.metric("Tickets", ticket_count)
col4.metric("Escalations", escalation_count)

st.divider()

# ─── Chat history ─────────────────────────────────────────────────────────────
chat_container = st.container()

with chat_container:
    if not st.session_state.messages:
        st.info(
            "👋 Welcome! Ask me anything about IT support — VPN setup, password resets, "
            "ticket creation, or anything else. Use the sample queries in the sidebar to get started.",
            icon="💬",
        )

    for msg in st.session_state.messages:
        role = msg["role"]

        if role == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(msg["content"])

        elif role == "assistant":
            with st.chat_message("assistant", avatar="🛠️"):
                st.markdown(msg["content"])

                # ── Metadata expander ──────────────────────────────────────
                meta_parts = []
                if msg.get("confidence_score") is not None:
                    score = msg["confidence_score"]
                    bar = "🟢" if score >= 0.7 else ("🟡" if score >= 0.4 else "🔴")
                    meta_parts.append(f"{bar} Confidence: **{score:.0%}**")
                if msg.get("ticket_id"):
                    meta_parts.append(f"🎫 Ticket: `{msg['ticket_id']}`")
                if msg.get("escalation_case"):
                    meta_parts.append(f"🚨 Escalation: `{msg['escalation_case']}`")

                if meta_parts:
                    st.markdown("  \n".join(meta_parts))

                if msg.get("sources"):
                    with st.expander(f"📚 Sources ({len(msg['sources'])})"):
                        for s in msg["sources"]:
                            fname = s.get("source_file", "—")
                            page = s.get("page_number", "—")
                            ver = s.get("doc_version", "—")
                            score_s = s.get("score")
                            score_str = f"  _(score: {score_s:.2f})_" if score_s else ""
                            st.markdown(f"- **{fname}** · page {page} · {ver}{score_str}")

        elif role == "error":
            with st.chat_message("assistant", avatar="⚠️"):
                st.error(msg["content"])


# ─── Chat input ───────────────────────────────────────────────────────────────
# Use pending_query from sidebar buttons, or the chat_input box
user_input: str | None = st.chat_input(
    "Ask a question or describe your IT issue…",
    disabled=not healthy,
)

# Sidebar sample query takes priority
if st.session_state.pending_query:
    user_input = st.session_state.pending_query
    st.session_state.pending_query = None


def _process_input(text: str) -> None:
    """Append user message, call API, append assistant response."""
    text = text.strip()
    if not text:
        return

    # Append user turn
    st.session_state.messages.append({"role": "user", "content": text})

    # Call API with spinner
    with st.spinner("Thinking…"):
        data = _send_message(text)

    if data is None:
        st.session_state.messages.append(
            {"role": "error", "content": "Failed to reach the API. See error above."}
        )
        return

    # Append assistant turn
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": data.get("response", ""),
            "sources": data.get("sources") or [],
            "ticket_id": data.get("ticket_id"),
            "escalation_case": data.get("escalation_case"),
            "confidence_score": data.get("confidence_score"),
        }
    )


if user_input:
    _process_input(user_input)
    st.rerun()
