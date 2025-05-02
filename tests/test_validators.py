import pytest
import pandas as pd
from src.quality.validators import check_completeness, check_range, run_quality_report


def _df():
    return pd.DataFrame({
        "id_usgs": ["us001", "us002"],
        "magnitud": [5.2, 3.1],
        "latitud": [-15.23, -12.04],
        "longitud": [-75.12, -77.04],
        "profundidad_km": [35.0, 80.0],
    })


def test_completeness_full():
    result = check_completeness(_df(), ["magnitud", "latitud"])
    assert result["score"] == 100.0


def test_completeness_nulls():
    df = _df()
    df.loc[0, "magnitud"] = None
    result = check_completeness(df, ["magnitud"])
    assert result["score"] < 100


def test_range_ok():
    result = check_range(_df())
    assert result["score"] == 100.0


def test_range_bad_mag():
    df = _df()
    df.loc[0, "magnitud"] = -1
    result = check_range(df)
    assert len(result["issues"]) > 0


def test_quality_report():
    report = run_quality_report(_df())
    assert report["score_total"] > 90
    assert report["filas"] == 2
