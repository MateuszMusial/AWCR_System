import logging
import logging.config
import json
import os

LOGGING_CONFIG_FILE = "logging_config.json"
LOGS_DIRECTORY = "Logs"


def setup_logger() -> None:
    """
    Function to set up logger configuration from file.
    """
    if not os.path.exists("Logs"):
        create_log_directory()

    with open(LOGGING_CONFIG_FILE, "r", encoding='utf-8') as file:
        config = json.load(file)
    logging.config.dictConfig(config)


def get_logger(name: str = __name__):
    """
    Function to create logger for specific module.
    """
    return logging.getLogger(name)


def create_log_directory() -> None:
    """
    Function to create logs directory.
    """
    os.makedirs(LOGS_DIRECTORY)
