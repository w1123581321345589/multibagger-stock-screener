from backend.models.factors import (
    SizeFactor, BookToMarketFactor, FCFYieldFactor,
    ProfitabilityFactor, InvestmentPatternFactor,
    MomentumFactor, MacroEnvironmentFactor,
    FCFConversionFactor, FCFMarginFactor, InsiderOwnershipFactor,
    BuybackIntensityFactor, MoatProxyFactor
)
from backend.services.quality_filters import QualityPreFilter
from backend.utils.constants import FACTOR_WEIGHTS
from backend.utils.helpers import get_score_color, get_classification
from typing import Dict, Any, List


class MultibaggerScorer:
    CORE_WEIGHTS = {
        'fcf_yield': 0.20,
        'book_to_market': 0.15,
        'momentum': 0.14,
        'size': 0.12,
        'profitability': 0.12,
        'investment_pattern': 0.12,
        'macro': 0.10,
    }
    
    def __init__(self, mode: str = 'multibagger'):
        self.mode = mode
        self.size_factor = SizeFactor()
        self.btm_factor = BookToMarketFactor()
        self.fcf_factor = FCFYieldFactor()
        self.profit_factor = ProfitabilityFactor()
        self.invest_factor = InvestmentPatternFactor()
        self.momentum_factor = MomentumFactor()
        self.macro_factor = MacroEnvironmentFactor()
        
        self.fcf_conversion_factor = FCFConversionFactor()
        self.fcf_margin_factor = FCFMarginFactor()
        self.insider_factor = InsiderOwnershipFactor()
        self.buyback_factor = BuybackIntensityFactor()
        self.moat_factor = MoatProxyFactor()
        
        self.pre_filter = QualityPreFilter()
    
    def set_mode(self, mode: str):
        self.mode = mode
    
    def calculate_composite_score(self, stock_data: dict, macro_data: dict) -> dict:
        size = self.size_factor.calculate(stock_data)
        btm = self.btm_factor.calculate(stock_data)
        fcf = self.fcf_factor.calculate(stock_data)
        profit = self.profit_factor.calculate(stock_data)
        invest = self.invest_factor.calculate(stock_data)
        momentum = self.momentum_factor.calculate(stock_data)
        macro = self.macro_factor.calculate(macro_data)
        
        core_factors = {
            'size': size,
            'book_to_market': btm,
            'fcf_yield': fcf,
            'profitability': profit,
            'investment_pattern': invest,
            'momentum': momentum,
            'macro': macro
        }
        
        base_score = (
            fcf['score'] * self.CORE_WEIGHTS['fcf_yield'] +
            btm['score'] * self.CORE_WEIGHTS['book_to_market'] +
            momentum['score'] * self.CORE_WEIGHTS['momentum'] +
            size['score'] * self.CORE_WEIGHTS['size'] +
            profit['score'] * self.CORE_WEIGHTS['profitability'] +
            invest['score'] * self.CORE_WEIGHTS['investment_pattern'] +
            macro['score'] * self.CORE_WEIGHTS['macro']
        )
        
        fcf_conv = self.fcf_conversion_factor.calculate(stock_data)
        fcf_margin = self.fcf_margin_factor.calculate(stock_data)
        insider = self.insider_factor.calculate(stock_data)
        buyback = self.buyback_factor.calculate(stock_data)
        moat = self.moat_factor.calculate(stock_data)
        
        bonus_factors = {
            'fcf_conversion': fcf_conv,
            'fcf_margin': fcf_margin,
            'insider_ownership': insider,
            'buyback_intensity': buyback,
            'moat_proxy': moat
        }
        
        total_bonus = sum(f['bonus'] for f in bonus_factors.values())
        
        adjustments = 0
        flags = []
        
        if btm.get('flag') == 'CRITICAL_WARNING':
            adjustments -= 30
            flags.append({
                'type': 'critical',
                'flag': 'NEGATIVE_EQUITY',
                'message': 'Negative equity - liabilities exceed assets',
                'impact': -30
            })
        
        if profit['score'] < 20 and invest.get('pattern') == 'DECLINING':
            adjustments -= 20
            flags.append({
                'type': 'critical',
                'flag': 'DECLINING_LOSS_MAKER',
                'message': 'Loss-making company with shrinking assets',
                'impact': -20
            })
        
        if buyback['shares_change_1y_pct'] > 10:
            adjustments -= 10
            flags.append({
                'type': 'warning',
                'flag': 'HEAVY_DILUTION',
                'message': f"Shares increased {buyback['shares_change_1y_pct']:.1f}% YoY",
                'impact': -10
            })
        
        if invest.get('pattern') == 'UNSUSTAINABLE_GROWTH':
            adjustments -= 8
            flags.append({
                'type': 'warning',
                'flag': 'UNSUSTAINABLE_GROWTH',
                'message': 'Asset growth significantly outpacing EBITDA growth',
                'impact': -8
            })
        
        optimal_combo = (
            size['score'] >= 75 and
            btm['score'] >= 60 and
            fcf['score'] >= 65 and
            momentum['score'] >= 65
        )
        
        if optimal_combo:
            adjustments += 10
            flags.append({
                'type': 'positive',
                'flag': 'OPTIMAL_MULTIBAGGER_PROFILE',
                'message': 'Hits all key multibagger criteria: small, undervalued, cash-generating, beaten-down',
                'impact': 10
            })
        
        if self.mode == 'compounder':
            quality_combo = (
                moat['score'] >= 50 and
                insider['score'] >= 70 and
                fcf_conv['score'] >= 80
            )
            if quality_combo:
                adjustments += 8
                flags.append({
                    'type': 'positive',
                    'flag': 'QUALITY_COMPOUNDER',
                    'message': 'Strong moat + owner-operator + quality earnings',
                    'impact': 8
                })
        
        final_score = base_score + total_bonus + adjustments
        final_score = max(0, min(100, final_score))
        
        if final_score >= 80:
            classification = "STRONG BUY"
            color = "green"
        elif final_score >= 68:
            classification = "BUY"
            color = "light_green"
        elif final_score >= 55:
            classification = "ACCUMULATE"
            color = "yellow_green"
        elif final_score >= 42:
            classification = "HOLD"
            color = "yellow"
        elif final_score >= 30:
            classification = "WEAK"
            color = "orange"
        else:
            classification = "AVOID"
            color = "red"
        
        flag_names = [f['flag'] if isinstance(f, dict) else f for f in flags]
        
        return {
            'ticker': stock_data.get('ticker', 'UNKNOWN'),
            'company_name': stock_data.get('company_name', 'Unknown Company'),
            'sector': stock_data.get('sector'),
            'composite_score': round(final_score, 1),
            'base_score': round(base_score, 1),
            'total_bonus': round(total_bonus, 1),
            'adjustments': round(adjustments, 1),
            'classification': classification,
            'color': color,
            'mode': self.mode,
            'flags': flag_names,
            'flags_detailed': flags,
            'factor_breakdown': core_factors,
            'bonus_breakdown': bonus_factors,
            'optimal_combo': optimal_combo,
            'market_cap': stock_data.get('market_cap', 0),
            'current_price': stock_data.get('current_price', 0)
        }
    
    def screen_stocks(self, stocks_data: List[dict], macro_data: dict, 
                      min_score: int = 50, sectors: List[str] = None,
                      max_market_cap: float = None, apply_prefilter: bool = True) -> List[dict]:
        results = []
        
        for stock in stocks_data:
            if sectors and stock.get('sector') not in sectors:
                continue
            if max_market_cap and stock.get('market_cap', 0) > max_market_cap:
                continue
            
            if apply_prefilter:
                filter_result = self.pre_filter.apply_filters(stock, self.mode)
                if not filter_result['passed']:
                    continue
            
            score_result = self.calculate_composite_score(stock, macro_data)
            
            if score_result['composite_score'] >= min_score:
                results.append(score_result)
        
        results.sort(key=lambda x: x['composite_score'], reverse=True)
        
        return results
