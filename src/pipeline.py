import argparse
import json
import logging
import time

import pandas as pd

from src.config.settings import ANIO_INICIO, ANIO_FIN, PROCESSED_DIR
from src.extract.usgs_client import fetch_yearly, parse_feature
from src.transform.cleaner import features_to_dataframe, clean_earthquakes, add_classifications
from src.transform.enricher import (
    monthly_stats, magnitude_distribution, depth_analysis,
    significant_events, gutenberg_richter,
)
from src.quality.validators import run_quality_report
from src.load.warehouse import init_db, load_to_db
from src.utils.logger import get_logger

log = get_logger(__name__)


def run_pipeline(start_year: int = None, end_year: int = None, min_mag: float = 2.0) -> dict:
    t0 = time.time()
    start_year = start_year or ANIO_INICIO
    end_year = end_year or ANIO_FIN

    log.info("descargando sismos %d-%d (mag >= %.1f)", start_year, end_year, min_mag)

    features = fetch_yearly(start_year, end_year, min_mag)
    parsed = [parse_feature(f) for f in features]

    df = features_to_dataframe(parsed)
    df = clean_earthquakes(df)
    df = add_classifications(df)

    quality = run_quality_report(df)
    log.info("calidad: %.1f%%", quality["score_total"])

    conn = init_db()
    loaded = load_to_db(df, conn)
    conn.close()

    monthly = monthly_stats(df)
    monthly.to_csv(PROCESSED_DIR / "stats_mensuales.csv", index=False)

    mag_dist = magnitude_distribution(df)
    mag_dist.to_csv(PROCESSED_DIR / "distribucion_magnitud.csv", index=False)

    depth = depth_analysis(df)
    depth.to_csv(PROCESSED_DIR / "analisis_profundidad.csv", index=False)

    sig = significant_events(df)
    sig.to_csv(PROCESSED_DIR / "eventos_significativos.csv", index=False)

    gr = gutenberg_richter(df)
    gr.to_csv(PROCESSED_DIR / "gutenberg_richter.csv", index=False)

    elapsed = round(time.time() - t0, 1)
    log.info("pipeline completado en %.1fs", elapsed)

    return {
        "sismos_procesados": len(df),
        "sismos_cargados": loaded,
        "eventos_significativos": len(sig),
        "calidad_pct": quality["score_total"],
        "periodo": f"{start_year}-{end_year}",
        "duracion_seg": elapsed,
    }


def main():
    parser = argparse.ArgumentParser(description="ETL sismologia Peru - USGS")
    parser.add_argument("--start", type=int, default=ANIO_INICIO)
    parser.add_argument("--end", type=int, default=ANIO_FIN)
    parser.add_argument("--min-mag", type=float, default=2.0)
    args = parser.parse_args()

    result = run_pipeline(args.start, args.end, args.min_mag)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
