export default function ValueProposition() {
  return (
    <section id="solutions" className="bg-gray-800 py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            One Platform, Every Sourcing Scenario.
          </h2>
          <p className="text-xl text-gray-400 max-w-2xl mx-auto">
            Built for e-commerce brands, FBA sellers, and enterprise procurement teams.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {/* For E-commerce Brands */}
          <div className="bg-gray-900 border border-gray-700 rounded-xl p-8 hover:border-cyan-400 transition-colors">
            <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg flex items-center justify-center mb-6">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
              </svg>
            </div>
            <h3 className="text-2xl font-bold mb-3">For E-commerce Brands</h3>
            <p className="text-gray-400 leading-relaxed">
              Optimize margins with precise DDP calculations including packaging & duties.
              Make data-driven sourcing decisions for your Shopify, WooCommerce, or custom storefront.
            </p>
          </div>

          {/* For FBA Sellers */}
          <div className="bg-gray-900 border border-gray-700 rounded-xl p-8 hover:border-orange-400 transition-colors">
            <div className="w-12 h-12 bg-gradient-to-br from-orange-500 to-yellow-500 rounded-lg flex items-center justify-center mb-6">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
            </div>
            <h3 className="text-2xl font-bold mb-3">For FBA Sellers</h3>
            <p className="text-gray-400 leading-relaxed">
              Real-time fee calculators and Q4 inventory planning to protect your ROI.
              Navigate Amazon FBA complexities with confidence.
            </p>
          </div>

          {/* For Enterprise Buyers */}
          <div className="bg-gray-900 border border-gray-700 rounded-xl p-8 hover:border-blue-400 transition-colors">
            <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center mb-6">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 className="text-2xl font-bold mb-3">For Enterprise Buyers</h3>
            <p className="text-gray-400 leading-relaxed">
              Bulk CSV analysis, supplier verification, and PDF RFQ generation for teams.
              Scale your procurement operations with enterprise-grade tools.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}

