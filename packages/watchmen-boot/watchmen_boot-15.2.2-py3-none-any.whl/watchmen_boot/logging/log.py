import logging
import logging.handlers
import sys
from pythonjsonlogger import jsonlogger
from watchmen_boot.config.config import PROD, settings


def init():
    logger = logging.getLogger()
    logger.setLevel(logging.NOTSET)

    # Add stdout handler, with level INFO
    console = logging.StreamHandler(sys.stdout)
    if settings.ENVIRONMENT == PROD:
        console.setLevel(logging.ERROR)
    else:
        console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-13s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logger.addHandler(console)
    # Add file rotating handler, with level DEBUG
    if settings.LOGGER_FILE_ON:
        if settings.LOGGER_JSON_FORMAT:
            log_handler = logging.handlers.RotatingFileHandler(filename=settings.LOGGER_FILE, maxBytes=10242880,
                                                               backupCount=5, encoding='utf-8')
            log_handler.setLevel(logging.INFO)
            formatter = jsonlogger.JsonFormatter(
                '%(asctime)s - %(process)d - %(threadName)s - %(name)s - %(levelname)s - %(message)s')
            log_handler.setFormatter(formatter)
            logger.addHandler(log_handler)
        else:
            rotating_handler = logging.handlers.RotatingFileHandler(filename='temp/rotating.log', maxBytes=10242880,
                                                                    backupCount=5, encoding='utf-8')
            rotating_handler.setLevel(logging.ERROR)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            rotating_handler.setFormatter(formatter)
            logger.addHandler(rotating_handler)
