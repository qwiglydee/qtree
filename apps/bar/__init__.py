""" Forms app

Using pages and forms
"""

from back.io import page, form, message

TRIALS = ["foo", "bar", "baz"]


def script():
    yield page("bar/welcome.html", {"text": "Hello..."})

    yield message("<h3>Now you're gonna play some simple trials</h3>")

    replies = []
    progress = {"total": len(TRIALS), "iter": 0}

    for trial in TRIALS:
        progress["iter"] += 1
        response = yield form("bar/trial.html", {"trial": trial, "progress": progress}, {"reply": str})
        replies.append(response["reply"])

    score = sum(trial == reply for trial, reply in zip(TRIALS, replies))

    yield page("bar/results.html", {"score": score})

    yield message("<p>Thanks for participation</p>")
