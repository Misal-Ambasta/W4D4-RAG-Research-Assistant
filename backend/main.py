from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import uuid
from datetime import datetime
import os
from dotenv import load_dotenv

from langchain_ollama import OllamaEmbeddings

from document_processing import process_pdf
from vector_store import add_documents, delete_document, similarity_search
from web_search import search_web, summarize_results
from sparse_retrieval import load_or_create_index, BM25Index
from response_synthesis import synthesize_response, resolve_conflicts
from source_verification import credibility_score, filter_sources
from citation import CitationManager, generate_citation
from cache import frequent_query_cache, response_cache

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Research Assistant API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
_embeddings = None
_bm25_index = None
_citation_manager = CitationManager()
_user_sessions = {}

# Pydantic models
class SearchRequest(BaseModel):
    query: str
    search_type: str = "hybrid"  # document, web, hybrid
    k: int = 5
    source_filter: Optional[str] = None
    min_credibility: float = 0.5
    enable_cache: bool = True

class SearchResponse(BaseModel):
    query: str
    search_type: str
    results: List[Dict[str, Any]]
    total_results: int
    response_time: float
    sources: List[Dict[str, Any]]
    citations: List[str]
    confidence: float
    quality: str

class SessionRequest(BaseModel):
    user_id: str
    session_name: Optional[str] = None

class HistoryEntry(BaseModel):
    query: str
    results: int


class RatingRequest(BaseModel):
    query: str
    rating: int  # 1-5
    feedback: Optional[str] = None

def get_embeddings():
    global _embeddings
    if _embeddings is None:
        ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")

        # The user's .env file might have the full endpoint, but OllamaEmbeddings needs the base URL.
        if ollama_host.endswith("/api/embeddings"):
            ollama_host = ollama_host.rsplit("/api/embeddings", 1)[0]
        
        print(f"Using Ollama host: {ollama_host}")
        try:
            _embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=ollama_host)
        except Exception as e:
            raise HTTPException(
                status_code=503, 
                detail=f"Failed to initialize embeddings. Ensure Ollama is running and accessible at {ollama_host}. Error: {e}"
            )
    return _embeddings

def get_bm25_index():
    global _bm25_index
    if _bm25_index is None:
        _bm25_index = load_or_create_index()
    return _bm25_index

def get_user_session(user_id: str):
    if user_id not in _user_sessions:
        _user_sessions[user_id] = {
            "id": user_id,
            "created_at": datetime.now().isoformat(),
            "search_history": [],
            "ratings": []
        }
    return _user_sessions[user_id]

@app.get("/")
def root():
    return {"message": "Research Assistant API is running", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/documents/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    """Upload and process PDF documents for vector storage."""
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    all_ids = []
    processed_docs = []
    
    for file in files:
        try:
            docs = process_pdf(file)
            ids = add_documents(docs, get_embeddings())
            all_ids.extend(ids)
            processed_docs.extend(docs)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to process {file.filename}: {str(e)}")
    
    # Update BM25 index with new documents
    global _bm25_index
    if processed_docs:
        _bm25_index = load_or_create_index(processed_docs)
    
    return {
        "status": "success",
        "uploaded_files": len(files),
        "document_ids": all_ids,
        "total_chunks": len(all_ids)
    }

@app.delete("/documents/{doc_id}")
async def remove_document(doc_id: str):
    """Remove a document from the vector store."""
    try:
        delete_document(doc_id, get_embeddings())
        return {"status": "deleted", "document_id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {str(e)}")

@app.post("/search", response_model=SearchResponse)
async def hybrid_search(request: SearchRequest):
    """Advanced hybrid search combining documents and web sources."""
    start_time = datetime.now()
    
    # Check cache first
    cache_key = f"{request.query}_{request.search_type}_{request.k}"
    if request.enable_cache:
        cached_result = response_cache.get(cache_key)
        if cached_result:
            return cached_result
    
    all_results = []
    web_sources = []
    
    try:
        # Document search (dense + sparse)
        if request.search_type in ["document", "hybrid"]:
            # Dense retrieval
            doc_results = similarity_search(
                request.query, 
                request.k, 
                get_embeddings(), 
                {"source": request.source_filter} if request.source_filter else None
            )
            
            # Sparse retrieval
            bm25_results = get_bm25_index().search(request.query, request.k)
            
            # Combine and format document results
            for doc in doc_results:
                result = {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "source_type": "document",
                    "score": 0.7  # Default dense score
                }
                all_results.append(result)
            
            # Add BM25 results
            for bm25_result in bm25_results:
                result = {
                    "content": bm25_result.get("content", ""),
                    "metadata": bm25_result["metadata"],
                    "source_type": "document",
                    "score": bm25_result["score"]
                }
                all_results.append(result)
        
        # Web search
        if request.search_type in ["web", "hybrid"]:
            try:
                web_results = search_web(request.query, request.k)
                for web_result in web_results:
                    # Add credibility scoring
                    credibility = credibility_score(web_result)
                    result = {
                        "content": web_result["snippet"],
                        "metadata": {
                            "title": web_result["title"],
                            "url": web_result["link"],
                            "source": "web",
                            "credibility": credibility
                        },
                        "source_type": "web",
                        "score": credibility
                    }
                    all_results.append(result)
                    web_sources.append(web_result)
            except Exception as e:
                print(f"Web search failed: {e}")
        
        # Filter by credibility
        if request.min_credibility > 0:
            all_results = [r for r in all_results if r["score"] >= request.min_credibility]
        
        # Resolve conflicts and synthesize response
        if all_results:
            synthesis_sources = [{"snippet": r["content"], "metadata": r["metadata"]} for r in all_results]
            synthesis_result = synthesize_response(resolve_conflicts(synthesis_sources), request.query)
            
            confidence = synthesis_result["confidence"]
            quality = synthesis_result["quality"]
            top_sources = synthesis_result["sources"]
        else:
            confidence = 0.0
            quality = "low"
            top_sources = []
        
        # Generate citations
        citations = []
        for result in all_results[:5]:  # Top 5 for citations
            citation = generate_citation(result["metadata"])
            citations.append(citation)
            _citation_manager.add(result["metadata"])
        
        # Prepare response
        response = SearchResponse(
            query=request.query,
            search_type=request.search_type,
            results=all_results,
            total_results=len(all_results),
            response_time=(datetime.now() - start_time).total_seconds(),
            sources=top_sources,
            citations=citations,
            confidence=confidence,
            quality=quality
        )
        
        # Cache the response
        if request.enable_cache:
            response_cache.set(cache_key, response, ttl=3600)  # 1 hour
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.post("/sessions/create")
async def create_session(request: SessionRequest):
    """Create a new user session."""
    session = get_user_session(request.user_id)
    if request.session_name:
        session["name"] = request.session_name
    return {"session_id": request.user_id, "session": session}

@app.get("/sessions/{user_id}/history")
async def get_search_history(user_id: str):
    """Get user's search history."""
    session = get_user_session(user_id)
    return {"user_id": user_id, "search_history": session["search_history"]}

@app.post("/sessions/{user_id}/history")
async def add_to_history(user_id: str, entry: HistoryEntry):
    """Add search to user's history."""
    session = get_user_session(user_id)
    session["search_history"].append({
        "query": entry.query,
        "results_count": entry.results,
        "timestamp": datetime.now().isoformat()
    })
    return {"status": "added", "history_length": len(session["search_history"])}

@app.post("/feedback/rating")
async def submit_rating(request: RatingRequest):
    """Submit user rating and feedback."""
    # Store rating (in production, this would go to a database)
    rating_data = {
        "query": request.query,
        "rating": request.rating,
        "feedback": request.feedback,
        "timestamp": datetime.now().isoformat()
    }
    
    # Add to frequent query cache for monitoring
    frequent_query_cache.set(f"rating_{request.query}", rating_data, ttl=86400)
    
    return {"status": "rating_submitted", "rating": request.rating}

@app.get("/citations")
async def get_citations(style: str = "APA"):
    """Get formatted citations for all sources."""
    citations = _citation_manager.format_all(style)
    return {"style": style, "citations": citations}

@app.get("/analytics/queries")
async def get_query_analytics():
    """Get analytics on frequent queries and ratings."""
    # In production, this would query actual analytics database
    return {
        "total_queries": len(frequent_query_cache.cache),
        "cache_hits": "Not implemented",
        "average_rating": "Not implemented"
    }

@app.post("/cache/clear")
async def clear_cache():
    """Clear all caches."""
    response_cache.clear()
    frequent_query_cache.clear()
    return {"status": "caches_cleared"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
