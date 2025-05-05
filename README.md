# ETL Sismologia - Peru

Soy Gian Cruz.

Pipeline ETL que consume la API publica del USGS (United States Geological Survey) para extraer, transformar y analizar la actividad sismica del Peru. Los datos se cargan a un warehouse SQLite y se generan reportes de distribucion de magnitud, profundidad y la relacion Gutenberg-Richter.

Peru se ubica en el Cinturon de Fuego del Pacifico y registra miles de sismos al anio. La placa de Nazca subduce bajo la placa Sudamericana generando actividad sismica constante, especialmente en la zona sur del pais.

## Que hace

- Consulta la API USGS FDSNWS filtrando por bounding box de Peru
- Parsea features GeoJSON a registros tabulares
- Clasifica sismos por magnitud (micro a gran), profundidad y region
- Genera estadisticas mensuales por region sismica
- Calcula distribucion de magnitudes y relacion Gutenberg-Richter
- Identifica eventos significativos (mag >= 5.0)
- Analisis de profundidad por region (superficial, intermedio, profundo)
- Carga a SQLite con indices optimizados
- Contenedorizado con Docker

## Instalacion

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
│   ├── config/settings.py         # Bbox Peru, categorias, config
│   ├── extract/usgs_client.py     # Cliente API USGS con retry
│   ├── transform/
│   │   ├── cleaner.py             # Parsing GeoJSON, clasificaciones
│   │   └── enricher.py            # Stats, Gutenberg-Richter
│   ├── quality/validators.py      # Validacion de rangos y completitud
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

| Fuente | Descripcion | Enlace |
|--------|-------------|--------|
| USGS Earthquake Catalog API | API publica de eventos sismicos globales (GeoJSON) | [https://earthquake.usgs.gov/fdsnws/event/1/](https://earthquake.usgs.gov/fdsnws/event/1/) |
| USGS Earthquake Hazards Program | Programa de monitoreo sismico del USGS | [https://earthquake.usgs.gov/](https://earthquake.usgs.gov/) |
| IGP Peru | Instituto Geofisico del Peru - monitoreo sismico nacional | [https://www.igp.gob.pe/servicios/centro-sismologico-nacional/](https://www.igp.gob.pe/servicios/centro-sismologico-nacional/) |
