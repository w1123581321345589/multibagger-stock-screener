from typing import Dict, Any
import numpy as np


def to_python_type(value):
    if isinstance(value, (np.bool_, np.integer, np.floating)):
        return value.item()
    if isinstance(value, np.ndarray):
        return value.tolist()
    return value


class SizeFactor:
    def calculate(self, stock_data: dict) -> dict:
        market_cap = stock_data.get('market_cap', 0)
        enterprise_value = stock_data.get('enterprise_value', market_cap)
        
        if enterprise_value < 250_000_000:
            score = 100
            tier = "Micro-cap (Optimal)"
        elif enterprise_value < 500_000_000:
            score = 85
            tier = "Small-cap (Strong)"
        elif enterprise_value < 2_000_000_000:
            score = 60
            tier = "Small-cap (Moderate)"
        elif enterprise_value < 10_000_000_000:
            score = 35
            tier = "Mid-cap (Weak)"
        else:
            score = 10
            tier = "Large-cap (Poor)"
            
        return {
            'score': score,
            'tier': tier,
            'market_cap': market_cap,
            'enterprise_value': enterprise_value,
            'weight': 0.12
        }


class BookToMarketFactor:
    def calculate(self, stock_data: dict) -> dict:
        total_equity = stock_data.get('total_equity', 0)
        market_cap = stock_data.get('market_cap', 1)
        
        if total_equity <= 0:
            return {
                'score': 0,
                'tier': "Negative Equity (AVOID)",
                'book_to_market': None,
                'flag': 'CRITICAL_WARNING',
                'weight': 0.15
            }
        
        b_m = total_equity / market_cap if market_cap > 0 else 0
        
        if b_m >= 1.0:
            score = 100
            tier = "Deep Value (Optimal)"
        elif b_m >= 0.70:
            score = 85
            tier = "Strong Value"
        elif b_m >= 0.40:
            score = 65
            tier = "Moderate Value (Threshold Met)"
        elif b_m >= 0.20:
            score = 35
            tier = "Growth-Valued"
        else:
            score = 10
            tier = "Overvalued (Weak)"
            
        return {
            'score': score,
            'tier': tier,
            'book_to_market': round(b_m, 3),
            'weight': 0.15
        }


class FCFYieldFactor:
    def calculate(self, stock_data: dict) -> dict:
        fcf = stock_data.get('free_cash_flow', 0)
        market_cap = stock_data.get('market_cap', 1)
        
        if market_cap <= 0:
            market_cap = 1
            
        fcf_yield = (fcf / market_cap) * 100
        
        if fcf <= 0:
            return {
                'score': 15,
                'tier': "Negative FCF (Caution)",
                'fcf_yield': round(fcf_yield, 2),
                'fcf_yield_pct': f"{round(fcf_yield, 2)}%",
                'weight': 0.20
            }
        
        if fcf_yield >= 10:
            score = 100
            tier = "Exceptional FCF Yield"
        elif fcf_yield >= 7:
            score = 90
            tier = "Strong FCF Yield"
        elif fcf_yield >= 5:
            score = 75
            tier = "Good FCF Yield"
        elif fcf_yield >= 3:
            score = 55
            tier = "Moderate FCF Yield"
        elif fcf_yield >= 1:
            score = 35
            tier = "Low FCF Yield"
        else:
            score = 20
            tier = "Minimal FCF Yield"
            
        return {
            'score': score,
            'tier': tier,
            'fcf_yield': round(fcf_yield, 2),
            'fcf_yield_pct': f"{round(fcf_yield, 2)}%",
            'weight': 0.20
        }


class ProfitabilityFactor:
    def calculate(self, stock_data: dict) -> dict:
        ebitda = stock_data.get('ebitda', 0)
        revenue = stock_data.get('revenue', 1)
        net_income = stock_data.get('net_income', 0)
        total_assets = stock_data.get('total_assets', 1)
        
        ebitda_margin = (ebitda / revenue * 100) if revenue > 0 else 0
        roa = (net_income / total_assets * 100) if total_assets > 0 else 0
        
        if ebitda_margin < 0 and roa < 0:
            return {
                'score': 5,
                'tier': "Loss-Making (HIGH RISK)",
                'ebitda_margin': round(ebitda_margin, 2),
                'ebitda_margin_pct': f"{round(ebitda_margin, 2)}%",
                'roa': round(roa, 2),
                'roa_pct': f"{round(roa, 2)}%",
                'flag': 'WARNING',
                'weight': 0.12
            }
        
        if ebitda_margin >= 25:
            base_score = 95
            tier = "Exceptional Profitability"
        elif ebitda_margin >= 18:
            base_score = 80
            tier = "Strong Profitability"
        elif ebitda_margin >= 12:
            base_score = 65
            tier = "Good Profitability"
        elif ebitda_margin >= 5:
            base_score = 45
            tier = "Moderate Profitability"
        elif ebitda_margin > 0:
            base_score = 30
            tier = "Weak Profitability"
        else:
            base_score = 10
            tier = "Negative EBITDA"
        
        roa_bonus = min(10, max(0, roa * 0.5))
        
        return {
            'score': min(100, base_score + roa_bonus),
            'tier': tier,
            'ebitda_margin': round(ebitda_margin, 2),
            'ebitda_margin_pct': f"{round(ebitda_margin, 2)}%",
            'roa': round(roa, 2),
            'roa_pct': f"{round(roa, 2)}%",
            'weight': 0.12
        }


class InvestmentPatternFactor:
    def calculate(self, stock_data: dict) -> dict:
        asset_growth = to_python_type(stock_data.get('asset_growth_yoy', 0))
        ebitda_growth = to_python_type(stock_data.get('ebitda_growth_yoy', 0))
        
        investment_sustainable = bool(asset_growth <= ebitda_growth)
        
        if asset_growth > 0 and investment_sustainable:
            score = 90
            tier = "Optimal: Growing Assets, EBITDA-Funded"
            pattern = "SUSTAINABLE_GROWTH"
        elif asset_growth > 0 and not investment_sustainable:
            score = 40
            tier = "Caution: Asset Growth Outpacing EBITDA"
            pattern = "UNSUSTAINABLE_GROWTH"
        elif asset_growth <= 0 and ebitda_growth > 0:
            score = 60
            tier = "Profitable but Not Reinvesting"
            pattern = "CASH_COW"
        elif asset_growth <= 0 and ebitda_growth <= 0:
            score = 20
            tier = "Shrinking (Negative Assets & EBITDA)"
            pattern = "DECLINING"
        else:
            score = 50
            tier = "Neutral"
            pattern = "NEUTRAL"
            
        return {
            'score': score,
            'tier': tier,
            'pattern': pattern,
            'asset_growth_yoy': float(round(asset_growth, 2)),
            'ebitda_growth_yoy': float(round(ebitda_growth, 2)),
            'investment_sustainable': investment_sustainable,
            'weight': 0.12
        }


class MomentumFactor:
    def calculate(self, stock_data: dict) -> dict:
        current_price = stock_data.get('current_price', 0)
        high_52w = stock_data.get('high_52_week', current_price)
        low_52w = stock_data.get('low_52_week', current_price)
        return_1m = stock_data.get('return_1_month', 0)
        return_3m = stock_data.get('return_3_month', 0)
        return_6m = stock_data.get('return_6_month', 0)
        
        price_range_diff = high_52w - low_52w
        if price_range_diff > 0:
            price_range = ((current_price - low_52w) / price_range_diff) * 100
        else:
            price_range = 50
        
        if price_range <= 20:
            range_score = 95
            range_tier = "Near 52-Week Low (Optimal Entry)"
        elif price_range <= 35:
            range_score = 80
            range_tier = "Lower Range (Good Entry)"
        elif price_range <= 50:
            range_score = 60
            range_tier = "Mid Range (Neutral)"
        elif price_range <= 70:
            range_score = 40
            range_tier = "Upper Range (Caution)"
        elif price_range <= 85:
            range_score = 25
            range_tier = "Near Highs (Poor Entry)"
        else:
            range_score = 10
            range_tier = "At 52-Week High (Avoid)"
        
        if return_6m <= -30:
            momentum_score = 90
            momentum_tier = "Significantly Down (Contrarian Opportunity)"
        elif return_6m <= -15:
            momentum_score = 75
            momentum_tier = "Moderately Down (Good Setup)"
        elif return_6m <= 0:
            momentum_score = 60
            momentum_tier = "Slightly Down (Neutral)"
        elif return_6m <= 20:
            momentum_score = 40
            momentum_tier = "Up Modestly (Weaker)"
        else:
            momentum_score = 20
            momentum_tier = "Up Significantly (Poor Setup)"
        
        combined_score = (range_score * 0.6) + (momentum_score * 0.4)
        
        return {
            'score': round(combined_score),
            'price_range': round(price_range, 1),
            'price_range_tier': range_tier,
            'return_1m': round(return_1m, 2),
            'return_3m': round(return_3m, 2),
            'return_6m': round(return_6m, 2),
            'momentum_tier': momentum_tier,
            'weight': 0.14
        }


class MacroEnvironmentFactor:
    def calculate(self, macro_data: dict) -> dict:
        current_fed_rate = macro_data.get('fed_funds_rate', 5.0)
        fed_rate_1y_ago = macro_data.get('fed_funds_rate_1y_ago', 5.0)
        rate_trajectory = macro_data.get('fed_rate_trajectory', 'stable')
        
        rate_change = current_fed_rate - fed_rate_1y_ago
        
        if rate_trajectory == 'falling' or rate_change <= -0.5:
            score = 95
            tier = "Falling Rates (Tailwind)"
            adjustment = "+5% expected return"
        elif rate_trajectory == 'stable' or abs(rate_change) < 0.5:
            score = 70
            tier = "Stable Rates (Neutral)"
            adjustment = "0% adjustment"
        elif rate_change >= 1.5:
            score = 25
            tier = "Rapidly Rising Rates (Strong Headwind)"
            adjustment = "-10% expected return"
        else:
            score = 45
            tier = "Moderately Rising Rates (Headwind)"
            adjustment = "-5% expected return"
            
        return {
            'score': score,
            'tier': tier,
            'current_fed_rate': current_fed_rate,
            'rate_change_1y': round(rate_change, 2),
            'trajectory': rate_trajectory,
            'return_adjustment': adjustment,
            'weight': 0.10
        }


class FCFConversionFactor:
    MAX_BONUS = 8
    
    def calculate(self, stock_data: dict) -> dict:
        fcf = stock_data.get('free_cash_flow', 0)
        net_income = stock_data.get('net_income', 0)
        
        if net_income <= 0:
            return {
                'score': 0,
                'tier': "N/A (Loss-Making)",
                'fcf_conversion': None,
                'fcf_conversion_pct': "N/A",
                'bonus': 0,
                'weight': 0.0
            }
        
        conversion = (fcf / net_income) * 100
        
        if conversion >= 130:
            score = 100
            tier = "Exceptional: FCF >> Net Income"
            bonus = 8
        elif conversion >= 110:
            score = 92
            tier = "Excellent: FCF > Net Income"
            bonus = 6
        elif conversion >= 95:
            score = 80
            tier = "Strong: Near-Perfect Conversion"
            bonus = 4
        elif conversion >= 85:
            score = 68
            tier = "Good: Healthy Conversion"
            bonus = 2
        elif conversion >= 70:
            score = 50
            tier = "Moderate: Some Non-Cash Items"
            bonus = 0
        elif conversion >= 50:
            score = 30
            tier = "Weak: Significant Non-Cash Earnings"
            bonus = -2
        else:
            score = 15
            tier = "Poor: Earnings Quality Concern"
            bonus = -5
            
        return {
            'score': score,
            'tier': tier,
            'fcf_conversion': round(conversion, 1),
            'fcf_conversion_pct': f"{round(conversion, 1)}%",
            'bonus': bonus,
            'weight': 0.0
        }


class FCFMarginFactor:
    MAX_BONUS = 5
    
    def calculate(self, stock_data: dict) -> dict:
        fcf = stock_data.get('free_cash_flow', 0)
        revenue = stock_data.get('revenue', 0)
        
        if revenue <= 0 or fcf <= 0:
            return {
                'score': 10,
                'tier': "Negative or Zero",
                'fcf_margin': 0,
                'fcf_margin_pct': "0%",
                'bonus': 0,
                'weight': 0.0
            }
        
        fcf_margin = (fcf / revenue) * 100
        
        if fcf_margin >= 30:
            score = 100
            tier = "Exceptional: Cash Machine"
            bonus = 5
        elif fcf_margin >= 20:
            score = 85
            tier = "Excellent: Very High FCF Generation"
            bonus = 4
        elif fcf_margin >= 12:
            score = 70
            tier = "Strong: Good Cash Generation"
            bonus = 2
        elif fcf_margin >= 6:
            score = 50
            tier = "Moderate: Decent Cash Generation"
            bonus = 0
        elif fcf_margin >= 2:
            score = 30
            tier = "Low: Limited Cash Generation"
            bonus = 0
        else:
            score = 15
            tier = "Minimal: Capex-Heavy Business"
            bonus = 0
            
        return {
            'score': score,
            'tier': tier,
            'fcf_margin': round(fcf_margin, 2),
            'fcf_margin_pct': f"{round(fcf_margin, 2)}%",
            'bonus': bonus,
            'weight': 0.0
        }


class InsiderOwnershipFactor:
    MAX_BONUS = 8
    
    def calculate(self, stock_data: dict) -> dict:
        insider_pct = stock_data.get('insider_ownership_pct', 0)
        is_founder_led = stock_data.get('founder_ceo', False)
        
        if insider_pct >= 25:
            score = 100
            tier = "Very High Insider Ownership"
            bonus = 6
        elif insider_pct >= 15:
            score = 85
            tier = "High Insider Ownership"
            bonus = 5
        elif insider_pct >= 10:
            score = 70
            tier = "Significant Insider Ownership"
            bonus = 3
        elif insider_pct >= 5:
            score = 50
            tier = "Moderate Insider Ownership"
            bonus = 1
        else:
            score = 30
            tier = "Low Insider Ownership"
            bonus = 0
        
        if is_founder_led:
            bonus += 2
            tier += " + Founder-Led"
            score = min(100, score + 10)
            
        return {
            'score': score,
            'tier': tier,
            'insider_ownership_pct': round(insider_pct, 1),
            'is_founder_led': is_founder_led,
            'bonus': bonus,
            'weight': 0.0
        }


class BuybackIntensityFactor:
    MAX_BONUS = 6
    
    def calculate(self, stock_data: dict) -> dict:
        shares_change_1y = stock_data.get('shares_change_1y_pct', 0)
        shares_change_3y = stock_data.get('shares_change_3y_pct', 0)
        
        if shares_change_1y <= -5:
            score = 100
            tier = "Aggressive Buybacks"
            bonus = 4
        elif shares_change_1y <= -2:
            score = 85
            tier = "Significant Buybacks"
            bonus = 3
        elif shares_change_1y <= 0:
            score = 65
            tier = "Modest Buybacks"
            bonus = 1
        elif shares_change_1y <= 2:
            score = 45
            tier = "Slight Dilution"
            bonus = 0
        elif shares_change_1y <= 5:
            score = 25
            tier = "Moderate Dilution"
            bonus = -1
        else:
            score = 10
            tier = "Heavy Dilution (Red Flag)"
            bonus = -3
        
        if shares_change_3y <= -10:
            bonus += 2
            tier += " (Consistent Pattern)"
        elif shares_change_3y >= 15:
            bonus -= 2
            tier += " (Chronic Diluter)"
            
        return {
            'score': score,
            'tier': tier,
            'shares_change_1y_pct': round(shares_change_1y, 2),
            'shares_change_3y_pct': round(shares_change_3y, 2),
            'bonus': bonus,
            'weight': 0.0
        }


class MoatProxyFactor:
    MAX_BONUS = 6
    
    def calculate(self, stock_data: dict) -> dict:
        gross_margin = stock_data.get('gross_margin', 0)
        gross_margin_5y_std = stock_data.get('gross_margin_5y_std', 100)
        roic = stock_data.get('roic', 0)
        wacc = stock_data.get('wacc', 10)
        
        moat_score = 0
        moat_signals = []
        
        if gross_margin >= 50 and gross_margin_5y_std <= 3:
            moat_score += 35
            moat_signals.append("Stable high margins")
        elif gross_margin >= 40 and gross_margin_5y_std <= 5:
            moat_score += 25
            moat_signals.append("Good margin stability")
        elif gross_margin >= 30:
            moat_score += 15
            moat_signals.append("Decent margins")
        
        roic_spread = roic - wacc
        if roic_spread >= 15:
            moat_score += 40
            moat_signals.append("Exceptional returns on capital")
        elif roic_spread >= 8:
            moat_score += 30
            moat_signals.append("Strong returns on capital")
        elif roic_spread >= 3:
            moat_score += 15
            moat_signals.append("Above-average returns")
        
        if moat_score >= 60:
            tier = "Strong Moat Proxy"
            bonus = 5
        elif moat_score >= 40:
            tier = "Moderate Moat Proxy"
            bonus = 3
        elif moat_score >= 20:
            tier = "Weak Moat Proxy"
            bonus = 1
        else:
            tier = "No Moat Signals"
            bonus = 0
            
        return {
            'score': moat_score,
            'tier': tier,
            'source': 'calculated',
            'moat_signals': moat_signals,
            'gross_margin': gross_margin,
            'gross_margin_5y_std': gross_margin_5y_std,
            'roic': roic,
            'roic_spread': round(roic_spread, 2),
            'bonus': bonus,
            'weight': 0.0
        }
