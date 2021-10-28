import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("app")

logger.setLevel(logging.INFO)

formatter = logging.Formatter("[%(asctime)s:%(levelname)s] %(message)s")

file_handler = RotatingFileHandler("app.log", maxBytes=1 * 1024 * 1024, backupCount=2)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
