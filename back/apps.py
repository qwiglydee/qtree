from dataclasses import dataclass, field
from pathlib import Path
import logging
import inspect
import random
from string import capwords
from importlib import import_module

from .models import Model, Data
from .templates import templates

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

    @classmethod
    def importapps(cls, path: Path):  # -> dict[str, App]
        apps = [p.name for p in path.iterdir() if p.is_dir() and (p / "__init__.py").exists()]
        return {app: cls(app, import_module(f"apps.{app}")) for app in apps}


async def run(app: App):
    logger = logging.getLogger(f"{__name__}:{app.name}")

    script = app.module.script()

    logger.debug(f"starting")
    input = yield  # 0th iteration of run
    assert App.READY in input

    output = script.send(None)  # 0th iteration of script
    inputs = ["next"]

    try:
        while True:
            input = yield {"html": output, "inputs": inputs}

            if App.READY in input:
                logger.debug(f"pagre reloaded")
                continue

            output = script.send(input)
    except StopIteration:
        raise GeneratorExit({App.TERMINATE: True})
