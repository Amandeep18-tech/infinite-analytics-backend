from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter(prefix="/weather", tags=["Weather"])

SG_WEATHER_API = "https://api.data.gov.sg/v1/environment/air-temperature"

@router.get("/temperature")
async def get_weather():
    async with httpx.AsyncClient() as client:
        response = await client.get(SG_WEATHER_API)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch data from SG Weather API")

        data = response.json()
        return {
            "timestamp": data.get("items", [{}])[0].get("timestamp"),
            "readings": data.get("items", [{}])[0].get("readings", []),
            "stations": data.get("metadata", {}).get("stations", [])
        }
