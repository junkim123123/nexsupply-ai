'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function HeroSection() {
  const router = useRouter();
  const [productInput, setProductInput] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [loadingText, setLoadingText] = useState('🔍 Searching global suppliers...');

  // 로딩 텍스트 롤링 효과
  useEffect(() => {
    if (isAnalyzing) {
      const texts = [
        '🔍 Searching global suppliers...',
        '🚢 Calculating freight rates...',
        '⚖️ Checking FDA & Customs risks...',
        '💰 Finalizing profit margins...'
      ];
      
      let i = 0;
      const interval = setInterval(() => {
        setLoadingText(texts[i % texts.length]);
        i++;
      }, 800); // 0.8초마다 텍스트 변경

      return () => clearInterval(interval);
    }
  }, [isAnalyzing]);

  const handleAnalyze = () => {
    const trimmedInput = productInput.trim();
    
    if (!trimmedInput) {
      return;
    }

    if (isAnalyzing) {
      return;
    }

    // 로딩 상태 시작
    setIsAnalyzing(true);

    // 2.5초 뒤에 결과 페이지로 이동
    const url = `/analysis?product=${encodeURIComponent(trimmedInput)}`;
    
    setTimeout(() => {
      router.push(url);
    }, 2500);
  };

  return (
    <section className="relative bg-gradient-to-b from-gray-900 via-gray-900 to-gray-800 py-20 lg:py-32 overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute inset-0" style={{
          backgroundImage: `radial-gradient(circle at 2px 2px, rgba(255,255,255,0.15) 1px, transparent 0)`,
          backgroundSize: '40px 40px'
        }}></div>
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          {/* Main Headline */}
          <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold mb-6 bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
            Global Sourcing Intelligence.
            <br />
            <span className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
              Simplified.
            </span>
          </h1>

          {/* Subheadline */}
          <p className="text-xl md:text-2xl text-gray-400 mb-8 max-w-3xl mx-auto">
            Analyze products, calculate true landed costs, and detect compliance risks in seconds.
            <br />
            Whether you sell on <span className="text-orange-400 font-semibold">Amazon</span>,{' '}
            <span className="text-cyan-400 font-semibold">Shopify</span>, or{' '}
            <span className="text-blue-400 font-semibold">B2B Wholesale</span>.
          </p>

          {/* Search Form Area (Input + Button) */}
          <div className="max-w-2xl mx-auto mb-6 relative z-20">
            <div className="flex flex-col sm:flex-row gap-3 w-full">
              {/* Input Field */}
              <input
                type="text"
                placeholder="e.g., Yoga Mat, Silicone Spatula"
                value={productInput}
                onChange={(e) => setProductInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !isAnalyzing && productInput.trim()) {
                    e.preventDefault();
                    handleAnalyze();
                  }
                }}
                disabled={isAnalyzing}
                aria-label="Product name input"
                className="flex-1 px-6 py-4 rounded-xl bg-slate-800/80 border border-slate-700 text-white text-lg focus:ring-2 focus:ring-blue-500 focus:outline-none focus:bg-slate-800 transition-all placeholder:text-slate-500 disabled:opacity-50 backdrop-blur-sm"
              />

              {/* Analyze Button */}
              <button
                type="button"
                disabled={isAnalyzing}
                onClick={handleAnalyze}
                aria-label="Analyze product"
                className={`
                  relative overflow-hidden px-8 py-4 rounded-xl font-bold text-lg text-white transition-all duration-300
                  bg-gradient-to-r from-red-500 to-pink-600 shadow-lg
                  ${isAnalyzing
                    ? 'opacity-90 cursor-wait brightness-90'
                    : 'hover:scale-105 hover:shadow-red-500/25 active:scale-95 cursor-pointer'
                  }
                  min-w-[180px] h-[60px] flex items-center justify-center whitespace-nowrap
                `}
              >
              <div className="relative z-10 flex items-center gap-2">
                {isAnalyzing ? (
                  <>
                    <svg
                      className="animate-spin h-5 w-5 text-white"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                    >
                      <circle
                        className="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        strokeWidth="4"
                      ></circle>
                      <path
                        className="opacity-100"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                      ></path>
                    </svg>
                    <span className="font-semibold text-base">{loadingText}</span>
                  </>
                ) : (
                  <>
                    <span>Analyze Now</span>
                    <span className="text-xl">🚀</span>
                  </>
                )}
              </div>

              {/* Loading Progress Bar Overlay */}
              {isAnalyzing && (
                <div className="absolute bottom-0 left-0 h-1 bg-white/40 w-full">
                  <div
                    className="h-full bg-white/90"
                    style={{ width: '100%', animation: 'progress 2s ease-in-out infinite' }}
                  ></div>
                </div>
              )}
            </button>
            </div>
          </div>

          {/* Tagline */}
          <p className="text-gray-500 text-sm">
            Your AI Sourcing Agent for the Modern Supply Chain.
          </p>
        </div>
      </div>
    </section>
  );
}

