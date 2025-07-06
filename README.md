# Research Assistant - Advanced RAG with Web Integration

A comprehensive Research Assistant application that combines document-based search with real-time web search integration, implementing advanced RAG (Retrieval-Augmented Generation) techniques.

## 🌟 Features

### Core Capabilities
- **PDF Document Upload & Processing** - Upload and process multiple PDF documents with OCR fallback
- **Hybrid Search** - Combines document search with real-time web search
- **Advanced Retrieval Methods**:
  - Dense retrieval using semantic embeddings (Ollama nomic-embed-text)
  - Sparse retrieval using BM25 keyword matching
  - Hybrid scoring and ranking
- **Response Synthesis** - Multi-source response generation with confidence scoring
- **Source Verification** - Credibility assessment and source ranking
- **Citation Management** - Automatic citation generation in multiple formats (APA, MLA, Chicago)
- **Intelligent Caching** - Query caching for improved performance
- **User Session Management** - Track search history and user interactions
- **Response Quality Monitoring** - User feedback and rating system

### Technical Implementation
- **Backend**: FastAPI with comprehensive API endpoints
- **Frontend**: React with TypeScript and modern UI components
- **Vector Database**: ChromaDB for semantic search
- **Web Search**: Serper.dev API integration
- **Embeddings**: Ollama nomic-embed-text model
- **Text Processing**: Advanced chunking with RecursiveCharacterTextSplitter
- **Cross-Encoder Re-ranking**: For improved result precision

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │  External APIs  │
│   (React/TS)    │◄──►│   (FastAPI)     │◄──►│   (Serper.dev)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                    ┌─────────┼─────────┐
                    │         │         │
            ┌───────▼───┐ ┌───▼───┐ ┌───▼────┐
            │ ChromaDB  │ │ BM25  │ │ Cache  │
            │(Vector DB)│ │(Sparse)│ │ Layer │
            └───────────┘ └───────┘ └────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Ollama installed with nomic-embed-text model
- (Optional) Serper.dev API key for web search

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (create `.env` file):
   ```env
   SERPER_API_KEY=your_serper_api_key_here  # Optional for web search
   ```

5. **Start the backend server**:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```

4. **Open your browser** to `http://localhost:5173`

### Ollama Setup

1. **Install Ollama**: Follow instructions at [ollama.ai](https://ollama.ai)

2. **Pull the embedding model**:
   ```bash
   ollama pull nomic-embed-text
   ```

3. **Optional - Pull LLM for summarization**:
   ```bash
   ollama pull gemma:2b
   ```

## 📖 Usage Guide

### 1. Document Upload
- Drag and drop PDF files or click to browse
- Multiple files supported (up to 50MB each)
- Automatic text extraction with OCR fallback
- Documents are processed, chunked, and indexed automatically

### 2. Search Types

#### Document Search
- Search only uploaded PDF documents
- Uses semantic similarity matching
- Includes sparse (BM25) keyword matching

#### Web Search
- Real-time internet search via Serper.dev
- Source credibility assessment
- Result filtering and ranking

#### Hybrid Search (Recommended)
- Combines document and web search results
- Intelligent ranking and deduplication
- Multi-source response synthesis

### 3. Advanced Features

#### Search Options
- **Number of Results**: 3-20 results
- **Source Filter**: Filter by document name
- **Credibility Threshold**: Minimum credibility score (0.0-1.0)
- **Caching**: Enable/disable query caching

#### Response Quality
- **Confidence Score**: AI-generated confidence in the response
- **Quality Assessment**: High/Medium/Low quality rating
- **Response Time**: Search and processing time
- **Source Count**: Number of unique sources used

#### User Features
- **Search History**: Track all searches in session
- **Response Rating**: Rate responses 1-5 stars with feedback
- **Citations**: Automatic citation generation
- **Session Statistics**: Upload and search metrics

## 🛠️ API Endpoints

### Document Management
- `POST /documents/upload` - Upload PDF documents
- `DELETE /documents/{doc_id}` - Remove a document

### Search
- `POST /search` - Advanced hybrid search with all options

### Session Management
- `POST /sessions/create` - Create user session
- `GET /sessions/{user_id}/history` - Get search history
- `POST /sessions/{user_id}/history` - Add to search history

### Feedback & Analytics
- `POST /feedback/rating` - Submit response rating
- `GET /citations` - Get formatted citations
- `GET /analytics/queries` - Get query analytics

### Utility
- `POST /cache/clear` - Clear all caches
- `GET /health` - Health check

## 📁 Project Structure

```
W4D4-RAG-Research-Assistant/
├── backend/                    # FastAPI backend
│   ├── main.py                # Main API application
│   ├── document_processing.py # PDF processing utilities
│   ├── vector_store.py        # ChromaDB integration
│   ├── web_search.py          # Serper.dev integration
│   ├── sparse_retrieval.py    # BM25 implementation
│   ├── response_synthesis.py  # Multi-source synthesis
│   ├── source_verification.py # Credibility assessment
│   ├── citation.py            # Citation management
│   ├── cache.py               # Caching utilities
│   └── requirements.txt       # Python dependencies
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── App.tsx           # Main application
│   │   └── App.css           # Custom styling
│   ├── package.json          # Node.js dependencies
│   └── vite.config.ts        # Vite configuration
├── README.md                  # This file
└── problem_statement.md       # Project requirements
```

## 🔧 Configuration

### Environment Variables
- `SERPER_API_KEY`: API key for Serper.dev web search (optional)

### Model Configuration
- **Embedding Model**: `nomic-embed-text` (via Ollama)
- **LLM Model**: `gemma:2b` (for summarization, optional)
- **Cross-Encoder**: `cross-encoder/ms-marco-MiniLM-L-6-v2`

### Search Parameters
- **Chunk Size**: 500 characters with 50 character overlap
- **Default Results**: 5 per search type
- **Cache TTL**: 1 hour for search results
- **Min Credibility**: 0.5 (configurable)

## 🌐 Browser Support
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues

1. **Ollama Connection Error**
   - Ensure Ollama is running: `ollama serve`
   - Check if model is pulled: `ollama list`

2. **Web Search Not Working**
   - Verify SERPER_API_KEY in environment
   - Check API key validity at serper.dev

3. **PDF Processing Issues**
   - Install Tesseract for OCR: `apt-get install tesseract-ocr`
   - Check file size limits (50MB max)

4. **CORS Issues**
   - Ensure backend is running on port 8000
   - Check frontend API_BASE configuration

### Performance Optimization
- Enable caching for frequent queries
- Adjust chunk size based on document types
- Use credibility filtering to reduce noise
- Consider using approximate nearest neighbor search for large document sets

## 📊 Monitoring & Analytics

The system includes built-in monitoring for:
- Search response times
- Query frequency and patterns
- User satisfaction ratings
- Cache hit rates
- Source credibility distribution

## 🔮 Future Enhancements

- [ ] Multi-language document support
- [ ] Advanced query understanding with NLP
- [ ] Real-time collaborative features
- [ ] Custom embedding fine-tuning
- [ ] GraphQL API support
- [ ] Mobile application
- [ ] Advanced analytics dashboard
- [ ] Integration with more search engines