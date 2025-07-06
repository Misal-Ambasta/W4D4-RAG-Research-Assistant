# RAG Research Assistant: Backend Flow Documentation

This document explains the backend flow of the system: which API endpoints are called, which internal functions/modules are triggered, and how data moves through the pipeline. Each endpoint is described with both stepwise arrows and a Mermaid diagram for clarity.

---

## 1. Document Upload Endpoint

**Flow:**
Client uploads PDF(s) -> `/upload` (FastAPI) -> `pdfplumber`/`PyPDF2` -> `langchain` chunking -> Embedding via Ollama -> Store in `chromadb` vector store -> Update BM25 index

**Stepwise:**
Client -> `/upload` -> PDF Parser -> Text Chunker -> Embedding Model -> Vector Store -> BM25 Index

**Mermaid:**
```mermaid
sequenceDiagram
    participant C as Client
    participant API as /upload Endpoint
    participant PDF as PDF Parser
    participant Chunk as Text Chunker
    participant Emb as Embedding Model
    participant Vec as Vector Store
    participant BM as BM25 Index
    C->>API: Upload PDF
    API->>PDF: Parse PDF
    PDF->>Chunk: Chunk Text
    Chunk->>Emb: Generate Embeddings
    Emb->>Vec: Store Embeddings
    Chunk->>BM: Update BM25 Index
```

---

## 2. Search Endpoint (Hybrid Retrieval)

**Flow:**
Client submits query -> `/search` (FastAPI) -> `cache.py` (frequent_query_cache) check -> Dense retrieval (`chromadb` vector store) -> Sparse retrieval (`BM25Index` in `sparse_retrieval.py`) -> Combine scores -> Rerank (cross-encoder) -> Return results

**Stepwise:**
Client -> `/search` -> Cache Check -> Dense Retrieval -> Sparse Retrieval -> Hybrid Combiner -> Cross-Encoder Rerank -> Response

**Mermaid:**
```mermaid
sequenceDiagram
    participant C as Client
    participant API as /search Endpoint
    participant Cache as Cache Check
    participant Dense as Dense Retrieval
    participant Sparse as Sparse Retrieval
    participant Hybrid as Hybrid Combiner
    participant Rank as Cross-Encoder
    C->>API: Query
    API->>Cache: Check Cache
    API->>Dense: Dense Retrieval
    API->>Sparse: Sparse Retrieval
    Dense->>Hybrid: Pass Results
    Sparse->>Hybrid: Pass Results
    Hybrid->>Rank: Rerank Top-K
    Rank->>API: Ranked Results
    API->>C: Return Results
```

---

## 3. Web Search Endpoint

**Flow:**
Client requests web search -> `/web_search` (FastAPI) -> `web_search.py:search_web` -> Serper API -> Clean/strip HTML -> Summarize (`summarize_results`) -> Return summary/results

**Stepwise:**
Client -> `/web_search` -> `search_web` -> Serper API -> Clean HTML -> Summarize -> Response

**Mermaid:**
```mermaid
sequenceDiagram
    participant C as Client
    participant API as /web_search Endpoint
    participant WS as search_web
    participant Serper as Serper API
    participant Clean as Clean HTML
    participant Sum as Summarize
    C->>API: Web Query
    API->>WS: Call search_web
    WS->>Serper: Query
    Serper->>WS: Results
    WS->>Clean: Strip HTML
    Clean->>Sum: Summarize
    Sum->>API: Summary
    API->>C: Return Summary
```

---

## 4. Citation Generation Endpoint

**Flow:**
Client requests citation -> `/citation` (FastAPI) -> `citation.py:generate_citation` -> Format citation -> Return

**Stepwise:**
Client -> `/citation` -> `generate_citation` -> Format -> Response

**Mermaid:**
```mermaid
sequenceDiagram
    participant C as Client
    participant API as /citation Endpoint
    participant Gen as generate_citation
    C->>API: Request Citation
    API->>Gen: Generate Citation
    Gen->>API: Citation String
    API->>C: Return Citation
```

---

## 5. Response Synthesis Endpoint

**Flow:**
Client submits query -> `/synthesize` (FastAPI) -> `response_synthesis.py:synthesize_response` -> Aggregate sources -> Rerank/conflict resolution -> Assess confidence/quality -> Return answer

**Stepwise:**
Client -> `/synthesize` -> `synthesize_response` -> Aggregate -> Rerank -> Assess -> Response

**Mermaid:**
```mermaid
sequenceDiagram
    participant C as Client
    participant API as /synthesize Endpoint
    participant Synth as synthesize_response
    C->>API: Synthesize Query
    API->>Synth: Aggregate Sources
    Synth->>Synth: Rerank, Assess
    Synth->>API: Final Answer
    API->>C: Return Synthesized Response
```

---

## 6. Caching Layer

- All endpoints may interact with `cache.py` for frequent query and response caching.
- Cache is checked before heavy computation and updated after response.

---

**Note:**
- Arrows (->) show the stepwise flow.
- Mermaid diagrams visualize the same process for each endpoint.
- Internal function calls (e.g., `search_web`, `generate_citation`, `synthesize_response`) are shown for clarity.

---

## 7. Document Deletion Endpoint

**Flow:**
Client requests to delete a document by ID -> `/documents/{doc_id}` (FastAPI) -> `vector_store.py:delete_document` -> Remove from `chromadb` -> Update BM25 index

**Stepwise:**
Client -> `/documents/{doc_id}` -> Vector Store -> BM25 Index -> Response

**Mermaid:**
```mermaid
sequenceDiagram
    participant C as Client
    participant API as /documents/{doc_id}
    participant Vec as Vector Store
    participant BM as BM25 Index
    C->>API: Delete Document(doc_id)
    API->>Vec: Delete from ChromaDB
    API->>BM: Update BM25 Index
    API->>C: Confirmation
```

---

## 8. Session Management Endpoints

### Create Session
**Flow:**
Client requests to create a new session -> `/sessions/create` (FastAPI) -> Generate new user ID -> Return user ID

**Mermaid:**
```mermaid
sequenceDiagram
    participant C as Client
    participant API as /sessions/create
    C->>API: Request new session
    API->>API: Generate User ID
    API->>C: Return User ID
```

### Get/Update History
**Flow:**
Client requests history or adds a new entry -> `/sessions/{user_id}/history` (FastAPI) -> Interact with session store -> Return history or confirmation

**Mermaid:**
```mermaid
sequenceDiagram
    participant C as Client
    participant API as /sessions/{user_id}/history
    participant Store as Session Store
    C->>API: GET/POST History
    API->>Store: Read/Write History
    Store->>API: Return Data
    API->>C: Return History/Confirmation
```

---

## 9. Feedback & Analytics Endpoints

### Submit Feedback
**Flow:**
Client submits a rating for a response -> `/feedback/rating` (FastAPI) -> Store feedback data -> Use for quality monitoring

**Mermaid:**
```mermaid
sequenceDiagram
    participant C as Client
    participant API as /feedback/rating
    participant DB as Feedback DB
    C->>API: Submit Rating
    API->>DB: Store Feedback
    DB->>API: Confirmation
    API->>C: OK
```

### Get Analytics
**Flow:**
Admin/Client requests query analytics -> `/analytics/queries` (FastAPI) -> Fetch data from analytics store -> Return analytics data

**Mermaid:**
```mermaid
sequenceDiagram
    participant C as Client
    participant API as /analytics/queries
    participant DB as Analytics DB
    C->>API: Request Analytics
    API->>DB: Fetch Query Data
    DB->>API: Return Data
    API->>C: Return Analytics
```

---

## 10. Utility Endpoints

### Clear Cache
**Flow:**
Client requests to clear cache -> `/cache/clear` (FastAPI) -> `cache.py:clear_all_caches` -> Return confirmation

**Mermaid:**
```mermaid
sequenceDiagram
    participant C as Client
    participant API as /cache/clear
    participant Cache as cache.py
    C->>API: Request Cache Clear
    API->>Cache: clear_all_caches()
    Cache->>API: Confirmation
    API->>C: OK
```

### Health Check
**Flow:**
System monitor requests health check -> `/health` (FastAPI) -> Check service status -> Return "OK"

**Mermaid:**
```mermaid
sequenceDiagram
    participant M as Monitor
    participant API as /health
    M->>API: GET /health
    API->>API: Check Status
    API->>M: {"status": "OK"}
```
