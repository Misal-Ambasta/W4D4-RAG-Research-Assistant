import React from 'react';

interface SearchHistoryItem {
  query: string;
  results_count: number;
  timestamp: string;
}

interface SearchHistoryProps {
  history: SearchHistoryItem[];
  onSearch: (query: string, searchType: string) => void;
}

const SearchHistory: React.FC<SearchHistoryProps> = ({ history, onSearch }) => {
  if (!history || history.length === 0) {
    return (
      <div className="text-center py-6 text-gray-500">
        <svg className="w-12 h-12 mx-auto mb-2 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p className="text-sm">No search history yet</p>
      </div>
    );
  }

  const formatTimestamp = (timestamp: string) => {
    try {
      const date = new Date(timestamp);
      return date.toLocaleString();
    } catch {
      return timestamp;
    }
  };

  const getTimeAgo = (timestamp: string) => {
    try {
      const date = new Date(timestamp);
      const now = new Date();
      const diffMs = now.getTime() - date.getTime();
      const diffMins = Math.floor(diffMs / 60000);
      const diffHours = Math.floor(diffMins / 60);
      const diffDays = Math.floor(diffHours / 24);

      if (diffMins < 1) return 'Just now';
      if (diffMins < 60) return `${diffMins}m ago`;
      if (diffHours < 24) return `${diffHours}h ago`;
      if (diffDays === 1) return 'Yesterday';
      return `${diffDays}d ago`;
    } catch {
      return '';
    }
  };

  const handleHistoryClick = (query: string) => {
    onSearch(query, 'hybrid');
  };

  return (
    <div className="max-h-96 overflow-y-auto">
      <div className="space-y-2">
        {history.slice().reverse().map((item, index) => (
          <div
            key={index}
            className="bg-white border border-gray-200 rounded-lg p-3 hover:shadow-sm transition-shadow cursor-pointer"
            onClick={() => handleHistoryClick(item.query)}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {item.query}
                </p>
                <div className="flex items-center space-x-2 mt-1">
                  <span className="text-xs text-gray-500">
                    {item.results_count} results
                  </span>
                  <span className="text-xs text-gray-400">•</span>
                  <span className="text-xs text-gray-500">
                    {getTimeAgo(item.timestamp)}
                  </span>
                </div>
              </div>
              <div className="flex items-center space-x-1 ml-2">
                <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>
          </div>
        ))}
      </div>
      
      {history.length > 5 && (
        <div className="mt-3 text-center">
          <p className="text-xs text-gray-500">
            Showing recent searches
          </p>
        </div>
      )}
    </div>
  );
};

export default SearchHistory;
