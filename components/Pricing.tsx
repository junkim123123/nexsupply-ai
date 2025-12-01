export default function Pricing() {
  return (
    <section className="bg-gray-900 py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            Pricing for Scale
          </h2>
          <p className="text-xl text-gray-400 max-w-2xl mx-auto">
            Choose the plan that fits your sourcing volume.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {/* Starter */}
          <div className="bg-gray-800 border border-gray-700 rounded-xl p-8">
            <h3 className="text-2xl font-bold mb-2">Starter</h3>
            <p className="text-gray-400 mb-6">For solo entrepreneurs</p>
            <div className="mb-6">
              <span className="text-4xl font-bold">$29</span>
              <span className="text-gray-400">/month</span>
            </div>
            <ul className="space-y-3 mb-8">
              <li className="flex items-center text-gray-300">
                <span className="text-green-400 mr-2">✓</span>
                50 analyses/month
              </li>
              <li className="flex items-center text-gray-300">
                <span className="text-green-400 mr-2">✓</span>
                Basic cost calculator
              </li>
              <li className="flex items-center text-gray-300">
                <span className="text-green-400 mr-2">✓</span>
                Single channel (FBA/B2B/DTC)
              </li>
              <li className="flex items-center text-gray-300">
                <span className="text-green-400 mr-2">✓</span>
                Email support
              </li>
            </ul>
            <button className="w-full bg-gray-700 hover:bg-gray-600 text-white py-3 rounded-lg font-medium transition-colors">
              Start Free Trial
            </button>
          </div>

          {/* Growth */}
          <div className="bg-gradient-to-br from-blue-500/10 to-cyan-500/10 border-2 border-blue-500 rounded-xl p-8 relative">
            <div className="absolute top-0 right-0 bg-blue-500 text-white px-4 py-1 rounded-bl-lg rounded-tr-xl text-sm font-semibold">
              Most Popular
            </div>
            <h3 className="text-2xl font-bold mb-2">Growth</h3>
            <p className="text-gray-400 mb-6">For growing brands & FBA sellers</p>
            <div className="mb-6">
              <span className="text-4xl font-bold">$99</span>
              <span className="text-gray-400">/month</span>
            </div>
            <ul className="space-y-3 mb-8">
              <li className="flex items-center text-gray-300">
                <span className="text-blue-400 mr-2">✓</span>
                500 analyses/month
              </li>
              <li className="flex items-center text-gray-300">
                <span className="text-blue-400 mr-2">✓</span>
                Multi-channel comparison
              </li>
              <li className="flex items-center text-gray-300">
                <span className="text-blue-400 mr-2">✓</span>
                FBA fee calculator
              </li>
              <li className="flex items-center text-gray-300">
                <span className="text-blue-400 mr-2">✓</span>
                Compliance checks
              </li>
              <li className="flex items-center text-gray-300">
                <span className="text-blue-400 mr-2">✓</span>
                Priority support
              </li>
            </ul>
            <button className="w-full bg-gradient-to-r from-blue-500 to-cyan-400 text-white py-3 rounded-lg font-medium hover:from-blue-600 hover:to-cyan-500 transition-all shadow-lg shadow-blue-500/50">
              Start Free Trial
            </button>
          </div>

          {/* Corporate */}
          <div className="bg-gray-800 border border-gray-700 rounded-xl p-8">
            <h3 className="text-2xl font-bold mb-2">Corporate</h3>
            <p className="text-gray-400 mb-6">For procurement teams</p>
            <div className="mb-6">
              <span className="text-4xl font-bold">Custom</span>
            </div>
            <ul className="space-y-3 mb-8">
              <li className="flex items-center text-gray-300">
                <span className="text-purple-400 mr-2">✓</span>
                Unlimited analyses
              </li>
              <li className="flex items-center text-gray-300">
                <span className="text-purple-400 mr-2">✓</span>
                API access
              </li>
              <li className="flex items-center text-gray-300">
                <span className="text-purple-400 mr-2">✓</span>
                Bulk CSV analysis
              </li>
              <li className="flex items-center text-gray-300">
                <span className="text-purple-400 mr-2">✓</span>
                Multi-user accounts
              </li>
              <li className="flex items-center text-gray-300">
                <span className="text-purple-400 mr-2">✓</span>
                Dedicated support
              </li>
            </ul>
            <a 
              href="mailto:outreach@nexsupply.net"
              className="w-full bg-gray-700 hover:bg-gray-600 text-white py-3 rounded-lg font-medium transition-colors block text-center"
            >
              Contact Sales
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}

