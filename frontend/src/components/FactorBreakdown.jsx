import React from 'react'

function FactorBreakdown({ breakdown, bonusBreakdown }) {
  const factors = [
    { 
      key: 'fcf_yield', 
      name: 'FCF Yield', 
      weight: '20%',
      description: '#1 predictor of multibagger returns',
      getValue: (f) => f?.fcf_yield_pct || 'N/A'
    },
    { 
      key: 'book_to_market', 
      name: 'Book-to-Market', 
      weight: '15%',
      description: 'Value indicator - higher means more undervalued',
      getValue: (f) => f?.book_to_market?.toFixed(2) || 'N/A'
    },
    { 
      key: 'momentum', 
      name: 'Entry Point (Contrarian)', 
      weight: '14%',
      description: 'Near 52-week lows = better entry',
      getValue: (f) => f?.price_range_tier || 'N/A'
    },
    { 
      key: 'size', 
      name: 'Size', 
      weight: '12%',
      description: 'Smaller = higher return potential',
      getValue: (f) => f?.tier || 'N/A'
    },
    { 
      key: 'profitability', 
      name: 'Profitability', 
      weight: '12%',
      description: 'EBITDA margin + ROA',
      getValue: (f) => f?.ebitda_margin_pct || 'N/A'
    },
    { 
      key: 'investment_pattern', 
      name: 'Investment Pattern', 
      weight: '12%',
      description: 'Growth funded by EBITDA',
      getValue: (f) => f?.pattern?.replace(/_/g, ' ') || 'N/A'
    },
    { 
      key: 'macro', 
      name: 'Macro Environment', 
      weight: '10%',
      description: 'Interest rate trajectory',
      getValue: (f) => f?.tier || 'N/A'
    }
  ]

  const bonusFactors = [
    { key: 'fcf_conversion', name: 'Earnings Quality', getDetail: (f) => f?.fcf_conversion_pct },
    { key: 'fcf_margin', name: 'FCF Margin', getDetail: (f) => f?.fcf_margin_pct },
    { key: 'insider_ownership', name: 'Owner-Operator', getDetail: (f) => f?.insider_ownership_pct ? `${f.insider_ownership_pct}% insider` : null },
    { key: 'buyback_intensity', name: 'Buybacks', getDetail: (f) => f?.shares_change_1y_pct != null ? `${f.shares_change_1y_pct > 0 ? '+' : ''}${f.shares_change_1y_pct.toFixed(1)}% shares` : null },
    { key: 'moat_proxy', name: 'Moat', getDetail: (f) => f?.moat_signals?.join(', ') },
  ]

  const getScoreColor = (score) => {
    if (score >= 80) return 'bg-green-500'
    if (score >= 60) return 'bg-lime-500'
    if (score >= 40) return 'bg-yellow-500'
    if (score >= 20) return 'bg-orange-500'
    return 'bg-red-500'
  }

  return (
    <div className="space-y-6">
      <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
        <h2 className="text-xl font-bold text-white mb-4">Core Factors (Yartseva Research)</h2>
        
        <div className="space-y-4">
          {factors.map((factor) => {
            const factorData = breakdown?.[factor.key]
            const score = factorData?.score || 0
            
            return (
              <div key={factor.key} className="bg-gray-700 rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h3 className="font-semibold text-white">{factor.name}</h3>
                    <p className="text-xs text-gray-400">{factor.description}</p>
                  </div>
                  <div className="text-right">
                    <span className="text-sm text-gray-400">Weight: {factor.weight}</span>
                    <div className="text-lg font-bold text-white">{Math.round(score)}/100</div>
                  </div>
                </div>
                
                <div className="w-full bg-gray-600 rounded-full h-2 mb-2">
                  <div 
                    className={`h-2 rounded-full ${getScoreColor(score)}`}
                    style={{ width: `${score}%` }}
                  />
                </div>
                
                <div className="flex justify-between text-sm">
                  <span className="text-gray-300">{factorData?.tier || 'N/A'}</span>
                  <span className="text-gray-400">{factor.getValue(factorData)}</span>
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {bonusBreakdown && (
        <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
          <h2 className="text-xl font-bold text-white mb-4">Quality Bonuses (Compounding Quality)</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {bonusFactors.map((factor) => {
              const factorData = bonusBreakdown?.[factor.key]
              const bonus = factorData?.bonus || 0
              const detail = factor.getDetail(factorData)
              
              return (
                <div 
                  key={factor.key} 
                  className={`rounded-lg p-4 border ${
                    bonus > 0 ? 'bg-green-900/20 border-green-700' :
                    bonus < 0 ? 'bg-red-900/20 border-red-700' :
                    'bg-gray-700 border-gray-600'
                  }`}
                >
                  <div className="flex justify-between items-center mb-2">
                    <h3 className="font-medium text-white">{factor.name}</h3>
                    <span className={`text-lg font-bold ${
                      bonus > 0 ? 'text-green-400' :
                      bonus < 0 ? 'text-red-400' :
                      'text-gray-500'
                    }`}>
                      {bonus > 0 ? '+' : ''}{bonus} pts
                    </span>
                  </div>
                  <div className="text-sm text-gray-400">{factorData?.tier || 'N/A'}</div>
                  {detail && <div className="text-xs text-gray-500 mt-1">{detail}</div>}
                </div>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}

export default FactorBreakdown
