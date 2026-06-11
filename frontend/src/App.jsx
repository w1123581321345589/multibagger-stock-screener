import React, { useState, useEffect } from 'react'
import ScreenerDashboard from './components/ScreenerDashboard'
import StockDetail from './components/StockDetail'
import Header from './components/Header'

function App() {
  const [view, setView] = useState('screener')
  const [selectedStock, setSelectedStock] = useState(null)
  const [mode, setMode] = useState('multibagger')

  const handleStockSelect = (ticker) => {
    setSelectedStock(ticker)
    setView('detail')
  }

  const handleBackToScreener = () => {
    setView('screener')
    setSelectedStock(null)
  }

  const handleModeChange = (newMode) => {
    setMode(newMode)
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Header onBackToScreener={handleBackToScreener} showBack={view === 'detail'} />
      <main className="container mx-auto px-4 py-6">
        {view === 'screener' ? (
          <ScreenerDashboard onStockSelect={handleStockSelect} mode={mode} onModeChange={handleModeChange} />
        ) : (
          <StockDetail ticker={selectedStock} onBack={handleBackToScreener} mode={mode} />
        )}
      </main>
    </div>
  )
}

export default App
