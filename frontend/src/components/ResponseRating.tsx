import React, { useState } from 'react';

interface ResponseRatingProps {
  onRating: (rating: number, feedback?: string) => void;
}

const ResponseRating: React.FC<ResponseRatingProps> = ({ onRating }) => {
  const [rating, setRating] = useState<number>(0);
  const [feedback, setFeedback] = useState<string>('');
  const [submitted, setSubmitted] = useState<boolean>(false);
  const [showFeedback, setShowFeedback] = useState<boolean>(false);

  const handleStarClick = (value: number) => {
    setRating(value);
    if (value <= 3) {
      setShowFeedback(true);
    }
  };

  const handleSubmit = () => {
    if (rating > 0) {
      onRating(rating, feedback || undefined);
      setSubmitted(true);
      setTimeout(() => {
        setSubmitted(false);
        setRating(0);
        setFeedback('');
        setShowFeedback(false);
      }, 2000);
    }
  };

  const getRatingText = (value: number) => {
    switch (value) {
      case 1: return 'Poor';
      case 2: return 'Fair';
      case 3: return 'Good';
      case 4: return 'Very Good';
      case 5: return 'Excellent';
      default: return '';
    }
  };

  if (submitted) {
    return (
      <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
        <div className="flex items-center justify-center mb-2">
          <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <p className="text-green-800 font-medium">Thank you for your feedback!</p>
        <p className="text-green-600 text-sm">Your rating helps us improve our service.</p>
      </div>
    );
  }

  return (
    <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
      <div className="text-center mb-4">
        <h4 className="text-lg font-semibold text-gray-900 mb-2">Rate this response</h4>
        <p className="text-sm text-gray-600">How helpful was this search result?</p>
      </div>

      {/* Star Rating */}
      <div className="flex items-center justify-center space-x-1 mb-4">
        {[1, 2, 3, 4, 5].map((star) => (
          <button
            key={star}
            onClick={() => handleStarClick(star)}
            className={`w-8 h-8 transition-colors duration-200 ${
              star <= rating
                ? 'text-yellow-400 hover:text-yellow-500'
                : 'text-gray-300 hover:text-gray-400'
            }`}
          >
            <svg
              className="w-full h-full"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
          </button>
        ))}
      </div>

      {/* Rating Text */}
      {rating > 0 && (
        <div className="text-center mb-4">
          <span className="text-sm font-medium text-gray-700">
            {getRatingText(rating)}
          </span>
        </div>
      )}

      {/* Feedback Text Area */}
      {showFeedback && (
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Help us improve (optional):
          </label>
          <textarea
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
            placeholder="What could be better about this response?"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            rows={3}
          />
        </div>
      )}

      {/* Submit Button */}
      <div className="text-center">
        <button
          onClick={handleSubmit}
          disabled={rating === 0}
          className={`px-6 py-2 rounded-lg font-medium transition-colors ${
            rating > 0
              ? 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2'
              : 'bg-gray-300 text-gray-500 cursor-not-allowed'
          }`}
        >
          Submit Rating
        </button>
      </div>
    </div>
  );
};

export default ResponseRating;
