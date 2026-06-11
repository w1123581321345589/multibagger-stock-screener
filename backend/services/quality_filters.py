from typing import Dict, List, Any


class QualityPreFilter:
    STRICT_FILTERS = {
        'revenue_growth_5yr_cagr': ('>=', 7),
        'earnings_growth_5yr_cagr': ('>=', 9),
        'fcf_conversion': ('>=', 85),
        'net_debt_to_ebitda': ('<=', 1),
        'roic': ('>=', 15),
        'profit_margin': ('>=', 10),
    }
    
    LOOSE_FILTERS = {
        'market_cap_min': ('>=', 50_000_000),
        'market_cap_max': ('<=', 50_000_000_000),
        'total_equity': ('>', 0),
        'net_debt_to_ebitda': ('<=', 4),
    }
    
    EXCLUSIONS = {
        'sectors': ['Financials'],
        'industries': [
            'Shell Companies',
            'Blank Checks', 
            'Asset Management',
            'REITs'
        ]
    }
    
    def apply_filters(self, stock_data: dict, mode: str = 'multibagger') -> dict:
        filters = self.LOOSE_FILTERS if mode == 'multibagger' else self.STRICT_FILTERS
        failed = []
        warnings = []
        
        market_cap = stock_data.get('market_cap', 0)
        total_equity = stock_data.get('total_equity', 0)
        ebitda = stock_data.get('ebitda', 0)
        total_debt = stock_data.get('total_debt', 0)
        
        if mode == 'multibagger':
            if market_cap < 50_000_000:
                failed.append(f"Market cap too small: ${market_cap:,.0f} < $50M")
            if market_cap > 50_000_000_000:
                failed.append(f"Market cap too large: ${market_cap:,.0f} > $50B")
            if total_equity <= 0:
                failed.append(f"Negative or zero equity: ${total_equity:,.0f}")
            if ebitda > 0:
                net_debt_to_ebitda = (total_debt - stock_data.get('cash', 0)) / ebitda
                if net_debt_to_ebitda > 4:
                    failed.append(f"Too much leverage: Net Debt/EBITDA = {net_debt_to_ebitda:.1f}")
        else:
            roic = stock_data.get('roic', 0)
            if roic < 15:
                failed.append(f"ROIC too low: {roic:.1f}% < 15%")
            fcf = stock_data.get('free_cash_flow', 0)
            net_income = stock_data.get('net_income', 0)
            if net_income > 0:
                fcf_conversion = (fcf / net_income) * 100
                if fcf_conversion < 85:
                    failed.append(f"FCF conversion too low: {fcf_conversion:.1f}% < 85%")
            if ebitda > 0:
                net_debt_to_ebitda = (total_debt - stock_data.get('cash', 0)) / ebitda
                if net_debt_to_ebitda > 1:
                    failed.append(f"Too much leverage for compounder: Net Debt/EBITDA = {net_debt_to_ebitda:.1f}")
        
        sector = stock_data.get('sector', '')
        industry = stock_data.get('industry', '')
        
        if sector in self.EXCLUSIONS['sectors']:
            failed.append(f"Excluded sector: {sector}")
        if industry in self.EXCLUSIONS['industries']:
            failed.append(f"Excluded industry: {industry}")
            
        return {
            'passed': len(failed) == 0,
            'failed_filters': failed,
            'warnings': warnings
        }
