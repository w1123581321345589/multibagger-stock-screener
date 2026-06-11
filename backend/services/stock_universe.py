import requests
import os
from typing import List, Dict, Optional
import json
from datetime import datetime, timedelta

CACHE_FILE = "/tmp/stock_universe_cache.json"
CACHE_TTL = 24  # hours


class StockUniverseService:
    def __init__(self):
        self.fmp_api_key = os.environ.get('FMP_API_KEY', 'demo')
        self.base_url = "https://financialmodelingprep.com/api/v3"

    def _load_cache(self) -> Optional[Dict]:
        try:
            if os.path.exists(CACHE_FILE):
                with open(CACHE_FILE, 'r') as f:
                    cache = json.load(f)
                    cached_time = datetime.fromisoformat(cache.get('timestamp', '2000-01-01'))
                    if datetime.now() - cached_time < timedelta(hours=CACHE_TTL):
                        return cache
        except Exception:
            pass
        return None

    def _save_cache(self, data: Dict):
        try:
            data['timestamp'] = datetime.now().isoformat()
            with open(CACHE_FILE, 'w') as f:
                json.dump(data, f)
        except Exception:
            pass
    
    def get_screener_stocks(self, 
                           market_cap_min: float = None,
                           market_cap_max: float = None,
                           limit: int = 200) -> List[str]:
        cache = self._load_cache()
        if cache and 'tickers' in cache:
            tickers = cache['tickers']
            return tickers[:limit]
        
        try:
            tickers = self._fetch_from_fmp_screener(market_cap_min, market_cap_max, limit)
            if tickers:
                self._save_cache({'tickers': tickers})
                return tickers[:limit]
        except Exception as e:
            print(f"FMP API error: {e}")
        
        return self._get_fallback_universe()[:limit]
    
    def _fetch_from_fmp_screener(self, 
                                  market_cap_min: float = None,
                                  market_cap_max: float = None,
                                  limit: int = 200) -> List[str]:
        url = f"{self.base_url}/stock-screener"
        params = {
            'apikey': self.fmp_api_key,
            'exchange': 'NYSE,NASDAQ',
            'isActivelyTrading': 'true',
            'limit': min(limit * 2, 1000),
        }
        
        if market_cap_min:
            params['marketCapMoreThan'] = int(market_cap_min)
        if market_cap_max:
            params['marketCapLowerThan'] = int(market_cap_max)
        
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            stocks = response.json()
            if isinstance(stocks, list):
                tickers = [s.get('symbol') for s in stocks if s.get('symbol')]
                return tickers
        
        return []
    
    def get_stocks_by_sector(self, sector: str, limit: int = 50) -> List[str]:
        url = f"{self.base_url}/stock-screener"
        params = {
            'apikey': self.fmp_api_key,
            'exchange': 'NYSE,NASDAQ',
            'sector': sector,
            'isActivelyTrading': 'true',
            'limit': limit,
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                stocks = response.json()
                if isinstance(stocks, list):
                    return [s.get('symbol') for s in stocks if s.get('symbol')]
        except Exception as e:
            print(f"Sector screener error: {e}")
        
        return []
    
    def get_small_cap_stocks(self, limit: int = 100) -> List[str]:
        return self.get_screener_stocks(
            market_cap_min=100_000_000,
            market_cap_max=2_000_000_000,
            limit=limit
        )
    
    def get_mid_cap_stocks(self, limit: int = 100) -> List[str]:
        return self.get_screener_stocks(
            market_cap_min=2_000_000_000,
            market_cap_max=10_000_000_000,
            limit=limit
        )
    
    def get_micro_cap_stocks(self, limit: int = 50) -> List[str]:
        return self.get_screener_stocks(
            market_cap_min=50_000_000,
            market_cap_max=300_000_000,
            limit=limit
        )
    
    def _get_fallback_universe(self) -> List[str]:
        return [
            "UPST", "BILL", "PATH", "DOCS", "GTLB", "MARA", "RIOT", "IONQ", "SOFI", "HOOD",
            "COIN", "PLTR", "RBLX", "DKNG", "PINS", "SNAP", "ROKU", "SQ", "MGNI", "PUBM",
            "GPRO", "SONO", "CRSR", "DM", "SSYS", "DDD", "NNOX", "BFLY", "DNA", "RXRX",
            "PYPL", "U", "ABNB", "DASH", "CRWD", "SNOW", "SHOP", "MELI", "AMD", "MU",
            "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "BRK-B", "JPM", "JNJ",
            "V", "PG", "UNH", "HD", "MA", "DIS", "BAC", "ADBE", "CRM", "NFLX",
            "XOM", "VZ", "INTC", "T", "PFE", "MRK", "CVX", "WMT", "KO", "GILD",
            "AFRM", "OPEN", "LMND", "ROOT", "ACHR", "JOBY", "LILM", "EVTL", "RIVN", "LCID",
            "NIO", "XPEV", "LI", "FSR", "GOEV", "WKHS", "RIDE", "NKLA", "HYLN", "ARVL",
            "SPCE", "RKLB", "ASTR", "RDW", "MNTS", "BKSY", "ASTS", "GSAT", "IRDM", "VSAT"
        ]


stock_universe_service = StockUniverseService()
