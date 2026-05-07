import urllib.request
import urllib.parse
import json

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI(title="Clima API", description="Clima actual por ciudad usando Open-Meteo")

WMO_CODES = {
    0: "Despejado", 1: "Mayormente despejado", 2: "Parcialmente nublado", 3: "Nublado",
    45: "Niebla", 48: "Niebla con escarcha",
    51: "Llovizna ligera", 53: "Llovizna moderada", 55: "Llovizna densa",
    61: "Lluvia ligera", 63: "Lluvia moderada", 65: "Lluvia intensa",
    71: "Nieve ligera", 73: "Nieve moderada", 75: "Nieve intensa",
    80: "Chubascos ligeros", 81: "Chubascos moderados", 82: "Chubascos violentos",
    95: "Tormenta eléctrica", 99: "Tormenta con granizo",
}


class WeatherResponse(BaseModel):
    city: str
    country: str
    latitude: float
    longitude: float
    condition: str
    temperature_c: float
    feels_like_c: float
    humidity_pct: int
    wind_kmh: float
    updated_at: str


def fetch(url: str):
    with urllib.request.urlopen(url, timeout=10) as r:
        return json.loads(r.read())


def geocode(city: str):
    parts = [p.strip() for p in city.split(",")]
    name_query = parts[0]
    country_hint = parts[1].lower() if len(parts) > 1 else None

    url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(name_query)}&count=10&language=es"
    data = fetch(url)
    results = data.get("results")
    if not results:
        raise HTTPException(status_code=404, detail=f"Ciudad '{city}' no encontrada.")

    if country_hint:
        match = next(
            (r for r in results if country_hint in r.get("country", "").lower()), None
        )
        if match:
            results = [match]

    r = results[0]
    return r["latitude"], r["longitude"], r["name"], r.get("country", "")


def get_weather(lat: float, lon: float):
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,apparent_temperature,relative_humidity_2m,"
        f"wind_speed_10m,weathercode"
        f"&wind_speed_unit=kmh&timezone=auto"
    )
    return fetch(url)["current"]


@app.get("/weather", response_model=WeatherResponse)
def weather(city: str = Query(..., description="Nombre de ciudad, ej: 'San Felipe, Chile'")):
    lat, lon, name, country = geocode(city)
    w = get_weather(lat, lon)
    return WeatherResponse(
        city=name,
        country=country,
        latitude=lat,
        longitude=lon,
        condition=WMO_CODES.get(w["weathercode"], f"Código {w['weathercode']}"),
        temperature_c=w["temperature_2m"],
        feels_like_c=w["apparent_temperature"],
        humidity_pct=w["relative_humidity_2m"],
        wind_kmh=w["wind_speed_10m"],
        updated_at=w["time"],
    )
