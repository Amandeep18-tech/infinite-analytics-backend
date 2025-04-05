import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.routers import auth, profile, binance, weather
from starlette.middleware.sessions import SessionMiddleware
load_dotenv(override=True)


app = FastAPI()
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("JWT_SECRET")
)
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(binance.router)
app.include_router(weather.router)
