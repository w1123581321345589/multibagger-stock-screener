import React from 'react'
import ScoreGauge from './ScoreGauge'
import QualityBadges from './QualityBadges'

function StockCard({ stock, onClick, mode = 'multibagger' }) {
  const getColorClass = (color) => {
    const colors = {
      green: 'bg-green-500',
      light_green: 'bg-lime-500',
      yellow_green: 'bg-lime-600',
      yellow: 'bg-yellow-500',
      orange: 'bg-orange-500',
      red: 'bg-red-500'
    }
    return colors[color] || 'bg-gray-500'
  }

  const formatMarketCap = (value) => {
    if (value == null || value === 0) return 'N/A'
    if (value >= 1e12) return `$${(value / 1e12).toFixed(2)}T`
    if (value >= 1e9) return `$${(value / 1e9).toFixed(2)}B`
    if (value >= 1e6) return `$${(value / 1e6).toFixed(0)}M`
    return `$${value.toLocaleString()}`
  }

  const getFlagIcon = (flag) => {
    const icons = {
      'NEGATIVE_EQUITY': '!',
      'DECLINING_LOSS_MAKER': '-',
      'HEAVY_DILUTION': '~',
      'UNSUSTAINABLE_GROWTH': '!',
      'OPTIMAL_MULTIBAGGER_PROFILE': '*',
      'QUALITY_COMPOUNDER': '*',
    }
    return icons[flag] || '.'
  }

  const getFlagType = (flag) => {
    if (flag === 'OPTIMAL_MULTIBAGGER_PROFILE' || flag === 'QUALITY_COMPOUNDER') {
      return 'positive'
    }
    return 'warning'
  }

  return (
    <div 
      className="bg-gray-800 rounded-lg p-4 border border-gray-700 hover:border-gray-600 cursor-pointer transition-all hover:shadow-lg"
      onClick={onClick}
    >
      <div className="flex justify-between items-start mb-3">
        <div>
          <h3 className="text-lg font-bold text-white">{stock.ticker}</h3>
          <p className="text-sm text-gray-400 truncate max-w-[180px]">{stock.company_name}</p>
          <p className="text-xs text-gray-500">{stock.sector}</p>
        </div>
        <ScoreGauge score={stock.composite_score} color={stock.color} />
      </div>

      <div className="grid grid-cols-2 gap-2 text-sm mb-3">
        <div>
          <span className="text-gray-500">Price</span>
          <p className="text-white">
            {stock.current_price != null ? `$${Number(stock.current_price).toFixed(2)}` : 'N/A'}
          </p>
        </div>
        <div>
          <span className="text-gray-500">Market Cap</span>
          <p className="text-white">{formatMarketCap(stock.market_cap)}</p>
        </div>
      </div>

      <div className={`text-xs px-2 py-1 rounded text-center ${getColorClass(stock.color)} text-white font-medium`}>
        {stock.classification}
      </div>

      {stock.flags && stock.flags.length > 0 && (
        <div className="mt-2 flex flex-wrap gap-1">
          {stock.flags.map((flag, index) => {
            const flagName = typeof flag === 'string' ? flag : flag.flag
            const flagType = getFlagType(flagName)
            return (
              <span 
                key={index}
                className={`text-xs px-2 py-0.5 rounded ${
                  flagType === 'positive'
                    ? 'bg-green-900 text-green-300' 
                    : 'bg-red-900 text-red-300'
                }`}
              >
                {getFlagIcon(flagName)} {flagName.replace(/_/g, ' ')}
              </span>
            )
          })}
        </div>
      )}

      <QualityBadges bonusFactors={stock.bonus_breakdown} />

      <div className="mt-3 pt-3 border-t border-gray-700">
        <div className="grid grid-cols-3 gap-2 text-xs">
          <div className="text-center">
            <span className="text-gray-500 block">FCF Yield</span>
            <span className="text-white">{stock.factor_breakdown?.fcf_yield?.fcf_yield_pct || 'N/A'}</span>
          </div>
          <div className="text-center">
            <span className="text-gray-500 block">B/M</span>
            <span className="text-white">
              {stock.factor_breakdown?.book_to_market?.book_to_market != null 
                ? Number(stock.factor_breakdown.book_to_market.book_to_market).toFixed(2) 
                : 'N/A'}
            </span>
          </div>
          <div className="text-center">
            <span className="text-gray-500 block">Momentum</span>
            <span className="text-white">
              {stock.factor_breakdown?.momentum?.return_6m != null 
                ? `${Number(stock.factor_breakdown.momentum.return_6m).toFixed(1)}%` 
                : 'N/A'}
            </span>
          </div>
        </div>
      </div>

      {stock.total_bonus !== undefined && stock.total_bonus !== 0 && (
        <div className="mt-2 text-xs text-center">
          <span className={stock.total_bonus > 0 ? 'text-green-400' : 'text-red-400'}>
            Quality Bonus: {stock.total_bonus > 0 ? '+' : ''}{stock.total_bonus.toFixed(1)} pts
          </span>
        </div>
      )}
    </div>
  )
}

export default StockCard
