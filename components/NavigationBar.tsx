'use client';

import { useState } from 'react';

export default function NavigationBar() {
  const [solutionsOpen, setSolutionsOpen] = useState(false);

  return (
    <nav className="bg-gray-900 border-b border-gray-800 sticky top-0 z-50 backdrop-blur-md bg-opacity-95">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-cyan-400 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">N</span>
            </div>
            <span className="text-xl font-bold text-white">NexSupply</span>
          </div>

          {/* Menu Items */}
          <div className="hidden md:flex items-center space-x-8">
            {/* Solutions Dropdown */}
            <div 
              className="relative"
              onMouseEnter={() => setSolutionsOpen(true)}
              onMouseLeave={() => setSolutionsOpen(false)}
            >
              <button className="text-gray-300 hover:text-white transition-colors flex items-center space-x-1">
                <span>Solutions</span>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              
              {solutionsOpen && (
                <div className="absolute top-full left-0 mt-2 w-64 bg-gray-800 border border-gray-700 rounded-lg shadow-xl py-2">
                  <a href="#fba" className="block px-4 py-2 text-gray-300 hover:bg-gray-700 hover:text-white transition-colors">
                    For FBA
                  </a>
                  <a href="#brands" className="block px-4 py-2 text-gray-300 hover:bg-gray-700 hover:text-white transition-colors">
                    For Brands
                  </a>
                  <a href="#enterprise" className="block px-4 py-2 text-gray-300 hover:bg-gray-700 hover:text-white transition-colors">
                    For Enterprise
                  </a>
                </div>
              )}
            </div>

            <a href="#pricing" className="text-gray-300 hover:text-white transition-colors">Pricing</a>
            <a href="#resources" className="text-gray-300 hover:text-white transition-colors">Resources</a>
          </div>

          {/* CTA Buttons */}
          <div className="flex items-center space-x-4">
            <a 
              href="mailto:outreach@nexsupply.net"
              className="text-gray-300 hover:text-white transition-colors hidden sm:block"
            >
              Log In
            </a>
            <a 
              href="mailto:outreach@nexsupply.net"
              className="bg-gradient-to-r from-blue-500 to-cyan-400 text-white px-6 py-2 rounded-lg font-medium hover:from-blue-600 hover:to-cyan-500 transition-all shadow-lg shadow-blue-500/50 inline-block"
            >
              Start Sourcing Free
            </a>
          </div>
        </div>
      </div>
    </nav>
  );
}

