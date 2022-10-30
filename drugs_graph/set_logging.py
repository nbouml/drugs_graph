import logging
from os import remove
from os.path import exists
from typing import Any


def setup_logger(logger_name: str, log_file: str, level: Any = logging.WARNING) -> None:
    """
    this method will set up the logger
    Parameters
    ----------
    logger_name: str
            the name of section in logger
    log_file: str
            the name of the file of the logger
    level: Any
            the level of log from logging package


    Returns
    -------
    None

    """
    # Erase log if already exists
    # if exists(log_file):
    #     remove(log_file)
    # Configure log file
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='a')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    l.setLevel(level)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)
