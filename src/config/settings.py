import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
LOG_DIR = BASE_DIR / "logs"

for _d in (RAW_DIR, PROCESSED_DIR, LOG_DIR):
    _d.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "sismos.db"

USGS_API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
USGS_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_BACKOFF = 2.0

PERU_BBOX = {
    "minlatitude": -18.35,
    "maxlatitude": -0.04,
    "minlongitude": -81.33,
    "maxlongitude": -68.65,
}

MAG_CATEGORIES = {
    "micro": (0, 2.0),
    "menor": (2.0, 4.0),
    "ligero": (4.0, 5.0),
    "moderado": (5.0, 6.0),
    "fuerte": (6.0, 7.0),
    "mayor": (7.0, 8.0),
    "gran": (8.0, 10.0),
}

REGIONES_SISMICAS = {
    "norte": {"lat_min": -6.0, "lat_max": -0.04},
    "centro": {"lat_min": -12.0, "lat_max": -6.0},
    "sur": {"lat_min": -18.35, "lat_max": -12.0},
}

ANIO_INICIO = 2014
ANIO_FIN = 2024
