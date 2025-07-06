import React, { useState } from 'react';

interface SearchFormProps {
  onSearch: (query: string, searchType: string, options: any) => void;
  loading?: boolean;
}

const SearchForm: React.FC<SearchFormProps> = ({ onSearch, loading = false }) => {
  const [query, setQuery] = useState('');
  const [searchType, setSearchType] = useState('hybrid');
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [advancedOptions, setAdvancedOptions] = useState({
    k: 5,
    source_filter: '',
    min_credibility: 0.5,
    enable_cache: true
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    
    onSearch(query, searchType, {
      ...advancedOptions,
      source_filter: advancedOptions.source_filter || null
    });
  };

  const handleAdvancedChange = (key: string, value: any) => {
    setAdvancedOptions(prev => ({ ...prev, [key]: value }));
  };

  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Main Search Input */}
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search documents, web, or both..."
            className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent placeholder-gray-500 text-lg"
            disabled={loading}
          />
        </div>

        {/* Search Type Selection */}
        <div className="flex space-x-4">
          {['document', 'web', 'hybrid'].map((type) => (
            <label key={type} className="flex items-center">
              <input
                type="radio"
                name="searchType"
                value={type}
                checked={searchType === type}
                onChange={(e) => setSearchType(e.target.value)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300"
                disabled={loading}
              />
              <span className="ml-2 text-sm font-medium text-gray-700 capitalize">
                {type === 'hybrid' ? 'Hybrid (Documents + Web)' : type}
              </span>
            </label>
          ))}
        </div>

        {/* Advanced Options Toggle */}
        <div className="flex items-center justify-between">
          <button
            type="button"
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="text-sm text-blue-600 hover:text-blue-800 flex items-center"
          >
            <svg className={`h-4 w-4 mr-1 transform transition-transform ${showAdvanced ? 'rotate-90' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
            Advanced Options
          </button>
          
          <button
            type="submit"
            disabled={!query.trim() || loading}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center"
          >
            {loading ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="m100 50l-5.5 9.5h-11l-5.5-9.5 5.5-9.5h11l5.5 9.5z" />
                </svg>
                Searching...
              </>
            ) : (
              'Search'
            )}
          </button>
        </div>

        {/* Advanced Options Panel */}
        {showAdvanced && (
          <div className="bg-gray-50 p-4 rounded-lg border space-y-4">
            <h4 className="font-medium text-gray-900">Advanced Search Options</h4>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Number of Results */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Number of Results
                </label>
                <select
                  value={advancedOptions.k}
                  onChange={(e) => handleAdvancedChange('k', parseInt(e.target.value))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value={3}>3</option>
                  <option value={5}>5</option>
                  <option value={10}>10</option>
                  <option value={15}>15</option>
                  <option value={20}>20</option>
                </select>
              </div>

              {/* Source Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Source Filter
                </label>
                <input
                  type="text"
                  value={advancedOptions.source_filter}
                  onChange={(e) => handleAdvancedChange('source_filter', e.target.value)}
                  placeholder="Filter by source (e.g., filename)"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              {/* Minimum Credibility */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Minimum Credibility: {advancedOptions.min_credibility}
                </label>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.1"
                  value={advancedOptions.min_credibility}
                  onChange={(e) => handleAdvancedChange('min_credibility', parseFloat(e.target.value))}
                  className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                />
              </div>

              {/* Enable Cache */}
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="enable_cache"
                  checked={advancedOptions.enable_cache}
                  onChange={(e) => handleAdvancedChange('enable_cache', e.target.checked)}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label htmlFor="enable_cache" className="ml-2 block text-sm text-gray-700">
                  Enable caching
                </label>
              </div>
            </div>
          </div>
        )}
      </form>

      {/* Search Type Descriptions */}
      <div className="text-xs text-gray-500 bg-gray-50 p-3 rounded-lg">
        <div className="space-y-1">
          <div><strong>Document:</strong> Search only uploaded PDF documents using semantic similarity</div>
          <div><strong>Web:</strong> Search the internet for current information</div>
          <div><strong>Hybrid:</strong> Combine document and web search with intelligent ranking</div>
        </div>
      </div>
    </div>
  );
};

export default SearchForm;
