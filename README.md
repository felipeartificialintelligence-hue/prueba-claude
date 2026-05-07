# clima.py

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Consulta el clima actual de cualquier ciudad usando la API gratuita de [Open-Meteo](https://open-meteo.com/) — sin API key. Disponible como CLI y como API REST.

---

## CLI

```bash
python3 clima.py <ciudad>
python3 clima.py "San Felipe, Chile"
python3 clima.py "Buenos Aires, Argentina"
```

**Ejemplo de salida:**

```
Clima actual en San Felipe, Chile
  Condicion:      Despejado
  Temperatura:    16.5 °C
  Sensacion:      13.1 °C
  Humedad:        37 %
  Viento:         10.7 km/h
  Actualizacion:  2026-05-07T15:45
```

---

## API REST

### Instalación

```bash
pip install -r requirements.txt
```

### Iniciar servidor

```bash
python3 -m uvicorn api:app --port 8000
```

### Endpoints

#### `GET /weather`

| Parámetro | Tipo   | Descripción                          |
|-----------|--------|--------------------------------------|
| `city`    | string | Nombre de ciudad, ej: `San Felipe, Chile` |

**Ejemplo:**

```bash
curl "http://localhost:8000/weather?city=San+Felipe,+Chile"
```

**Respuesta:**

```json
{
  "city": "San Felipe",
  "country": "Chile",
  "latitude": -32.74976,
  "longitude": -70.72584,
  "condition": "Despejado",
  "temperature_c": 16.3,
  "feels_like_c": 13.0,
  "humidity_pct": 38,
  "wind_kmh": 10.5,
  "updated_at": "2026-05-07T16:00"
}
```

#### `GET /docs`

Documentación interactiva (Swagger UI) en `http://localhost:8000/docs`.

---

---

## Docker

### Build y run

```bash
docker build -t clima-api .
docker run -p 8000:8000 clima-api
```

La API quedará disponible en `http://localhost:8000`.

---

## Requisitos

- Python 3.x
- CLI: sin dependencias externas (solo stdlib)
- API: `fastapi`, `uvicorn` (ver `requirements.txt`)
