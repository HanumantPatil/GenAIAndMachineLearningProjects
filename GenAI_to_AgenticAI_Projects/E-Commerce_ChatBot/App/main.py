import streamlit as st
from router import router
from faq import faq_chain, ingest_faq_data
from pathlib import Path

PATH = Path(__file__).parent
faq_path = PATH / "Resources/faq_data.csv"
ingest_faq_data(faq_path)

st.title("E-Commerce ChatBot")

def ask(query):
    route_choice = router(query)
    assert not isinstance(route_choice, list)
    route = route_choice.name
    print(f"Routing user input: {query}")
    print(f"Determined route: {route}")
    if route == "faq":
        return faq_chain(query)
    elif route == "sql":
        from sql import sql_chain
        return sql_chain(query)
    if route is None:
        return "I couldn't determine how to handle that question."
    return f"this route '{route}' is not handled."

user_input = st.chat_input("Type your message here...")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.setdefault("messages", [])

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)
    response = ask(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)


# python -m streamlit run .\E-Commerce_ChatBot\App\main.py