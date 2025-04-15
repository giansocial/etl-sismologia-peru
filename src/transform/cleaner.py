import logging
import pandas as pd
from datetime import datetime, timezone

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
    if mag < 2:
        return "micro"
    if mag < 4:
        return "menor"
    if mag < 5:
        return "ligero"
    if mag < 6:
        return "moderado"
    if mag < 7:
        return "fuerte"
    if mag < 8:
        return "mayor"
    return "gran"


def classify_depth(depth_km: float) -> str:
    if depth_km < 70:
        return "superficial"
    if depth_km < 300:
        return "intermedio"
    return "profundo"


def classify_region(lat: float) -> str:
    if lat > -6.0:
        return "norte"
    if lat > -12.0:
        return "centro"
    return "sur"


def add_classifications(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["cat_magnitud"] = df["magnitud"].apply(classify_magnitude)
    df["cat_profundidad"] = df["profundidad_km"].apply(classify_depth)
    df["region_sismica"] = df["latitud"].apply(classify_region)
    return df
