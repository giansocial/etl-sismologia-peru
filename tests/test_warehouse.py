import pytest
import pandas as pd
from pathlib import Path
from src.load.warehouse import init_db, load_to_db


@pytest.fixture
def db(tmp_path):
    conn = init_db(tmp_path / "test.db")
    yield conn
    conn.close()


def _df():
    return pd.DataFrame({
        "id_usgs": ["us001", "us002"],
        "magnitud": [5.2, 3.1],
        "profundidad_km": [35.0, 80.0],
        "latitud": [-15.23, -12.04],
        "longitud": [-75.12, -77.04],
        "lugar": ["near Nazca", "near Lima"],
        "anio": [2024, 2024],
        "mes": [1, 1],
        "hora": [10, 14],
        "tipo_magnitud": ["mww", "mb"],
        "tsunami": [0, 0],
        "felt": [10, None],
        "sig": [400, 50],
        "cat_magnitud": ["moderado", "menor"],
        "cat_profundidad": ["superficial", "intermedio"],
        "region_sismica": ["sur", "centro"],
    })


def test_init_creates_table(db):
    cur = db.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {r[0] for r in cur.fetchall()}
    assert "sismos" in tables


def test_load_inserts(db):
    loaded = load_to_db(_df(), db)
    assert loaded == 2
    cur = db.execute("SELECT COUNT(*) FROM sismos")
    assert cur.fetchone()[0] == 2


def test_load_upsert(db):
    load_to_db(_df(), db)
    load_to_db(_df(), db)
    cur = db.execute("SELECT COUNT(*) FROM sismos")
    assert cur.fetchone()[0] == 2


def test_load_query_by_region(db):
    load_to_db(_df(), db)
    cur = db.execute("SELECT COUNT(*) FROM sismos WHERE region_sismica = 'sur'")
    assert cur.fetchone()[0] == 1
