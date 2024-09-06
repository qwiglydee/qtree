"""Bar app

Just a stub with templates
"""

import logging

logger = logging.getLogger(__name__)


def script():
    logger.debug("started")

    resp = yield "welcome"

    logger.debug(f"{resp=}")

    logger.debug("completed")
