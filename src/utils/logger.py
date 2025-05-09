import logging
import os
from src.config.settings import LOG_DIR


def get_logger(name):
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger = logging.getLogger(name)

    if not logger.handlers:
        console = logging.StreamHandler()
        console.setFormatter(
            logging.Formatter("%(asctime)s %(name)s [%(levelname)s] %(message)s")
        )
        logger.addHandler(console)

        fh = logging.FileHandler(LOG_DIR / "sismo.log", encoding="utf-8")
        fh.setFormatter(
            logging.Formatter("%(asctime)s %(name)s [%(levelname)s] %(message)s")
        )
        logger.addHandler(fh)

    logger.setLevel(getattr(logging, log_level, logging.INFO))
    return logger
