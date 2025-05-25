import logging
import sqlite3
from pathlib import Path
import pandas as pd

from src.config.settings import DB_PATH

log = logging.getLogger(__name__)

SCHEMA = """
CREATE TABLE IF NOT EXISTS sismos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usgs TEXT UNIQUE NOT NULL,
    magnitud REAL NOT NULL,
    profundidad_km REAL,
    latitud REAL,
    longitud REAL,
    lugar TEXT,
    fecha_utc TEXT,
    anio INTEGER,
    mes INTEGER,
    hora INTEGER,
    tipo_magnitud TEXT,
    tsunami INTEGER DEFAULT 0,
    felt INTEGER,
    sig INTEGER,
    cat_magnitud TEXT,
    cat_profundidad TEXT,
    region_sismica TEXT
);

CREATE INDEX IF NOT EXISTS idx_sismos_anio ON sismos(anio);
CREATE INDEX IF NOT EXISTS idx_sismos_mag ON sismos(magnitud);
CREATE INDEX IF NOT EXISTS idx_sismos_region ON sismos(region_sismica);
"""


def init_db(db_path: Path = None) -> sqlite3.Connection:
    db_path = db_path or DB_PATH
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.executescript(SCHEMA)
    conn.commit()
    return conn


def load_to_db(df: pd.DataFrame, conn: sqlite3.Connection) -> int:
    cols = [
        "id_usgs", "magnitud", "profundidad_km", "latitud", "longitud",
        "lugar", "fecha_utc", "anio", "mes", "hora", "tipo_magnitud",
        "tsunami", "felt", "sig", "cat_magnitud", "cat_profundidad",
        "region_sismica",
    ]
    available = [c for c in cols if c in df.columns]
    placeholders = ",".join(["?"] * len(available))
    col_str = ",".join(available)
    sql = f"INSERT OR REPLACE INTO sismos ({col_str}) VALUES ({placeholders})"

    loaded = 0
    for _, row in df.iterrows():
        values = []
        for c in available:
            v = row[c]
            if hasattr(v, "isoformat"):
                v = v.isoformat()
            elif pd.isna(v):
                v = None
            values.append(v)
        conn.execute(sql, values)
        loaded += 1

    conn.commit()
    log.info("cargados %d sismos al warehouse", loaded)
    return loaded
