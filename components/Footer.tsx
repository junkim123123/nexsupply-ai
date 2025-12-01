export default function Footer() {
  return (
    <footer className="bg-gray-900 border-t border-gray-800 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          {/* Company */}
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-cyan-400 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">N</span>
              </div>
              <span className="text-xl font-bold text-white">NexSupply</span>
            </div>
            <p className="text-gray-400 text-sm mb-3">
              Global Sourcing Intelligence for the Modern Supply Chain.
            </p>
            <div className="space-y-2 text-sm">
              <a 
                href="https://nexsupply.net" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-white transition-colors block"
              >
                nexsupply.net
              </a>
              <a 
                href="mailto:outreach@nexsupply.net"
                className="text-gray-400 hover:text-white transition-colors block"
              >
                outreach@nexsupply.net
              </a>
            </div>
          </div>

          {/* Solutions */}
          <div>
            <h4 className="text-white font-semibold mb-4">Solutions</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              <li><a href="#fba" className="hover:text-white transition-colors">For FBA</a></li>
              <li><a href="#brands" className="hover:text-white transition-colors">For Brands</a></li>
              <li><a href="#enterprise" className="hover:text-white transition-colors">For Enterprise</a></li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h4 className="text-white font-semibold mb-4">Resources</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              <li><a href="mailto:outreach@nexsupply.net" className="hover:text-white transition-colors">API Docs</a></li>
              <li><a href="mailto:outreach@nexsupply.net" className="hover:text-white transition-colors">Blog</a></li>
              <li><a href="mailto:outreach@nexsupply.net" className="hover:text-white transition-colors">Help Center</a></li>
            </ul>
          </div>

          {/* Enterprise */}
          <div>
            <h4 className="text-white font-semibold mb-4">Enterprise</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              <li><a href="mailto:outreach@nexsupply.net" className="hover:text-white transition-colors">Enterprise Solutions</a></li>
              <li><a href="mailto:outreach@nexsupply.net" className="hover:text-white transition-colors">Partnership</a></li>
              <li><a href="mailto:outreach@nexsupply.net" className="hover:text-white transition-colors">Contact Sales</a></li>
            </ul>
          </div>
        </div>

        {/* CTA Section */}
        <div className="border-t border-gray-800 pt-8 mb-8 text-center">
          <p className="text-2xl font-bold mb-2 bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
            Smart. Simple. Supply.
          </p>
          <p className="text-gray-400 mb-4">Reach Out to NexSupply</p>
          <a 
            href="mailto:outreach@nexsupply.net"
            className="text-blue-400 hover:text-blue-300 text-lg font-medium transition-colors inline-block"
          >
            outreach@nexsupply.net
          </a>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-gray-800 pt-8 flex flex-col md:flex-row justify-between items-center">
          <p className="text-gray-400 text-sm">
            © 2025 NexSupply. All rights reserved.
          </p>
          <div className="flex space-x-6 mt-4 md:mt-0">
            <a href="mailto:outreach@nexsupply.net" className="text-gray-400 hover:text-white text-sm transition-colors">Privacy</a>
            <a href="mailto:outreach@nexsupply.net" className="text-gray-400 hover:text-white text-sm transition-colors">Terms</a>
            <a href="mailto:outreach@nexsupply.net" className="text-gray-400 hover:text-white text-sm transition-colors">Cookie Policy</a>
          </div>
        </div>
      </div>
    </footer>
  );
}

