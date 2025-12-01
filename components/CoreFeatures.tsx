export default function CoreFeatures() {
  return (
    <section className="bg-gray-900 py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            The Engine Behind Smart Sourcing
          </h2>
          <p className="text-xl text-gray-400 max-w-2xl mx-auto">
            Three core capabilities that make the difference.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {/* True Landed Cost */}
          <div className="bg-gradient-to-br from-gray-800 to-gray-900 border border-gray-700 rounded-xl p-8">
            <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-500 rounded-lg flex items-center justify-center mb-6">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h3 className="text-2xl font-bold mb-3">True Landed Cost</h3>
            <p className="text-gray-400 leading-relaxed mb-4">
              Factor in tariffs (Section 301), freight rates, and hidden port fees automatically.
              No surprises at customs.
            </p>
            <ul className="space-y-2 text-sm text-gray-500">
              <li className="flex items-center">
                <span className="text-green-400 mr-2">✓</span>
                Section 301 Tariff Calculations
              </li>
              <li className="flex items-center">
                <span className="text-green-400 mr-2">✓</span>
                Real-time Freight Rates
              </li>
              <li className="flex items-center">
                <span className="text-green-400 mr-2">✓</span>
                Port & Handling Fees
              </li>
            </ul>
          </div>

          {/* Regulatory Shield */}
          <div className="bg-gradient-to-br from-gray-800 to-gray-900 border border-gray-700 rounded-xl p-8">
            <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center mb-6">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <h3 className="text-2xl font-bold mb-3">Regulatory Shield</h3>
            <p className="text-gray-400 leading-relaxed mb-4">
              AI-driven checks for FDA, CPSC, and labeling requirements before you import.
              Stay compliant from day one.
            </p>
            <ul className="space-y-2 text-sm text-gray-500">
              <li className="flex items-center">
                <span className="text-blue-400 mr-2">✓</span>
                FDA Registration Checks
              </li>
              <li className="flex items-center">
                <span className="text-blue-400 mr-2">✓</span>
                CPSC/CPC Certification
              </li>
              <li className="flex items-center">
                <span className="text-blue-400 mr-2">✓</span>
                Labeling Requirements
              </li>
            </ul>
          </div>

          {/* Supplier Vetting */}
          <div className="bg-gradient-to-br from-gray-800 to-gray-900 border border-gray-700 rounded-xl p-8">
            <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg flex items-center justify-center mb-6">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <h3 className="text-2xl font-bold mb-3">Supplier Vetting</h3>
            <p className="text-gray-400 leading-relaxed mb-4">
              Verify factory credentials and predict lead times based on real-time logistics data.
              De-risk your supply chain.
            </p>
            <ul className="space-y-2 text-sm text-gray-500">
              <li className="flex items-center">
                <span className="text-purple-400 mr-2">✓</span>
                Factory Verification
              </li>
              <li className="flex items-center">
                <span className="text-purple-400 mr-2">✓</span>
                Lead Time Predictions
              </li>
              <li className="flex items-center">
                <span className="text-purple-400 mr-2">✓</span>
                Quality Score Analysis
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}

