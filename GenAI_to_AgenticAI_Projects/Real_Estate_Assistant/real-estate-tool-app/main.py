import streamlit as st
# streamlit run  .\Real_Estate_Assistant\real-estate-tool-app\main.py
st.set_page_config(page_title="Real Estate Assistant", page_icon="🏠", layout="wide")

URL_PROCESSING_STEPS = 8


def format_progress_message(status_message: str) -> str:
    """Remove the internal log prefix before displaying a progress step."""
    return status_message.removeprefix("[INFO] ")


def answer_progress(status_message: str) -> int:
    """Map answer-generation milestones to stable progress percentages."""
    milestones = {
        "Generating answer": 10,
        "Creating Groq LLM": 25,
        "Retrieving relevant documents": 40,
        "Building prompt": 60,
        "Answer generation complete": 90,
        "Source URLs": 100,
    }
    return next(
        (
            percent
            for milestone, percent in milestones.items()
            if milestone in status_message
        ),
        5,
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Real Estate Assistant")
st.caption("Ask questions about the web pages you add to the knowledge base.")

with st.sidebar:
    st.header("Knowledge Base")
    url_1 = st.text_input("URL 1", key="url_1")
    url_2 = st.text_input("URL 2", key="url_2")
    url_3 = st.text_input("URL 3", key="url_3")

    if st.button("Process URLs", width="stretch"):
        urls = [url for url in [url_1, url_2, url_3] if url]
        if not urls:
            st.warning("Enter at least one URL.")
        else:
            from rag import initialize_vector_store, process_urls

            with st.status("Processing sources...", expanded=True) as status:
                progress = st.progress(5, text="Loading the embedding model and vector store...")
                vector_store = initialize_vector_store()
                for step, message in enumerate(process_urls(urls, vector_store), start=1):
                    percent = min(10 + round(step / URL_PROCESSING_STEPS * 90), 100)
                    progress.progress(percent, text=format_progress_message(message))
                status.update(label="Sources ready", state="complete", expanded=False)
            st.success("URLs processed and stored.")

    if st.button("Clear conversation", width="stretch"):
        st.session_state.messages = []
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            st.caption(f"Sources: {', '.join(message['sources'])}")

if query := st.chat_input("Ask a question about your sources"):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        from rag import generate_answer, initialize_vector_store

        answer = ""
        sources: list[str] = []
        with st.status("Searching your sources...", expanded=True) as status:
            progress = st.progress(5, text="Loading the knowledge base...")
            vector_store = initialize_vector_store()
            for message in generate_answer(query=query, vector_store=vector_store):
                if message.startswith("[INFO]"):
                    progress.progress(
                        answer_progress(message),
                        text=format_progress_message(message),
                    )
                    if message.startswith("[INFO] Source URLs:"):
                        sources_text = message.removeprefix("[INFO] Source URLs: ")
                        sources = [source.strip(" '[]") for source in sources_text.split(",") if source.strip(" '[]")]
                else:
                    answer = message
            status.update(label="Answer ready", state="complete", expanded=False)

        st.markdown(answer)
        if sources:
            st.caption(f"Sources: {', '.join(sources)}")

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )
