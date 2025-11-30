import httpx
from fastmcp import FastMCP

mcp = FastMCP("WeatherMCP")


async def fetch_weather(lat: float, lon: float, unit: str = "metric") -> dict:
    """
    Fetch current weather from Open-Meteo (no API key needed).
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "hourly": "temperature_2m,relativehumidity_2m,weathercode",
        "forecast_days": 1,
    }
    if unit == "imperial":
        params["temperature_unit"] = "fahrenheit"
        params["windspeed_unit"] = "mph"

    async with httpx.AsyncClient(timeout=8) as client:
        response = await client.get("https://api.open-meteo.com/v1/forecast", params=params)
        response.raise_for_status()
        data = response.json()

    current = data.get("current_weather", {})
    return {
        "lat": lat,
        "lon": lon,
        "temperature": current.get("temperature"),
        "windspeed": current.get("windspeed"),
        "winddirection": current.get("winddirection"),
        "weathercode": current.get("weathercode"),
        "time": current.get("time"),
        "unit": unit,
        "source": "open-meteo.com",
    }


@mcp.tool
async def get_weather(lat: float, lon: float, unit: str = "metric") -> dict:
    """Get current weather by coordinates (metric or imperial)."""
    return await fetch_weather(lat, lon, unit)


@mcp.tool
async def get_weather_by_city(city: str, unit: str = "metric") -> dict:
    """Resolve city via Open-Meteo geocoding, then return current weather."""
    async with httpx.AsyncClient(timeout=8) as client:
        geo = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "en", "format": "json"},
        )
        geo.raise_for_status()
        geo_data = geo.json()

    results = geo_data.get("results") or []
    if not results:
        raise ValueError(f"City not found: {city}")

    location = results[0]
    return await fetch_weather(location["latitude"], location["longitude"], unit)


if __name__ == "__main__":
    mcp.run()
