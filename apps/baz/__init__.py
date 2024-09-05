""" Advanced flow

Combining nested scripts and other apps
"""

import logging

logger = logging.getLogger(__name__)


from back.io import page, form, message

from apps import bar


def script():
    yield page("baz/welcome.html")

    yield from questionnaire()

    yield message("<h3>Now you're gonna play some simple trials</h3>")

    yield from bar.script()

    yield message("<p>Thanks for participation</p>")


def questionnaire():
    gender, age, income = None, None, None

    response = yield form("baz/q_gender.html", {}, {"gender": str})
    gender = response["gender"]

    if gender != "F":
        response = yield form("baz/q_age.html", {}, {"age": str})
        age = response["age"]

    if gender != "M":
        response = yield form("baz/q_income.html", {}, {"income": str})
        income = response["income"]

    logging.debug(f"{gender=} {age=} {income=}")

    # NB: cannot return the values
