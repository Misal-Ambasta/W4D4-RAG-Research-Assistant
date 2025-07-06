import React, { useState } from 'react';

interface SearchResult {
  content: string;
  metadata: any;
  source_type: string;
  score: number;
}

interface SearchResultsProps {
  results: SearchResult[];
  citations: string[];
  onDelete?: (docId: string) => void;
}

const SearchResults: React.FC<SearchResultsProps> = ({ results, citations, onDelete }) => {
  const [expandedResult, setExpandedResult] = useState<number | null>(null);
  const [showCitations, setShowCitations] = useState(false);

  if (!results || results.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <svg className="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <p className="text-lg">No results found</p>
        <p className="text-sm">Try adjusting your search terms or criteria</p>
      </div>
    );
  }

  const toggleExpanded = (index: number) => {
    setExpandedResult(expandedResult === index ? null : index);
  };

  const getSourceIcon = (sourceType: string) => {
    switch (sourceType) {
      case 'document':
        return (
          <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        );
      case 'web':
        return (
          <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9-9a9 9 0 00-9 9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
          </svg>
        );
      default:
        return (
          <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        );
    }
  };

  const getCredibilityColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600 bg-green-100';
    if (score >= 0.6) return 'text-yellow-600 bg-yellow-100';
    if (score >= 0.4) return 'text-orange-600 bg-orange-100';
    return 'text-red-600 bg-red-100';
  };

  const truncateContent = (content: string, maxLength: number = 200) => {
    if (content.length <= maxLength) return content;
    return content.substring(0, maxLength) + '...';
  };

  return (
    <div className="space-y-4">
      {/* Results */}
      <div className="space-y-4">
        {results.map((result, index) => (
          <div key={index} className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
            {/* Header */}
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center space-x-2">
                {getSourceIcon(result.source_type)}
                <span className="font-medium text-gray-900 capitalize">
                  {result.source_type} Result
                </span>
                <span className="text-sm text-gray-500">#{index + 1}</span>
              </div>
              <div className="flex items-center space-x-2">
                {/* Score */}
                <div className="flex items-center space-x-1">
                  <svg className="w-4 h-4 text-yellow-500" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                  <span className="text-sm font-medium text-gray-600">
                    {result.score?.toFixed(2) || 'N/A'}
                  </span>
                </div>

                {/* Credibility (for web results) */}
                {result.source_type === 'web' && result.metadata?.credibility && (
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getCredibilityColor(result.metadata.credibility)}`}>
                    {Math.round(result.metadata.credibility * 100)}% credible
                  </span>
                )}

                {/* Expand/Collapse Button */}
                <button
                  onClick={() => toggleExpanded(index)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <svg className={`w-5 h-5 transform transition-transform ${expandedResult === index ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
              </div>
            </div>

            {/* Content */}
            <div className="mb-3">
              <p className="text-gray-800 leading-relaxed">
                {expandedResult === index ? result.content : truncateContent(result.content)}
              </p>
              {result.content.length > 200 && expandedResult !== index && (
                <button
                  onClick={() => toggleExpanded(index)}
                  className="text-blue-600 hover:text-blue-800 text-sm mt-2"
                >
                  Show more
                </button>
              )}
            </div>

            {/* Metadata */}
            <div className="border-t pt-3">
              <div className="flex flex-wrap gap-2 text-sm text-gray-600">
                {result.metadata?.title && (
                  <div className="flex items-center">
                    <span className="font-medium">Title:</span>
                    <span className="ml-1">{result.metadata.title}</span>
                  </div>
                )}
                {result.metadata?.source && (
                  <div className="flex items-center">
                    <span className="font-medium">Source:</span>
                    <span className="ml-1">{result.metadata.source}</span>
                  </div>
                )}
                {result.metadata?.url && (
                  <div className="flex items-center">
                    <span className="font-medium">URL:</span>
                    <a 
                      href={result.metadata.url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="ml-1 text-blue-600 hover:text-blue-800 hover:underline"
                    >
                      {result.metadata.url.length > 50 ? result.metadata.url.substring(0, 50) + '...' : result.metadata.url}
                    </a>
                  </div>
                )}
              </div>

              {/* Actions */}
              <div className="flex items-center justify-between mt-3">
                <div className="flex items-center space-x-2">
                  {result.metadata?.url && (
                    <a 
                      href={result.metadata.url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:text-blue-800 text-sm flex items-center"
                    >
                      <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                      </svg>
                      Open Link
                    </a>
                  )}
                </div>
                
                {onDelete && result.metadata?.doc_id && (
                  <button
                    onClick={() => onDelete(result.metadata.doc_id)}
                    className="text-red-600 hover:text-red-800 text-sm flex items-center"
                  >
                    <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                    Delete
                  </button>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Citations */}
      {citations && citations.length > 0 && (
        <div className="bg-gray-50 rounded-lg p-4 border">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-lg font-semibold text-gray-900 flex items-center">
              <svg className="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Citations
            </h3>
            <button
              onClick={() => setShowCitations(!showCitations)}
              className="text-blue-600 hover:text-blue-800 text-sm"
            >
              {showCitations ? 'Hide' : 'Show'}
            </button>
          </div>
          
          {showCitations && (
            <div className="space-y-2">
              {citations.map((citation, index) => (
                <div key={index} className="text-sm text-gray-700 bg-white p-3 rounded border-l-4 border-blue-500">
                  <span className="font-medium text-blue-600">[{index + 1}]</span> {citation}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default SearchResults;
