import React from 'react'

function ModeToggle({ mode, onModeChange }) {
  return (
    <div className="flex items-center bg-gray-800 rounded-lg p-1 border border-gray-700">
      <button
        onClick={() => onModeChange('multibagger')}
        className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
          mode === 'multibagger'
            ? 'bg-green-600 text-white'
            : 'text-gray-400 hover:text-white'
        }`}
      >
        Multibagger Hunter
      </button>
      <button
        onClick={() => onModeChange('compounder')}
        className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
          mode === 'compounder'
            ? 'bg-blue-600 text-white'
            : 'text-gray-400 hover:text-white'
        }`}
      >
        Quality Compounder
      </button>
    </div>
  )
}

export default ModeToggle
