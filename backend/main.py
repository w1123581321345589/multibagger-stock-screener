from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Optional, List
from enum import Enum
import os

from backend.services.data_fetcher import DataFetcher
from backend.services.scoring_engine import MultibaggerScorer
from backend.services.stock_universe import stock_universe_service
from backend.utils.constants import STOCK_UNIVERSE, SECTOR_MAP


class ScreenerMode(str, Enum):
    multibagger = "multibagger"
    compounder = "compounder"


app = FastAPI(title="Multibagger Stock Screener", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data_fetcher = DataFetcher()


@app.get("/api/screen")
async def screen_stocks(
    min_score: int = Query(50, description="Minimum composite score (0-100)"),
    max_market_cap: Optional[float] = Query(None, description="Maximum market cap in billions"),
    sectors: Optional[str] = Query(None, description="Comma-separated list of sectors"),
    limit: int = Query(50, description="Maximum number of results"),
    tickers: Optional[str] = Query(None, description="Comma-separated list of specific tickers to analyze"),
    mode: ScreenerMode = Query(ScreenerMode.multibagger, description="Screening mode: multibagger or compounder"),
    apply_prefilter: bool = Query(False, description="Apply quality pre-filters before scoring"),
    universe: str = Query("default", description="Universe source: default, small_cap, mid_cap, or expanded")
):
    try:
        scorer = MultibaggerScorer(mode=mode.value)
        
        if tickers:
            ticker_list = tickers.split(",")
        elif universe == "small_cap":
            ticker_list = stock_universe_service.get_small_cap_stocks(100)
        elif universe == "mid_cap":
            ticker_list = stock_universe_service.get_mid_cap_stocks(100)
        elif universe == "expanded":
            ticker_list = stock_universe_service.get_screener_stocks(limit=150)
        else:
            ticker_list = STOCK_UNIVERSE[:50]
        
        stocks_data = data_fetcher.get_all_stocks(ticker_list)
        macro_data = data_fetcher.get_macro_data()
        
        sector_list = sectors.split(",") if sectors else None
        max_cap = max_market_cap * 1_000_000_000 if max_market_cap else None
        
        results = scorer.screen_stocks(
            stocks_data=stocks_data,
            macro_data=macro_data,
            min_score=min_score,
            sectors=sector_list,
            max_market_cap=max_cap,
            apply_prefilter=apply_prefilter
        )
        
        return {
            "total_screened": len(stocks_data),
            "total_matches": len(results),
            "min_score": min_score,
            "mode": mode.value,
            "macro_environment": macro_data,
            "results": results[:limit]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stock/{ticker}")
async def get_stock_analysis(
    ticker: str,
    mode: ScreenerMode = Query(ScreenerMode.multibagger, description="Screening mode: multibagger or compounder")
):
    try:
        scorer = MultibaggerScorer(mode=mode.value)
        stock_data = data_fetcher.get_stock_data(ticker.upper())
        
        if not stock_data:
            raise HTTPException(status_code=404, detail=f"Stock {ticker} not found")
        
        macro_data = data_fetcher.get_macro_data()
        score_result = scorer.calculate_composite_score(stock_data, macro_data)
        
        return {
            "stock_data": stock_data,
            "score_analysis": score_result,
            "mode": mode.value
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sectors")
async def get_sectors():
    return {"sectors": list(SECTOR_MAP.keys())}


@app.get("/api/universe")
async def get_universe(
    source: str = Query("default", description="Source: default, small_cap, mid_cap, or expanded"),
    limit: int = Query(100, description="Maximum number of tickers")
):
    if source == "small_cap":
        tickers = stock_universe_service.get_small_cap_stocks(limit)
    elif source == "mid_cap":
        tickers = stock_universe_service.get_mid_cap_stocks(limit)
    elif source == "expanded":
        tickers = stock_universe_service.get_screener_stocks(limit=limit)
    else:
        tickers = STOCK_UNIVERSE[:limit]
    
    return {"tickers": tickers, "total": len(tickers), "source": source}


@app.get("/api/macro")
async def get_macro_environment():
    scorer = MultibaggerScorer(mode='multibagger')
    macro_data = data_fetcher.get_macro_data()
    macro_analysis = scorer.macro_factor.calculate(macro_data)
    return {
        "macro_data": macro_data,
        "analysis": macro_analysis
    }


@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "Multibagger Stock Screener"}


frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.exists(frontend_path):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_path, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        file_path = os.path.join(frontend_path, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_path, "index.html"))
