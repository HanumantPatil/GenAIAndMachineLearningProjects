import pandas as pd
from pathlib import Path
from groq import Groq
import chromadb
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_Model = "openai/gpt-oss-120b"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PATH = Path(__file__).parent
faq_path = PATH / "Resources/faq_data.csv"
chromadb_client = chromadb.Client()
collection_name_faq = "faqs"
ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
groq_client = Groq(api_key=GROQ_API_KEY)


def faq_chain(query):
    results = get_relevant_faqs(query)
    context = "".join([r.get("answer", "") for r in results["metadatas"][0]])  # type: ignore
    return generate_prompt(query, context)


def generate_prompt(query, context):
    prompt = f"""Given the question and context below, generate the answer based on the context only.
     if you don't know the answer, just say "I don't know". Don't try to make up an answer.
        QUESTION: {query}
        CONTEXT: {context}
     """
    # Call the LLM
    completion = groq_client.chat.completions.create(
        model=GROQ_Model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_completion_tokens=2048       
    )

    result = completion.choices[0].message.content  

    return result


def ingest_faq_data(faq_path):
    print(
        f"Starting ingestion of FAQ data from '{faq_path}' to Chromadb collection '{collection_name_faq}'."
    )
    if collection_name_faq not in [
        collection.name for collection in chromadb_client.list_collections()
    ]:
        collection = chromadb_client.get_or_create_collection(
            name=collection_name_faq, embedding_function=ef  # type: ignore
        )
        faq_data = pd.read_csv(faq_path)
        # Add your code to ingest the FAQ data to Chromadb here
        docs = faq_data["question"].tolist()

        _metadatas = [{"answer": answer} for answer in faq_data["answer"].tolist()]

        ids = [str(f"id_{i}") for i in range(len(docs))]
        collection.add(documents=docs, metadatas=_metadatas, ids=ids)
        print(f"Successfully ingested FAQ data to collection '{collection_name_faq}'.")
    else:
        print(f"Collection '{collection_name_faq}' already exists. Skipping ingestion.")


def get_relevant_faqs(query, top_k=2):
    collection = chromadb_client.get_collection(name=collection_name_faq)
    results = collection.query(query_texts=[query], n_results=top_k)
    return results


if __name__ == "__main__":
    # Ingest the FAQ data to Chromadb
    ingest_faq_data(faq_path)
    query = "How can I track my order?"
    # relevant_faqs = get_relevant_faqs(query)
    # print(f"Relevant FAQs for query '{query}':")
    # for i, (question, answer) in enumerate(zip(relevant_faqs['documents'][0], relevant_faqs['metadatas'][0])):
    #     print(f"{i + 1}. Question: {question}")
    #     print(f"   Answer: {answer['answer']}")

    print(f"Prompt for query '{query}':")
    print(faq_chain(query))
# python .\E-Commerce_ChatBot\App\faq.py
