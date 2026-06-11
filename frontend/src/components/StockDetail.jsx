import React, { useState, useEffect } from 'react'
import ScoreGauge from './ScoreGauge'
import FactorBreakdown from './FactorBreakdown'

function StockDetail({ ticker, onBack, mode = 'multibagger' }) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchStock = async () => {
      setLoading(true)
      try {
        const response = await fetch(`/api/stock/${ticker}?mode=${mode}`)
        if (!response.ok) throw new Error('Failed to fetch stock data')
        const result = await response.json()
        setData(result)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    if (ticker) fetchStock()
  }, [ticker, mode])

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-900/50 border border-red-700 text-red-300 px-4 py-3 rounded-lg">
        {error}
      </div>
    )
  }

  if (!data) return null

  const { stock_data, score_analysis } = data
  const formatMarketCap = (value) => {
    if (value == null || value === 0) return 'N/A'
    if (value >= 1e12) return `$${(value / 1e12).toFixed(2)}T`
    if (value >= 1e9) return `$${(value / 1e9).toFixed(2)}B`
    if (value >= 1e6) return `$${(value / 1e6).toFixed(0)}M`
    return `$${value.toLocaleString()}`
  }

  const formatPrice = (value) => {
    if (value == null) return 'N/A'
    return `$${Number(value).toFixed(2)}`
  }

  return (
    <div className="space-y-6">
      <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center gap-3">
              <h1 className="text-3xl font-bold text-white">{stock_data.ticker}</h1>
              <span className="text-sm px-2 py-1 bg-gray-700 rounded text-gray-300">
                {stock_data.sector}
              </span>
            </div>
            <p className="text-gray-400 mt-1">{stock_data.company_name}</p>
          </div>
          <ScoreGauge score={score_analysis.composite_score} color={score_analysis.color} size="large" />
        </div>

        <div className={`mt-4 px-4 py-2 rounded-lg text-center font-medium ${
          score_analysis.color === 'green' ? 'bg-green-900 text-green-300' :
          score_analysis.color === 'light_green' ? 'bg-lime-900 text-lime-300' :
          score_analysis.color === 'yellow' ? 'bg-yellow-900 text-yellow-300' :
          score_analysis.color === 'orange' ? 'bg-orange-900 text-orange-300' :
          'bg-red-900 text-red-300'
        }`}>
          {score_analysis.classification}
        </div>

        {score_analysis.flags && score_analysis.flags.length > 0 && (
          <div className="mt-4 flex flex-wrap gap-2">
            {score_analysis.flags.map((flag, index) => {
              const flagName = typeof flag === 'string' ? flag : flag.flag
              const isPositive = flagName === 'OPTIMAL_MULTIBAGGER_PROFILE' || flagName === 'QUALITY_COMPOUNDER'
              return (
                <span 
                  key={index}
                  className={`px-3 py-1 rounded-full text-sm font-medium ${
                    isPositive
                      ? 'bg-green-900 text-green-300' 
                      : 'bg-red-900 text-red-300'
                  }`}
                >
                  {flagName.replace(/_/g, ' ')}
                </span>
              )
            })}
          </div>
        )}
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
          <span className="text-sm text-gray-400">Current Price</span>
          <p className="text-2xl font-bold text-white">{formatPrice(stock_data.current_price)}</p>
        </div>
        <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
          <span className="text-sm text-gray-400">Market Cap</span>
          <p className="text-2xl font-bold text-white">{formatMarketCap(stock_data.market_cap)}</p>
        </div>
        <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
          <span className="text-sm text-gray-400">52-Week Range</span>
          <p className="text-lg font-bold text-white">
            {formatPrice(stock_data.low_52_week)} - {formatPrice(stock_data.high_52_week)}
          </p>
        </div>
        <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
          <span className="text-sm text-gray-400">Enterprise Value</span>
          <p className="text-2xl font-bold text-white">{formatMarketCap(stock_data.enterprise_value)}</p>
        </div>
      </div>

      <FactorBreakdown 
        breakdown={score_analysis.factor_breakdown} 
        bonusBreakdown={score_analysis.bonus_breakdown}
      />

      {score_analysis.total_bonus !== undefined && (
        <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
          <div className="flex justify-between items-center">
            <span className="text-gray-400">Score Breakdown</span>
            <div className="text-right">
              <div className="text-sm text-gray-400">
                Base: {score_analysis.base_score?.toFixed(1)} | 
                Bonus: <span className={score_analysis.total_bonus > 0 ? 'text-green-400' : score_analysis.total_bonus < 0 ? 'text-red-400' : ''}>
                  {score_analysis.total_bonus > 0 ? '+' : ''}{score_analysis.total_bonus?.toFixed(1)}
                </span> | 
                Adj: <span className={score_analysis.adjustments > 0 ? 'text-green-400' : score_analysis.adjustments < 0 ? 'text-red-400' : ''}>
                  {score_analysis.adjustments > 0 ? '+' : ''}{score_analysis.adjustments?.toFixed(1)}
                </span>
              </div>
              <div className="text-xl font-bold text-white">
                Final: {score_analysis.composite_score}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default StockDetail
