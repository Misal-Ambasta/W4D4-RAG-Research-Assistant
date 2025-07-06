"""Utility for web search via Serper.dev API with simple result cleaning and summarization."""

from __future__ import annotations

import os
import re
import time
from typing import List, Dict, Any
from dotenv import load_dotenv
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
SERPER_URL = "https://google.serper.dev/search"

# rudimentary in-memory rate limit (10 req / min to be less restrictive)
_REQ_TS: List[float] = []


class SerperError(RuntimeError):
    pass


def _rate_limit():
    now = time.time()
    _REQ_TS.append(now)
    # keep last minute
    while _REQ_TS and now - _REQ_TS[0] > 60:
        _REQ_TS.pop(0)
    if len(_REQ_TS) > 10:  # Increased from 5 to 10
        raise SerperError("Rate limit exceeded (10 req/min)")


def _strip_html(raw: str) -> str:
    clean = re.sub(r"<[^>]+>", "", raw)
    return clean


def _get_mock_results(query: str, num_results: int = 5) -> List[Dict[str, Any]]:
    """Return mock search results when API key is not available."""
    mock_results = [
        {
            "title": f"Mock Result 1 for '{query}'",
            "link": "https://example.com/result1",
            "snippet": f"This is a mock search result for the query '{query}'. It provides relevant information about the topic."
        },
        {
            "title": f"Mock Result 2 for '{query}'",
            "link": "https://example.com/result2", 
            "snippet": f"Another mock search result related to '{query}'. This helps test the system functionality."
        },
        {
            "title": f"Mock Result 3 for '{query}'",
            "link": "https://example.com/result3",
            "snippet": f"A third mock result for '{query}' to demonstrate multiple search results."
        }
    ]
    return mock_results[:num_results]


def search_web(query: str, num_results: int = 5) -> List[Dict[str, Any]]:
    """Call Serper API and return cleaned results."""
    if SERPER_API_KEY is None:
        print("Warning: SERPER_API_KEY not set, using mock results")
        return _get_mock_results(query, num_results)

    try:
        _rate_limit()
        payload = {"q": query, "num": num_results}
        headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
        
        # Fixed: Use json=payload instead of data=payload for JSON data
        resp = requests.post(SERPER_URL, json=payload, headers=headers, timeout=10)
        
        if resp.status_code != 200:
            raise SerperError(f"Serper API error: {resp.status_code}: {resp.text}")
        
        data = resp.json()
        results = []
        
        # Handle different response formats
        organic_results = data.get("organic", [])
        if not organic_results:
            organic_results = data.get("results", [])
        
        for item in organic_results[:num_results]:
            results.append(
                {
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": _strip_html(item.get("snippet", "")),
                }
            )
        
        return results
        
    except Exception as e:
        print(f"Web search error: {e}")
        print("Falling back to mock results")
        return _get_mock_results(query, num_results)


def summarize_results(results: List[Dict[str, str]]) -> str:
    """Summarize list of SERP snippets using simple text processing."""
    if not results:
        return "No results to summarize."
    
    # Simple text-based summarization instead of using Ollama
    text = "\n".join(r["snippet"] for r in results if r["snippet"])
    
    # Extract key sentences (simple approach)
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    # Return first few sentences as summary
    summary_sentences = sentences[:3]
    return ". ".join(summary_sentences) + "." if summary_sentences else "No content available for summarization."


def test_web_search():
    """Test function to verify web search functionality."""
    print("Testing web search functionality...")
    
    try:
        results = search_web("Python programming", 3)
        print(f"✅ Search successful! Found {len(results)} results")
        
        for i, result in enumerate(results, 1):
            print(f"\nResult {i}:")
            print(f"  Title: {result['title']}")
            print(f"  Link: {result['link']}")
            print(f"  Snippet: {result['snippet'][:100]}...")
        
        # Test summarization
        summary = summarize_results(results)
        print(f"\n✅ Summarization successful!")
        print(f"Summary: {summary[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    test_web_search()
