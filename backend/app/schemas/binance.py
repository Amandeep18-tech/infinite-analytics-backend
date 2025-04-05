from pydantic import BaseModel,Field
from typing import List, Literal

class Kline(BaseModel):
    open_time: int
    open: str
    high: str
    low: str
    close: str
    volume: str
    close_time: int

class KlineRequest(BaseModel):
    symbol: str = Field(..., example="BTCUSDT", description="Symbol pair (e.g., BTCUSDT)")
    interval: Literal[
        "1m", "3m", "5m", "15m", "30m", "1h", "2h",
        "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"
    ] = Field(..., description="Interval for each candlestick")
    limit: int = Field(100, gt=0, le=1000, description="Number of data points to fetch")