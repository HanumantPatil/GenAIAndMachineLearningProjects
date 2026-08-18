import os

USER_AGENT = (
    "RealEstateRAG/1.0 "
    "(https://github.com/HanumantPatil/GenAIAndMachineLearningProjects)"
)
os.environ["USER_AGENT"] = USER_AGENT

from functools import lru_cache
from uuid import uuid4


from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_chroma import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

load_dotenv()
#### python .\Real_Estate_Assistant\real-estate-tool-app\rag.py
CHUNK_SIZE = 500
CHUNK_OVERLAP = 20
VECTORSTORE_DIR = Path(__file__).parent / "resources/vectorstore"
COLLECTION_NAME = "real_estate_docs"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
GROQ_MODEL = "openai/gpt-oss-20b"
#EMBEDDING_MODEL = "Alibaba-NLP/gte-base-en-v1.5"


@lru_cache(maxsize=1)
def initialize_vector_store() -> Chroma:
    """Initialize and reuse the application's vector store."""
    print("[INFO] Initializing embedding model and vector store...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    # model_kwargs={"trust_remote_code": True}

    print("[INFO] Creating Groq LLM client...")
    ChatGroq(
        model=GROQ_MODEL,
        temperature=0.0,
        max_tokens=512,
        api_key=os.getenv("GROQ_API_KEY"),
    )
    store = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=str(VECTORSTORE_DIR),
        embedding_function=embeddings,
    )
    print(f"[INFO] Vector store ready at: {VECTORSTORE_DIR}")
    return store


def process_urls(urls: list[str], vector_store: Chroma):
    """Process a list of URLs."""

    yield f"[INFO] Starting URL processing for: {urls}"
    yield "[INFO] Resetting vector store collection..."
    vector_store.reset_collection()

    yield f"[INFO] Loading documents from {len(urls)} URL(s)..."
    loader = UnstructuredURLLoader(
        urls=urls,
        headers={"User-Agent": USER_AGENT},
    )
    documents = loader.load()
    yield f"[INFO] Loaded {len(documents)} documents."

    yield f"[INFO] Splitting documents into chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})..."
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    docs = text_splitter.split_documents(documents)
    yield f"[INFO] Created {len(docs)} document chunks."
    yield f"[INFO] Adding chunks to vector store at {VECTORSTORE_DIR}..."
    vector_store.add_documents(docs, ids=[str(uuid4()) for _ in docs])
    yield "[INFO] Document indexing complete."

    return docs

def generate_answer(query: str = "What is Retrieval-augmented generation?",
                    llm=None,
                    vector_store: Chroma = None):
    """Generate an answer to a query using the vector store."""
    yield f"[INFO] Generating answer for query: {query}"

    if llm is None:
        yield "[INFO] Creating Groq LLM for answer generation..."
        llm = ChatGroq(
            model=GROQ_MODEL,
            temperature=0.0,
            max_tokens=512,
            api_key=os.getenv("GROQ_API_KEY"),
        )

    if vector_store is None:
        yield "[INFO] No vector store provided; initializing default store..."
        vector_store = initialize_vector_store()

    yield "[INFO] Retrieving relevant documents from vector store..."
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    prompt = PromptTemplate.from_template(
        """Use the context below to answer the user question.

Context:
{context}

Question:
{question}

Answer concisely and include relevant source details when possible.
"""
    )
    retrieved_sources: list[str] = []

    def build_context(question: str) -> str:
        docs = retriever.invoke(question)
        retrieved_sources.extend(
            source
            for doc in docs
            if (source := doc.metadata.get("source")) and source not in retrieved_sources
        )
        print(f"[INFO] Retrieved {len(docs)} matching document chunks.")
        return "\n\n".join(doc.page_content for doc in docs)

    yield "[INFO] Building prompt and invoking LLM..."
    chain = (
        {
            "context": lambda q: build_context(q),
            "question": lambda q: q,
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    answer = chain.invoke(query)
    yield "[INFO] Answer generation complete."
    yield answer
    yield f"[INFO] Source URLs: {retrieved_sources}"

if __name__ == "__main__":
    print("[INFO] Starting RAG pipeline...")
    source_urls = [
        "https://en.wikipedia.org/wiki/Retrieval-augmented_generation",
        "https://en.wikipedia.org/wiki/Vector_database",
    ]

    print("[INFO] Initializing vector store...")
    store = initialize_vector_store()
    print("[INFO] Processing source URLs...")
    process_urls(source_urls, store)
    # results = store.similarity_search(
    #     "What is Retrieval-augmented generation?",
    #     k=2,
    # )
    # print("Results:")
    # for result in results:
    #     print(result)

    print("[INFO] Requesting final answer...")
    for msg in generate_answer(query="What is Retrieval-augmented generation?", vector_store=store):
        print(msg)
