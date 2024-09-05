""" Advanced flow

Combining scripts and other apps
"""

import logging

logger = logging.getLogger(__name__)


from back.io import page, form

from apps import bar


def script():
    yield page("baz/welcome.html")

    yield from questionnaire()

    yield from bar.script()


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
