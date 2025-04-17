import pandas as pd
import numpy as np


def monthly_stats(df: pd.DataFrame) -> pd.DataFrame:
    monthly = (
        df.groupby(["anio", "mes", "region_sismica"])
        .agg(
            total_sismos=("id_usgs", "count"),
            mag_promedio=("magnitud", "mean"),
            mag_max=("magnitud", "max"),
            prof_promedio=("profundidad_km", "mean"),
            con_tsunami=("tsunami", "sum"),
        )
        .round(2)
        .reset_index()
    )
    return monthly


def magnitude_distribution(df: pd.DataFrame) -> pd.DataFrame:
    dist = (
        df.groupby(["anio", "cat_magnitud"])["id_usgs"]
        .count()
        .reset_index(name="total")
    )
    year_total = dist.groupby("anio")["total"].transform("sum")
    dist["porcentaje"] = (dist["total"] / year_total * 100).round(1)
    return dist


def depth_analysis(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["region_sismica", "cat_profundidad"])
        .agg(
            total=("id_usgs", "count"),
            mag_promedio=("magnitud", "mean"),
        )
        .round(2)
        .reset_index()
    )


def significant_events(df: pd.DataFrame, min_mag: float = 5.0) -> pd.DataFrame:
    sig = df[df["magnitud"] >= min_mag].copy()
    sig = sig.sort_values("magnitud", ascending=False)
    cols = [
        "id_usgs", "fecha_local", "magnitud", "profundidad_km",
        "lugar", "region_sismica", "tsunami", "felt", "sig",
    ]
    available = [c for c in cols if c in sig.columns]
    return sig[available].reset_index(drop=True)


def gutenberg_richter(df: pd.DataFrame) -> pd.DataFrame:
    mags = np.arange(2.0, 8.5, 0.5)
    rows = []
    total = len(df)
    for m in mags:
        n = len(df[df["magnitud"] >= m])
        log_n = np.log10(n) if n > 0 else 0
        rows.append({"magnitud_min": m, "n_eventos": n, "log10_n": round(log_n, 3)})
    return pd.DataFrame(rows)
