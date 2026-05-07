import sys
import urllib.request
import json

WMO_CODES = {
    0: "Despejado", 1: "Mayormente despejado", 2: "Parcialmente nublado", 3: "Nublado",
    45: "Niebla", 48: "Niebla con escarcha",
    51: "Llovizna ligera", 53: "Llovizna moderada", 55: "Llovizna densa",
    61: "Lluvia ligera", 63: "Lluvia moderada", 65: "Lluvia intensa",
    71: "Nieve ligera", 73: "Nieve moderada", 75: "Nieve intensa",
    80: "Chubascos ligeros", 81: "Chubascos moderados", 82: "Chubascos violentos",
    95: "Tormenta eléctrica", 99: "Tormenta con granizo",
}

def fetch(url):
    with urllib.request.urlopen(url, timeout=10) as r:
        return json.loads(r.read())

def geocode(city):
    parts = [p.strip() for p in city.split(",")]
    name_query = parts[0]
    country_hint = parts[1].lower() if len(parts) > 1 else None

    url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(name_query)}&count=10&language=es"
    data = fetch(url)
    results = data.get("results")
    if not results:
        print(f"Ciudad '{city}' no encontrada.")
        sys.exit(1)

    if country_hint:
        match = next(
            (r for r in results if country_hint in r.get("country", "").lower()),
            None,
        )
        if match:
            results = [match]

    r = results[0]
    return r["latitude"], r["longitude"], r["name"], r.get("country", "")

def get_weather(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,apparent_temperature,relative_humidity_2m,"
        f"wind_speed_10m,weathercode"
        f"&wind_speed_unit=kmh&timezone=auto"
    )
    return fetch(url)["current"]

def main():
    if len(sys.argv) < 2:
        print("Uso: python clima.py <ciudad>")
        sys.exit(1)

    import urllib.parse
    city = " ".join(sys.argv[1:])
    lat, lon, name, country = geocode(city)
    w = get_weather(lat, lon)

    desc = WMO_CODES.get(w["weathercode"], f"Código {w['weathercode']}")

    print(f"\nClima actual en {name}, {country}")
    print(f"  Condicion:      {desc}")
    print(f"  Temperatura:    {w['temperature_2m']} °C")
    print(f"  Sensacion:      {w['apparent_temperature']} °C")
    print(f"  Humedad:        {w['relative_humidity_2m']} %")
    print(f"  Viento:         {w['wind_speed_10m']} km/h")
    print(f"  Actualizacion:  {w['time']}\n")

if __name__ == "__main__":
    main()
