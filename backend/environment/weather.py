import requests
import os

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


def fetch_weather(lat: float, lon: float):
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&units=metric&appid={OPENWEATHER_API_KEY}"
    )

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    return {
        "temperature_c": data["main"]["temp"],
        "humidity_pct": data["main"]["humidity"],
        "rain_mm": data.get("rain", {}).get("1h", 0),
        "wind_speed": data["wind"]["speed"],
        "climate": data["weather"][0]["description"]
    }