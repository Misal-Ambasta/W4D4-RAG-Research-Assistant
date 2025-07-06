# Chroma vector store setup for local development
"""Vector store helper built around Chroma.

This module centralises all vector-DB interactions so that FastAPI routes can
remain clean and focused on HTTP concerns only.  All functions are synchronous
for simplicity – LangChain handles async poorly – but can be migrated later.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime

from langchain_chroma import Chroma
from langchain.embeddings.base import Embeddings
from langchain_core.documents import Document

# Persistent DB dir (./chroma_db by default)
DB_DIR = Path(__file__).parent / "chroma_db"
DB_DIR.mkdir(exist_ok=True)

# A single collection for now – can be expanded later
_COLLECTION_NAME = "documents"


def get_vectorstore(embedding: Embeddings) -> Chroma:
    """Load (or create) the Chroma vector store with persistence enabled."""
    return Chroma(persist_directory=str(DB_DIR), embedding_function=embedding, collection_name=_COLLECTION_NAME)


def _filter_complex_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Filter complex metadata types to simple types supported by Chroma."""
    filtered_metadata = {}
    for key, value in metadata.items():
        if value is None:
            filtered_metadata[key] = None
        elif isinstance(value, (str, int, float, bool)):
            filtered_metadata[key] = value
        elif isinstance(value, datetime):
            filtered_metadata[key] = value.isoformat()
        else:
            # Convert other types to string
            filtered_metadata[key] = str(value)
    return filtered_metadata


# CRUD operations -----------------------------------------------------------

def add_documents(docs: List[Document], embedding: Embeddings) -> List[str]:
    # Filter complex metadata (e.g., datetime) to str, int, float, bool, or None
    for doc in docs:
        doc.metadata = _filter_complex_metadata(doc.metadata)
    
    vs = get_vectorstore(embedding)
    ids = vs.add_documents(docs)
    return ids


def delete_document(doc_id: str, embedding: Embeddings) -> None:
    vs = get_vectorstore(embedding)
    vs.delete([doc_id])


def similarity_search(query: str, k: int, embedding: Embeddings, metadata_filter: Optional[Dict[str, str]] = None):
    vs = get_vectorstore(embedding)
    return vs.similarity_search(query, k=k, filter=metadata_filter)


# Example: get_or_create_collection('support_docs')
