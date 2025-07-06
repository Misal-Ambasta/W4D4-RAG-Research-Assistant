"""Basic sparse retrieval using BM25 algorithm."""

from __future__ import annotations

import pickle
from pathlib import Path
from typing import List, Dict, Any

from langchain_core.documents import Document
from rank_bm25 import BM25Okapi
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
STOP_WORDS = set(stopwords.words('english'))

INDEX_PATH = Path(__file__).parent / "bm25_index.pkl"


class BM25Index:
    def __init__(self):
        self.doc_texts: List[List[str]] = []
        self.doc_metadata: List[Dict[str, Any]] = []
        self.doc_contents: List[str] = []  # Store original content
        self.bm25 = None

    def build(self, docs: List[Document]):
        """Build BM25 index from documents."""
        self.doc_texts = [self._preprocess(d.page_content) for d in docs]
        self.doc_metadata = [d.metadata for d in docs]
        self.doc_contents = [d.page_content for d in docs]
        self.bm25 = BM25Okapi(self.doc_texts)

    @staticmethod
    def _preprocess(text: str) -> List[str]:
        """Preprocess text by tokenizing and removing stopwords."""
        try:
            tokens = [t.lower() for t in word_tokenize(text) if t.isalpha() and t.lower() not in STOP_WORDS]
            return tokens
        except Exception:
            # Fallback to simple split if NLTK fails
            return [t.lower() for t in text.split() if t.isalpha() and t.lower() not in STOP_WORDS]

    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search the BM25 index and return top-k results."""
        if self.bm25 is None or not self.doc_texts:
            return []
        
        q_tokens = self._preprocess(query)
        if not q_tokens:
            return []
        
        scores = self.bm25.get_scores(q_tokens)
        ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        
        results = []
        for i in ranked_indices:
            if i < len(self.doc_contents) and scores[i] > 0:  # Only return positive scores
                results.append({
                    "content": self.doc_contents[i],
                    "metadata": self.doc_metadata[i],
                    "score": float(scores[i])
                })
        
        return results

    def add_documents(self, docs: List[Document]):
        """Add new documents to existing index."""
        new_texts = [self._preprocess(d.page_content) for d in docs]
        new_metadata = [d.metadata for d in docs]
        new_contents = [d.page_content for d in docs]
        
        self.doc_texts.extend(new_texts)
        self.doc_metadata.extend(new_metadata)
        self.doc_contents.extend(new_contents)
        
        # Rebuild BM25 index
        self.bm25 = BM25Okapi(self.doc_texts)


def load_or_create_index(docs: List[Document] | None = None) -> BM25Index:
    """Load existing BM25 index or create new one."""
    index = BM25Index()
    
    # Try to load existing index
    if INDEX_PATH.exists():
        try:
            with INDEX_PATH.open("rb") as f:
                saved_index = pickle.load(f)
                if hasattr(saved_index, 'doc_texts') and hasattr(saved_index, 'doc_metadata'):
                    index = saved_index
        except Exception as e:
            print(f"Failed to load existing index: {e}")
    
    # Build new index if documents provided
    if docs:
        if hasattr(index, 'doc_texts') and index.doc_texts:
            # Add to existing index
            index.add_documents(docs)
        else:
            # Build new index
            index.build(docs)
        
        # Save updated index
        try:
            with INDEX_PATH.open("wb") as f:
                pickle.dump(index, f)
        except Exception as e:
            print(f"Failed to save index: {e}")
    
    return index


def rebuild_index(docs: List[Document]) -> BM25Index:
    """Rebuild the entire BM25 index."""
    index = BM25Index()
    index.build(docs)
    
    try:
        with INDEX_PATH.open("wb") as f:
            pickle.dump(index, f)
    except Exception as e:
        print(f"Failed to save rebuilt index: {e}")
    
    return index
