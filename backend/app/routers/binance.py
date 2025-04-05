from typing import List
from backend.app.schemas.binance import Kline, KlineRequest
from fastapi import APIRouter, HTTPException,Depends
import httpx

router = APIRouter(prefix="/binance", tags=["Binance"])

BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/24hr"

@router.get("/coins")
async def get_all_coins():
    async with httpx.AsyncClient() as client:
        response = await client.get(BINANCE_API_URL)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch data from Binance")
        return response.json()

@router.get("/coin/{symbol}")
async def get_coin(symbol: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(BINANCE_API_URL)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch data from Binance")
        
        coins = response.json()
        coin_data = next((coin for coin in coins if coin["symbol"] == symbol.upper()), None)
        if not coin_data:
            raise HTTPException(status_code=404, detail="Coin not found")

        trend = "📈 Rising" if float(coin_data["priceChangePercent"]) > 0 else "📉 Falling"
        return {
            "symbol": coin_data["symbol"],
            "lastPrice": coin_data["lastPrice"],
            "priceChangePercent": coin_data["priceChangePercent"],
            "trend": trend
        }

@router.get("/klines", response_model=List[Kline])
async def get_klines(req: KlineRequest = Depends()):
    """
    Retrieve Kline (candlestick) data for a specific symbol and interval.
    """
    params = {
        "symbol": req.symbol.upper(),
        "interval": req.interval,
        "limit": req.limit
    }
    print(params)
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.binance.com/api/v3/klines", params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch data from Binance")

        kline_data = response.json()

        return [
            Kline(
                open_time=k[0],
                open=k[1],
                high=k[2],
                low=k[3],
                close=k[4],
                volume=k[5],
                close_time=k[6]
            )
            for k in kline_data
        ]