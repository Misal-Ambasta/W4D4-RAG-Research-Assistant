"""Citation management and formatting utilities for RAG pipeline."""

from typing import Dict, List
from datetime import datetime

CITATION_STYLES = {
    "APA": "{author}. ({year}). {title}. {source}. {url}",
    "MLA": "{author}. \"{title}.\" {source}, {year}, {url}.",
    "Chicago": "{author}. \"{title}.\" {source} ({year}): {url}.",
}

def generate_citation(meta: Dict, style: str = "APA") -> str:
    """Generate a citation string from metadata in the given style."""
    year = meta.get("published", "")[:4] if meta.get("published") else "n.d."
    return CITATION_STYLES.get(style, CITATION_STYLES["APA"]).format(
        author=meta.get("author", "Anon"),
        year=year,
        title=meta.get("title", "Untitled"),
        source=meta.get("source", "Web"),
        url=meta.get("url", meta.get("link", "")),
    )

def verify_citation(meta: Dict) -> bool:
    """Basic check for citation completeness."""
    required = ["author", "title", "source", "url"]
    return all(meta.get(k) for k in required)

class CitationManager:
    def __init__(self):
        self.citations: List[Dict] = []

    def add(self, meta: Dict):
        if meta not in self.citations:
            self.citations.append(meta)

    def format_all(self, style: str = "APA") -> List[str]:
        return [generate_citation(m, style) for m in self.citations]

    def verify_all(self) -> List[bool]:
        return [verify_citation(m) for m in self.citations]
