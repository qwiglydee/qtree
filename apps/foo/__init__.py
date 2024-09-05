"""Basic app

Using very basic i/o
"""

from back.io import input, output, update, NEXT_BTN


TRIALS = ["foo", "bar", "baz"]


def script():
    yield output(
        """
                 <h2>Welcome to Foo</h2>
                 <p>{{text}}</p>
                 """
    )
    yield update({"text": "Hello!"})
    yield input(NEXT_BTN)

    yield update({"text": "This is a sample app"})
    yield input(NEXT_BTN)

    yield update({"text": "You're gonna play 3 simple trials"})
    yield input(NEXT_BTN)

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

        response = yield input({"reply": str, "next": bool})
        responses.append(response["reply"])

    score = sum(trial == resp for trial, resp in zip(TRIALS, responses))
    yield output(
        f"""
                 <h2>Results</h2>
                 <p>Your score: {score}</p>
                 """
    )
    yield input(NEXT_BTN)
