import React from 'react'

function QualityBadges({ bonusFactors }) {
  if (!bonusFactors) return null
  
  const badges = []
  
  if (bonusFactors.fcf_conversion?.bonus >= 4) {
    badges.push({ icon: 'checkmark', label: 'Quality Earnings', color: 'green' })
  }
  
  if (bonusFactors.insider_ownership?.bonus >= 5) {
    badges.push({ icon: 'person', label: 'Owner-Operator', color: 'blue' })
  }
  
  if (bonusFactors.buyback_intensity?.bonus >= 3) {
    badges.push({ icon: 'refresh', label: 'Buybacks', color: 'purple' })
  }
  
  if (bonusFactors.moat_proxy?.bonus >= 4) {
    badges.push({ icon: 'shield', label: 'Moat', color: 'amber' })
  }
  
  if (bonusFactors.fcf_margin?.bonus >= 3) {
    badges.push({ icon: 'cash', label: 'Cash Machine', color: 'emerald' })
  }
  
  if (badges.length === 0) return null
  
  const colorClasses = {
    green: 'bg-green-900/40 text-green-400',
    blue: 'bg-blue-900/40 text-blue-400',
    purple: 'bg-purple-900/40 text-purple-400',
    amber: 'bg-amber-900/40 text-amber-400',
    emerald: 'bg-emerald-900/40 text-emerald-400',
  }
  
  const iconMap = {
    checkmark: '\u2713',
    person: '\u263A',
    refresh: '\u21BB',
    shield: '\u2694',
    cash: '$'
  }
  
  return (
    <div className="flex flex-wrap gap-1 mt-2">
      {badges.map((badge, i) => (
        <span 
          key={i}
          className={`text-xs px-2 py-0.5 rounded-full ${colorClasses[badge.color]}`}
        >
          {iconMap[badge.icon]} {badge.label}
        </span>
      ))}
    </div>
  )
}

export default QualityBadges
