import requests
import os

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


def fetch_air_quality(lat: float, lon: float):
    url = (
        "http://api.openweathermap.org/data/2.5/air_pollution"
        f"?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
    )

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    aqi_data = data["list"][0]

    return {
        "aqi": aqi_data["main"]["aqi"],  # 1 (Good) → 5 (Very Poor)
        "pm2_5": aqi_data["components"]["pm2_5"],
        "pm10": aqi_data["components"]["pm10"],
        "co": aqi_data["components"]["co"],
        "no2": aqi_data["components"]["no2"],
        "o3": aqi_data["components"]["o3"]
    }