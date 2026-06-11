from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def format_market_cap(value: float) -> str:
    if value >= 1_000_000_000_000:
        return f"${value / 1_000_000_000_000:.2f}T"
    elif value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    else:
        return f"${value:,.0f}"


def format_percentage(value: float) -> str:
    return f"{value:.2f}%"


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    if denominator == 0 or denominator is None:
        return default
    return numerator / denominator


def get_score_color(score: float) -> str:
    if score >= 80:
        return "green"
    elif score >= 65:
        return "light_green"
    elif score >= 50:
        return "yellow"
    elif score >= 35:
        return "orange"
    else:
        return "red"


def get_classification(score: float) -> str:
    if score >= 80:
        return "STRONG BUY — High Multibagger Potential"
    elif score >= 65:
        return "BUY — Good Multibagger Characteristics"
    elif score >= 50:
        return "HOLD — Some Positive Factors"
    elif score >= 35:
        return "WEAK — Limited Potential"
    else:
        return "AVOID — Poor Multibagger Profile"
