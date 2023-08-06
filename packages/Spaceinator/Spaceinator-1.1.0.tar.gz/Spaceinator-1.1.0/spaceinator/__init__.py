"""
Setup Logging for a file (app.log) and to the screen.
This app is intended to run with the command prompt visible.
"""

import logging
from configparser import ConfigParser

__version__ = "1.1.0"
__version_info__ = ("1", "1", "0")

LOGGING_FORMAT = "%(asctime)2s - %(levelname)5s - %(message)s"
LOGGING_DATETIME_FORMAT = "%m/%d/%Y %I:%M:%S %p"
LOGGING_FILENAME = "app.log"


def setup_logger():
    # Logging Setup
    log = logging.getLogger("main")
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter(LOGGING_FORMAT, datefmt=LOGGING_DATETIME_FORMAT)

    file_handler = logging.FileHandler(
        filename=LOGGING_FILENAME, mode="w", encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    log.addHandler(stream_handler)


class Config(ConfigParser):
    FILENAME = "config.ini"

    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self) -> None:
        self.read(Config.FILENAME)
        if not self.has_section("main"):
            self.add_section("main")
            self.set("main", "min_minute", "5")
            self.set("main", "max_minute", "10")
            self.set("main", "times_pressed", "0")

    def save(self) -> None:
        with open(Config.FILENAME, "w+") as config_file:
            self.write(config_file)
