import logging
import pandas as pd
from datetime import datetime, timezone

from src.config.settings import MAG_CATEGORIES, REGIONES_SISMICAS

log = logging.getLogger(__name__)


def features_to_dataframe(parsed: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(parsed)
    if "timestamp_ms" in df.columns:
        df["fecha_utc"] = pd.to_datetime(df["timestamp_ms"], unit="ms", utc=True)
        df["fecha_local"] = df["fecha_utc"].dt.tz_convert("America/Lima")
        df["anio"] = df["fecha_local"].dt.year
        df["mes"] = df["fecha_local"].dt.month
        df["hora"] = df["fecha_local"].dt.hour
    return df


def clean_earthquakes(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    before = len(df)

    df = df.drop_duplicates(subset=["id_usgs"])
    dupes = before - len(df)
    if dupes > 0:
        log.info("eliminados %d duplicados", dupes)

    df = df.dropna(subset=["magnitud", "latitud", "longitud"])

    df = df[df["magnitud"] >= 0]
    df = df[df["profundidad_km"] >= 0]

    log.info("registros limpios: %d (de %d)", len(df), before)
    return df.reset_index(drop=True)


def classify_magnitude(mag: float) -> str:
    for cat, (_low, high) in MAG_CATEGORIES.items():
        if mag < high:
            return cat
    return list(MAG_CATEGORIES.keys())[-1]


def classify_depth(depth_km: float) -> str:
    if depth_km < 70:
        return "superficial"
    if depth_km < 300:
        return "intermedio"
    return "profundo"


def classify_region(lat: float) -> str:
    for region, bounds in REGIONES_SISMICAS.items():
        if lat > bounds["lat_min"]:
            return region
    return list(REGIONES_SISMICAS.keys())[-1]


def add_classifications(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["cat_magnitud"] = df["magnitud"].apply(classify_magnitude)
    df["cat_profundidad"] = df["profundidad_km"].apply(classify_depth)
    df["region_sismica"] = df["latitud"].apply(classify_region)
    return df
