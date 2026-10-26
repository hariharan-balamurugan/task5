
import os
from statistics import mean

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query

load_dotenv()

app = FastAPI(title="Weather API")

API_URL = os.getenv(
    "OPEN_METEO_URL",
    "https://api.open-meteo.com/v1/forecast"
)

DEFAULT_LATITUDE = float(os.getenv("DEFAULT_LATITUDE", "11.0168"))
DEFAULT_LONGITUDE = float(os.getenv("DEFAULT_LONGITUDE", "76.9558"))
TIMEOUT = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "10"))


@app.get("/")
def home():
    return {"message": "Welcome to Weather API"}


@app.get("/weather")
async def get_weather(
    latitude: float = Query(DEFAULT_LATITUDE, ge=-90, le=90),
    longitude: float = Query(DEFAULT_LONGITUDE, ge=-180, le=180)
):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m",
        "forecast_days": 1,
        "timezone": "auto"
    }

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(API_URL, params=params)
            response.raise_for_status()
            data = response.json()

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Weather API request timed out"
        )

    except httpx.HTTPError:
        raise HTTPException(
            status_code=502,
            detail="Failed to fetch weather data"
        )

    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    temperatures = hourly.get("temperature_2m", [])

    readings = [
        {"time": time, "temperature": temp}
        for time, temp in zip(times, temperatures)
        if isinstance(temp, (int, float))
    ]

    if not readings:
        raise HTTPException(
            status_code=502,
            detail="No temperature data available"
        )

    values = [item["temperature"] for item in readings]

    average_temp = round(mean(values), 2)
    min_temp = round(min(values), 2)
    max_temp = round(max(values), 2)

    if average_temp < 10:
        summary = "Cold weather"
    elif average_temp < 25:
        summary = "Mild weather"
    else:
        summary = "Warm weather"

    return {
        "location": {
            "latitude": data.get("latitude", latitude),
            "longitude": data.get("longitude", longitude),
            "timezone": data.get("timezone", "unknown")
        },
        "average_temperature": average_temp,
        "minimum_temperature": min_temp,
        "maximum_temperature": max_temp,
        "temperature_unit": data.get(
            "hourly_units", {}
        ).get("temperature_2m", "°C"),
        "summary": summary,
        "hourly_forecast": readings
    }