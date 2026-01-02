def summarize_environment(weather: dict, air: dict) -> str:
    return (
        f"Weather conditions: temperature {weather['temperature_c']}°C, "
        f"humidity {weather['humidity_pct']}%, "
        f"rainfall {weather['rain_mm']} mm, "
        f"climate is {weather['climate']}. "
        f"Air quality index (AQI) is {air['aqi']} "
        f"(PM2.5: {air['pm2_5']}, PM10: {air['pm10']})."
    )