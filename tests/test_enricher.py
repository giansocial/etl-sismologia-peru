import pytest
import pandas as pd
import numpy as np
from src.transform.enricher import (
    monthly_stats, magnitude_distribution, depth_analysis,
    significant_events, gutenberg_richter,
)


def _sample_df():
    np.random.seed(42)
    n = 200
    return pd.DataFrame({
        "id_usgs": [f"us{i:04d}" for i in range(n)],
        "magnitud": np.random.uniform(2, 7, n).round(1),
        "profundidad_km": np.random.uniform(5, 300, n).round(1),
        "latitud": np.random.uniform(-18, -1, n),
        "anio": np.random.choice([2022, 2023, 2024], n),
        "mes": np.random.randint(1, 13, n),
        "region_sismica": np.random.choice(["norte", "centro", "sur"], n),
        "cat_magnitud": np.random.choice(["menor", "ligero", "moderado"], n),
        "cat_profundidad": np.random.choice(["superficial", "intermedio"], n),
        "tsunami": np.random.choice([0, 1], n, p=[0.95, 0.05]),
        "felt": np.random.choice([None, 5, 10, 50], n),
        "sig": np.random.randint(10, 500, n),
    })


def test_monthly_stats():
    df = _sample_df()
    result = monthly_stats(df)
    assert "total_sismos" in result.columns
    assert "mag_promedio" in result.columns
    assert len(result) > 0


def test_magnitude_distribution():
    df = _sample_df()
    result = magnitude_distribution(df)
    assert "porcentaje" in result.columns
    for anio in result["anio"].unique():
        total = result[result["anio"] == anio]["porcentaje"].sum()
        assert abs(total - 100) < 0.5


def test_depth_analysis():
    df = _sample_df()
    result = depth_analysis(df)
    assert "total" in result.columns
    assert len(result) > 0


def test_significant_events():
    df = _sample_df()
    df["fecha_local"] = pd.Timestamp("2024-01-01")
    df["lugar"] = "test"
    sig = significant_events(df, min_mag=5.0)
    assert all(sig["magnitud"] >= 5.0)


def test_significant_empty():
    df = _sample_df()
    df["magnitud"] = 2.0
    df["fecha_local"] = pd.Timestamp("2024-01-01")
    df["lugar"] = "test"
    sig = significant_events(df, min_mag=8.0)
    assert len(sig) == 0


def test_gutenberg_richter():
    df = _sample_df()
    gr = gutenberg_richter(df)
    assert "log10_n" in gr.columns
    assert gr["n_eventos"].iloc[0] >= gr["n_eventos"].iloc[-1]
