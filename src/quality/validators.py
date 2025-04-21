import logging
import pandas as pd

log = logging.getLogger(__name__)


def check_completeness(df: pd.DataFrame, cols: list[str]) -> dict:
    total = len(df)
    if total == 0:
        return {"score": 0.0, "detalles": {}}
    det = {}
    for c in cols:
        if c in df.columns:
            det[c] = round((1 - df[c].isnull().sum() / total) * 100, 1)
        else:
            det[c] = 0.0
    return {"score": round(sum(det.values()) / len(det), 1), "detalles": det}


def check_range(df: pd.DataFrame) -> dict:
    issues = []
    if "magnitud" in df.columns:
        bad_mag = len(df[(df["magnitud"] < 0) | (df["magnitud"] > 10)])
        if bad_mag:
            issues.append(f"{bad_mag} magnitudes fuera de rango")
    if "profundidad_km" in df.columns:
        bad_depth = len(df[(df["profundidad_km"] < 0) | (df["profundidad_km"] > 700)])
        if bad_depth:
            issues.append(f"{bad_depth} profundidades fuera de rango")
    if "latitud" in df.columns:
        bad_lat = len(df[(df["latitud"] < -18.35) | (df["latitud"] > -0.04)])
        if bad_lat:
            issues.append(f"{bad_lat} latitudes fuera del bbox Peru")
    score = 100.0 if not issues else max(0, 100 - len(issues) * 10)
    return {"score": score, "issues": issues}


def run_quality_report(df: pd.DataFrame) -> dict:
    required = ["id_usgs", "magnitud", "latitud", "longitud", "profundidad_km"]
    completeness = check_completeness(df, required)
    range_check = check_range(df)

    total = completeness["score"] * 0.5 + range_check["score"] * 0.5
    report = {
        "score_total": round(total, 1),
        "completitud": completeness,
        "rangos": range_check,
        "filas": len(df),
    }
    log.info("calidad: %.1f%% (%d filas)", total, len(df))
    return report
