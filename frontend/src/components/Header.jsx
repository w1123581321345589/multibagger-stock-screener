import React from 'react'

function Header({ onBackToScreener, showBack }) {
  return (
    <header className="bg-gray-800 border-b border-gray-700 py-4">
      <div className="container mx-auto px-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          {showBack && (
            <button
              onClick={onBackToScreener}
              className="text-gray-400 hover:text-white transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
            </button>
          )}
          <div>
            <h1 className="text-xl font-bold text-white">Multibagger Stock Screener</h1>
            <p className="text-sm text-gray-400">Find stocks with 10x+ return potential</p>
          </div>
        </div>
        <div className="text-sm text-gray-500">
          Based on "The Alchemy of Multibagger Stocks" research
        </div>
      </div>
    </header>
  )
}

export default Header
