'use client';

import { useSearchParams } from 'next/navigation';
import { useEffect, useState, Suspense } from 'react';

function AnalysisContent() {
  const searchParams = useSearchParams();
  const product = searchParams.get('product');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate loading time
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1000);
    return () => clearTimeout(timer);
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-400">Loading analysis...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Analysis Results</h1>
          <p className="text-gray-400">
            Analysis for: <span className="text-blue-400 font-semibold">{product || 'Unknown Product'}</span>
          </p>
        </div>

        {/* Results Placeholder */}
        <div className="bg-gray-800 rounded-lg p-8 border border-gray-700">
          <h2 className="text-2xl font-semibold mb-4">Product Analysis</h2>
          <p className="text-gray-400 mb-4">
            This is a placeholder page. Connect to your Streamlit backend or API to display real analysis results.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
            <div className="bg-gray-700/50 rounded-lg p-6">
              <h3 className="text-lg font-semibold mb-2">Cost Breakdown</h3>
              <p className="text-gray-400 text-sm">Manufacturing, shipping, and duty costs will appear here.</p>
            </div>
            
            <div className="bg-gray-700/50 rounded-lg p-6">
              <h3 className="text-lg font-semibold mb-2">Risk Assessment</h3>
              <p className="text-gray-400 text-sm">Regulatory and compliance risks will appear here.</p>
            </div>
            
            <div className="bg-gray-700/50 rounded-lg p-6">
              <h3 className="text-lg font-semibold mb-2">Market Insights</h3>
              <p className="text-gray-400 text-sm">Market analysis and competition data will appear here.</p>
            </div>
          </div>
        </div>

        {/* Back Button */}
        <div className="mt-8">
          <button
            onClick={() => window.history.back()}
            className="bg-gray-800 hover:bg-gray-700 text-white px-6 py-3 rounded-lg transition-colors"
          >
            ← Back to Home
          </button>
        </div>
      </div>
    </div>
  );
}

export default function AnalysisPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-400">Loading...</p>
        </div>
      </div>
    }>
      <AnalysisContent />
    </Suspense>
  );
}

