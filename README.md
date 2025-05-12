# ETL Sismología - Perú

¿Sabías que Perú registra más de 400 sismos perceptibles al año y que se ubica en una de las zonas de subducción más activas del planeta? El terremoto de Pisco en 2007 (8.0 Mw) dejó 595 muertos y más de USD 500 millones en daños. La data sísmica para anticipar patrones de riesgo existe, pero estaba dispersa en un catálogo de texto plano del USGS.

Soy Gian Cruz. Construí este pipeline ETL para consumir la API pública del USGS, extraer eventos sísmicos dentro del territorio peruano, clasificarlos por magnitud, profundidad y región, y calcular la relación Gutenberg-Richter que describe la distribución estadística de magnitudes. Todo containerizado con Docker.

## Qué hace

- Consulta la API USGS FDSNWS filtrando por bounding box de Perú
- Parsea features GeoJSON a registros tabulares
- Clasifica sismos por magnitud (micro a gran), profundidad y región
- Genera estadísticas mensuales por región sísmica
- Calcula distribución de magnitudes y relación Gutenberg-Richter
- Identifica eventos significativos (mag >= 5.0)
- Análisis de profundidad por región (superficial, intermedio, profundo)
- Carga a SQLite con índices optimizados
- Contenedorizado con Docker

## Instalación

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Uso

```bash
# Pipeline completo (2014-2024, mag >= 2.0)
python -m src.pipeline

# Rango personalizado
python -m src.pipeline --start 2020 --end 2024 --min-mag 3.0
```

### Con Docker

```bash
docker compose up --build
```

## Tests

```bash
pytest tests/ -v
```

## Stack

- Python 3.10+
- requests (API USGS)
- pandas + numpy
- SQLite
- Docker
- pytest

## Estructura

```
etl-sismologia-peru/
├── src/
│   ├── config/settings.py         # Bbox Perú, categorías, config
│   ├── extract/usgs_client.py     # Cliente API USGS con retry
│   ├── transform/
│   │   ├── cleaner.py             # Parsing GeoJSON, clasificaciones
│   │   └── enricher.py            # Stats, Gutenberg-Richter
│   ├── quality/validators.py      # Validación de rangos y completitud
│   ├── load/warehouse.py          # SQLite con indices
│   ├── utils/logger.py
│   └── pipeline.py                # Orquestador (CLI)
├── tests/
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Fuentes de datos

| Fuente | Descripción | Enlace |
|--------|-------------|--------|
| USGS Earthquake Catalog API | API pública de eventos sísmicos globales (GeoJSON) | [https://earthquake.usgs.gov/fdsnws/event/1/](https://earthquake.usgs.gov/fdsnws/event/1/) |
| USGS Earthquake Hazards Program | Programa de monitoreo sísmico del USGS | [https://earthquake.usgs.gov/](https://earthquake.usgs.gov/) |
| IGP Perú | Instituto Geofísico del Perú - monitoreo sísmico nacional | [https://www.igp.gob.pe/servicios/centro-sismologico-nacional/](https://www.igp.gob.pe/servicios/centro-sismologico-nacional/) |

## Licencia

MIT

---

# Seismology ETL - Peru

Did you know Peru records over 400 perceptible earthquakes per year and sits on one of the most active subduction zones on the planet? The 2007 Pisco earthquake (8.0 Mw) killed 595 people and caused over USD 500 million in damages. The seismic data to anticipate risk patterns exists, but it was scattered across USGS plain-text catalogs.

I'm Gian Cruz. I built this ETL pipeline to consume the USGS public API, extract seismic events within Peruvian territory, classify them by magnitude, depth, and region, and compute the Gutenberg-Richter relationship that describes the statistical distribution of earthquake magnitudes.

## Quick start

```bash
git clone https://github.com/giansocial/etl-sismologia-peru.git
cd etl-sismologia-peru
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python -m src.pipeline --start 2010 --end 2024
```

## Data sources

| Source | Description | Link |
|--------|-------------|------|
| USGS Earthquake Catalog API | Global seismic events public API (GeoJSON) | [https://earthquake.usgs.gov/fdsnws/event/1/](https://earthquake.usgs.gov/fdsnws/event/1/) |
| USGS Earthquake Hazards Program | USGS seismic monitoring program | [https://earthquake.usgs.gov/](https://earthquake.usgs.gov/) |

## License

MIT
