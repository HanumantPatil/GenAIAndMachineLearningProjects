"""Azure AI Search index schema for the IT knowledge base."""
from __future__ import annotations

from azure.search.documents.indexes.models import (
    HnswAlgorithmConfiguration,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SearchIndex,
    SemanticConfiguration,
    SemanticField,
    SemanticPrioritizedFields,
    SemanticSearch,
    SimpleField,
    VectorSearch,
    VectorSearchProfile,
)

INDEX_NAME = "it-helpdesk-kb"
SEMANTIC_CONFIG_NAME = "it-helpdesk-semantic"
VECTOR_DIMENSIONS = 3072  # text-embedding-3-large


def build_index_schema() -> SearchIndex:
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True, filterable=True),
        SearchableField(name="content", type=SearchFieldDataType.String, analyzer_name="en.microsoft"),
        SimpleField(name="source_file", type=SearchFieldDataType.String, filterable=True, facetable=True),
        SimpleField(name="doc_version", type=SearchFieldDataType.String, filterable=True, facetable=True),
        SimpleField(name="page_number", type=SearchFieldDataType.Int32, filterable=True, sortable=True),
        SimpleField(name="access_role", type=SearchFieldDataType.String, filterable=True),
        SearchField(
            name="content_vector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=VECTOR_DIMENSIONS,
            vector_search_profile_name="hnsw-profile",
        ),
    ]

    vector_search = VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(name="hnsw")],
        profiles=[VectorSearchProfile(name="hnsw-profile", algorithm_configuration_name="hnsw")],
    )

    semantic_search = SemanticSearch(
        configurations=[
            SemanticConfiguration(
                name=SEMANTIC_CONFIG_NAME,
                prioritized_fields=SemanticPrioritizedFields(
                    content_fields=[SemanticField(field_name="content")],
                    keywords_fields=[
                        SemanticField(field_name="source_file"),
                        SemanticField(field_name="doc_version"),
                    ],
                ),
            )
        ]
    )

    return SearchIndex(
        name=INDEX_NAME,
        fields=fields,
        vector_search=vector_search,
        semantic_search=semantic_search,
    )
