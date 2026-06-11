import React, { useState, useEffect } from 'react'

function FilterPanel({ filters, setFilters, onApply, loading, universe, onUniverseChange }) {
  const [sectors, setSectors] = useState([])

  useEffect(() => {
    fetch('/api/sectors')
      .then(res => res.json())
      .then(data => setSectors(data.sectors || []))
      .catch(() => setSectors([]))
  }, [])

  const handleMinScoreChange = (e) => {
    setFilters({ ...filters, minScore: parseInt(e.target.value) || 0 })
  }

  const handleMarketCapChange = (value) => {
    setFilters({ ...filters, maxMarketCap: value })
  }

  const handleSectorToggle = (sector) => {
    const newSectors = filters.sectors.includes(sector)
      ? filters.sectors.filter(s => s !== sector)
      : [...filters.sectors, sector]
    setFilters({ ...filters, sectors: newSectors })
  }

  return (
    <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
      <h3 className="text-lg font-semibold mb-4">Filters</h3>
      
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div>
          <label className="block text-sm text-gray-400 mb-2">Stock Universe</label>
          <select
            value={universe || 'default'}
            onChange={(e) => onUniverseChange && onUniverseChange(e.target.value)}
            className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded text-white text-sm"
          >
            <option value="default">Default (50 stocks)</option>
            <option value="small_cap">Small Cap ($100M-$2B)</option>
            <option value="mid_cap">Mid Cap ($2B-$10B)</option>
            <option value="expanded">Expanded (150+ stocks)</option>
          </select>
        </div>

        <div>
          <label className="block text-sm text-gray-400 mb-2">
            Minimum Score: {filters.minScore}
          </label>
          <input
            type="range"
            min="0"
            max="100"
            value={filters.minScore}
            onChange={handleMinScoreChange}
            className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>0</span>
            <span>100</span>
          </div>
        </div>

        <div>
          <label className="block text-sm text-gray-400 mb-2">Max Market Cap</label>
          <div className="flex flex-wrap gap-2">
            {[
              { label: 'Any', value: null },
              { label: '<$500M', value: 0.5 },
              { label: '<$2B', value: 2 },
              { label: '<$10B', value: 10 }
            ].map((option) => (
              <button
                key={option.label}
                onClick={() => handleMarketCapChange(option.value)}
                className={`px-3 py-1 text-sm rounded ${
                  filters.maxMarketCap === option.value
                    ? 'bg-green-600 text-white'
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                {option.label}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm text-gray-400 mb-2">Sectors</label>
          <div className="flex flex-wrap gap-1 max-h-20 overflow-y-auto">
            {sectors.slice(0, 6).map((sector) => (
              <button
                key={sector}
                onClick={() => handleSectorToggle(sector)}
                className={`px-2 py-1 text-xs rounded ${
                  filters.sectors.includes(sector)
                    ? 'bg-green-600 text-white'
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                {sector}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="mt-4 flex justify-end">
        <button
          onClick={onApply}
          disabled={loading}
          className="px-6 py-2 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 text-white rounded-lg font-medium transition-colors"
        >
          {loading ? 'Screening...' : 'Apply Filters'}
        </button>
      </div>
    </div>
  )
}

export default FilterPanel
