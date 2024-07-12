import logging
import os
from logging import handlers


def configure_logger():
    logging.basicConfig(level=logging.INFO)
    log_folder = os.path.join("src", "data", "logs")
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    log_file = os.path.join(log_folder, "log.log")
    handler = handlers.RotatingFileHandler(
        filename=log_file, maxBytes=1e7, backupCount=5, encoding="utf-8"
    )
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logging.getLogger().addHandler(handler)
