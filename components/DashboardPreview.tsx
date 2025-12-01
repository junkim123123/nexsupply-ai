'use client';

export default function DashboardPreview() {
  return (
    <section className="bg-gray-800 py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            Mission Control
          </h2>
          <p className="text-xl text-gray-400 max-w-2xl mx-auto">
            Real-time insights across all your sourcing channels.
          </p>
        </div>

        {/* World Map Background */}
        <div className="relative bg-gray-900 rounded-2xl p-8 mb-12 border border-gray-700 overflow-hidden">
          <div className="absolute inset-0 opacity-20">
            {/* Simplified World Map Visualization */}
            <svg viewBox="0 0 1200 600" className="w-full h-full">
              {/* Routes */}
              <path
                d="M 300 200 Q 400 150 500 200"
                stroke="url(#gradient1)"
                strokeWidth="3"
                fill="none"
                className="animate-pulse"
              />
              <path
                d="M 200 250 Q 350 200 550 250"
                stroke="url(#gradient2)"
                strokeWidth="3"
                fill="none"
                className="animate-pulse"
                style={{ animationDelay: '0.5s' }}
              />
              <path
                d="M 800 300 Q 900 250 1000 300"
                stroke="url(#gradient3)"
                strokeWidth="3"
                fill="none"
                className="animate-pulse"
                style={{ animationDelay: '1s' }}
              />
              
              <defs>
                <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#a855f7" />
                  <stop offset="100%" stopColor="#ec4899" />
                </linearGradient>
                <linearGradient id="gradient2" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#10b981" />
                  <stop offset="100%" stopColor="#06b6d4" />
                </linearGradient>
                <linearGradient id="gradient3" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#06b6d4" />
                  <stop offset="100%" stopColor="#a855f7" />
                </linearGradient>
              </defs>
            </svg>
          </div>
          
          {/* Route Labels */}
          <div className="relative z-10 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-8">
            <div className="bg-gray-800 border border-purple-500/50 rounded-lg p-4 backdrop-blur-sm">
              <div className="flex items-center space-x-2 mb-2">
                <div className="w-3 h-3 bg-purple-500 rounded-full animate-pulse"></div>
                <span className="text-sm text-gray-400">China to US (West Coast)</span>
              </div>
            </div>
            <div className="bg-gray-800 border border-green-500/50 rounded-lg p-4 backdrop-blur-sm">
              <div className="flex items-center space-x-2 mb-2">
                <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-sm text-gray-400">India to US (East Coast)</span>
              </div>
            </div>
            <div className="bg-gray-800 border border-cyan-500/50 rounded-lg p-4 backdrop-blur-sm">
              <div className="flex items-center space-x-2 mb-2">
                <div className="w-3 h-3 bg-cyan-500 rounded-full animate-pulse"></div>
                <span className="text-sm text-gray-400">Vietnam to EU (Rotterdam)</span>
              </div>
            </div>
          </div>
        </div>

        {/* Dashboard Widgets */}
        <div className="grid md:grid-cols-3 gap-6">
          {/* Multi-Channel Margin Comparison */}
          <div className="bg-gray-900 border border-gray-700 rounded-xl p-6">
            <h3 className="text-lg font-semibold mb-4">Multi-Channel Margin Comparison</h3>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm text-gray-400">Amazon FBA</span>
                  <span className="text-green-400 font-semibold flex items-center">
                    22% ↗
                  </span>
                </div>
                <div className="w-full bg-gray-800 rounded-full h-3">
                  <div className="bg-gradient-to-r from-green-500 to-emerald-500 h-3 rounded-full" style={{ width: '22%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm text-gray-400">Shopify DTC</span>
                  <span className="text-green-400 font-semibold flex items-center">
                    35% ↗
                  </span>
                </div>
                <div className="w-full bg-gray-800 rounded-full h-3">
                  <div className="bg-gradient-to-r from-green-500 to-emerald-500 h-3 rounded-full" style={{ width: '35%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm text-gray-400">Wholesale B2B</span>
                  <span className="text-green-400 font-semibold flex items-center">
                    18% ↗
                  </span>
                </div>
                <div className="w-full bg-gray-800 rounded-full h-3">
                  <div className="bg-gradient-to-r from-green-500 to-emerald-500 h-3 rounded-full" style={{ width: '18%' }}></div>
                </div>
              </div>
            </div>
          </div>

          {/* Supplier Risk Score */}
          <div className="bg-gray-900 border border-gray-700 rounded-xl p-6">
            <h3 className="text-lg font-semibold mb-4">Supplier Risk Score</h3>
            <div className="flex flex-col items-center justify-center py-4">
              <div className="relative w-32 h-32 mb-4">
                <svg className="transform -rotate-90 w-32 h-32">
                  <circle
                    cx="64"
                    cy="64"
                    r="56"
                    stroke="currentColor"
                    strokeWidth="8"
                    fill="none"
                    className="text-gray-800"
                  />
                  <circle
                    cx="64"
                    cy="64"
                    r="56"
                    stroke="url(#riskGradient)"
                    strokeWidth="8"
                    fill="none"
                    strokeDasharray={`${85 * 3.14} ${100 * 3.14}`}
                    strokeLinecap="round"
                  />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-3xl font-bold text-white">85</span>
                </div>
                <defs>
                  <linearGradient id="riskGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#a855f7" />
                    <stop offset="100%" stopColor="#10b981" />
                  </linearGradient>
                </defs>
              </div>
              <span className="text-green-400 font-semibold">Low Risk</span>
              <div className="mt-4 space-y-2 text-sm text-gray-400">
                <div>✓ Financial Health</div>
                <div>✓ Quality Control</div>
                <div>✓ Geopolitical Stability</div>
              </div>
            </div>
          </div>

          {/* Real-time Tariff Alerts */}
          <div className="bg-gray-900 border border-gray-700 rounded-xl p-6">
            <h3 className="text-lg font-semibold mb-4">Real-time Tariff Alerts</h3>
            <div className="space-y-3">
              <div className="flex items-start space-x-3 p-3 bg-red-500/10 border border-red-500/30 rounded-lg">
                <div className="w-2 h-2 bg-red-500 rounded-full mt-2"></div>
                <div className="flex-1">
                  <p className="text-sm font-medium">US-China Tariff Update</p>
                  <p className="text-xs text-gray-400">+$5 on Electronics</p>
                </div>
              </div>
              <div className="flex items-start space-x-3 p-3 bg-blue-500/10 border border-blue-500/30 rounded-lg">
                <div className="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                <div className="flex-1">
                  <p className="text-sm font-medium">EU Carbon Border Tax</p>
                  <p className="text-xs text-gray-400">Imminent: EU Carbon Post Update</p>
                </div>
              </div>
              <div className="flex items-start space-x-3 p-3 bg-orange-500/10 border border-orange-500/30 rounded-lg">
                <div className="w-2 h-2 bg-orange-500 rounded-full mt-2"></div>
                <div className="flex-1">
                  <p className="text-sm font-medium">Vietnam Port Congestion</p>
                  <p className="text-xs text-gray-400">Vietnam Port Congestion Alert</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

