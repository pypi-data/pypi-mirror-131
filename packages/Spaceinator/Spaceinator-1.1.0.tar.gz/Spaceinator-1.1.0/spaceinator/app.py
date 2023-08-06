import logging

from spaceinator import Config, setup_logger, utils

setup_logger()
log = logging.getLogger("main")

config = Config()


def run():
    log.debug("Starting Spaceinator App.")

    utils.display_title()
    utils.instructions()

    utils.get_min_value(config=config)
    utils.get_max_value(config=config)
    utils.run(config=config)


if __name__ == "__main__":
    run()
