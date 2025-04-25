import time
import logging
import requests

from src.config.settings import (
    USGS_API_URL, USGS_TIMEOUT, MAX_RETRIES, RETRY_BACKOFF, PERU_BBOX,
)

log = logging.getLogger(__name__)


def fetch_earthquakes(
    start_date: str,
    end_date: str,
    min_magnitude: float = 2.0,
    bbox: dict = None,
) -> list[dict]:
    bbox = bbox or PERU_BBOX
    params = {
        "format": "geojson",
        "starttime": start_date,
        "endtime": end_date,
        "minmagnitude": min_magnitude,
        **bbox,
        "orderby": "time",
        "limit": 20000,
    }

    last_err = None
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(USGS_API_URL, params=params, timeout=USGS_TIMEOUT)
            resp.raise_for_status()
            data = resp.json()
            features = data.get("features", [])
            log.info("obtenidos %d sismos (%s a %s)", len(features), start_date, end_date)
            return features
        except requests.exceptions.RequestException as e:
            wait = RETRY_BACKOFF * (2 ** attempt)
            log.warning("error (intento %d): %s, esperando %.1fs", attempt + 1, e, wait)
            time.sleep(wait)
            last_err = e

    raise ConnectionError(f"fallo tras {MAX_RETRIES} intentos: {last_err}")


def fetch_yearly(start_year: int, end_year: int, min_mag: float = 2.0) -> list[dict]:
    all_events = []
    for year in range(start_year, end_year + 1):
        start = f"{year}-01-01"
        end = f"{year}-12-31"
        events = fetch_earthquakes(start, end, min_magnitude=min_mag)
        all_events.extend(events)
        if year < end_year:
            time.sleep(1.5)
    return all_events


def parse_feature(feature: dict) -> dict:
    props = feature.get("properties", {})
    coords = feature.get("geometry", {}).get("coordinates", [None, None, None])
    ts = props.get("time")

    return {
        "id_usgs": feature.get("id"),
        "magnitud": props.get("mag"),
        "lugar": props.get("place", ""),
        "timestamp_ms": ts,
        "profundidad_km": coords[2] if len(coords) > 2 else None,
        "latitud": coords[1] if len(coords) > 1 else None,
        "longitud": coords[0] if len(coords) > 0 else None,
        "tipo_magnitud": props.get("magType", ""),
        "estado": props.get("status", ""),
        "tsunami": props.get("tsunami", 0),
        "felt": props.get("felt"),
        "sig": props.get("sig"),
    }
