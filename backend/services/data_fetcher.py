import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging
from backend.utils.constants import STOCK_UNIVERSE, SECTOR_MAP

logger = logging.getLogger(__name__)


def to_python(value):
    if value is None:
        return 0
    if isinstance(value, (np.bool_, np.integer, np.floating)):
        return value.item()
    if isinstance(value, np.ndarray):
        return value.tolist()
    if pd.isna(value):
        return 0
    return value


class DataFetcher:
    def __init__(self):
        self.cache = {}
        self.cache_duration = timedelta(hours=1)
    
    def get_stock_data(self, ticker: str) -> Optional[Dict[str, Any]]:
        cache_key = f"{ticker}_data"
        if cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            if datetime.now() - cached_time < self.cache_duration:
                return cached_data
        
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            hist = stock.history(period="1y")
            if hist.empty:
                return None
            
            current_price = hist['Close'].iloc[-1] if not hist.empty else info.get('currentPrice', 0)
            high_52w = hist['High'].max() if not hist.empty else info.get('fiftyTwoWeekHigh', current_price)
            low_52w = hist['Low'].min() if not hist.empty else info.get('fiftyTwoWeekLow', current_price)
            
            price_1m_ago = hist['Close'].iloc[-22] if len(hist) >= 22 else hist['Close'].iloc[0]
            price_3m_ago = hist['Close'].iloc[-66] if len(hist) >= 66 else hist['Close'].iloc[0]
            price_6m_ago = hist['Close'].iloc[-132] if len(hist) >= 132 else hist['Close'].iloc[0]
            
            return_1m = ((current_price - price_1m_ago) / price_1m_ago * 100) if price_1m_ago > 0 else 0
            return_3m = ((current_price - price_3m_ago) / price_3m_ago * 100) if price_3m_ago > 0 else 0
            return_6m = ((current_price - price_6m_ago) / price_6m_ago * 100) if price_6m_ago > 0 else 0
            
            market_cap = info.get('marketCap', 0)
            enterprise_value = info.get('enterpriseValue', market_cap)
            total_equity = info.get('bookValue', 0) * info.get('sharesOutstanding', 0) if info.get('bookValue') else 0
            
            if total_equity == 0:
                total_equity = info.get('totalStockholderEquity', 0)
            
            total_assets = info.get('totalAssets', 0)
            free_cash_flow = info.get('freeCashflow', 0)
            ebitda = info.get('ebitda', 0)
            revenue = info.get('totalRevenue', 0)
            net_income = info.get('netIncomeToCommon', 0)
            
            financials = stock.financials
            prev_total_assets = 0
            prev_ebitda = 0
            
            if financials is not None and not financials.empty:
                try:
                    if 'Total Assets' in financials.index and len(financials.columns) >= 2:
                        prev_total_assets = financials.loc['Total Assets'].iloc[1] if not pd.isna(financials.loc['Total Assets'].iloc[1]) else 0
                    if 'EBITDA' in financials.index and len(financials.columns) >= 2:
                        prev_ebitda = financials.loc['EBITDA'].iloc[1] if not pd.isna(financials.loc['EBITDA'].iloc[1]) else 0
                except:
                    pass
            
            asset_growth = ((total_assets - prev_total_assets) / prev_total_assets * 100) if prev_total_assets > 0 else 0
            ebitda_growth = ((ebitda - prev_ebitda) / abs(prev_ebitda) * 100) if prev_ebitda != 0 else 0
            
            sector = info.get('sector', 'Unknown')
            for sec, tickers in SECTOR_MAP.items():
                if ticker in tickers:
                    sector = sec
                    break
            
            gross_profit = info.get('grossProfits', 0)
            gross_margin = (gross_profit / revenue * 100) if revenue > 0 else 0
            
            shares_outstanding = info.get('sharesOutstanding', 0)
            insider_pct = info.get('heldPercentInsiders', 0) * 100 if info.get('heldPercentInsiders') else 0
            
            shares_change_1y = 0
            shares_change_3y = 0
            try:
                balance_sheet = stock.balance_sheet
                if balance_sheet is not None and not balance_sheet.empty:
                    if 'Common Stock' in balance_sheet.index or 'Ordinary Shares Number' in balance_sheet.index:
                        shares_row = 'Ordinary Shares Number' if 'Ordinary Shares Number' in balance_sheet.index else 'Common Stock'
                        if len(balance_sheet.columns) >= 2:
                            current_shares = balance_sheet.loc[shares_row].iloc[0]
                            prev_shares = balance_sheet.loc[shares_row].iloc[1]
                            if prev_shares and prev_shares > 0 and not pd.isna(current_shares) and not pd.isna(prev_shares):
                                shares_change_1y = ((current_shares - prev_shares) / prev_shares) * 100
                        if len(balance_sheet.columns) >= 4:
                            shares_3y_ago = balance_sheet.loc[shares_row].iloc[3]
                            current_shares = balance_sheet.loc[shares_row].iloc[0]
                            if shares_3y_ago and shares_3y_ago > 0 and not pd.isna(current_shares) and not pd.isna(shares_3y_ago):
                                shares_change_3y = ((current_shares - shares_3y_ago) / shares_3y_ago) * 100
            except:
                pass
            
            roic = 0
            try:
                operating_income = info.get('operatingIncome', 0)
                invested_capital = total_equity + info.get('totalDebt', 0) - info.get('cash', 0)
                if invested_capital > 0:
                    roic = (operating_income / invested_capital) * 100
            except:
                pass
            
            total_debt = info.get('totalDebt', 0)
            cash = info.get('cash', info.get('totalCash', 0))
            
            stock_data = {
                'ticker': ticker,
                'company_name': info.get('shortName', info.get('longName', ticker)),
                'sector': sector,
                'industry': info.get('industry', 'Unknown'),
                'market_cap': to_python(market_cap),
                'enterprise_value': to_python(enterprise_value),
                'current_price': to_python(current_price),
                'total_equity': to_python(total_equity),
                'total_assets': to_python(total_assets),
                'free_cash_flow': to_python(free_cash_flow),
                'ebitda': to_python(ebitda),
                'revenue': to_python(revenue),
                'net_income': to_python(net_income),
                'high_52_week': to_python(high_52w),
                'low_52_week': to_python(low_52w),
                'return_1_month': to_python(return_1m),
                'return_3_month': to_python(return_3m),
                'return_6_month': to_python(return_6m),
                'asset_growth_yoy': to_python(asset_growth),
                'ebitda_growth_yoy': to_python(ebitda_growth),
                'gross_margin': to_python(gross_margin),
                'gross_margin_5y_std': 5.0,
                'roic': to_python(roic),
                'wacc': 10.0,
                'insider_ownership_pct': to_python(insider_pct),
                'founder_ceo': False,
                'shares_change_1y_pct': to_python(shares_change_1y),
                'shares_change_3y_pct': to_python(shares_change_3y),
                'total_debt': to_python(total_debt),
                'cash': to_python(cash),
                'last_updated': datetime.now().isoformat()
            }
            
            self.cache[cache_key] = (stock_data, datetime.now())
            
            return stock_data
            
        except Exception as e:
            logger.error(f"Error fetching data for {ticker}: {str(e)}")
            return None
    
    def get_macro_data(self) -> Dict[str, Any]:
        return {
            'fed_funds_rate': 4.5,
            'fed_funds_rate_1y_ago': 5.25,
            'fed_rate_trajectory': 'falling'
        }
    
    def get_all_stocks(self, tickers: List[str] = None) -> List[Dict[str, Any]]:
        if tickers is None:
            tickers = STOCK_UNIVERSE
        
        stocks_data = []
        for ticker in tickers:
            data = self.get_stock_data(ticker)
            if data:
                stocks_data.append(data)
        
        return stocks_data
    
    def get_stock_universe(self) -> List[str]:
        return STOCK_UNIVERSE.copy()
