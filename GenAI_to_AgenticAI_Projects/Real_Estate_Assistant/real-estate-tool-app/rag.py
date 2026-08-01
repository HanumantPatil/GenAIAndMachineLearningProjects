import os

os.environ["USER_AGENT"] = "RealEstateRAG/1.0 (contact: your-email@example.com)"

from uuid import uuid4

from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_chroma import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

CHUNK_SIZE = 500
CHUNK_OVERLAP = 20
VECTORSTORE_DIR = Path(__file__).parent / "resources/vectorstore"
COLLECTION_NAME = "real_estate_docs"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def initialize_vector_store() -> Chroma:
    """Initialize the vector store for the application."""
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=str(VECTORSTORE_DIR),
        embedding_function=embeddings,
    )


def process_urls(urls: list[str], vector_store: Chroma):
    """Process a list of URLs."""
    print(f"Initialized components for URLs: {urls}")
    vector_store.reset_collection()
    print(f"Processing URLs: {urls}")
    loader = UnstructuredURLLoader(urls=urls)
    documents = loader.load()
    print(f"Loaded {len(documents)} documents from URLs: {urls}")
    print(f"Splitting documents into chunks of size {CHUNK_SIZE} with overlap {CHUNK_OVERLAP}")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    docs = text_splitter.split_documents(documents)
    print(f"Split documents into {len(docs)} chunks.")
    print(f"Adding documents to vector store: {VECTORSTORE_DIR}")
    vector_store.add_documents(docs, ids=[str(uuid4()) for _ in docs])

    return docs


if __name__ == "__main__":
    source_urls = [
        "https://en.wikipedia.org/wiki/Retrieval-augmented_generation",
        "https://en.wikipedia.org/wiki/Vector_database",
    ]

    store = initialize_vector_store()
    process_urls(source_urls, store)
    results = store.similarity_search(
        "What is Retrieval-augmented generation?",
        k=2,
    )
    print("Results:")
    for result in results:
        print(result)
