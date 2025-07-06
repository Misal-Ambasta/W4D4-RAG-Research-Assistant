import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import DocumentUpload from './components/DocumentUpload';
import SearchForm from './components/SearchForm';
import SearchResults from './components/SearchResults';
import SearchHistory from './components/SearchHistory';
import ResponseRating from './components/ResponseRating';
import ResponseDisplay from './components/ResponseDisplay';
import './App.css';

// Types
interface SearchResult {
  content: string;
  metadata: any;
  source_type: string;
  score: number;
}

interface SearchResponse {
  query: string;
  search_type: string;
  results: SearchResult[];
  total_results: number;
  response_time: number;
  sources: any[];
  citations: string[];
  confidence: number;
  quality: string;
}

interface SearchHistory {
  query: string;
  results_count: number;
  timestamp: string;
}

const API_BASE = 'http://localhost:8000';

function Dashboard() {
  const [searchResponse, setSearchResponse] = useState<SearchResponse | null>(null);
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [userId] = useState(() => `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`);
  const [searchHistory, setSearchHistory] = useState<SearchHistory[]>([]);
  const [showHistory, setShowHistory] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);

  // Initialize user session
  useEffect(() => {
    const initializeSession = async () => {
      try {
        await fetch(`${API_BASE}/sessions/create`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ 
            user_id: userId, 
            session_name: 'Research Session' 
          })
        });
      } catch (err) {
        console.error('Failed to initialize session:', err);
      }
    };

    initializeSession();
  }, [userId]);

  // Load search history
  const loadSearchHistory = async () => {
    try {
      const response = await fetch(`${API_BASE}/sessions/${userId}/history`);
      if (response.ok) {
        const data = await response.json();
        setSearchHistory(data.search_history || []);
      }
    } catch (err) {
      console.error('Failed to load search history:', err);
    }
  };

  useEffect(() => {
    loadSearchHistory();
  }, [userId]);

  const handleUpload = async (files: File[]) => {
    setUploadedFiles(files);
    if (!files || files.length === 0) {
      setUploadStatus(null);
      return;
    }

    setLoading(true);
    setError(null);
    setUploadStatus('Uploading and processing documents...');

    try {
      const formData = new FormData();
      for (const file of files) {
        formData.append('files', file);
      }

      const response = await fetch(`${API_BASE}/documents/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Upload failed');
      }

      const data = await response.json();
      setUploadStatus(`Successfully uploaded ${data.uploaded_files} files (${data.total_chunks} chunks)`);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Upload failed';
      setError(errorMessage);
      setUploadStatus(null);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (query: string, searchType: string, options: any = {}) => {
    if (!query.trim()) {
      setError('Please enter a search query');
      return;
    }

    setLoading(true);
    setError(null);
    setSearchResponse(null);

    try {
      const searchRequest = {
        query: query.trim(),
        search_type: searchType,
        k: options.k || 5,
        source_filter: options.source_filter || null,
        min_credibility: options.min_credibility || 0.5,
        enable_cache: options.enable_cache !== false
      };

      const response = await fetch(`${API_BASE}/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(searchRequest)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Search failed');
      }

      const data = await response.json();
      setSearchResponse(data);

      // Add to search history
      await fetch(`${API_BASE}/sessions/${userId}/history`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: query.trim(),
          results: data.total_results
        })
      });

      // Refresh search history
      loadSearchHistory();

    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Search failed';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleRating = async (rating: number, feedback?: string) => {
    if (!searchResponse) return;

    try {
      await fetch(`${API_BASE}/feedback/rating`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: searchResponse.query,
          rating,
          feedback
        })
      });
    } catch (err) {
      console.error('Failed to submit rating:', err);
    }
  };

  const clearError = () => setError(null);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Research Assistant
          </h1>
          <p className="text-xl text-gray-600">
            Advanced RAG with Web Integration
          </p>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4 flex items-center justify-between">
            <div className="flex items-center">
              <div className="text-red-800">
                <svg className="w-5 h-5 mr-2 inline" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
                {error}
              </div>
            </div>
            <button
              onClick={clearError}
              className="text-red-600 hover:text-red-800"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </button>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Upload & Search */}
          <div className="lg:col-span-2 space-y-6">
            {/* Document Upload Section */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4 flex items-center">
                <svg className="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                Upload Documents
              </h2>
              <DocumentUpload onUpload={handleUpload} />
              {uploadStatus && (
                <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg text-green-800">
                  {uploadStatus}
                </div>
              )}
            </div>

            {/* Search Section */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4 flex items-center">
                <svg className="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                Hybrid Search
              </h2>
              <SearchForm onSearch={handleSearch} loading={loading} />
            </div>

            {/* Search Results */}
            {searchResponse && (
              <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-2xl font-semibold text-gray-900 flex items-center">
                    <svg className="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    Results
                  </h2>
                  <div className="flex items-center space-x-4 text-sm text-gray-600">
                    <span>Found: {searchResponse.total_results}</span>
                    <span>Time: {searchResponse.response_time.toFixed(2)}s</span>
                    <span className={`px-2 py-1 rounded-full text-xs ${
                      searchResponse.quality === 'high' ? 'bg-green-100 text-green-800' :
                      searchResponse.quality === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      Quality: {searchResponse.quality}
                    </span>
                  </div>
                </div>
                <ResponseDisplay response={searchResponse} />
                <SearchResults results={searchResponse.results} citations={searchResponse.citations} />
                <ResponseRating onRating={handleRating} />
              </div>
            )}
          </div>

          {/* Right Column - History & Info */}
          <div className="space-y-6">
            {/* Search History */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-semibold text-gray-900 flex items-center">
                  <svg className="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Search History
                </h3>
                <button
                  onClick={() => setShowHistory(!showHistory)}
                  className="text-blue-600 hover:text-blue-800"
                >
                  {showHistory ? 'Hide' : 'Show'}
                </button>
              </div>
              {showHistory && <SearchHistory history={searchHistory} onSearch={handleSearch} />}
            </div>

            {/* Stats */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Session Stats</h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Uploaded Files:</span>
                  <span className="font-medium">{uploadedFiles.length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Total Searches:</span>
                  <span className="font-medium">{searchHistory.length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Session ID:</span>
                  <span className="font-mono text-xs text-gray-500">{userId.slice(-8)}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
      </Routes>
    </Router>
  );
}

export default App;
