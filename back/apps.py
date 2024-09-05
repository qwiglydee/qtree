from dataclasses import dataclass, field
from pathlib import Path
import logging
import inspect
import random
from string import capwords
from importlib import import_module

from jinja2 import Template  # replace with something else

from .types import Model, Data, Effect, AppScript, AppRoutine
from .templates import MyUdefined

logger = logging.getLogger(__name__)


class App:
    READY = "READY"  # signal of page just loaded
    RESTORE = "RESTORE"  # signal to restore page state
    TERMINATE = "TERMINATE"  # signal to close page

    def __init__(self, name, module):
        self.name = name
        self.module = module
        if module.__doc__:
            doc = module.__doc__.splitlines()
            self.title = capwords(doc[0])
            self.description = "".join(doc[1:])
        else:
            self.title = name.capitalize()
            self.description = ""

        assert hasattr(self.module, "script")
        assert inspect.isgeneratorfunction(self.module.script)

    @classmethod
    def importapps(cls, path: Path):  # -> dict[str, App]
        apps = [p.name for p in path.iterdir() if p.is_dir() and (p / "__init__.py").exists()]
        return {app: cls(app, import_module(f"apps.{app}")) for app in apps}


@dataclass
class State:
    template: Template | None = None
    data: Data = field(default_factory=dict)
    content: str = ""
    inputs: Model = field(default_factory=dict)

    def affect(self, effect: Effect):
        if "T" in effect:
            assert isinstance(effect["T"], str)
            self.template = Template(effect["T"], undefined=MyUdefined)
            self.content = self.template.render(self.data)

        if "V" in effect:
            assert self.template and isinstance(self.template, Template)
            assert isinstance(effect["V"], dict)
            self.data.update(effect["V"])
            self.content = self.template.render(self.data)

        if "I" in effect:
            assert isinstance(effect["I"], dict)
            self.inputs = effect["I"]
        else:
            self.inputs = dict()


async def run(app: App) -> AppRoutine:
    logger = logging.getLogger(f"{__name__}:{app.name}")

    script: AppScript = app.module.script()
    assert inspect.isgenerator(script)

    logger.debug(f"starting")

    state = State()

    input: Data = yield  # type: ignore # the 0th iter of run
    assert App.READY in input

    effect = script.send(None)  # the 0th iteration
    state.affect(effect)
    logger.debug(f"initial {effect=}")

    try:
        while True:
            logger.debug(f"{state.content=} {state.inputs=}")

            input = yield {"html": state.content, "inputs": list(state.inputs.keys())}  # breaks here on page reload
            logger.debug(f"{input=}")

            # restores here after page reoad
            if App.READY in input:
                logger.debug(f"pagre reloaded")
                continue

            effect = script.send(input)  # raises here a StopIteration
            state.affect(effect)
            logger.debug(f"{effect=}")
    except StopIteration:
        logger.debug("completed")
        raise GeneratorExit({App.TERMINATE: True})
