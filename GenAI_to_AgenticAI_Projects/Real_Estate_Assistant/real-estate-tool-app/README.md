---
title: Real Estate Assistant
summary: Streamlit RAG chat application for asking questions about content loaded from web pages.
ms.date: 2026-08-20
ms.topic: overview
---

## Overview

Real Estate Assistant is a Streamlit retrieval-augmented generation (RAG)
application. Add web page URLs, index their text in ChromaDB, then ask questions
in a chat interface. Answers are generated with Groq and list the retrieved source
URLs.

## Features

* Process up to three URLs from the sidebar
* Split loaded content into chunks and store embeddings in ChromaDB
* Ask follow-up questions in a persistent chat conversation
* Show indexing and retrieval progress in the UI
* Display source URLs used for each response

## RAG Pipeline

The application separates RAG into an ingestion pipeline, which builds the
knowledge base, and a retrieval pipeline, which answers questions from that
knowledge base.

```text
Ingestion
URLs -> load pages -> LangChain Documents -> split into chunks
   -> create embeddings -> store vectors and metadata in ChromaDB

Retrieval
Question -> similarity search -> four relevant chunks -> build prompt
       -> Groq chat model -> parse text answer -> display source URLs
```

### Ingestion Pipeline

The `process_urls()` generator in `rag.py` runs ingestion when you select
**Process URLs**. It reports each stage to the Streamlit progress UI.

| Stage | Library and import | Class or method | Purpose and output |
| --- | --- | --- | --- |
| Reset collection | `langchain-chroma` | `Chroma.reset_collection()` | Removes the previous `real_estate_docs` collection contents before indexing the new URLs |
| Load web pages | `langchain-community` | `UnstructuredURLLoader` | Downloads each URL through the `unstructured` integration and returns LangChain `Document` objects containing page text and source metadata |
| Split text | `langchain-text-splitters` | `RecursiveCharacterTextSplitter` | Splits documents into 500-character chunks with 20-character overlap while preserving metadata |
| Create embeddings | `langchain-huggingface` and `sentence-transformers` | `HuggingFaceEmbeddings` | Converts each chunk into a vector with `sentence-transformers/all-MiniLM-L6-v2` |
| Generate IDs | Python standard library | `uuid.uuid4()` | Assigns a unique string ID to every document chunk |
| Index and persist | `langchain-chroma` and `chromadb` | `Chroma.add_documents()` | Stores chunk text, embedding vectors, IDs, and source metadata under `resources/vectorstore/` |

`initialize_vector_store()` creates the shared `Chroma` instance and its
`HuggingFaceEmbeddings` embedding function. Python's `functools.lru_cache`
reuses that instance during the Streamlit process.

### Retrieval And Answer Pipeline

The `generate_answer()` generator in `rag.py` runs this pipeline for each chat
question.

| Stage | Library and import | Class or method | Purpose and output |
| --- | --- | --- | --- |
| Initialize the model | `langchain-groq` | `ChatGroq` | Creates a deterministic Groq chat client for `openai/gpt-oss-20b` with temperature `0.0` and a 512-token limit |
| Create the retriever | `langchain-chroma` | `Chroma.as_retriever()` | Wraps Chroma as a LangChain vector-store retriever with `k=4` |
| Retrieve context | `langchain-core` retriever interface | `retriever.invoke()` | Embeds the question, performs similarity search, and returns the four closest `Document` chunks |
| Collect citations | LangChain `Document` metadata | `Document.metadata.get()` | Reads each retrieved document's `source` URL and removes duplicate URLs |
| Build the prompt | `langchain-core` | `PromptTemplate.from_template()` | Inserts the retrieved chunk text into `{context}` and the user input into `{question}` |
| Compose the chain | LangChain Expression Language (LCEL) | `Runnable` pipe operator (`\|`) | Connects context construction, prompt formatting, the Groq model, and output parsing |
| Generate the answer | `langchain-groq` | `ChatGroq.invoke()` through LCEL | Sends the grounded prompt to Groq and returns the model response |
| Parse output | `langchain-core` | `StrOutputParser` | Converts the chat response into the final answer string shown by Streamlit |

The source URLs come from metadata attached during URL loading. They identify
the pages represented by the retrieved chunks, while the generated answer is
based on the concatenated text of those chunks.

### Supporting Libraries

| Library | Role |
| --- | --- |
| `streamlit` | Provides URL inputs, progress indicators, chat history, and answer rendering |
| `python-dotenv` | Loads `GROQ_API_KEY` from the repository `.env` file with `load_dotenv()` |
| `pathlib` | Builds the platform-independent path to the persisted vector store |

## Prerequisites

* Python 3.11 or later
* A Groq API key

Install the repository dependencies from the project root:

```powershell
.\.venv-x64\Scripts\python.exe -m pip install -r requirements.txt
```

Create a `.env` file in the repository root with your Groq API key:

```text
GROQ_API_KEY=your_groq_api_key
```

The application currently uses `openai/gpt-oss-20b`, configured by
`GROQ_MODEL` in `rag.py`. The model must be available to the configured Groq
account.

## Run The App

From the repository root, start Streamlit:

```powershell
.\.venv-x64\Scripts\streamlit.exe run .\Real_Estate_Assistant\real-estate-tool-app\main.py
```

Streamlit prints the local URL in the terminal, normally
`http://localhost:8501`.

## Use The Chat

1. Enter one or more source URLs in the sidebar.
2. Select **Process URLs** and wait until the status displays `Sources ready`.
3. Enter a question in the chat input.
4. Review the generated answer and its source URLs.
5. Use **Clear conversation** to remove the local chat history. The indexed
   ChromaDB documents remain available until the next URL processing run resets
   the collection.

## Project Files

| File | Purpose |
| --- | --- |
| `main.py` | Streamlit chat interface and URL processing controls |
| `rag.py` | URL loading, chunking, ChromaDB indexing, and Groq retrieval chain |
| `resources/vectorstore/` | Persisted ChromaDB collection |

## Troubleshooting

If Groq returns a `model_not_found` error, query the models available to your
API key and update `GROQ_MODEL` in `rag.py` to an accessible chat model. Confirm
that `GROQ_API_KEY` is set and restart Streamlit after changing `.env`.
