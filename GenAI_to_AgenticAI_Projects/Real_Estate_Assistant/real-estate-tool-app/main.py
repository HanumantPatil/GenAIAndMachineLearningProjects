import streamlit as st
# streamlit run  .\Real_Estate_Assistant\real-estate-tool-app\main.py
st.title("Real Estate Assistant Tool")


url_1 = st.sidebar.text_input("URL 1", key="url_1")
url_2 = st.sidebar.text_input("URL 2", key="url_2")
url_3 = st.sidebar.text_input("URL 3", key="url_3")

process_url_button = st.sidebar.button("Process URLs")

if process_url_button:
    urls = [url for url in [url_1, url_2, url_3] if url]
    if not urls:
        st.warning("Please enter at least one URL.")
    else:
        from rag import initialize_vector_store, process_urls

        vector_store = initialize_vector_store()

        for msg in process_urls(urls, vector_store):
            st.info(msg)
        st.success("URLs processed and documents stored in the vector store.")

query = st.text_input("Enter your query:")
ask_button = st.button("Ask")

if ask_button:
    if not query:
        st.warning("Please enter a query.")
    else:
        from rag import initialize_vector_store, generate_answer

        vector_store = initialize_vector_store()
        for msg in generate_answer(query=query, vector_store=vector_store):
            st.info(msg)
