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

## What it does

ETL pipeline consuming the USGS public earthquake API to extract, transform, and analyze seismic activity in Peru. Data loads into a SQLite warehouse with reports on magnitude distribution, depth analysis, and the Gutenberg-Richter relationship.

Peru sits on the Pacific Ring of Fire. The Nazca plate subducts beneath the South American plate, generating constant seismic activity, especially in the southern region.

---

## Fuentes de datos

| Fuente | Descripción | Enlace |
|--------|-------------|--------|
| USGS Earthquake Catalog API | API pública de eventos sísmicos globales (GeoJSON) | [https://earthquake.usgs.gov/fdsnws/event/1/](https://earthquake.usgs.gov/fdsnws/event/1/) |
| USGS Earthquake Hazards Program | Programa de monitoreo sísmico del USGS | [https://earthquake.usgs.gov/](https://earthquake.usgs.gov/) |
| IGP Perú | Instituto Geofísico del Perú - monitoreo sísmico nacional | [https://www.igp.gob.pe/servicios/centro-sismologico-nacional/](https://www.igp.gob.pe/servicios/centro-sismologico-nacional/) |
