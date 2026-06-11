import React, { useState, useEffect } from 'react'
import StockCard from './StockCard'
import FilterPanel from './FilterPanel'
import MacroIndicator from './MacroIndicator'
import ModeToggle from './ModeToggle'

function ScreenerDashboard({ onStockSelect, mode, onModeChange }) {
  const [stocks, setStocks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [universe, setUniverse] = useState('default')
  const [filters, setFilters] = useState({
    minScore: 30,
    maxMarketCap: null,
    sectors: []
  })
  const [macroData, setMacroData] = useState(null)

  const fetchStocks = async () => {
    setLoading(true)
    setError(null)
    try {
      const params = new URLSearchParams()
      params.append('min_score', filters.minScore)
      params.append('limit', 50)
      params.append('mode', mode)
      params.append('universe', universe)
      
      if (filters.maxMarketCap) {
        params.append('max_market_cap', filters.maxMarketCap)
      }
      if (filters.sectors.length > 0) {
        params.append('sectors', filters.sectors.join(','))
      }

      const response = await fetch(`/api/screen?${params.toString()}`)
      if (!response.ok) throw new Error('Failed to fetch stocks')
      
      const data = await response.json()
      setStocks(data.results || [])
      setMacroData(data.macro_environment)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchStocks()
  }, [mode])

  const handleApplyFilters = () => {
    fetchStocks()
  }

  const handleModeChange = (newMode) => {
    onModeChange(newMode)
  }

  const getModeDescription = () => {
    if (mode === 'multibagger') {
      return 'Finding 10x+ return potential with small-cap, deep value, contrarian entry'
    }
    return 'Finding consistent 15%+ CAGR with wide moat, owner-operators, buybacks'
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <ModeToggle mode={mode} onModeChange={handleModeChange} />
        <p className="text-sm text-gray-400">{getModeDescription()}</p>
      </div>

      {macroData && <MacroIndicator macroData={macroData} />}
      
      <FilterPanel 
        filters={filters} 
        setFilters={setFilters} 
        onApply={handleApplyFilters}
        loading={loading}
        universe={universe}
        onUniverseChange={setUniverse}
      />

      {loading && (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500"></div>
        </div>
      )}

      {error && (
        <div className="bg-red-900/50 border border-red-700 text-red-300 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      {!loading && !error && (
        <>
          <div className="flex justify-between items-center">
            <h2 className="text-lg font-semibold">
              {stocks.length} Stocks Found
            </h2>
            <span className="text-sm text-gray-400">
              Sorted by {mode === 'multibagger' ? 'Multibagger' : 'Compounder'} Score
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {stocks.map((stock) => (
              <StockCard 
                key={stock.ticker} 
                stock={stock} 
                onClick={() => onStockSelect(stock.ticker)}
                mode={mode}
              />
            ))}
          </div>

          {stocks.length === 0 && (
            <div className="text-center py-12 text-gray-400">
              No stocks match your criteria. Try adjusting the filters.
            </div>
          )}
        </>
      )}
    </div>
  )
}

export default ScreenerDashboard
