import React from 'react'

function MacroIndicator({ macroData }) {
  const getTrajectoryColor = (trajectory) => {
    if (trajectory === 'falling') return 'text-green-400'
    if (trajectory === 'rising') return 'text-red-400'
    return 'text-yellow-400'
  }

  const getTrajectoryIcon = (trajectory) => {
    if (trajectory === 'falling') return '↓'
    if (trajectory === 'rising') return '↑'
    return '→'
  }

  return (
    <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm text-gray-400">Macro Environment</h3>
          <div className="flex items-center gap-2 mt-1">
            <span className="text-lg font-semibold text-white">
              Fed Funds Rate: {macroData.fed_funds_rate}%
            </span>
            <span className={`text-lg ${getTrajectoryColor(macroData.fed_rate_trajectory)}`}>
              {getTrajectoryIcon(macroData.fed_rate_trajectory)}
            </span>
          </div>
        </div>
        <div className={`px-3 py-1 rounded-full text-sm font-medium ${
          macroData.fed_rate_trajectory === 'falling' 
            ? 'bg-green-900 text-green-300'
            : macroData.fed_rate_trajectory === 'rising'
            ? 'bg-red-900 text-red-300'
            : 'bg-yellow-900 text-yellow-300'
        }`}>
          {macroData.fed_rate_trajectory === 'falling' && 'Tailwind for Growth'}
          {macroData.fed_rate_trajectory === 'rising' && 'Headwind for Growth'}
          {macroData.fed_rate_trajectory === 'stable' && 'Neutral Environment'}
        </div>
      </div>
    </div>
  )
}

export default MacroIndicator
