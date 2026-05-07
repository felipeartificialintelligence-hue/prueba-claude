# clima.py

CLI para consultar el clima actual de cualquier ciudad usando la API gratuita de [Open-Meteo](https://open-meteo.com/) — sin API key.

## Uso

```bash
python3 clima.py <ciudad>
python3 clima.py "San Felipe, Chile"
python3 clima.py "Buenos Aires, Argentina"
```

## Ejemplo

```
Clima actual en San Felipe, Chile
  Condicion:      Despejado
  Temperatura:    16.5 °C
  Sensacion:      13.1 °C
  Humedad:        37 %
  Viento:         10.7 km/h
  Actualizacion:  2026-05-07T15:45
```

## Requisitos

- Python 3.x
- Sin dependencias externas (solo stdlib)
