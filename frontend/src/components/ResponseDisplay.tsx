import React from 'react';

interface SearchResponse {
  query: string;
  search_type: string;
  results: any[];
  total_results: number;
  response_time: number;
  sources: any[];
  citations: string[];
  confidence: number;
  quality: string;
}

interface ResponseDisplayProps {
  response: SearchResponse;
}

const ResponseDisplay: React.FC<ResponseDisplayProps> = ({ response }) => {
  const getQualityColor = (quality: string) => {
    switch (quality) {
      case 'high':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low':
        return 'bg-red-100 text-red-800 border-red-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return 'text-green-600';
    if (confidence >= 0.6) return 'text-yellow-600';
    if (confidence >= 0.4) return 'text-orange-600';
    return 'text-red-600';
  };

  const getSearchTypeIcon = (searchType: string) => {
    switch (searchType) {
      case 'document':
        return (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        );
      case 'web':
        return (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9-9a9 9 0 00-9 9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
          </svg>
        );
      case 'hybrid':
        return (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        );
      default:
        return null;
    }
  };

  return (
    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-lg font-semibold text-blue-900 flex items-center">
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          Search Summary
        </h3>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
        {/* Search Type */}
        <div className="flex items-center space-x-2">
          <div className="text-blue-600">
            {getSearchTypeIcon(response.search_type)}
          </div>
          <div>
            <p className="text-sm font-medium text-gray-900">Search Type</p>
            <p className="text-sm text-gray-600 capitalize">{response.search_type}</p>
          </div>
        </div>

        {/* Results Count */}
        <div className="flex items-center space-x-2">
          <div className="text-blue-600">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
            </svg>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-900">Results</p>
            <p className="text-sm text-gray-600">{response.total_results} found</p>
          </div>
        </div>

        {/* Response Time */}
        <div className="flex items-center space-x-2">
          <div className="text-blue-600">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-900">Response Time</p>
            <p className="text-sm text-gray-600">{response.response_time.toFixed(2)}s</p>
          </div>
        </div>

        {/* Sources */}
        <div className="flex items-center space-x-2">
          <div className="text-blue-600">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
            </svg>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-900">Sources</p>
            <p className="text-sm text-gray-600">{response.sources.length} unique</p>
          </div>
        </div>
      </div>

      {/* Quality and Confidence */}
      <div className="flex items-center space-x-4">
        <div className={`px-3 py-1 rounded-full text-sm font-medium border ${getQualityColor(response.quality)}`}>
          Quality: {response.quality}
        </div>
        <div className="flex items-center space-x-2">
          <span className="text-sm font-medium text-gray-700">Confidence:</span>
          <div className="flex items-center space-x-1">
            <span className={`text-sm font-bold ${getConfidenceColor(response.confidence)}`}>
              {Math.round(response.confidence * 100)}%
            </span>
            <div className="w-20 bg-gray-200 rounded-full h-2">
              <div 
                className={`h-2 rounded-full ${response.confidence >= 0.8 ? 'bg-green-500' : 
                  response.confidence >= 0.6 ? 'bg-yellow-500' : 
                  response.confidence >= 0.4 ? 'bg-orange-500' : 'bg-red-500'}`}
                style={{ width: `${response.confidence * 100}%` }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Query */}
      <div className="mt-3 pt-3 border-t border-blue-200">
        <p className="text-sm text-gray-600 mb-1">Query:</p>
        <p className="text-sm font-medium text-gray-900 bg-white px-3 py-2 rounded border">
          "{response.query}"
        </p>
      </div>
    </div>
  );
};

export default ResponseDisplay;
