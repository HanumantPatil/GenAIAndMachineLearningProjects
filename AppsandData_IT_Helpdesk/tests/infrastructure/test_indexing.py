"""Tests for indexing pipeline components."""
import os
import tempfile
import pytest
from unittest.mock import MagicMock, patch, call
from src.infrastructure.indexing.chunker import chunk_text
from src.infrastructure.indexing.embedder import Embedder


class TestChunker:
    def test_produces_at_least_one_chunk(self):
        chunks = chunk_text("hello world", "doc.txt", "v1")
        assert len(chunks) >= 1

    def test_chunk_has_required_fields(self):
        chunks = chunk_text("some text content", "f.txt", "v2")
        c = chunks[0]
        assert "id" in c
        assert "content" in c
        assert c["source_file"] == "f.txt"
        assert c["doc_version"] == "v2"

    def test_overlap_produces_multiple_chunks(self):
        words = " ".join([f"word{i}" for i in range(600)])
        chunks = chunk_text(words, "long.txt", "v1", chunk_size=100, overlap=20)
        assert len(chunks) >= 2

    def test_access_role_default_public(self):
        chunks = chunk_text("text", "f.txt", "v1")
        assert chunks[0]["access_role"] == "public"

    def test_access_role_custom(self):
        chunks = chunk_text("text", "f.txt", "v1", access_role="it_admin")
        assert chunks[0]["access_role"] == "it_admin"

    def test_page_numbers_increment(self):
        words = " ".join([f"w{i}" for i in range(300)])
        chunks = chunk_text(words, "f.txt", "v1", chunk_size=50, overlap=0)
        pages = [c["page_number"] for c in chunks]
        assert pages == list(range(1, len(chunks) + 1))


class TestEmbedder:
    @patch("src.infrastructure.indexing.embedder.AzureOpenAI")
    def test_embed_documents_adds_vector(self, MockAzureOpenAI):
        mock_response = MagicMock()
        mock_response.data = [MagicMock(embedding=[0.1] * 3072)]
        MockAzureOpenAI.return_value.embeddings.create.return_value = mock_response
        embedder = Embedder("https://x", "key")
        docs = [{"content": "test text"}]
        result = embedder.embed_documents(docs)
        assert "content_vector" in result[0]
        assert len(result[0]["content_vector"]) == 3072

    @patch("src.infrastructure.indexing.embedder.AzureOpenAI")
    def test_embed_query_returns_list(self, MockAzureOpenAI):
        mock_response = MagicMock()
        mock_response.data = [MagicMock(embedding=[0.5] * 3072)]
        MockAzureOpenAI.return_value.embeddings.create.return_value = mock_response
        embedder = Embedder("https://x", "key")
        vec = embedder.embed_query("search query")
        assert len(vec) == 3072

    @patch("src.infrastructure.indexing.embedder.AzureOpenAI")
    def test_embed_documents_batches(self, MockAzureOpenAI):
        """Test batching when more than batch_size documents provided."""
        mock_resp = MagicMock()
        mock_resp.data = [MagicMock(embedding=[0.1] * 3072) for _ in range(16)]
        MockAzureOpenAI.return_value.embeddings.create.return_value = mock_resp
        embedder = Embedder("https://x", "key")
        docs = [{"content": f"doc {i}"} for i in range(20)]
        result = embedder.embed_documents(docs)
        assert len(result) == 20
        assert all("content_vector" in d for d in result)


class TestIndexSchema:
    def test_build_index_schema_returns_search_index(self):
        from src.infrastructure.indexing.index_schema import build_index_schema, INDEX_NAME
        from azure.search.documents.indexes.models import SearchIndex
        schema = build_index_schema()
        assert isinstance(schema, SearchIndex)
        assert schema.name == INDEX_NAME

    def test_build_index_schema_has_vector_field(self):
        from src.infrastructure.indexing.index_schema import build_index_schema
        schema = build_index_schema()
        field_names = [f.name for f in schema.fields]
        assert "content_vector" in field_names
        assert "content" in field_names
        assert "id" in field_names

    def test_build_index_schema_has_semantic_config(self):
        from src.infrastructure.indexing.index_schema import build_index_schema, SEMANTIC_CONFIG_NAME
        schema = build_index_schema()
        config_names = [c.name for c in schema.semantic_search.configurations]
        assert SEMANTIC_CONFIG_NAME in config_names


class TestIndexingPipeline:
    def test_ensure_index_calls_create_or_update(self):
        from src.infrastructure.indexing.run_indexing_pipeline import ensure_index
        index_client = MagicMock()
        ensure_index(index_client)
        index_client.create_or_update_index.assert_called_once()

    def test_ensure_index_raises_on_failure(self):
        from src.infrastructure.indexing.run_indexing_pipeline import ensure_index
        index_client = MagicMock()
        index_client.create_or_update_index.side_effect = RuntimeError("service unavailable")
        with pytest.raises(RuntimeError):
            ensure_index(index_client)

    def test_index_directory_processes_txt_files(self):
        from pathlib import Path
        from src.infrastructure.indexing.run_indexing_pipeline import index_directory

        with tempfile.TemporaryDirectory() as tmp_dir:
            # Write a sample text file
            txt_path = Path(tmp_dir) / "manual.txt"
            txt_path.write_text("Chapter 1: VPN setup instructions. " * 20, encoding="utf-8")

            search_client = MagicMock()
            embedder = MagicMock()
            embedder.embed_documents.side_effect = lambda docs: [
                {**d, "content_vector": [0.1] * 3072} for d in docs
            ]

            index_directory(Path(tmp_dir), "v1", "public", search_client, embedder)

            embedder.embed_documents.assert_called()
            search_client.upload_documents.assert_called()

    def test_main_runs_full_pipeline(self):
        from src.infrastructure.indexing.run_indexing_pipeline import main
        from src.infrastructure.config.settings import Settings

        fake_settings = Settings(
            cosmos_endpoint="https://x", cosmos_key="k",
            azure_openai_endpoint="https://x", azure_openai_api_key="k",
            azure_openai_deployment="gpt-4o", azure_openai_embedding_deployment="emb",
            azure_search_endpoint="https://x", azure_search_api_key="k",
            azure_search_index="test-idx",
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            txt_path = os.path.join(tmp_dir, "doc.txt")
            with open(txt_path, "w") as f:
                f.write("Some IT documentation content.")

            with patch("sys.argv", ["run", "--data-dir", tmp_dir]), \
                 patch("src.infrastructure.indexing.run_indexing_pipeline.get_settings", return_value=fake_settings), \
                 patch("src.infrastructure.indexing.run_indexing_pipeline.SearchIndexClient") as MockIdxClient, \
                 patch("src.infrastructure.indexing.run_indexing_pipeline.SearchClient") as MockSearchClient, \
                 patch("src.infrastructure.indexing.run_indexing_pipeline.Embedder") as MockEmbedder:

                MockEmbedder.return_value.embed_documents.side_effect = lambda docs: [
                    {**d, "content_vector": [0.0] * 3072} for d in docs
                ]
                main()

            MockIdxClient.return_value.create_or_update_index.assert_called_once()
            MockSearchClient.return_value.upload_documents.assert_called()



class TestChunker:
    def test_produces_at_least_one_chunk(self):
        chunks = chunk_text("hello world", "doc.txt", "v1")
        assert len(chunks) >= 1

    def test_chunk_has_required_fields(self):
        chunks = chunk_text("some text content", "f.txt", "v2")
        c = chunks[0]
        assert "id" in c
        assert "content" in c
        assert c["source_file"] == "f.txt"
        assert c["doc_version"] == "v2"

    def test_overlap_produces_multiple_chunks(self):
        words = " ".join([f"word{i}" for i in range(600)])
        chunks = chunk_text(words, "long.txt", "v1", chunk_size=100, overlap=20)
        assert len(chunks) >= 2

    def test_access_role_default_public(self):
        chunks = chunk_text("text", "f.txt", "v1")
        assert chunks[0]["access_role"] == "public"

    def test_access_role_custom(self):
        chunks = chunk_text("text", "f.txt", "v1", access_role="it_admin")
        assert chunks[0]["access_role"] == "it_admin"

    def test_page_numbers_increment(self):
        words = " ".join([f"w{i}" for i in range(300)])
        chunks = chunk_text(words, "f.txt", "v1", chunk_size=50, overlap=0)
        pages = [c["page_number"] for c in chunks]
        assert pages == list(range(1, len(chunks) + 1))


class TestEmbedder:
    @patch("src.infrastructure.indexing.embedder.AzureOpenAI")
    def test_embed_documents_adds_vector(self, MockAzureOpenAI):
        mock_response = MagicMock()
        mock_response.data = [MagicMock(embedding=[0.1] * 3072)]
        MockAzureOpenAI.return_value.embeddings.create.return_value = mock_response
        embedder = Embedder("https://x", "key")
        docs = [{"content": "test text"}]
        result = embedder.embed_documents(docs)
        assert "content_vector" in result[0]
        assert len(result[0]["content_vector"]) == 3072

    @patch("src.infrastructure.indexing.embedder.AzureOpenAI")
    def test_embed_query_returns_list(self, MockAzureOpenAI):
        mock_response = MagicMock()
        mock_response.data = [MagicMock(embedding=[0.5] * 3072)]
        MockAzureOpenAI.return_value.embeddings.create.return_value = mock_response
        embedder = Embedder("https://x", "key")
        vec = embedder.embed_query("search query")
        assert len(vec) == 3072
