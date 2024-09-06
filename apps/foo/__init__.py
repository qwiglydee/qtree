"""Foo app

Just a stub
"""

import logging

logger = logging.getLogger(__name__)


def script():
    logger.debug("started")

    resp = yield "welcome"

    logger.debug(f"{resp=}")

    logger.debug("completed")
