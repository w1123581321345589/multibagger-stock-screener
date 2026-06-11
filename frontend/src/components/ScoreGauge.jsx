import React from 'react'

function ScoreGauge({ score, color, size = 'default' }) {
  const getColorClass = (color) => {
    const colors = {
      green: 'text-green-500 border-green-500',
      light_green: 'text-lime-500 border-lime-500',
      yellow: 'text-yellow-500 border-yellow-500',
      orange: 'text-orange-500 border-orange-500',
      red: 'text-red-500 border-red-500'
    }
    return colors[color] || 'text-gray-500 border-gray-500'
  }

  const sizeClasses = size === 'large' 
    ? 'w-24 h-24 text-2xl'
    : 'w-14 h-14 text-lg'

  return (
    <div 
      className={`${sizeClasses} rounded-full border-4 flex items-center justify-center font-bold ${getColorClass(color)}`}
    >
      {Math.round(score)}
    </div>
  )
}

export default ScoreGauge
