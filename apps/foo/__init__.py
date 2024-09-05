"""Basic app

Using very basic i/o
"""

import logging

from back.io import input, output, update

logger = logging.getLogger(__name__)


def setup():
    "setup something"
    pass


TRIALS = ["foo", "bar", "baz"]


def script():
    logger.debug("started")

    logger.debug("welcome page")
    yield output(
        """
                 <h2>Welcome to Foo</h2>
                 <p>Hello...</p>
                 """
    )
    yield input({"next": bool})

    logger.debug("trial page")
    yield output(
        """
                 <h2>Trial {{progress.iter}}/{{progress.total}}</h2>
                 <p><b>{{trial}}</b></p>
                 <hr style="width: 100%">
                 <input type="text" name="reply" autofocus>
                 """
    )
    progress = {"total": len(TRIALS), "iter": 0}

    responses = []
    for trial in TRIALS:
        progress["iter"] += 1
        yield update({"progress": progress, "trial": trial})
        logger.debug(f"{progress=} {trial=}")

        response = yield input({"reply": str, "next": bool})
        responses.append(response["reply"])
        logger.debug(f"{response=}")

    logger.debug("results page")

    score = sum(trial == resp for trial, resp in zip(TRIALS, responses))
    yield output(
        """
                 <h2>Results</h2>
                 <p>{{score}}</p>
                 """
    )
    yield update({"score": score})
    yield input({"next": bool})

    logger.debug("completed")
