"""Source verification and credibility assessment utilities for RAG pipeline."""

import requests
import tldextract
from datetime import datetime, timezone
from typing import Dict, Any
from urllib.parse import urlparse

# Example domain reputation list (would use a real API/service in production)
REPUTABLE_DOMAINS = {"wikipedia.org", "nature.com", "nytimes.com", "bbc.co.uk", "reuters.com", "nasa.gov"}

# Example domain blacklist
BLACKLISTED_DOMAINS = {"clickbait.com", "fakenews.net"}


def check_domain_reputation(url: str) -> str:
    domain = tldextract.extract(url).registered_domain
    if domain in BLACKLISTED_DOMAINS:
        return "blacklist"
    if domain in REPUTABLE_DOMAINS:
        return "trusted"
    return "unknown"


def assess_content_freshness(published_date: str) -> float:
    """Returns a freshness score [0,1] based on recency (ISO date string expected)."""
    try:
        pub_dt = datetime.fromisoformat(published_date.replace("Z", "+00:00"))
        days = (datetime.now(timezone.utc) - pub_dt).days
        if days < 30:
            return 1.0
        elif days < 180:
            return 0.7
        elif days < 365:
            return 0.4
        else:
            return 0.1
    except Exception:
        return 0.0


def credibility_score(source: Dict[str, Any]) -> float:
    """Score source based on domain, freshness, and other heuristics."""
    rep = check_domain_reputation(source.get("link", ""))
    freshness = assess_content_freshness(source.get("published", ""))
    base = 0.5
    if rep == "trusted":
        base += 0.3
    elif rep == "blacklist":
        base -= 0.4
    return min(1.0, max(0.0, base + 0.2 * freshness))


def filter_sources(sources: list, min_score: float = 0.5) -> list:
    """Filter out sources below a credibility threshold."""
    return [s for s in sources if credibility_score(s) >= min_score]
