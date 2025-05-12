import pytest
import pandas as pd
from src.transform.cleaner import (
    features_to_dataframe, clean_earthquakes,
    classify_magnitude, classify_depth, classify_region,
    add_classifications,
)


def _sample_parsed():
    return [
        {
            "id_usgs": "us001",
            "magnitud": 5.2,
            "lugar": "near Nazca",
            "timestamp_ms": 1700000000000,
            "profundidad_km": 35.0,
            "latitud": -15.23,
            "longitud": -75.12,
            "tipo_magnitud": "mww",
            "estado": "reviewed",
            "tsunami": 0,
            "felt": 10,
            "sig": 400,
        },
        {
            "id_usgs": "us002",
            "magnitud": 3.1,
            "lugar": "near Lima",
            "timestamp_ms": 1700100000000,
            "profundidad_km": 80.0,
            "latitud": -12.04,
            "longitud": -77.04,
            "tipo_magnitud": "mb",
            "estado": "reviewed",
            "tsunami": 0,
            "felt": None,
            "sig": 50,
        },
    ]


def test_features_to_df():
    df = features_to_dataframe(_sample_parsed())
    assert "fecha_utc" in df.columns
    assert "anio" in df.columns
    assert len(df) == 2


def test_clean_removes_dupes():
    data = _sample_parsed()
    data.append(data[0].copy())
    df = features_to_dataframe(data)
    cleaned = clean_earthquakes(df)
    assert len(cleaned) == 2


def test_clean_drops_null_mag():
    data = _sample_parsed()
    data[0]["magnitud"] = None
    df = features_to_dataframe(data)
    cleaned = clean_earthquakes(df)
    assert len(cleaned) == 1


def test_classify_magnitude():
    assert classify_magnitude(1.5) == "micro"
    assert classify_magnitude(3.0) == "menor"
    assert classify_magnitude(4.5) == "ligero"
    assert classify_magnitude(5.5) == "moderado"
    assert classify_magnitude(6.5) == "fuerte"
    assert classify_magnitude(7.5) == "mayor"
    assert classify_magnitude(8.5) == "gran"


def test_classify_depth():
    assert classify_depth(30) == "superficial"
    assert classify_depth(150) == "intermedio"
    assert classify_depth(500) == "profundo"


def test_classify_region():
    assert classify_region(-3.0) == "norte"
    assert classify_region(-9.0) == "centro"
    assert classify_region(-15.0) == "sur"


def test_add_classifications():
    df = features_to_dataframe(_sample_parsed())
    df = clean_earthquakes(df)
    result = add_classifications(df)
    assert "cat_magnitud" in result.columns
    assert "cat_profundidad" in result.columns
    assert "region_sismica" in result.columns
