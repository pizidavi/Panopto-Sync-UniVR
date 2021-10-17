import sys
import logging

StreamHandler = logging.StreamHandler(sys.stdout)
StreamHandler.setLevel(logging.INFO)
StreamHandler.setFormatter(logging.Formatter('%(levelname)s:%(asctime)s: %(message)s'))

# FileHandler = logging.FileHandler('syslog.log')
# FileHandler.setLevel(logging.DEBUG)
# FileHandler.setFormatter(logging.Formatter('%(levelname)s:%(name)s:%(asctime)s:%(message)s'))


def get_logger(name: str) -> logging.Logger:
    """
    Auto-set important options in logger
    :param name: logger's name
    :return: logger
    """
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    logger.addHandler(StreamHandler)
    # logger.addHandler(FileHandler)
    return logger


def set_level(level: int) -> None:
    StreamHandler.setLevel(level)
    if level <= 10:
        StreamHandler.setFormatter(logging.Formatter('%(levelname)s:%(name)s:%(asctime)s: %(message)s'))
