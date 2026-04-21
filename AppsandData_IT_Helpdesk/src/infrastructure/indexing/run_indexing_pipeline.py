"""run_indexing_pipeline.py -- CLI script to index documents into Azure AI Search."""
from __future__ import annotations
import argparse
import logging
from pathlib import Path

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient

from src.infrastructure.config.settings import get_settings
from src.infrastructure.indexing.chunker import chunk_text
from src.infrastructure.indexing.embedder import Embedder
from src.infrastructure.indexing.index_schema import build_index_schema

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def _extract_text(file_path: Path) -> str:
    """Extract plain text from .txt, .pdf, or .docx files."""
    suffix = file_path.suffix.lower()
    if suffix == ".txt":
        return file_path.read_text(encoding="utf-8", errors="ignore")
    if suffix == ".pdf":
        import pdfplumber
        pages = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pages.append(text)
        return "\n".join(pages)
    if suffix in (".docx", ".doc"):
        import docx as _docx
        doc = _docx.Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    return ""


def ensure_index(index_client: SearchIndexClient) -> None:
    schema = build_index_schema()
    try:
        index_client.create_or_update_index(schema)
        logger.info("Index '%s' created/updated.", schema.name)
    except Exception as exc:
        logger.error("Failed to create index: %s", exc)
        raise


def index_directory(
    data_dir: Path,
    doc_version: str,
    access_role: str,
    search_client: SearchClient,
    embedder: Embedder,
) -> None:
    supported = {".txt", ".pdf", ".docx", ".doc"}
    files = [f for f in data_dir.rglob("*") if f.suffix.lower() in supported]
    if not files:
        logger.warning("No supported documents found in %s", data_dir)
        return
    total_chunks = 0
    for doc_file in sorted(files):
        text = _extract_text(doc_file)
        if not text.strip():
            logger.warning("Skipping %s -- no text extracted.", doc_file.name)
            continue
        chunks = chunk_text(
            text=text,
            source_file=doc_file.name,
            doc_version=doc_version,
            access_role=access_role,
        )
        chunks = embedder.embed_documents(chunks)
        # Upload in batches of 100
        for i in range(0, len(chunks), 100):
            search_client.upload_documents(chunks[i : i + 100])
        total_chunks += len(chunks)
        logger.info("Indexed %s (%d chunks).", doc_file.name, len(chunks))
    logger.info("Total chunks indexed: %d", total_chunks)


def main() -> None:
    parser = argparse.ArgumentParser(description="Index IT documents into Azure AI Search.")
    parser.add_argument("--data-dir", default="data/raw", help="Directory containing documents (.txt/.pdf/.docx).")
    parser.add_argument("--doc-version", default="v1.0", help="Document version tag.")
    parser.add_argument("--access-role", default="public", help="RBAC access role.")
    args = parser.parse_args()

    settings = get_settings()
    credential = AzureKeyCredential(settings.azure_search_api_key)

    index_client = SearchIndexClient(settings.azure_search_endpoint, credential)
    ensure_index(index_client)

    embedder = Embedder(
        endpoint=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_api_key,
        deployment=settings.azure_openai_embedding_deployment,
    )
    search_client = SearchClient(
        settings.azure_search_endpoint,
        settings.azure_search_index,
        credential,
    )

    index_directory(Path(args.data_dir), args.doc_version, args.access_role, search_client, embedder)
    logger.info("Indexing complete.")


if __name__ == "__main__":
    main()




