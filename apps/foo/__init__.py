"""Sample app

The app does nothing.
"""

import logging


logger = logging.getLogger(__name__)


def setup():
    "setup something"
    pass


def main():
    logger.debug("starting")
    result = yield "something"
    logger.debug(f"{result=}")
