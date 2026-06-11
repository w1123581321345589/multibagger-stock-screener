FACTOR_WEIGHTS = {
    'fcf_yield': 0.20,
    'book_to_market': 0.15,
    'momentum': 0.14,
    'size': 0.12,
    'profitability': 0.12,
    'investment_pattern': 0.12,
    'macro': 0.10,
    'quality_adjustments': 0.05
}

SIZE_THRESHOLDS = {
    'micro_cap': 250_000_000,
    'small_cap': 500_000_000,
    'mid_cap_low': 2_000_000_000,
    'mid_cap_high': 10_000_000_000,
}

BTM_THRESHOLDS = {
    'deep_value': 1.0,
    'strong_value': 0.70,
    'moderate_value': 0.40,
    'growth_valued': 0.20,
}

FCF_YIELD_THRESHOLDS = {
    'exceptional': 10,
    'strong': 7,
    'good': 5,
    'moderate': 3,
    'low': 1,
}

EBITDA_MARGIN_THRESHOLDS = {
    'exceptional': 25,
    'strong': 18,
    'good': 12,
    'moderate': 5,
}

STOCK_UNIVERSE = [
    # Small/Mid Cap First - Better Multibagger Potential
    "UPST", "BILL", "PATH", "DOCS", "GTLB", "MARA", "RIOT", "IONQ", "SOFI", "HOOD",
    "COIN", "PLTR", "RBLX", "DKNG", "PINS", "SNAP", "ROKU", "SQ", "MGNI", "PUBM",
    "GPRO", "SONO", "CRSR", "DM", "SSYS", "DDD", "NNOX", "BFLY", "DNA", "RXRX",
    # Mid Cap ($2B-$10B)
    "PYPL", "U", "ABNB", "DASH", "CRWD", "SNOW", "SHOP", "MELI", "AMD", "MU",
    # Large Cap (for comparison/benchmarking)
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "BRK-B", "JPM", "JNJ",
    "V", "PG", "UNH", "HD", "MA", "DIS", "BAC", "ADBE", "CRM", "NFLX",
    "XOM", "VZ", "INTC", "T", "PFE", "MRK", "CVX", "WMT", "KO", "GILD"
]

SECTOR_MAP = {
    "Technology": ["AAPL", "MSFT", "GOOGL", "NVDA", "AMD", "INTC", "ORCL", "CRM", "ADBE", "NOW", "PLTR", "CRWD", "SNOW"],
    "Communication": ["META", "NFLX", "DIS", "VZ", "T", "GOOGL", "ROKU", "SNAP", "PINS"],
    "Consumer Cyclical": ["AMZN", "TSLA", "HD", "NKE", "MCD", "SBUX", "LOW", "TGT", "BKNG", "ABNB", "DASH"],
    "Financial": ["BRK-B", "JPM", "BAC", "GS", "BLK", "AXP", "C", "SCHW", "PNC", "USB", "COIN", "HOOD", "SOFI"],
    "Healthcare": ["JNJ", "UNH", "PFE", "MRK", "ABT", "TMO", "LLY", "ABBV", "AMGN", "GILD", "BMY", "MDT", "ISRG", "ZTS", "SYK", "DHR"],
    "Consumer Defensive": ["PG", "WMT", "KO", "PEP", "COST", "CL", "MDLZ"],
    "Energy": ["XOM", "CVX"],
    "Industrials": ["CAT", "HON", "UNP", "DE", "MMM", "ADP"],
    "Utilities": ["DUK", "SO"],
    "Real Estate": ["PLD"],
}
